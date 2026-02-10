import pytest
from unittest.mock import create_autospec, MagicMock, patch
from sqlalchemy.orm import Session
from datetime import date
from typing import List

# Importaciones de tu proyecto
from aclimate_v3_orm.models import (
    ClimateHistoricalDaily,
    MngLocation,
    MngAdmin2,
    MngAdmin1,
    MngCountry,
    MngClimateMeasure
)
from aclimate_v3_orm.schemas import ClimateHistoricalDailyRead, ClimateHistoricalDailyCreate
from aclimate_v3_orm.services.climate_historical_daily_service import (
    ClimateHistoricalDailyService
)
from aclimate_v3_orm.validations import ClimateHistoricalDailyValidator

@pytest.fixture
def mock_db():
    """Fixture para una sesión de base de datos mockeada"""
    return create_autospec(Session, instance=True)

@pytest.fixture
def daily_service():
    """Fixture para el servicio de datos diarios"""
    return ClimateHistoricalDailyService()

# ---- Tests CRUD básicos ----
def test_create_daily_record(daily_service, mock_db):
    """Test para crear un registro diario"""
    record_data = ClimateHistoricalDailyCreate(
        location_id=1,
        measure_id=1,
        date=date(2023, 6, 1),
        value=25.5
    )
    
    # Configurar mocks
    mock_db.query.return_value.filter.return_value.first.return_value = None
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    
    def mock_refresh(obj):
        obj.id = 1
    
    mock_db.refresh.side_effect = mock_refresh
    
    # Mockear validación
    with patch.object(ClimateHistoricalDailyValidator, 'create_validate'):
        result = daily_service.create(record_data, db=mock_db)
    
    assert isinstance(result, ClimateHistoricalDailyRead)
    assert result.id == 1
    assert result.date == date(2023, 6, 1)
    assert result.value == 25.5

def test_update_daily_record(daily_service, mock_db):
    """Test para actualizar un registro diario"""
    record_id = 1
    update_data = {"value": 26.0, "date": date(2023, 6, 2)}
    existing_record = ClimateHistoricalDaily(
        id=record_id,
        location_id=1,
        measure_id=1,
        date=date(2023, 6, 1),
        value=25.5
    )
    
    mock_db.query.return_value.get.return_value = existing_record
    
    result = daily_service.update(record_id, update_data, db=mock_db)
    
    assert result.value == 26.0
    assert result.date == date(2023, 6, 2)
    mock_db.commit.assert_called_once()

# ---- Tests para métodos de consulta ----
def test_get_by_location_id(daily_service, mock_db):
    """Test para obtener registros por location_id"""
    location_id = 1
    mock_records = [
        ClimateHistoricalDaily(id=1, location_id=location_id, measure_id=1, date=date(2023, 1, 1), value=20.0),
        ClimateHistoricalDaily(id=2, location_id=location_id, measure_id=2, date=date(2023, 1, 2), value=21.0)
    ]
    
    mock_db.query.return_value.filter.return_value.all.return_value = mock_records
    
    result = daily_service.get_by_location_id(location_id, db=mock_db)
    
    assert len(result) == 2
    assert all(r.location_id == location_id for r in result)

def test_get_by_location_name(daily_service, mock_db):
    """Test para obtener registros por nombre de ubicación"""
    location_name = "Test Location"
    mock_location = MngLocation(id=1, admin_2_id=1,
                                name=location_name,
                                machine_name="test-location",
                                latitude=12.34,
                                longitude=56.78,
                                altitude=23,
                                source_id=1,
                                ext_id="Test1",
                                visible=True,
                                enable=True)
    mock_record = ClimateHistoricalDaily(id=1, location_id=1, measure_id=1, date=date(2023, 1, 1), value=20.0)
    mock_record.location = mock_location
    
    # Configurar mocks para el join
    query_mock = MagicMock()
    join_mock = MagicMock()
    filter_mock = MagicMock()
    
    mock_db.query.return_value = query_mock
    query_mock.join.return_value = join_mock
    join_mock.filter.return_value = filter_mock
    filter_mock.all.return_value = [mock_record]
    
    result = daily_service.get_by_location_name(location_name, db=mock_db)
    
    assert len(result) == 1
    assert result[0].location.name == location_name
    query_mock.join.assert_called_once_with(ClimateHistoricalDaily.location)

def test_get_by_country_id(daily_service, mock_db):
    """Test para obtener registros por country_id"""
    country_id = 1
    mock_country = MngCountry(id=country_id, name="Test Country", iso2="CL", enable=True)
    mock_admin1 = MngAdmin1(id=1, country=mock_country, name="Test", ext_id="CLIM1", enable=True, country_id=country_id)
    mock_admin2 = MngAdmin2(id=1, admin_1=mock_admin1, name="Test", ext_id="CLIM2_CTY", enable=True, admin_1_id=1, visible=True)
    mock_location = MngLocation(id=1, admin_2_id=1, admin_2=mock_admin2,
                                name="Test Location",
                                machine_name="test-location-country",
                                latitude=12.34,
                                longitude=56.78,
                                source_id=1,
                                altitude=23,
                                ext_id="Test1",
                                visible=True,
                                enable=True)
    mock_record = ClimateHistoricalDaily(id=1, location_id=1, measure_id=1, date=date(2023, 1, 1), value=20.0)
    mock_record.location = mock_location
    
    # Configurar mocks para múltiples joins
    query_mock = MagicMock()
    join1_mock = MagicMock()
    join2_mock = MagicMock()
    join3_mock = MagicMock()
    filter_mock = MagicMock()
    
    mock_db.query.return_value = query_mock
    query_mock.join.return_value = join1_mock
    join1_mock.join.return_value = join2_mock
    join2_mock.join.return_value = join3_mock
    join3_mock.filter.return_value = filter_mock
    filter_mock.all.return_value = [mock_record]
    
    result = daily_service.get_by_country_id(country_id, db=mock_db)
    print(result)
    assert len(result) == 1
    assert result[0].location.admin_2.admin_1.country_id == country_id

def test_get_by_measure_id(daily_service, mock_db):
    """Test para obtener registros por measure_id"""
    measure_id = 1
    mock_records = [
        ClimateHistoricalDaily(id=1, location_id=1, measure_id=measure_id, date=date(2023, 1, 1), value=20.0),
        ClimateHistoricalDaily(id=2, location_id=2, measure_id=measure_id, date=date(2023, 1, 2), value=21.0)
    ]
    
    mock_db.query.return_value.filter.return_value.all.return_value = mock_records
    
    result = daily_service.get_by_measure_id(measure_id, db=mock_db)
    
    assert len(result) == 2
    assert all(r.measure_id == measure_id for r in result)

def test_get_by_date(daily_service, mock_db):
    """Test para obtener registros por fecha específica"""
    specific_date = date(2023, 6, 1)
    mock_records = [
        ClimateHistoricalDaily(id=1, location_id=1, measure_id=1, date=specific_date, value=25.0),
        ClimateHistoricalDaily(id=2, location_id=2, measure_id=1, date=specific_date, value=26.0)
    ]
    
    mock_db.query.return_value.filter.return_value.all.return_value = mock_records
    
    result = daily_service.get_by_date(specific_date, db=mock_db)
    
    assert len(result) == 2
    assert all(r.date == specific_date for r in result)

def test_get_by_date_range(daily_service, mock_db):
    """Test para obtener registros por rango de fechas"""
    start_date = date(2023, 6, 1)
    end_date = date(2023, 6, 30)
    mock_records = [
        ClimateHistoricalDaily(id=1, location_id=1, measure_id=1, date=date(2023, 6, 15), value=25.0),
        ClimateHistoricalDaily(id=2, location_id=2, measure_id=1, date=date(2023, 6, 20), value=26.0)
    ]
    
    mock_db.query.return_value.filter.return_value.all.return_value = mock_records
    
    result = daily_service.get_by_date_range(start_date, end_date, db=mock_db)
    
    assert len(result) == 2
    assert all(start_date <= r.date <= end_date for r in result)

# ---- Tests de validación ----
def test_validate_create_duplicate(daily_service, mock_db):
    """Test para validar registros duplicados"""
    record_data = {
        "location_id": 1,
        "measure_id": 1,
        "date": date(2023, 6, 1),
        "value": 25.5
    }
    
    # Configurar mock para simular que ya existe
    mock_db.query.return_value.filter.return_value.first.return_value = ClimateHistoricalDaily(id=99, **record_data)
    
    with patch.object(ClimateHistoricalDailyValidator, 'create_validate', side_effect=ValueError("Record already exists")):
        with pytest.raises(ValueError) as excinfo:
            daily_service.create(record_data, db=mock_db)
        
        assert "Record already exists" in str(excinfo.value)

# ---- Tests para validación de esquemas ----
def test_daily_schema_validation():
    """Test para validar el esquema ClimateHistoricalDailyCreate"""
    # Test de validación exitosa
    valid_data = {
        "location_id": 1,
        "measure_id": 1,
        "date": "2023-06-01",
        "value": 25.5
    }
    record = ClimateHistoricalDailyCreate(**valid_data)
    assert record.date == date(2023, 6, 1)
    
    # Test de validación fallida (fecha inválida)
    with pytest.raises(ValueError):
        ClimateHistoricalDailyCreate(location_id=1, measure_id=1, date="invalid-date", value=25.5)
    
    # Test de validación fallida (falta campo requerido)
    with pytest.raises(ValueError):
        ClimateHistoricalDailyCreate(location_id=1, measure_id=1, date="2023-06-01")  # Falta value
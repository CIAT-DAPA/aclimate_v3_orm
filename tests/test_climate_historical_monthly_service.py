import pytest
from unittest.mock import create_autospec, MagicMock, patch
from sqlalchemy.orm import Session
from datetime import date
from typing import List

# Importaciones de tu proyecto
from aclimate_v3_orm.models import (
    ClimateHistoricalMonthly,
    MngLocation,
    MngAdmin2,
    MngAdmin1,
    MngCountry,
    MngClimateMeasure
)
from aclimate_v3_orm.schemas import ClimateHistoricalMonthlyRead, ClimateHistoricalMonthlyCreate
from aclimate_v3_orm.services.climate_historical_monthly_service import (
    ClimateHistoricalMonthlyService
)
from aclimate_v3_orm.validations import ClimateHistoricalMonthlyValidator

@pytest.fixture
def mock_db():
    """Fixture para una sesión de base de datos mockeada"""
    return create_autospec(Session, instance=True)

@pytest.fixture
def monthly_service():
    """Fixture para el servicio de datos mensuales"""
    return ClimateHistoricalMonthlyService()

# ---- Tests CRUD básicos ----
def test_create_monthly_record(monthly_service, mock_db):
    """Test para crear un registro mensual"""
    record_data = ClimateHistoricalMonthlyCreate(
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
    with patch.object(ClimateHistoricalMonthlyValidator, 'create_validate'):
        result = monthly_service.create(record_data, db=mock_db)
    
    assert isinstance(result, ClimateHistoricalMonthlyRead)
    assert result.id == 1
    assert result.date == date(2023, 6, 1)
    assert result.value == 25.5

def test_update_monthly_record(monthly_service, mock_db):
    """Test para actualizar un registro mensual"""
    record_id = 1
    update_data = {"value": 26.0, "date": date(2023, 7, 1)}
    existing_record = ClimateHistoricalMonthly(
        id=record_id,
        location_id=1,
        measure_id=1,
        date=date(2023, 6, 1),
        value=25.5
    )
    
    mock_db.query.return_value.get.return_value = existing_record
    
    result = monthly_service.update(record_id, update_data, db=mock_db)
    
    assert result.value == 26.0
    assert result.date == date(2023, 7, 1)
    mock_db.commit.assert_called_once()

# ---- Tests para métodos de consulta ----
def test_get_by_location_id(monthly_service, mock_db):
    """Test para obtener registros por location_id"""
    location_id = 1
    mock_records = [
        ClimateHistoricalMonthly(id=1, location_id=location_id, measure_id=1, date=date(2023, 1, 1), value=20.0),
        ClimateHistoricalMonthly(id=2, location_id=location_id, measure_id=2, date=date(2023, 2, 1), value=21.0)
    ]
    
    mock_db.query.return_value.filter.return_value.all.return_value = mock_records
    
    result = monthly_service.get_by_location_id(location_id, db=mock_db)
    
    assert len(result) == 2
    assert all(r.location_id == location_id for r in result)

def test_get_by_location_name(monthly_service, mock_db):
    """Test para obtener registros por nombre de ubicación"""
    location_name = "Test Location"
    mock_location = MngLocation(id=1, admin_2_id=1,
                                name=location_name,
                                latitude=12.34,
                                longitude=56.78,
                                altitude=23,
                                source_id=1,
                                ext_id="Test1",
                                visible=True,
                                enable=True)
    mock_record = ClimateHistoricalMonthly(id=1, location_id=1, measure_id=1, date=date(2023, 1, 1), value=20.0)
    mock_record.location = mock_location
    
    # Configurar mocks para el join
    query_mock = MagicMock()
    join_mock = MagicMock()
    filter_mock = MagicMock()
    
    mock_db.query.return_value = query_mock
    query_mock.join.return_value = join_mock
    join_mock.filter.return_value = filter_mock
    filter_mock.all.return_value = [mock_record]
    
    result = monthly_service.get_by_location_name(location_name, db=mock_db)
    
    assert len(result) == 1
    assert result[0].location.name == location_name
    query_mock.join.assert_called_once_with(ClimateHistoricalMonthly.location)

def test_get_by_country_id(monthly_service, mock_db):
    """Test para obtener registros por country_id"""
    country_id = 1
    mock_country = MngCountry(id=country_id, name="Test Country", iso2="CL", enable=True)
    mock_admin1 = MngAdmin1(id=1, country=mock_country, name="Test", ext_id="CLIM1", enable=True, country_id=country_id)
    mock_admin2 = MngAdmin2(id=1, admin_1=mock_admin1, name="Test", ext_id="CLIM2_CTY", enable=True, admin_1_id=1, visible=True)
    mock_location = MngLocation(id=1, admin_2_id=1, admin_2=mock_admin2,
                                name="Test Location",
                                latitude=12.34,
                                longitude=56.78,
                                altitude=23,
                                source_id=1,
                                ext_id="Test1",
                                visible=True,
                                enable=True)
    mock_record = ClimateHistoricalMonthly(id=1, location_id=1, measure_id=1, date=date(2023, 1, 1), value=20.0)
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
    
    result = monthly_service.get_by_country_id(country_id, db=mock_db)
    
    assert len(result) == 1
    assert result[0].location.admin_2.admin_1.country_id == country_id

def test_get_by_admin1_id(monthly_service, mock_db):
    """Test para obtener registros por admin1_id"""
    admin1_id = 1
    mock_admin1 = MngAdmin1(id=admin1_id, name="Test", ext_id="REG1", enable=True, country_id=1)
    mock_admin2 = MngAdmin2(id=1, admin_1=mock_admin1, name="Test", ext_id="REG2", enable=True, admin_1_id=admin1_id, visible=True)
    mock_location = MngLocation(id=1, admin_2_id=1, admin_2=mock_admin2,
                                name="Test Location",
                                latitude=12.34,
                                longitude=56.78,
                                altitude=23,
                                source_id=1,
                                ext_id="Test1",
                                visible=True,
                                enable=True)
    mock_record = ClimateHistoricalMonthly(id=1, location_id=1, measure_id=1, date=date(2023, 1, 1), value=20.0)
    mock_record.location = mock_location
    
    # Configurar mocks para joins
    query_mock = MagicMock()
    join1_mock = MagicMock()
    join2_mock = MagicMock()
    filter_mock = MagicMock()
    
    mock_db.query.return_value = query_mock
    query_mock.join.return_value = join1_mock
    join1_mock.join.return_value = join2_mock
    join2_mock.filter.return_value = filter_mock
    filter_mock.all.return_value = [mock_record]
    
    result = monthly_service.get_by_admin1_id(admin1_id, db=mock_db)
    
    assert len(result) == 1
    assert result[0].location.admin_2.admin_1_id == admin1_id

def test_get_by_measure_id(monthly_service, mock_db):
    """Test para obtener registros por measure_id"""
    measure_id = 1
    mock_records = [
        ClimateHistoricalMonthly(id=1, location_id=1, measure_id=measure_id, date=date(2023, 1, 1), value=20.0),
        ClimateHistoricalMonthly(id=2, location_id=2, measure_id=measure_id, date=date(2023, 2, 1), value=21.0)
    ]
    
    mock_db.query.return_value.filter.return_value.all.return_value = mock_records
    
    result = monthly_service.get_by_measure_id(measure_id, db=mock_db)
    
    assert len(result) == 2
    assert all(r.measure_id == measure_id for r in result)

def test_get_by_date(monthly_service, mock_db):
    """Test para obtener registros por año y mes"""
    year = 2023
    month = 6
    target_date = date(year, month, 1)
    mock_records = [
        ClimateHistoricalMonthly(id=1, location_id=1, measure_id=1, date=target_date, value=25.0),
        ClimateHistoricalMonthly(id=2, location_id=2, measure_id=1, date=target_date, value=26.0)
    ]
    
    mock_db.query.return_value.filter.return_value.all.return_value = mock_records
    
    result = monthly_service.get_by_date(year, month, db=mock_db)
    
    assert len(result) == 2
    assert all(r.date == target_date for r in result)

def test_get_by_date_range(monthly_service, mock_db):
    """Test para obtener registros por rango de fechas"""
    start_date = date(2023, 6, 1)
    end_date = date(2023, 8, 1)
    mock_records = [
        ClimateHistoricalMonthly(id=1, location_id=1, measure_id=1, date=date(2023, 6, 1), value=25.0),
        ClimateHistoricalMonthly(id=2, location_id=2, measure_id=1, date=date(2023, 7, 1), value=26.0)
    ]
    
    mock_db.query.return_value.filter.return_value.all.return_value = mock_records
    
    result = monthly_service.get_by_date_range(start_date, end_date, db=mock_db)
    
    assert len(result) == 2
    assert all(start_date <= r.date <= end_date for r in result)

# ---- Tests de validación ----
def test_validate_create_duplicate(monthly_service, mock_db):
    """Test para validar registros duplicados"""
    record_data = {
        "location_id": 1,
        "measure_id": 1,
        "date": date(2023, 6, 1),
        "value": 25.5
    }
    
    # Configurar mock para simular que ya existe
    mock_db.query.return_value.filter.return_value.first.return_value = ClimateHistoricalMonthly(id=99, **record_data)
    
    with patch.object(ClimateHistoricalMonthlyValidator, 'create_validate', side_effect=ValueError("Record already exists")):
        with pytest.raises(ValueError) as excinfo:
            monthly_service.create(record_data, db=mock_db)
        
        assert "Record already exists" in str(excinfo.value)

# ---- Tests para validación de esquemas ----
def test_monthly_schema_validation():
    """Test para validar el esquema ClimateHistoricalMonthlyCreate"""
    # Test de validación exitosa
    valid_data = {
        "location_id": 1,
        "measure_id": 1,
        "date": "2023-06-01",
        "value": 25.5
    }
    record = ClimateHistoricalMonthlyCreate(**valid_data)
    assert record.date == date(2023, 6, 1)
    
    # Test de validación fallida (fecha inválida)
    with pytest.raises(ValueError):
        ClimateHistoricalMonthlyCreate(location_id=1, measure_id=1, date="invalid-date", value=25.5)
    
    # Test de validación fallida (falta campo requerido)
    with pytest.raises(ValueError):
        ClimateHistoricalMonthlyCreate(location_id=1, measure_id=1, date="2023-06-01")  # Falta value
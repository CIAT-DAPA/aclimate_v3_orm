import pytest
from unittest.mock import create_autospec, MagicMock, patch
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

# Importaciones de tu proyecto
from aclimate_v3_orm.models import (
    ClimateHistoricalClimatology,
    MngLocation,
    MngAdmin2,
    MngAdmin1,
    MngCountry,
    MngClimateMeasure
)
from aclimate_v3_orm.schemas import (
    ClimateHistoricalClimatologyRead,
    ClimateHistoricalClimatologyCreate
)
from aclimate_v3_orm.services.climate_historical_climatology_service import (
    ClimateHistoricalClimatologyService
)
from aclimate_v3_orm.validations import ClimateHistoricalClimatologyValidator

@pytest.fixture
def mock_db():
    """Fixture para una sesión de base de datos mockeada"""
    return create_autospec(Session, instance=True)

@pytest.fixture
def climatology_service():
    """Fixture para el servicio de climatología"""
    return ClimateHistoricalClimatologyService()

# ---- Tests CRUD básicos ----
def test_create_climatology_record(climatology_service, mock_db):
    """Test para crear un registro de climatología"""
    record_data = ClimateHistoricalClimatologyCreate(
        location_id=1,
        measure_id=1,
        month=6,
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
    with patch.object(ClimateHistoricalClimatologyValidator, 'create_validate'):
        result = climatology_service.create(record_data, db=mock_db)
    
    assert isinstance(result, ClimateHistoricalClimatologyRead)
    assert result.id == 1
    assert result.month == 6
    assert result.value == 25.5

def test_update_climatology_record(climatology_service, mock_db):
    """Test para actualizar un registro de climatología"""
    record_id = 1
    update_data = {"value": 26.0, "month": 7}
    existing_record = ClimateHistoricalClimatology(
        id=record_id,
        location_id=1,
        measure_id=1,
        month=6,
        value=25.5
    )
    
    mock_db.query.return_value.get.return_value = existing_record
    
    result = climatology_service.update(record_id, update_data, db=mock_db)
    
    assert result.value == 26.0
    assert result.month == 7
    mock_db.commit.assert_called_once()

# ---- Tests para métodos de consulta ----
def test_get_by_location_id(climatology_service, mock_db):
    """Test para obtener registros por location_id"""
    location_id = 1
    mock_records = [
        ClimateHistoricalClimatology(id=1, location_id=location_id, measure_id=1, month=1, value=20.0),
        ClimateHistoricalClimatology(id=2, location_id=location_id, measure_id=1, month=2, value=21.0)
    ]
    
    mock_db.query.return_value.filter.return_value.all.return_value = mock_records
    
    result = climatology_service.get_by_location_id(location_id, db=mock_db)
    
    assert len(result) == 2
    assert all(r.location_id == location_id for r in result)

def test_get_by_location_name(climatology_service, mock_db):
    """Test para obtener registros por nombre de ubicación"""
    location_name = "Test Location"
    mock_location = MngLocation(id=1, admin_2_id=1,
                                name=location_name,
                                latitude=12.34,
                                longitude=56.78,
                                altitude=23,
                                ext_id="Test1",
                                origin="CHIRPS",
                                visible=True,
                                enable=True)
    mock_record = ClimateHistoricalClimatology(id=1, location_id=1, measure_id=1, month=1, value=20.0)
    mock_record.location = mock_location
    
    # Configurar mocks para el join
    query_mock = MagicMock()
    join_mock = MagicMock()
    filter_mock = MagicMock()
    
    mock_db.query.return_value = query_mock
    query_mock.join.return_value = join_mock
    join_mock.filter.return_value = filter_mock
    filter_mock.all.return_value = [mock_record]
    
    result = climatology_service.get_by_location_name(location_name, db=mock_db)
    
    assert len(result) == 1
    assert result[0].location.name == location_name
    query_mock.join.assert_called_once_with(ClimateHistoricalClimatology.location)

def test_get_by_country_id(climatology_service, mock_db):
    """Test para obtener registros por country_id"""
    country_id = 1
    mock_country = MngCountry(id=country_id, name="Test Country", iso2="CL", enable=True)
    mock_admin1 = MngAdmin1(id=1, country=mock_country, name="Test", enable=True, country_id=country_id)
    mock_admin2 = MngAdmin2(id=1, admin_1=mock_admin1, name="Test", enable=True, admin_1_id=1, visible=True)
    mock_location = MngLocation(id=1, admin_2_id=1, admin_2=mock_admin2,
                                name="Test Location",
                                latitude=12.34,
                                longitude=56.78,
                                altitude=23,
                                ext_id="Test1",
                                origin="CHIRPS",
                                visible=True,
                                enable=True)

    mock_record = ClimateHistoricalClimatology(id=1, location_id=1, measure_id=1, month=1, value=20.0)
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
    
    result = climatology_service.get_by_country_id(country_id, db=mock_db)
    
    assert len(result) == 1
    assert result[0].location.admin_2.admin_1.country_id == country_id

def test_get_by_country_name(climatology_service, mock_db):
    """Test para obtener registros por nombre de país"""
    country_name = "Test Country"
    mock_country = MngCountry(id=1, name=country_name, iso2="CL", enable=True)
    mock_admin1 = MngAdmin1(id=1, country=mock_country, name="Test", enable=True, country_id=1)
    mock_admin2 = MngAdmin2(id=1, admin_1=mock_admin1, name="Test", enable=True, admin_1_id=1, visible=True)
    mock_location = MngLocation(id=1, admin_2_id=1, admin_2=mock_admin2,
                                name="Test Location",
                                latitude=12.34,
                                longitude=56.78,
                                altitude=23,
                                ext_id="Test1",
                                origin="CHIRPS",
                                visible=True,
                                enable=True)
    mock_record = ClimateHistoricalClimatology(id=1, location_id=1, measure_id=1, month=1, value=20.0)
    mock_record.location = mock_location
    
    # Configurar mocks para múltiples joins
    query_mock = MagicMock()
    join1_mock = MagicMock()
    join2_mock = MagicMock()
    join3_mock = MagicMock()
    join4_mock = MagicMock()
    filter_mock = MagicMock()
    
    mock_db.query.return_value = query_mock
    query_mock.join.return_value = join1_mock
    join1_mock.join.return_value = join2_mock
    join2_mock.join.return_value = join3_mock
    join3_mock.join.return_value = join4_mock
    join4_mock.filter.return_value = filter_mock
    filter_mock.all.return_value = [mock_record]
    
    result = climatology_service.get_by_country_name(country_name, db=mock_db)
    
    assert len(result) == 1
    assert result[0].location.admin_2.admin_1.country.name == country_name

def test_get_by_admin1_id(climatology_service, mock_db):
    """Test para obtener registros por admin1_id"""
    admin1_id = 1
    
    # Configurar objetos relacionados
    mock_admin1 = MngAdmin1(id=admin1_id, country_id=1, name="region 1", enable=True)
    mock_admin2 = MngAdmin2(id=1, admin_1_id=admin1_id, name="region2", visible=True, enable=True, admin_1=mock_admin1)
    mock_location = MngLocation(id=1,
                                admin_2_id=1, 
                                admin_2=mock_admin2,
                                latitude=12.34,
                                longitude=56.78,
                                visible=True,
                                name="Test Location",
                                altitude=23,
                                ext_id="Test1",
                                origin="CHIRPS",
                                enable=True)
        

    mock_record = ClimateHistoricalClimatology(id=1, 
                                               location_id=1, 
                                               measure_id=1, 
                                               month=1, 
                                               value=20.0)
    mock_record.location = mock_location
    
    # Configurar mocks para la cadena de llamadas
    query_mock = MagicMock()
    join1_mock = MagicMock()
    join2_mock = MagicMock()
    filter_mock = MagicMock()
    
    mock_db.query.return_value = query_mock
    query_mock.join.return_value = join1_mock  # Primer join (location)
    join1_mock.join.return_value = join2_mock  # Segundo join (admin_2)
    join2_mock.filter.return_value = filter_mock
    filter_mock.all.return_value = [mock_record]
    
    result = climatology_service.get_by_admin1_id(admin1_id, db=mock_db)
    
    # Verificaciones
    assert len(result) == 1
    assert result[0].location.admin_2.admin_1_id == admin1_id
    
    # Verificar que los joins se hicieron correctamente
    query_mock.join.assert_called_once_with(ClimateHistoricalClimatology.location)
    join1_mock.join.assert_called_once_with(MngLocation.admin_2)
    join2_mock.filter.assert_called_once()

def test_get_by_month(climatology_service, mock_db):
    """Test para obtener registros por mes"""
    month = 6
    mock_records = [
        ClimateHistoricalClimatology(id=1, location_id=1, measure_id=1, month=month, value=25.0),
        ClimateHistoricalClimatology(id=2, location_id=2, measure_id=1, month=month, value=26.0)
    ]
    
    mock_db.query.return_value.filter.return_value.all.return_value = mock_records
    
    result = climatology_service.get_by_month(month, db=mock_db)
    
    assert len(result) == 2
    assert all(r.month == month for r in result)

def test_get_by_measure_id(climatology_service, mock_db):
    """Test para obtener registros por measure_id"""
    measure_id = 1
    mock_records = [
        ClimateHistoricalClimatology(id=1, location_id=1, measure_id=measure_id, month=1, value=20.0),
        ClimateHistoricalClimatology(id=2, location_id=2, measure_id=measure_id, month=2, value=21.0)
    ]
    
    mock_db.query.return_value.filter.return_value.all.return_value = mock_records
    
    result = climatology_service.get_by_measure_id(measure_id, db=mock_db)
    
    assert len(result) == 2
    assert all(r.measure_id == measure_id for r in result)

def test_get_by_measure_name(climatology_service, mock_db):
    """Test para obtener registros por nombre de medida"""
    measure_name = "Temperature"
    mock_measure = MngClimateMeasure(id=1, name=measure_name, short_name="TMAX", unit="C", description="test", enable=True)
    mock_record = ClimateHistoricalClimatology(id=1, location_id=1, measure_id=1, month=1, value=20.0)
    mock_record.measure = mock_measure
    
    # Configurar mocks para el join
    query_mock = MagicMock()
    join_mock = MagicMock()
    filter_mock = MagicMock()
    
    mock_db.query.return_value = query_mock
    query_mock.join.return_value = join_mock
    join_mock.filter.return_value = filter_mock
    filter_mock.all.return_value = [mock_record]
    
    result = climatology_service.get_by_measure_name(measure_name, db=mock_db)
    
    assert len(result) == 1
    assert result[0].measure.name == measure_name

# ---- Tests de validación ----
def test_validate_create_duplicate(climatology_service, mock_db):
    """Test para validar registros duplicados"""
    record_data = ClimateHistoricalClimatologyCreate(
        location_id=1,
        measure_id=1,
        month=6,
        value=25.5
    )
    
    # Configurar mock para simular que ya existe
    mock_db.query.return_value.filter.return_value.first.return_value = ClimateHistoricalClimatology(id=99, location_id=1, measure_id=1, month=6)
    
    with patch.object(ClimateHistoricalClimatologyValidator, 'create_validate', side_effect=ValueError("Record already exists")):
        with pytest.raises(ValueError) as excinfo:
            climatology_service.create(record_data, db=mock_db)
        
        assert "Record already exists" in str(excinfo.value)

# ---- Tests para validación de esquemas ----
def test_climatology_schema_validation():
    """Test para validar el esquema ClimateHistoricalClimatologyCreate"""
    # Test de validación exitosa
    valid_data = {
        "location_id": 1,
        "measure_id": 1,
        "month": 6,
        "value": 25.5
    }
    record = ClimateHistoricalClimatologyCreate(**valid_data)
    assert record.month == 6
    
    # Test de validación fallida (mes inválido)
    with pytest.raises(ValueError):
        ClimateHistoricalClimatologyCreate(location_id=1, measure_id=1, month=13, value=25.5)
    
    # Test de validación fallida (falta campo requerido)
    with pytest.raises(ValueError):
        ClimateHistoricalClimatologyCreate(location_id=1, measure_id=1, month=6)  # Falta value
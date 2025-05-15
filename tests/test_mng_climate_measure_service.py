import pytest
from unittest.mock import create_autospec, MagicMock, patch
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List

# Importaciones de tu proyecto
from aclimate_v3_orm.models import MngClimateMeasure
from aclimate_v3_orm.schemas import ClimateMeasureCreate, ClimateMeasureRead, ClimateMeasureUpdate
from aclimate_v3_orm.services.mng_climate_measure_service import MngClimateMeasureService
from aclimate_v3_orm.validations import MngClimateMeasureNameValidator

@pytest.fixture
def mock_db():
    """Fixture para una sesión de base de datos mockeada"""
    return create_autospec(Session, instance=True)

@pytest.fixture
def climate_measure_service():
    """Fixture para el servicio de medidas climáticas"""
    return MngClimateMeasureService()

# ---- Tests CRUD básicos ----
def test_create_climate_measure(climate_measure_service, mock_db):
    """Test para crear una medida climática"""
    measure_data = ClimateMeasureCreate(
        name="Temperature",
        short_name="TEMP",
        unit="°C",
        description="Average temperature",
        enable=True
    )
    
    # Configurar mocks
    mock_db.query.return_value.filter.return_value.first.return_value = None
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    
    def mock_refresh(obj):
        obj.id = 1
    
    mock_db.refresh.side_effect = mock_refresh
    
    # Mockear validación
    with patch.object(MngClimateMeasureNameValidator, 'validate'):
        result = climate_measure_service.create(measure_data, db=mock_db)
    
    assert isinstance(result, ClimateMeasureRead)
    assert result.id == 1
    assert result.name == "Temperature"
    assert result.short_name == "TEMP"
    assert result.unit == "°C"

def test_update_climate_measure(climate_measure_service, mock_db):
    """Test para actualizar una medida climática"""
    measure_id = 1
    update_data = ClimateMeasureUpdate(
        short_name="TMP",
        description="Updated description"
    )
    existing_measure = MngClimateMeasure(
        id=measure_id,
        name="Temperature",
        short_name="TEMP",
        unit="°C",
        enable=True
    )
    
    mock_db.query.return_value.get.return_value = existing_measure
    
    result = climate_measure_service.update(measure_id, update_data, db=mock_db)
    
    assert result.short_name == "TMP"
    assert result.description == "Updated description"
    mock_db.commit.assert_called_once()

def test_delete_climate_measure(climate_measure_service, mock_db):
    """Test para eliminar (deshabilitar) una medida climática"""
    measure_id = 1
    existing_measure = MngClimateMeasure(
        id=measure_id,
        name="Temperature",
        short_name="TEMP",
        unit="°C",
        enable=True
    )
    
    mock_db.query.return_value.get.return_value = existing_measure
    
    result = climate_measure_service.delete(measure_id, db=mock_db)
    
    assert result is True
    assert existing_measure.enable is False
    mock_db.commit.assert_called_once()

# ---- Tests para métodos específicos ----
def test_get_by_name(climate_measure_service, mock_db):
    """Test para obtener medidas por nombre"""
    measure_name = "Temperature"
    mock_measures = [
        MngClimateMeasure(id=1, name=measure_name, short_name="TEMP", unit="°C", enable=True),
        MngClimateMeasure(id=2, name=measure_name, short_name="TEMP2", unit="°C", enable=False)
    ]
    
    # Test para medidas habilitadas
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_measures[0]]
    result = climate_measure_service.get_by_name(measure_name, db=mock_db)
    assert len(result) == 1
    assert result[0].name == measure_name
    assert result[0].enable is True
    
    # Test para todas las medidas (incluyendo deshabilitadas)
    mock_db.query.return_value.filter.return_value.all.return_value = mock_measures
    result = climate_measure_service.get_by_name(measure_name, enabled=None, db=mock_db)
    assert len(result) == 2

def test_get_by_short_name(climate_measure_service, mock_db):
    """Test para obtener medidas por nombre corto"""
    short_name = "TEMP"
    mock_measure = MngClimateMeasure(
        id=1, 
        name="Temperature", 
        short_name=short_name, 
        unit="°C", 
        enable=True
    )
    
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_measure]
    
    result = climate_measure_service.get_by_short_name(short_name, db=mock_db)
    
    assert len(result) == 1
    assert result[0].short_name == short_name
    assert result[0].enable is True

def test_get_all(climate_measure_service, mock_db):
    """Test para obtener todas las medidas climáticas"""
    mock_measures = [
        MngClimateMeasure(id=1, name="Temp", short_name="TEMP", unit="°C", enable=True),
        MngClimateMeasure(id=2, name="Precip", short_name="PREC", unit="mm", enable=True),
        MngClimateMeasure(id=3, name="Humidity", short_name="HUM", unit="%", enable=False)
    ]
    
    # Test para medidas habilitadas
    mock_db.query.return_value.filter.return_value.all.return_value = mock_measures[:2]
    result = climate_measure_service.get_all(db=mock_db)
    assert len(result) == 2
    assert all(m.enable is True for m in result)
    
    # Test para todas las medidas
    mock_db.query.return_value.all.return_value = mock_measures
    result = climate_measure_service.get_all(enabled=None, db=mock_db)
    assert len(result) == 3

# ---- Tests de validación ----
def test_validate_create_duplicate_name(climate_measure_service, mock_db):
    """Test para validar nombre duplicado al crear medida"""
    measure_data = ClimateMeasureCreate(
        name="Temperature",
        short_name="TEMP",
        unit="°C"
    )
    
    # Configurar mock para simular que ya existe
    mock_db.query.return_value.filter.return_value.first.return_value = MngClimateMeasure(id=99, name="Temperature")
    
    with patch.object(MngClimateMeasureNameValidator, 'validate', side_effect=ValueError("Name already exists")):
        with pytest.raises(ValueError) as excinfo:
            climate_measure_service.create(measure_data, db=mock_db)
        
        assert "Name already exists" in str(excinfo.value)

def test_validate_create_duplicate_short_name(climate_measure_service, mock_db):
    """Test para validar short_name duplicado al crear medida"""
    measure_data = ClimateMeasureCreate(
        name="New Temp",
        short_name="TEMP",
        unit="°C"
    )
    
    # Configurar mock para simular que ya existe
    mock_db.query.return_value.filter.return_value.first.return_value = MngClimateMeasure(id=99, short_name="TEMP")
    
    with pytest.raises(ValueError) as excinfo:
        climate_measure_service.create(measure_data, db=mock_db)
    
    assert "The climate measure with the name 'New Temp' already exists." in str(excinfo.value)

# ---- Tests para esquemas ----
def test_climate_measure_schema_validation():
    """Test para validar el esquema ClimateMeasureCreate"""
    # Test de validación exitosa
    valid_data = {
        "name": "Temperature",
        "short_name": "TEMP",
        "unit": "°C"
    }
    measure = ClimateMeasureCreate(**valid_data)
    assert measure.name == "Temperature"
    
    # Test de validación fallida (campo vacío)
    with pytest.raises(ValueError):
        ClimateMeasureCreate(name=" ", short_name="TEMP", unit="°C")
    
    # Test de validación fallida (falta campo requerido)
    with pytest.raises(ValueError):
        ClimateMeasureCreate(name="Temperature", short_name="TEMP")  # Falta unit
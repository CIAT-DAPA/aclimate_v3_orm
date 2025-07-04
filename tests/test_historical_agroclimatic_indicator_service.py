# test_historical_agroclimatic_indicator_service.py
import pytest
from unittest.mock import create_autospec, patch, MagicMock
from sqlalchemy.orm import Session
from datetime import date

# Importaciones de tu proyecto
from aclimate_v3_orm.models import HistoricalAgroclimaticIndicator
from aclimate_v3_orm.schemas import (
    HistoricalAgroclimaticIndicatorCreate,
    HistoricalAgroclimaticIndicatorRead,
    HistoricalAgroclimaticIndicatorUpdate
)
from aclimate_v3_orm.services import HistoricalAgroclimaticIndicatorService
from aclimate_v3_orm.validations import HistoricalAgroclimaticIndicatorValidator

@pytest.fixture
def mock_db():
    """Fixture para una sesión de base de datos mockeada"""
    return create_autospec(Session, instance=True)

@pytest.fixture
def indicator_service():
    """Fixture para el servicio de indicadores agroclimáticos históricos"""
    return HistoricalAgroclimaticIndicatorService()

def test_get_by_location(indicator_service, mock_db):
    """Test para obtener indicadores por location_id"""
    # Configurar datos de prueba
    mock_indicators = [
        HistoricalAgroclimaticIndicator(id=1, location_id=100, indicator_id=10, phenological_id=1, value=20.0, start_date=date(2023, 1, 1), end_date=date(2023, 1, 31)),
        HistoricalAgroclimaticIndicator(id=2, location_id=100, indicator_id=11, phenological_id=1, value=25.0, start_date=date(2023, 2, 1), end_date=date(2023, 2, 28))
    ]
    
    # Configurar el mock
    mock_db.query.return_value.filter.return_value.all.return_value = mock_indicators
    
    # Ejecutar el método
    result = indicator_service.get_by_location(100, db=mock_db)
    
    # Verificar resultados
    assert len(result) == 2
    assert all(isinstance(item, HistoricalAgroclimaticIndicatorRead) for item in result)
    assert all(item.location_id == 100 for item in result)
    
    # Verificar llamadas a la base de datos
    mock_db.query.assert_called_once_with(HistoricalAgroclimaticIndicator)
    mock_db.query.return_value.filter.assert_called_once()

def test_get_by_indicator(indicator_service, mock_db):
    """Test para obtener indicadores por indicator_id"""
    # Configurar datos de prueba
    mock_indicators = [
        HistoricalAgroclimaticIndicator(id=3, location_id=200, indicator_id=20, phenological_id=2, value=30.0, start_date=date(2023, 3, 1), end_date=date(2023, 3, 31)),
        HistoricalAgroclimaticIndicator(id=4, location_id=201, indicator_id=20, phenological_id=2, value=35.0, start_date=date(2023, 4, 1), end_date=date(2023, 4, 30))
    ]
    
    # Configurar el mock
    mock_db.query.return_value.filter.return_value.all.return_value = mock_indicators
    
    # Ejecutar el método
    result = indicator_service.get_by_indicator(20, db=mock_db)
    
    # Verificar resultados
    assert len(result) == 2
    assert all(isinstance(item, HistoricalAgroclimaticIndicatorRead) for item in result)
    assert all(item.indicator_id == 20 for item in result)
    
    # Verificar llamadas a la base de datos
    mock_db.query.assert_called_once_with(HistoricalAgroclimaticIndicator)
    mock_db.query.return_value.filter.assert_called_once()

def test_create_indicator_valid(indicator_service, mock_db):
    """Test para crear un indicador válido"""
    # Configurar datos de prueba
    indicator_data = HistoricalAgroclimaticIndicatorCreate(
        indicator_id=30,
        location_id=300,
        phenological_id=3,
        value=25.5,
        start_date=date(2023, 1, 1),
        end_date=date(2023, 1, 31)
    )
    mock_new_indicator = HistoricalAgroclimaticIndicator(
        id=5,
        **indicator_data.model_dump()
    )
    
    # Configurar el mock para refresh
    def mock_refresh(obj):
        if obj.id is None:
            obj.id = 5
    
    # Configurar los mocks
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.side_effect = mock_refresh
    
    # Mockear la validación
    with patch.object(HistoricalAgroclimaticIndicatorValidator, 'create_validate') as mock_validate:
        # Ejecutar el método
        result = indicator_service.create(obj_in=indicator_data, db=mock_db)
    
    # Verificar resultados
    assert isinstance(result, HistoricalAgroclimaticIndicatorRead)
    assert result.id == 5
    assert result.indicator_id == indicator_data.indicator_id
    assert result.location_id == indicator_data.location_id
    assert result.phenological_id == indicator_data.phenological_id
    assert result.value == indicator_data.value
    assert result.start_date == indicator_data.start_date
    assert result.end_date == indicator_data.end_date
    
    # Verificar llamadas
    mock_validate.assert_called_once_with(mock_db, indicator_data)
    mock_db.add.assert_called_once()
    mock_db.refresh.assert_called_once()

def test_update_indicator(indicator_service, mock_db):
    """Test para actualizar un indicador"""
    # Configurar datos de prueba
    indicator_id = 6
    existing_indicator = HistoricalAgroclimaticIndicator(
        id=indicator_id,
        indicator_id=40,
        location_id=400,
        phenological_id=4,
        value=15.0,
        start_date=date(2023, 2, 1),
        end_date=date(2023, 2, 28)
    )
    update_data = HistoricalAgroclimaticIndicatorUpdate(
        value=17.5,
        end_date=date(2023, 3, 15)
    )
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_indicator
    
    # Ejecutar el método
    result = indicator_service.update(indicator_id, update_data, db=mock_db)
    
    # Verificar resultados
    assert isinstance(result, HistoricalAgroclimaticIndicatorRead)
    assert result.id == indicator_id
    assert result.value == update_data.value
    assert result.end_date == update_data.end_date
    # Campos no actualizados deben permanecer igual
    assert result.indicator_id == existing_indicator.indicator_id
    assert result.location_id == existing_indicator.location_id
    assert result.phenological_id == existing_indicator.phenological_id
    assert result.start_date == existing_indicator.start_date
    
    # Verificar llamadas
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

def test_delete_indicator(indicator_service, mock_db):
    """Test para eliminar un indicador (borrado físico)"""
    # Configurar datos de prueba
    indicator_id = 7
    existing_indicator = HistoricalAgroclimaticIndicator(
        id=indicator_id,
        indicator_id=50,
        location_id=500,
        phenological_id=5,
        value=10.0,
        start_date=date(2023, 3, 1),
        end_date=date(2023, 3, 31)
    )
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_indicator
    
    # Ejecutar el método
    result = indicator_service.delete(indicator_id, db=mock_db)
    
    # Verificar resultados
    assert result is True
    # Como no hay campo enable, debería eliminarse físicamente
    mock_db.delete.assert_called_once_with(existing_indicator)
    mock_db.commit.assert_called_once()

def test_get_by_location_empty(indicator_service, mock_db):
    """Test para cuando no hay indicadores para un location_id"""
    # Configurar el mock para devolver lista vacía
    mock_db.query.return_value.filter.return_value.all.return_value = []
    
    # Ejecutar el método
    result = indicator_service.get_by_location(999, db=mock_db)
    
    # Verificar resultados
    assert isinstance(result, list)
    assert len(result) == 0

def test_get_by_indicator_empty(indicator_service, mock_db):
    """Test para cuando no hay indicadores para un indicator_id"""
    # Configurar el mock para devolver lista vacía
    mock_db.query.return_value.filter.return_value.all.return_value = []
    
    # Ejecutar el método
    result = indicator_service.get_by_indicator(999, db=mock_db)
    
    # Verificar resultados
    assert isinstance(result, list)
    assert len(result) == 0

def test_create_indicator_validation_failure(indicator_service, mock_db):
    """Test para validar fallos en la creación de indicador"""
    # Configurar datos de prueba
    indicator_data = HistoricalAgroclimaticIndicatorCreate(
        indicator_id=60,
        location_id=600,
        phenological_id=6,
        value=20.0,
        start_date=date(2023, 4, 1),
        end_date=date(2023, 3, 31)  # Fecha final anterior a la inicial
    )
    
    # Mockear la validación para que lance excepción
    with patch.object(HistoricalAgroclimaticIndicatorValidator, 'create_validate', 
                     side_effect=ValueError("End date must be after start date")):
        with pytest.raises(ValueError) as excinfo:
            indicator_service.create(indicator_data, db=mock_db)
        
        assert "End date must be after start date" in str(excinfo.value)
    
    # Verificar que no se llamó a commit
    mock_db.commit.assert_not_called()

def test_partial_update_indicator(indicator_service, mock_db):
    """Test para actualización parcial de un indicador"""
    # Configurar datos de prueba
    indicator_id = 8
    existing_indicator = HistoricalAgroclimaticIndicator(
        id=indicator_id,
        indicator_id=70,
        location_id=700,
        phenological_id=7,
        value=30.0,
        start_date=date(2023, 5, 1),
        end_date=date(2023, 5, 31)
    )
    update_data = HistoricalAgroclimaticIndicatorUpdate(
        value=32.5  # Solo actualizar valor
    )
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_indicator
    
    # Ejecutar el método
    result = indicator_service.update(indicator_id, update_data, db=mock_db)
    
    # Verificar resultados
    assert result.indicator_id == existing_indicator.indicator_id  # No cambió
    assert result.location_id == existing_indicator.location_id  # No cambió
    assert result.phenological_id == existing_indicator.phenological_id  # No cambió
    assert result.value == update_data.value  # Actualizado

def test_update_indicator_dates(indicator_service, mock_db):
    """Test para actualizar las fechas de un indicador"""
    # Configurar datos de prueba
    indicator_id = 9
    existing_indicator = HistoricalAgroclimaticIndicator(
        id=indicator_id,
        indicator_id=80,
        location_id=800,
        phenological_id=8,
        value=40.0,
        start_date=date(2023, 6, 1),
        end_date=date(2023, 6, 30)
    )
    update_data = HistoricalAgroclimaticIndicatorUpdate(
        start_date=date(2023, 6, 15),
        end_date=date(2023, 7, 15)
    )
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_indicator
    
    # Ejecutar el método
    result = indicator_service.update(indicator_id, update_data, db=mock_db)
    
    # Verificar resultados
    assert result.start_date == update_data.start_date
    assert result.end_date == update_data.end_date

def test_create_indicator_with_foreign_keys(indicator_service, mock_db):
    """Test para verificar manejo de claves foráneas"""
    # Configurar datos de prueba
    indicator_data = HistoricalAgroclimaticIndicatorCreate(
        indicator_id=90,
        location_id=900,
        phenological_id=9,
        value=50.0,
        start_date=date(2023, 7, 1),
        end_date=date(2023, 7, 31)
    )
    
    # Configurar el mock para refresh
    def mock_refresh(obj):
        obj.id = 10
    
    # Configurar los mocks
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.side_effect = mock_refresh
    
    # Mockear la validación
    with patch.object(HistoricalAgroclimaticIndicatorValidator, 'create_validate') as mock_validate:
        # Ejecutar el método
        result = indicator_service.create(obj_in=indicator_data, db=mock_db)
    
    # Verificar que las claves foráneas se mantienen
    assert result.indicator_id == indicator_data.indicator_id
    assert result.location_id == indicator_data.location_id
    assert result.phenological_id == indicator_data.phenological_id

def test_get_by_location_with_relations(indicator_service, mock_db):
    """Test para obtener indicadores con relaciones cargadas (aunque no se serializan)"""
    # Configurar datos de prueba
    mock_indicator = HistoricalAgroclimaticIndicator(
        id=11, 
        indicator_id=100, 
        location_id=1000,
        phenological_id=10,
        value=60.0,
        start_date=date(2023, 8, 1),
        end_date=date(2023, 8, 31)
    )
    # Agregar relaciones ficticias
    mock_indicator.indicator = MagicMock()
    mock_indicator.location = MagicMock()
    mock_indicator.phenological_stage = MagicMock()
    
    # Configurar el mock
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_indicator]
    
    # Ejecutar el método
    result = indicator_service.get_by_location(1000, db=mock_db)
    
    # Verificar resultados
    assert len(result) == 1
    assert result[0].id == 11
    # Las relaciones no deberían estar en el resultado serializado
    assert not hasattr(result[0], 'indicator')
    assert not hasattr(result[0], 'location')
    assert not hasattr(result[0], 'phenological_stage')
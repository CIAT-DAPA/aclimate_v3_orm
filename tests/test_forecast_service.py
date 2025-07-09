import pytest
from unittest.mock import create_autospec, MagicMock, patch
from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta, timezone
from typing import List, Optional

from aclimate_v3_orm.models import Forecast
from aclimate_v3_orm.schemas import ForecastCreate, ForecastRead, ForecastUpdate
from aclimate_v3_orm.services import ForecastService
from aclimate_v3_orm.validations import ForecastValidator

@pytest.fixture
def mock_db():
    """Fixture para una sesión de base de datos mockeada"""
    return create_autospec(Session, instance=True)

@pytest.fixture
def forecast_service():
    """Fixture para el servicio de pronósticos"""
    return ForecastService()

# ---- Tests para métodos específicos de ForecastService ----
def test_get_by_run_date(forecast_service, mock_db):
    """Test para obtener pronósticos por fecha de ejecución exacta"""
    run_date = date(2023, 10, 5)
    mock_forecasts = [
        Forecast(id=1, run_date=run_date, country_id=1, enable=True),
        Forecast(id=2, run_date=run_date, country_id=2, enable=True)
    ]
    
    mock_db.query.return_value.filter.return_value.all.return_value = mock_forecasts
    
    result = forecast_service.get_by_run_date(run_date, enabled=True, db=mock_db)
    
    assert len(result) == 2
    assert all(f.run_date == run_date for f in result)
    assert all(f.enable is True for f in result)

def test_get_by_run_date_disabled(forecast_service, mock_db):
    """Test para obtener pronósticos deshabilitados por fecha"""
    run_date = date(2023, 10, 5)
    mock_forecasts = [
        Forecast(id=3, run_date=run_date, country_id=3, enable=False)
    ]
    
    mock_db.query.return_value.filter.return_value.all.return_value = mock_forecasts
    
    result = forecast_service.get_by_run_date(run_date, enabled=False, db=mock_db)
    
    assert len(result) == 1
    assert result[0].id == 3
    assert result[0].enable is False

def test_get_by_date_range(forecast_service, mock_db):
    """Test para obtener pronósticos en un rango de fechas"""
    start_date = date(2023, 10, 1)
    end_date = date(2023, 10, 31)
    mock_forecasts = [
        Forecast(id=1, country_id=1, run_date=date(2023, 10, 5), enable=True), 
        Forecast(id=2, country_id=1, run_date=date(2023, 10, 15), enable=True)
    ]
    
    mock_db.query.return_value.filter.return_value.all.return_value = mock_forecasts
    
    result = forecast_service.get_by_date_range(start_date, end_date, enabled=True, db=mock_db)
    
    assert len(result) == 2
    assert all(start_date <= f.run_date <= end_date for f in result)

def test_get_by_date_range_empty(forecast_service, mock_db):
    """Test para rango de fechas sin resultados"""
    start_date = date(2023, 11, 1)
    end_date = date(2023, 11, 30)
    
    mock_db.query.return_value.filter.return_value.all.return_value = []
    
    result = forecast_service.get_by_date_range(start_date, end_date, enabled=True, db=mock_db)
    
    assert len(result) == 0

# ---- Tests para validación durante la creación ----
def test_create_forecast_with_validation(forecast_service, mock_db):
    """Test que verifica que se llama a la validación durante la creación"""
    forecast_data = ForecastCreate(
        country_id=1,
        run_date=date(2023, 10, 5)
    )
    
    # Mockear operaciones de base de datos
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    
    def mock_refresh(obj):
        obj.id = 1
    
    mock_db.refresh.side_effect = mock_refresh
    
    # Mockear validación
    with patch.object(ForecastValidator, 'create_validate') as mock_validate:
        result = forecast_service.create(forecast_data, db=mock_db)
    
    mock_validate.assert_called_once_with(mock_db, forecast_data)
    assert result.id == 1
    assert result.run_date == date(2023, 10, 5)

def test_create_forecast_validation_error(forecast_service, mock_db):
    """Test que verifica el manejo de errores de validación al crear"""
    invalid_data = ForecastCreate(
        country_id=1,
        run_date=date(2023, 10, 5)
    )
    
    # Configurar validación para lanzar error
    with patch.object(ForecastValidator, 'create_validate', 
                     side_effect=ValueError("Validation error")) as mock_validate:
        with pytest.raises(ValueError) as excinfo:
            forecast_service.create(invalid_data, db=mock_db)
        assert "Validation error" in str(excinfo.value)
    
    # Asegurar que no se hizo commit
    mock_db.commit.assert_not_called()

# ---- Tests para operaciones CRUD básicas ----
def test_create_forecast(forecast_service, mock_db):
    """Test para crear un nuevo pronóstico"""
    forecast_data = ForecastCreate(
        country_id=1,
        run_date=date(2023, 10, 5),
        enable=True)
    
    # Mockear validación y operaciones de DB
    with patch.object(ForecastValidator, 'create_validate'):
        mock_db.add.return_value = None
        mock_db.commit.return_value = None
        
        def mock_refresh(obj):
            obj.id = 1
        
        mock_db.refresh.side_effect = mock_refresh
        
        result = forecast_service.create(forecast_data, db=mock_db)
    
    assert result.id == 1
    assert result.country_id == 1
    assert result.run_date == date(2023, 10, 5)

def test_update_forecast(forecast_service, mock_db):
    """Test para actualizar un pronóstico existente"""
    forecast_id = 1
    update_data = {"run_date": date(2023, 10, 10)}  # Actualizar la fecha
    
    existing_forecast = Forecast(
        id=forecast_id,
        country_id=1,
        run_date=date(2023, 10, 5),
        enable=True
    )
    
    mock_db.query.return_value.get.return_value = existing_forecast
    
    # Simula el comportamiento de onupdate
    def mock_commit():
        existing_forecast.updated = datetime.now(timezone.utc)
    mock_db.commit.side_effect = mock_commit

    result = forecast_service.update(forecast_id, update_data, db=mock_db)
    
    assert result.run_date == date(2023, 10, 10)
    assert existing_forecast.updated is not None
    mock_db.commit.assert_called_once()

def test_delete_forecast(forecast_service, mock_db):
    """Test para eliminar (desactivar) un pronóstico"""
    forecast_id = 1
    existing_forecast = Forecast(
        id=forecast_id,
        country_id=1,
        run_date=date(2023, 10, 5),
        enable=True
    )
    
    mock_db.query.return_value.get.return_value = existing_forecast
    
    result = forecast_service.delete(forecast_id, db=mock_db)
    
    assert result is True
    assert existing_forecast.enable is False  # Verificar que se desactivó
    mock_db.commit.assert_called_once()

def test_get_by_id_found(forecast_service, mock_db):
    """Test para obtener un pronóstico por ID (encontrado)"""
    forecast_id = 1
    mock_forecast = Forecast(
        id=forecast_id,
        country_id=1,
        run_date=date(2023, 10, 5),
        enable=True
    )
    
    mock_db.query.return_value.get.return_value = mock_forecast
    
    result = forecast_service.get_by_id(forecast_id, db=mock_db)
    
    assert result.id == forecast_id
    assert result.country_id == 1

def test_get_by_id_not_found(forecast_service, mock_db):
    """Test para obtener un pronóstico por ID (no encontrado)"""
    forecast_id = 999
    mock_db.query.return_value.get.return_value = None
    
    result = forecast_service.get_by_id(forecast_id, db=mock_db)
    
    assert result is None

def test_get_all_forecasts(forecast_service, mock_db):
    """Test para obtener todos los pronósticos"""
    mock_forecasts = [
        Forecast(id=1, country_id=1, run_date=date(2023, 10, 5), enable=True),
        Forecast(id=2, country_id=2, run_date=date(2023, 10, 6), enable=True)
    ]
    
    mock_db.query.return_value.all.return_value = mock_forecasts
    
    result = forecast_service.get_all(db=mock_db)
    
    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 2

def test_get_all_forecasts_with_filters(forecast_service, mock_db):
    """Test para obtener pronósticos con filtros adicionales"""
    filters = {"country_id": 1}
    mock_forecasts = [
        Forecast(id=1, country_id=1, run_date=date(2023, 10, 5), enable=True)
    ]
    
    mock_db.query.return_value.filter_by.return_value.all.return_value = mock_forecasts
    
    result = forecast_service.get_all(db=mock_db, filters=filters)
    
    assert len(result) == 1
    assert result[0].country_id == 1
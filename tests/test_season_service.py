# test_season_service.py
import pytest
from unittest.mock import create_autospec, patch
from sqlalchemy.orm import Session
from datetime import date
from typing import List

# Importaciones de tu proyecto
from aclimate_v3_orm.models import Season
from aclimate_v3_orm.schemas import SeasonCreate, SeasonRead, SeasonUpdate
from aclimate_v3_orm.services import SeasonService
from aclimate_v3_orm.validations import SeasonValidator

@pytest.fixture
def mock_db():
    """Fixture para una sesión de base de datos mockeada"""
    return create_autospec(Session, instance=True)

@pytest.fixture
def service():
    """Fixture para el servicio de temporadas"""
    return SeasonService()

def test_get_by_location(service, mock_db):
    """Test para obtener temporadas por location_id"""
    # Configurar datos de prueba
    mock_seasons = [
        Season(id=1, location_id=100, crop_id=200, 
            planting_start=date(2023, 1, 1), planting_end=date(2023, 1, 31),
            season_start=date(2023, 1, 1), season_end=date(2023, 4, 30)),
        Season(id=2, location_id=100, crop_id=201, 
            planting_start=date(2023, 2, 1), planting_end=date(2023, 2, 28),
            season_start=date(2023, 2, 1), season_end=date(2023, 5, 31))
    ]
    
    # Configurar el mock
    mock_db.query.return_value.filter.return_value.all.return_value = mock_seasons
    
    # Ejecutar el método
    result = service.get_by_location(100, db=mock_db)
    
    # Verificar resultados
    assert len(result) == 2
    assert all(isinstance(item, SeasonRead) for item in result)
    assert all(item.location_id == 100 for item in result)
    
    # Verificar llamadas a la base de datos
    mock_db.query.assert_called_once_with(Season)
    mock_db.query.return_value.filter.assert_called_once()

def test_get_by_crop(service, mock_db):
    """Test para obtener temporadas por crop_id"""
    # Configurar datos de prueba
    mock_seasons = [
        Season(id=3, location_id=101, crop_id=300, 
               planting_start=date(2023, 3, 1), planting_end=date(2023, 3, 31), 
               season_start=date(2023, 3, 1), season_end=date(2023, 6, 30)),
        Season(id=4, location_id=102, crop_id=300, 
               planting_start=date(2023, 4, 1), planting_end=date(2023, 4, 30),
               season_start=date(2023, 4, 1), season_end=date(2023, 7, 31))
    ]
    
    # Configurar el mock
    mock_db.query.return_value.filter.return_value.all.return_value = mock_seasons
    
    # Ejecutar el método
    result = service.get_by_crop(300, db=mock_db)
    
    # Verificar resultados
    assert len(result) == 2
    assert all(isinstance(item, SeasonRead) for item in result)
    assert all(item.crop_id == 300 for item in result)
    
    # Verificar llamadas a la base de datos
    mock_db.query.assert_called_once_with(Season)
    mock_db.query.return_value.filter.assert_called_once()

def test_create_season_valid(service, mock_db):
    """Test para crear una temporada válida"""
    # Configurar datos de prueba
    season_data = SeasonCreate(
        location_id=200,
        crop_id=400,
        planting_start=date(2024, 1, 1),
        planting_end=date(2024, 1, 31),
        season_start=date(2024, 1, 1),
        season_end=date(2024, 4, 30)
    )
    mock_new_season = Season(
        id=5, 
        location_id=season_data.location_id,
        crop_id=season_data.crop_id,
        planting_start=season_data.planting_start,
        planting_end=season_data.planting_end,
        season_start=season_data.season_start,
        season_end=season_data.season_end 
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
    with patch.object(SeasonValidator, 'create_validate') as mock_validate:
        # Ejecutar el método
        result = service.create(obj_in=season_data, db=mock_db)
    
    # Verificar resultados
    assert isinstance(result, SeasonRead)
    assert result.id == 5
    assert result.location_id == season_data.location_id
    assert result.crop_id == season_data.crop_id
    assert result.planting_start == season_data.planting_start
    assert result.planting_end == season_data.planting_end
    
    # Verificar llamadas
    mock_validate.assert_called_once_with(mock_db, season_data)
    mock_db.add.assert_called_once()
    mock_db.refresh.assert_called_once()

def test_update_season(service, mock_db):
    """Test para actualizar una temporada"""
    # Configurar datos de prueba
    season_id = 6
    existing_season = Season(
        id=season_id,
        location_id=300,
        crop_id=500,
        planting_start=date(2023, 5, 1),
        planting_end=date(2023, 5, 31),
        season_start=date(2023, 5, 1),
        season_end=date(2023, 8, 31)
    )
    update_data = SeasonUpdate(
        planting_end=date(2023, 6, 15),
        season_start=date(2023, 6, 1),
        season_end=date(2023, 9, 30)
    )
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_season
    
    # Ejecutar el método
    result = service.update(season_id, update_data, db=mock_db)
    
    # Verificar resultados
    assert isinstance(result, SeasonRead)
    assert result.id == season_id
    assert result.planting_end == update_data.planting_end
    assert result.season_start == update_data.season_start
    # Campos no actualizados deben permanecer igual
    assert result.location_id == existing_season.location_id
    assert result.crop_id == existing_season.crop_id
    assert result.planting_start == existing_season.planting_start
    
    # Verificar llamadas
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

def test_delete_season(service, mock_db):
    """Test para eliminar una temporada"""
    # Configurar datos de prueba
    season_id = 7
    existing_season = Season(
        id=season_id,
        location_id=400,
        crop_id=600,
        planting_start=date(2023, 7, 1),
        planting_end=date(2023, 7, 31),
        season_start=date(2023, 7, 1),
        season_end=date(2023, 10, 31)
    )
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_season
    
    # Ejecutar el método
    result = service.delete(season_id, db=mock_db)
    
    # Verificar resultados
    assert result is True
    # Como no hay campo enable, debería eliminarse físicamente
    mock_db.delete.assert_called_once_with(existing_season)
    mock_db.commit.assert_called_once()

def test_get_by_location_empty(service, mock_db):
    """Test para cuando no hay temporadas para un location_id"""
    # Configurar el mock para devolver lista vacía
    mock_db.query.return_value.filter.return_value.all.return_value = []
    
    # Ejecutar el método
    result = service.get_by_location(999, db=mock_db)
    
    # Verificar resultados
    assert isinstance(result, list)
    assert len(result) == 0

def test_get_by_crop_empty(service, mock_db):
    """Test para cuando no hay temporadas para un crop_id"""
    # Configurar el mock para devolver lista vacía
    mock_db.query.return_value.filter.return_value.all.return_value = []
    
    # Ejecutar el método
    result = service.get_by_crop(999, db=mock_db)
    
    # Verificar resultados
    assert isinstance(result, list)
    assert len(result) == 0

def test_create_season_validation_failure(service, mock_db):
    """Test para validar fallos en la creación de temporada"""
    # Configurar datos de prueba
    season_data = SeasonCreate(
        location_id=500,
        crop_id=700,
        planting_start=date(2024, 2, 1),
        planting_end=date(2024, 1, 31),  # Fecha final anterior a la inicial
        season_start=date(2024, 2, 1),
        season_end=date(2024, 4, 30)
    )
    
    # Mockear la validación para que lance excepción
    with patch.object(SeasonValidator, 'create_validate', 
                     side_effect=ValueError("Planting end date must be after start date")):
        with pytest.raises(ValueError) as excinfo:
            service.create(season_data, db=mock_db)
        
        assert "Planting end date must be after start date" in str(excinfo.value)
    
    # Verificar que no se llamó a commit
    mock_db.commit.assert_not_called()

def test_partial_update_season(service, mock_db):
    """Test para actualización parcial de una temporada"""
    # Configurar datos de prueba
    season_id = 8
    existing_season = Season(
        id=season_id,
        location_id=600,
        crop_id=800,
        planting_start=date(2023, 8, 1),
        planting_end=date(2023, 8, 31),
        season_start=date(2023, 8, 1),
        season_end=date(2023, 10, 31)
    )
    update_data = SeasonUpdate(
        crop_id=801  # Solo actualizar crop_id
    )
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_season
    
    # Ejecutar el método
    result = service.update(season_id, update_data, db=mock_db)
    
    # Verificar resultados
    assert result.location_id == existing_season.location_id  # No cambió
    assert result.planting_start == existing_season.planting_start  # No cambió
    assert result.planting_end == existing_season.planting_end  # No cambió
    assert result.crop_id == update_data.crop_id  # Actualizado

def test_update_season_dates(service, mock_db):
    """Test para actualizar solo las fechas de una temporada"""
    # Configurar datos de prueba
    season_id = 9
    existing_season = Season(
        id=season_id,
        location_id=700,
        crop_id=900,
        planting_start=date(2023, 9, 1),
        planting_end=date(2023, 9, 30),
        season_start=date(2023, 9, 1),
        season_end=date(2024, 2, 28)
    )
    update_data = SeasonUpdate(
        season_start=date(2023, 10, 1),
        season_end=date(2024, 3, 31)
    )
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_season
    
    # Ejecutar el método
    result = service.update(season_id, update_data, db=mock_db)
    
    # Verificar resultados
    assert result.season_start == update_data.season_start
    assert result.season_end == update_data.season_end
    # Campos no actualizados deben permanecer igual
    assert result.location_id == existing_season.location_id
    assert result.crop_id == existing_season.crop_id
    assert result.planting_start == existing_season.planting_start
    assert result.planting_end == existing_season.planting_end
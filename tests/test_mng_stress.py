import pytest
from unittest.mock import create_autospec, patch
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List

# Importaciones de tu proyecto
from aclimate_v3_orm.models import MngStress
from aclimate_v3_orm.schemas import StressCreate, StressRead, StressUpdate
from aclimate_v3_orm.services import MngStressService
from aclimate_v3_orm.validations import MngStressValidator
from aclimate_v3_orm.enums import StressCategory

@pytest.fixture
def mock_db():
    """Fixture para una sesión de base de datos mockeada"""
    return create_autospec(Session, instance=True)

@pytest.fixture
def stress_service():
    """Fixture para el servicio de estrés"""
    return MngStressService()

def test_get_by_category(stress_service, mock_db):
    """Test para obtener estreses por categoría"""
    # Configurar datos de prueba
    
    mock_stresses = [
        MngStress(id=1, name="Stress1", short_name="S1", category=StressCategory.CROP),
        MngStress(id=2, name="Stress2", short_name="S2", category=StressCategory.CROP)
    ]
    # Configurar el mock
    mock_db.query.return_value.filter.return_value.all.return_value = mock_stresses
    
    # Ejecutar el método
    result = stress_service.get_by_category(StressCategory.CROP, db=mock_db)

    # Verificar resultados
    assert len(result) == 2
    assert all(isinstance(item, StressRead) for item in result)
    assert all(item.category == StressCategory.CROP for item in result)
    
    # Verificar llamadas a la base de datos
    mock_db.query.assert_called_once_with(MngStress)
    mock_db.query.return_value.filter.assert_called_once()

def test_create_stress_valid(stress_service, mock_db):
    """Test para crear un estrés válido"""
    # Configurar datos de prueba
    stress_data = StressCreate(name="New Stress", short_name="NS", category=StressCategory.WEATHER)
    mock_new_stress = MngStress(
        id=1, 
        name=stress_data.name, 
        category=stress_data.category,
        short_name=stress_data.short_name,
        description=stress_data.description,
        enable=True
    )
    
    # Configurar el mock para que refresh() actualice el objeto
    def mock_refresh(obj):
        if obj.id is None:
            obj.id = 1
    
    # Configurar los mocks
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.side_effect = mock_refresh
    
    # Mockear la validación
    with patch.object(MngStressValidator, 'create_validate') as mock_validate:
        # Ejecutar el método
        result = stress_service.create(obj_in=stress_data, db=mock_db)
    
    # Verificar resultados
    assert isinstance(result, StressRead)
    assert result.id == 1
    assert result.name == stress_data.name
    assert result.category == stress_data.category
    
    # Verificar llamadas
    mock_validate.assert_called_once_with(mock_db, stress_data)
    

def test_update_stress(stress_service, mock_db):
    """Test para actualizar un estrés"""
    # Configurar datos de prueba
    stress_id = 1
    update_data = StressUpdate(name="Updated Stress")
    existing_stress = MngStress(
        id=stress_id,
        name="Old Stress",
        category=StressCategory.CROP,
        short_name="OS",
        enable=True,
    )
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_stress
    
    # Ejecutar el método
    result = stress_service.update(stress_id, update_data, db=mock_db)
    
    # Verificar resultados
    assert isinstance(result, StressRead)
    assert result.id == stress_id
    assert result.name == update_data.name
    assert result.category == existing_stress.category  # No se actualizó
    
    # Verificar llamadas
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

def test_delete_stress(stress_service, mock_db):
    """Test para eliminar (deshabilitar) un estrés"""
    # Configurar datos de prueba
    stress_id = 1
    existing_stress = MngStress(
        id=stress_id,
        name="Stress to Delete",
        category="CategoryD",
        enable=True
    )
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_stress
    
    # Ejecutar el método
    result = stress_service.delete(stress_id, db=mock_db)
    
    # Verificar resultados
    assert result is True
    assert existing_stress.enable is False
    mock_db.commit.assert_called_once()

def test_get_by_category_empty(stress_service, mock_db):
    """Test para cuando no hay estreses en la categoría buscada"""
    # Configurar el mock para devolver lista vacía
    mock_db.query.return_value.filter.return_value.all.return_value = []
    
    # Ejecutar el método
    result = stress_service.get_by_category("Non-existent Category", db=mock_db)
    
    # Verificar resultados
    assert isinstance(result, list)
    assert len(result) == 0

def test_create_stress_validation_failure(stress_service, mock_db):
    """Test para validar fallos en la creación de estrés"""
    # Usar un valor válido para el Enum
    stress_data = StressCreate(name="", short_name="IS", category=StressCategory.CROP)
    # Mockear la validación para que lance excepción
    with patch.object(MngStressValidator, 'create_validate', 
                     side_effect=ValueError("Validation error")):
        with pytest.raises(ValueError) as excinfo:
            stress_service.create(stress_data, db=mock_db)
        assert "Validation error" in str(excinfo.value)
    mock_db.commit.assert_not_called()

def test_partial_update(stress_service, mock_db):
    """Test para actualización parcial de un estrés"""
    # Configurar datos de prueba
    stress_id = 1
    existing_stress = MngStress(
        id=stress_id,
        name="Existing Stress",
        short_name="ES",
        category=StressCategory.CROP,
        enable=True
    )
    update_data = StressUpdate(category=StressCategory.WEATHER)  # Solo actualizar categoría

    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_stress
    
    # Ejecutar el método
    result = stress_service.update(stress_id, update_data, db=mock_db)
    
    # Verificar resultados
    assert result.name == existing_stress.name
    assert result.category == update_data.category
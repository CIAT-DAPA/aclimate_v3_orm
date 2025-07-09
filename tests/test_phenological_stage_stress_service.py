# test_phenological_stage_stress_service.py
import pytest
from unittest.mock import create_autospec, patch
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List

# Importaciones de tu proyecto
from aclimate_v3_orm.models import PhenologicalStageStress
from aclimate_v3_orm.schemas import (
    PhenologicalStageStressCreate,
    PhenologicalStageStressRead,
    PhenologicalStageStressUpdate
)
from aclimate_v3_orm.services import PhenologicalStageStressService
from aclimate_v3_orm.validations import PhenologicalStageStressValidator

@pytest.fixture
def mock_db():
    """Fixture para una sesión de base de datos mockeada"""
    return create_autospec(Session, instance=True)

@pytest.fixture
def service():
    """Fixture para el servicio"""
    return PhenologicalStageStressService()

def test_get_by_stress(service, mock_db):
    """Test para obtener relaciones por stress_id"""
    # Configurar datos de prueba
    mock_relations = [
        PhenologicalStageStress(id=1, stress_id=10, phenological_stage_id=100, max=1.0, min=0.0),
        PhenologicalStageStress(id=2, stress_id=10, phenological_stage_id=101, max=1.0, min=0.0)
    ]
    
    # Configurar el mock
    mock_db.query.return_value.filter.return_value.all.return_value = mock_relations
    
    # Ejecutar el método
    result = service.get_by_stress(10, db=mock_db)
    
    # Verificar resultados
    assert len(result) == 2
    assert all(isinstance(item, PhenologicalStageStressRead) for item in result)
    assert all(item.stress_id == 10 for item in result)
    
    # Verificar llamadas a la base de datos
    mock_db.query.assert_called_once_with(PhenologicalStageStress)
    mock_db.query.return_value.filter.assert_called_once()

def test_get_by_phenological_stage(service, mock_db):
    """Test para obtener relaciones por phenological_stage_id"""
    # Configurar datos de prueba
    mock_relations = [
        PhenologicalStageStress(id=3, stress_id=20, phenological_stage_id=200, max=1.0, min=0.0),
        PhenologicalStageStress(id=4, stress_id=21, phenological_stage_id=200, max=1.0, min=0.0)
    ]
    
    # Configurar el mock
    mock_db.query.return_value.filter.return_value.all.return_value = mock_relations
    
    # Ejecutar el método
    result = service.get_by_phenological_stage(200, db=mock_db)
    
    # Verificar resultados
    assert len(result) == 2
    assert all(isinstance(item, PhenologicalStageStressRead) for item in result)
    assert all(item.phenological_stage_id == 200 for item in result)
    
    # Verificar llamadas a la base de datos
    mock_db.query.assert_called_once_with(PhenologicalStageStress)
    mock_db.query.return_value.filter.assert_called_once()

def test_create_relation_valid(service, mock_db):
    """Test para crear una relación válida"""
    # Configurar datos de prueba
    relation_data = PhenologicalStageStressCreate(
        id=1,
        stress_id=30, 
        phenological_stage_id=300,
        max=1.0,
        min=0.0
    )
    mock_new_relation = PhenologicalStageStress(
        id=5, 
        stress_id=relation_data.stress_id, 
        phenological_stage_id=relation_data.phenological_stage_id,
        max=relation_data.max,
        min=relation_data.min
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
    with patch.object(PhenologicalStageStressValidator, 'create_validate') as mock_validate:
        # Ejecutar el método
        result = service.create(obj_in=relation_data, db=mock_db)
    
    # Verificar resultados
    assert isinstance(result, PhenologicalStageStressRead)
    assert result.id == 5
    assert result.stress_id == relation_data.stress_id
    assert result.phenological_stage_id == relation_data.phenological_stage_id
    
    # Verificar llamadas
    mock_validate.assert_called_once_with(mock_db, relation_data)
    mock_db.add.assert_called_once()
    mock_db.refresh.assert_called_once()

def test_update_relation(service, mock_db):
    """Test para actualizar una relación"""
    # Configurar datos de prueba
    relation_id = 6
    existing_relation = PhenologicalStageStress(
        id=relation_id,
        stress_id=40,
        phenological_stage_id=400,
        max=1.0,
        min=0.0
    )
    update_data = PhenologicalStageStressUpdate(
        stress_id=41,
        phenological_stage_id=401
    )
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_relation
    
    # Ejecutar el método
    result = service.update(relation_id, update_data, db=mock_db)
    
    # Verificar resultados
    assert isinstance(result, PhenologicalStageStressRead)
    assert result.id == relation_id
    assert result.stress_id == update_data.stress_id
    assert result.phenological_stage_id == update_data.phenological_stage_id
    
    # Verificar llamadas
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

def test_delete_relation(service, mock_db):
    """Test para eliminar (deshabilitar) una relación"""
    # Configurar datos de prueba
    relation_id = 7
    existing_relation = PhenologicalStageStress(
        id=relation_id,
        stress_id=50,
        phenological_stage_id=500,
        max=1.0,
        min=0.0
    )
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_relation
    
    # Ejecutar el método
    result = service.delete(relation_id, db=mock_db)
    
    # Verificar resultados
    assert result is True
    assert existing_relation.enable is False
    mock_db.commit.assert_called_once()

def test_get_by_stress_empty(service, mock_db):
    """Test para cuando no hay relaciones para un stress_id"""
    # Configurar el mock para devolver lista vacía
    mock_db.query.return_value.filter.return_value.all.return_value = []
    
    # Ejecutar el método
    result = service.get_by_stress(999, db=mock_db)
    
    # Verificar resultados
    assert isinstance(result, list)
    assert len(result) == 0

def test_get_by_phenological_stage_empty(service, mock_db):
    """Test para cuando no hay relaciones para un phenological_stage_id"""
    # Configurar el mock para devolver lista vacía
    mock_db.query.return_value.filter.return_value.all.return_value = []
    
    # Ejecutar el método
    result = service.get_by_phenological_stage(999, db=mock_db)
    
    # Verificar resultados
    assert isinstance(result, list)
    assert len(result) == 0

def test_create_relation_validation_failure(service, mock_db):
    """Test para validar fallos en la creación de relación"""
    # Configurar datos de prueba
    relation_data = PhenologicalStageStressCreate(
        stress_id=60, 
        phenological_stage_id=600,
        max=1.0,
        min=0.0
    )
    
    # Mockear la validación para que lance excepción
    with patch.object(PhenologicalStageStressValidator, 'create_validate', 
                     side_effect=ValueError("Validation error")):
        with pytest.raises(ValueError) as excinfo:
            service.create(relation_data, db=mock_db)
        
        assert "Validation error" in str(excinfo.value)
    
    # Verificar que no se llamó a commit
    mock_db.commit.assert_not_called()

def test_partial_update(service, mock_db):
    """Test para actualización parcial de una relación"""
    # Configurar datos de prueba
    relation_id = 8
    existing_relation = PhenologicalStageStress(
        id=relation_id,
        stress_id=70,
        phenological_stage_id=700,
        max=1.0,
        min=0.0
    )
    update_data = PhenologicalStageStressUpdate(
        phenological_stage_id=701  # Solo actualizar phenological_stage_id
    )
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_relation
    
    # Ejecutar el método
    result = service.update(relation_id, update_data, db=mock_db)
    
    # Verificar resultados
    assert result.stress_id == existing_relation.stress_id  # No cambió
    assert result.phenological_stage_id == update_data.phenological_stage_id  # Actualizado
# test_mng_phenological_stage_service.py
import pytest
from unittest.mock import create_autospec, patch, MagicMock
from sqlalchemy.orm import Session

# Importaciones de tu proyecto
from aclimate_v3_orm.models import MngPhenologicalStage
from aclimate_v3_orm.schemas import PhenologicalStageCreate, PhenologicalStageRead, PhenologicalStageUpdate
from aclimate_v3_orm.services import MngPhenologicalStageService
from aclimate_v3_orm.validations import MngPhenologicalStageValidator

@pytest.fixture
def mock_db():
    """Fixture para una sesión de base de datos mockeada"""
    return create_autospec(Session, instance=True)

@pytest.fixture
def stage_service():
    """Fixture para el servicio de etapas fenológicas"""
    return MngPhenologicalStageService()

def test_get_by_crop(stage_service, mock_db):
    """Test para obtener etapas fenológicas por crop_id"""
    # Configurar datos de prueba
    mock_stages = [
        MngPhenologicalStage(id=1, crop_id=100, name="Germination", order_stage=1),
        MngPhenologicalStage(id=2, crop_id=100, name="Flowering", order_stage=2)
    ]
    
    # Configurar el mock
    mock_db.query.return_value.filter.return_value.all.return_value = mock_stages
    
    # Ejecutar el método
    result = stage_service.get_by_crop(100, db=mock_db)
    
    # Verificar resultados
    assert len(result) == 2
    assert all(isinstance(item, PhenologicalStageRead) for item in result)
    assert all(item.crop_id == 100 for item in result)
    
    # Verificar llamadas a la base de datos
    mock_db.query.assert_called_once_with(MngPhenologicalStage)
    mock_db.query.return_value.filter.assert_called_once()

def test_get_by_crop_empty(stage_service, mock_db):
    """Test para cuando no hay etapas para un crop_id"""
    # Configurar el mock para devolver lista vacía
    mock_db.query.return_value.filter.return_value.all.return_value = []
    
    # Ejecutar el método
    result = stage_service.get_by_crop(999, db=mock_db)
    
    # Verificar resultados
    assert isinstance(result, list)
    assert len(result) == 0

def test_create_stage_valid(stage_service, mock_db):
    """Test para crear una etapa fenológica válida"""
    # Configurar datos de prueba
    stage_data = PhenologicalStageCreate(
        crop_id=200,
        name="New Stage",
        order_stage=3,
        duration_avg_day=15
    )
    mock_new_stage = MngPhenologicalStage(
        id=3, 
        crop_id=stage_data.crop_id,
        name=stage_data.name,
        order_stage=stage_data.order_stage,
        duration_avg_day=stage_data.duration_avg_day
    )
    
    # Configurar el mock para refresh
    def mock_refresh(obj):
        if obj.id is None:
            obj.id = 3
    
    # Configurar los mocks
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.side_effect = mock_refresh
    
    # Mockear la validación
    with patch.object(MngPhenologicalStageValidator, 'create_validate') as mock_validate:
        # Ejecutar el método
        result = stage_service.create(obj_in=stage_data, db=mock_db)
    
    # Verificar resultados
    assert isinstance(result, PhenologicalStageRead)
    assert result.id == 3
    assert result.crop_id == stage_data.crop_id
    assert result.name == stage_data.name
    assert result.order_stage == stage_data.order_stage
    assert result.duration_avg_day == stage_data.duration_avg_day
    
    # Verificar llamadas
    mock_validate.assert_called_once_with(mock_db, stage_data)
    mock_db.add.assert_called_once()
    mock_db.refresh.assert_called_once()

def test_update_stage(stage_service, mock_db):
    """Test para actualizar una etapa fenológica"""
    # Configurar datos de prueba
    stage_id = 4
    existing_stage = MngPhenologicalStage(
        id=stage_id,
        crop_id=300,
        name="Old Stage",
        order_stage=1,
        duration_avg_day=10
    )
    update_data = PhenologicalStageUpdate(
        name="Updated Stage",
        description="New description",
        duration_avg_day=20
    )
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_stage
    
    # Ejecutar el método
    result = stage_service.update(stage_id, update_data, db=mock_db)
    
    # Verificar resultados
    assert isinstance(result, PhenologicalStageRead)
    assert result.id == stage_id
    assert result.name == update_data.name
    assert result.description == update_data.description
    assert result.duration_avg_day == update_data.duration_avg_day
    # Campos no actualizados deben permanecer igual
    assert result.crop_id == existing_stage.crop_id
    assert result.order_stage == existing_stage.order_stage
    
    # Verificar llamadas
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

def test_delete_stage(stage_service, mock_db):
    """Test para eliminar una etapa fenológica (borrado físico)"""
    # Configurar datos de prueba
    stage_id = 5
    existing_stage = MngPhenologicalStage(
        id=stage_id,
        crop_id=400,
        name="Stage to delete",
        order_stage=1
    )
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_stage
    
    # Ejecutar el método
    result = stage_service.delete(stage_id, db=mock_db)
    
    # Verificar resultados
    assert result is True
    # Como no hay campo enable, debería eliminarse físicamente
    mock_db.delete.assert_called_once_with(existing_stage)
    mock_db.commit.assert_called_once()

def test_create_stage_validation_failure(stage_service, mock_db):
    """Test para validar fallos en la creación de etapa"""
    # Configurar datos de prueba
    stage_data = PhenologicalStageCreate(
        crop_id=500,
        name="Invalid Stage",
        order_stage=1
    )
    
    # Mockear la validación para que lance excepción
    with patch.object(MngPhenologicalStageValidator, 'create_validate', 
                     side_effect=ValueError("Order stage already exists for this crop")):
        with pytest.raises(ValueError) as excinfo:
            stage_service.create(stage_data, db=mock_db)
        
        assert "Order stage already exists for this crop" in str(excinfo.value)
    
    # Verificar que no se llamó a commit
    mock_db.commit.assert_not_called()

def test_partial_update_stage(stage_service, mock_db):
    """Test para actualización parcial de una etapa"""
    # Configurar datos de prueba
    stage_id = 6
    existing_stage = MngPhenologicalStage(
        id=stage_id,
        crop_id=600,
        name="Existing Stage",
        order_stage=1,
        duration_avg_day=15
    )
    update_data = PhenologicalStageUpdate(
        duration_avg_day=20  # Solo actualizar duration_avg_day
    )
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_stage
    
    # Ejecutar el método
    result = stage_service.update(stage_id, update_data, db=mock_db)
    
    # Verificar resultados
    assert result.name == existing_stage.name  # No cambió
    assert result.order_stage == existing_stage.order_stage  # No cambió
    assert result.duration_avg_day == update_data.duration_avg_day  # Actualizado

def test_update_stage_order(stage_service, mock_db):
    """Test para actualizar el order_stage de una etapa"""
    # Configurar datos de prueba
    stage_id = 7
    existing_stage = MngPhenologicalStage(
        id=stage_id,
        crop_id=700,
        name="Stage",
        order_stage=2
    )
    update_data = PhenologicalStageUpdate(
        order_stage=1  # Cambiar el orden
    )
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_stage
    
    # Ejecutar el método
    result = stage_service.update(stage_id, update_data, db=mock_db)
    
    # Verificar resultados
    assert result.order_stage == update_data.order_stage

def test_create_stage_with_optional_fields(stage_service, mock_db):
    """Test para crear etapa con campos opcionales"""
    # Configurar datos de prueba
    stage_data = PhenologicalStageCreate(
        crop_id=800,
        name="Complete Stage",
        order_stage=4,
        short_name="CStage",
        description="Detailed description",
        duration_avg_day=30,
        start_model="ModelA",
        end_model="ModelB"
    )
    mock_new_stage = MngPhenologicalStage(
        id=8, 
        **stage_data.model_dump()
    )
    
    # Configurar el mock para refresh
    def mock_refresh(obj):
        obj.id = 8
    
    # Configurar los mocks
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.side_effect = mock_refresh
    
    # Mockear la validación
    with patch.object(MngPhenologicalStageValidator, 'create_validate'):
        # Ejecutar el método
        result = stage_service.create(obj_in=stage_data, db=mock_db)
    
    # Verificar resultados
    assert result.id == 8
    assert result.short_name == stage_data.short_name
    assert result.description == stage_data.description
    assert result.start_model == stage_data.start_model
    assert result.end_model == stage_data.end_model

def test_get_by_crop_with_relations(stage_service, mock_db):
    """Test para obtener etapas con relaciones cargadas (aunque no se serializan)"""
    # Configurar datos de prueba
    mock_stage = MngPhenologicalStage(
        id=9, 
        crop_id=900, 
        name="Stage with Relations",
        order_stage=1
    )
    # Agregar relaciones ficticias
    mock_stage.historical_agroclimatic_indicators = [MagicMock()]
    mock_stage.phenological_stage_stresses = [MagicMock()]
    
    # Configurar el mock
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_stage]
    
    # Ejecutar el método
    result = stage_service.get_by_crop(900, db=mock_db)
    
    # Verificar resultados
    assert len(result) == 1
    assert result[0].id == 9
    # Las relaciones no deberían estar en el resultado serializado
    assert not hasattr(result[0], 'historical_agroclimatic_indicators')
    assert not hasattr(result[0], 'phenological_stage_stresses')
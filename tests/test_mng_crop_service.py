# test_mng_crop_service.py
import pytest
from unittest.mock import create_autospec, patch
from sqlalchemy.orm import Session
from datetime import datetime, timezone

# Importaciones de tu proyecto
from aclimate_v3_orm.models import MngCrop
from aclimate_v3_orm.schemas import CropCreate, CropRead, CropUpdate
from aclimate_v3_orm.services import MngCropService
from aclimate_v3_orm.validations import MngCropValidator

@pytest.fixture
def mock_db():
    """Fixture para una sesión de base de datos mockeada"""
    return create_autospec(Session, instance=True)

@pytest.fixture
def crop_service():
    """Fixture para el servicio de cultivos"""
    return MngCropService()

def test_get_by_name_found(crop_service, mock_db):
    """Test para obtener un cultivo por nombre (encontrado)"""
    # Configurar datos de prueba
    mock_crop = MngCrop(id=1, name="Maize", enable=True)
    
    # Configurar el mock
    mock_db.query.return_value.filter.return_value.first.return_value = mock_crop
    
    # Ejecutar el método
    result = crop_service.get_by_name("Maize", db=mock_db)
    
    # Verificar resultados
    assert isinstance(result, CropRead)
    assert result.id == 1
    assert result.name == "Maize"
    assert result.enable is True
    
    # Verificar llamadas a la base de datos
    mock_db.query.assert_called_once_with(MngCrop)
    mock_db.query.return_value.filter.assert_called_once()

def test_get_by_name_not_found(crop_service, mock_db):
    """Test para obtener un cultivo por nombre (no encontrado)"""
    # Configurar el mock para devolver None
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    # Ejecutar el método
    result = crop_service.get_by_name("Non-existent Crop", db=mock_db)
    
    # Verificar resultados
    assert result is None

def test_get_all_enable_true(crop_service, mock_db):
    """Test para obtener todos los cultivos habilitados"""
    # Configurar datos de prueba
    mock_crops = [
        MngCrop(id=1, name="Maize", enable=True),
        MngCrop(id=2, name="Rice", enable=True)
    ]
    
    # Configurar el mock
    mock_db.query.return_value.filter.return_value.all.return_value = mock_crops
    
    # Ejecutar el método
    result = crop_service.get_all_enable(enabled=True, db=mock_db)
    
    # Verificar resultados
    assert len(result) == 2
    assert all(isinstance(item, CropRead) for item in result)
    assert all(item.enable is True for item in result)
    
    # Verificar llamadas a la base de datos
    mock_db.query.assert_called_once_with(MngCrop)
    mock_db.query.return_value.filter.assert_called_once()

def test_get_all_enable_false(crop_service, mock_db):
    """Test para obtener todos los cultivos deshabilitados"""
    # Configurar datos de prueba
    mock_crops = [
        MngCrop(id=3, name="Wheat", enable=False),
        MngCrop(id=4, name="Barley", enable=False)
    ]
    
    # Configurar el mock
    mock_db.query.return_value.filter.return_value.all.return_value = mock_crops
    
    # Ejecutar el método
    result = crop_service.get_all_enable(enabled=False, db=mock_db)
    
    # Verificar resultados
    assert len(result) == 2
    assert all(isinstance(item, CropRead) for item in result)
    assert all(item.enable is False for item in result)

def test_create_crop_valid(crop_service, mock_db):
    """Test para crear un cultivo válido"""
    # Configurar datos de prueba
    crop_data = CropCreate(name="New Crop")
    mock_new_crop = MngCrop(
        id=5, 
        name=crop_data.name,
        enable=True,
        register=datetime.now(timezone.utc),
        updated=datetime.now(timezone.utc)
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
    with patch.object(MngCropValidator, 'create_validate') as mock_validate:
        # Ejecutar el método
        result = crop_service.create(obj_in=crop_data, db=mock_db)
    
    # Verificar resultados
    assert isinstance(result, CropRead)
    assert result.id == 5
    assert result.name == crop_data.name
    assert result.enable is True
    
    # Verificar llamadas
    mock_validate.assert_called_once_with(mock_db, crop_data)
    mock_db.add.assert_called_once()
    mock_db.refresh.assert_called_once()

def test_update_crop(crop_service, mock_db):
    """Test para actualizar un cultivo"""
    # Configurar datos de prueba
    crop_id = 6
    existing_crop = MngCrop(
        id=crop_id,
        name="Old Crop",
        enable=True
    )
    update_data = CropUpdate(name="Updated Crop", enable=False)
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_crop
    
    # Ejecutar el método
    result = crop_service.update(crop_id, update_data, db=mock_db)
    
    # Verificar resultados
    assert isinstance(result, CropRead)
    assert result.id == crop_id
    assert result.name == update_data.name
    assert result.enable == update_data.enable
    
    # Verificar llamadas
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

def test_delete_crop(crop_service, mock_db):
    """Test para eliminar (deshabilitar) un cultivo"""
    # Configurar datos de prueba
    crop_id = 7
    existing_crop = MngCrop(
        id=crop_id,
        name="Crop to Delete",
        enable=True
    )
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_crop
    
    # Ejecutar el método
    result = crop_service.delete(crop_id, db=mock_db)
    
    # Verificar resultados
    assert result is True
    assert existing_crop.enable is False
    mock_db.commit.assert_called_once()

def test_create_crop_validation_failure(crop_service, mock_db):
    """Test para validar fallos en la creación de cultivo"""
    # Configurar datos de prueba
    crop_data = CropCreate(name="Invalid Crop")
    
    # Mockear la validación para que lance excepción
    with patch.object(MngCropValidator, 'create_validate', 
                     side_effect=ValueError("Name already exists")):
        with pytest.raises(ValueError) as excinfo:
            crop_service.create(crop_data, db=mock_db)
        
        assert "Name already exists" in str(excinfo.value)
    
    # Verificar que no se llamó a commit
    mock_db.commit.assert_not_called()

def test_partial_update_crop(crop_service, mock_db):
    """Test para actualización parcial de un cultivo"""
    # Configurar datos de prueba
    crop_id = 8
    existing_crop = MngCrop(
        id=crop_id,
        name="Existing Crop",
        enable=True
    )
    update_data = CropUpdate(enable=False)  # Solo actualizar estado
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_crop
    
    # Ejecutar el método
    result = crop_service.update(crop_id, update_data, db=mock_db)
    
    # Verificar resultados
    assert result.name == existing_crop.name  # No cambió
    assert result.enable == update_data.enable  # Actualizado

def test_get_all_enable_default(crop_service, mock_db):
    """Test para obtener cultivos habilitados por defecto"""
    # Configurar datos de prueba
    mock_crops = [
        MngCrop(id=9, name="Soybean", enable=True),
        MngCrop(id=10, name="Potato", enable=True)
    ]
    
    # Configurar el mock
    mock_db.query.return_value.filter.return_value.all.return_value = mock_crops
    
    # Ejecutar el método sin especificar 'enabled'
    result = crop_service.get_all_enable(db=mock_db)
    
    # Verificar resultados (debería devolver solo habilitados por defecto)
    assert len(result) == 2
    assert all(item.enable is True for item in result)
    
    # Verificar que el filtro se aplicó con enabled=True
    filter_call = mock_db.query.return_value.filter
    assert "enable" in str(filter_call.call_args[0][0])

def test_create_crop_with_default_enable(crop_service, mock_db):
    """Test que verifica que los nuevos cultivos se crean habilitados por defecto"""
    # Configurar datos de prueba
    crop_data = CropCreate(name="New Default Crop")
    
    # Configurar el mock para refresh
    def mock_refresh(obj):
        obj.id = 11
    
    # Configurar los mocks
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.side_effect = mock_refresh
    
    # Mockear la validación
    with patch.object(MngCropValidator, 'create_validate'):
        # Ejecutar el método
        result = crop_service.create(obj_in=crop_data, db=mock_db)
    
    # Verificar que el cultivo se creó habilitado
    assert result.enable is True
# test_mng_configuration_file_service.py
import pytest
from unittest.mock import create_autospec, patch, MagicMock
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from pydantic import ValidationError

# Importaciones de tu proyecto
from aclimate_v3_orm.models import MngConfigurationFile
from aclimate_v3_orm.schemas import (
    ConfigurationFileCreate,
    ConfigurationFileRead,
    ConfigurationFileUpdate
)
from aclimate_v3_orm.services import MngConfigurationFileService
from aclimate_v3_orm.validations import MngConfigurationFileValidator
from aclimate_v3_orm.services.base_service import BaseService

@pytest.fixture
def mock_db():
    """Fixture para una sesión de base de datos mockeada"""
    return create_autospec(Session, instance=True)

@pytest.fixture
def config_file_service():
    """Fixture para el servicio de archivos de configuración"""
    return MngConfigurationFileService()

def test_get_by_setup(config_file_service, mock_db):
    """Test para obtener archivos de configuración por setup_id"""
    # Configurar datos de prueba
    mock_files = [
        MngConfigurationFile(id=1, setup_id=100, name="File1", path="/path/to/file1", enable=True),
        MngConfigurationFile(id=2, setup_id=100, name="File2", path="/path/to/file2", enable=True)
    ]
    
    # Configurar el mock
    mock_db.query.return_value.filter.return_value.all.return_value = mock_files
    
    # Ejecutar el método
    result = config_file_service.get_by_setup(100, db=mock_db)
    
    # Verificar resultados
    assert len(result) == 2
    assert all(isinstance(item, ConfigurationFileRead) for item in result)
    assert all(item.setup_id == 100 for item in result)
    
    # Verificar llamadas a la base de datos
    mock_db.query.assert_called_once_with(MngConfigurationFile)
    mock_db.query.return_value.filter.assert_called_once()

def test_create_config_file_valid(config_file_service, mock_db):
    """Test para crear un archivo de configuración válido"""
    # Configurar datos de prueba
    file_data = ConfigurationFileCreate(
        setup_id=200,
        name="New Config",
        path="/new/path"
    )
    mock_new_file = MngConfigurationFile(
        id=3, 
        setup_id=file_data.setup_id,
        name=file_data.name,
        path=file_data.path,
        enable=True,
        register=datetime.now(timezone.utc),
        updated=datetime.now(timezone.utc)
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
    with patch.object(MngConfigurationFileValidator, 'create_validate') as mock_validate:
        # Ejecutar el método
        result = config_file_service.create(obj_in=file_data, db=mock_db)
    
    # Verificar resultados
    assert isinstance(result, ConfigurationFileRead)
    assert result.id == 3
    assert result.setup_id == file_data.setup_id
    assert result.name == file_data.name
    assert result.path == file_data.path
    
    # Verificar llamadas
    mock_validate.assert_called_once_with(mock_db, file_data)
    mock_db.add.assert_called_once()
    mock_db.refresh.assert_called_once()

def test_update_config_file(config_file_service, mock_db):
    """Test para actualizar un archivo de configuración"""
    # Configurar datos de prueba
    file_id = 4
    existing_file = MngConfigurationFile(
        id=file_id,
        setup_id=300,
        name="Old Config",
        path="/old/path",
        enable=True
    )
    update_data = ConfigurationFileUpdate(
        name="Updated Config",
        path="/updated/path"
    )
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_file
    
    # Ejecutar el método
    result = config_file_service.update(file_id, update_data, db=mock_db)
    
    # Verificar resultados
    assert isinstance(result, ConfigurationFileRead)
    assert result.id == file_id
    assert result.name == update_data.name
    assert result.path == update_data.path
    # Campos no actualizados deben permanecer igual
    assert result.setup_id == existing_file.setup_id
    assert result.enable == existing_file.enable
    
    # Verificar llamadas
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

def test_delete_config_file_soft_delete(config_file_service, mock_db):
    """Test para eliminar un archivo de configuración (soft delete)"""
    # Configurar datos de prueba
    file_id = 5
    existing_file = MngConfigurationFile(
        id=file_id,
        setup_id=400,
        name="Config to Delete",
        path="/delete/path",
        enable=True
    )
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_file
    
    # Ejecutar el método
    result = config_file_service.delete(file_id, db=mock_db)
    
    # Verificar resultados
    assert result is True
    # Debería ser un soft delete (deshabilitar)
    assert existing_file.enable is False
    mock_db.commit.assert_called_once()

def test_get_by_setup_empty(config_file_service, mock_db):
    """Test para cuando no hay archivos para un setup_id"""
    # Configurar el mock para devolver lista vacía
    mock_db.query.return_value.filter.return_value.all.return_value = []
    
    # Ejecutar el método
    result = config_file_service.get_by_setup(999, db=mock_db)
    
    # Verificar resultados
    assert isinstance(result, list)
    assert len(result) == 0

def test_create_config_file_validation_failure(config_file_service, mock_db):
    """Test para validar fallos en la creación de archivo"""
    # Configurar datos de prueba
    file_data = ConfigurationFileCreate(
        setup_id=500,
        name="Invalid Config",
        path="/invalid/path"
    )
    
    # Mockear la validación para que lance excepción
    with patch.object(MngConfigurationFileValidator, 'create_validate', 
                     side_effect=ValueError("Setup does not exist")):
        with pytest.raises(ValueError) as excinfo:
            config_file_service.create(file_data, db=mock_db)
        
        assert "Setup does not exist" in str(excinfo.value)
    
    # Verificar que no se llamó a commit
    mock_db.commit.assert_not_called()

def test_partial_update_config_file(config_file_service, mock_db):
    """Test para actualización parcial de un archivo"""
    # Configurar datos de prueba
    file_id = 6
    existing_file = MngConfigurationFile(
        id=file_id,
        setup_id=600,
        name="Partial Update",
        path="/partial/path",
        enable=True
    )
    update_data = ConfigurationFileUpdate(
        path="/updated/path"  # Solo actualizar path
    )
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_file
    
    # Ejecutar el método
    result = config_file_service.update(file_id, update_data, db=mock_db)
    
    # Verificar resultados
    assert result.name == existing_file.name  # No cambió
    assert result.setup_id == existing_file.setup_id  # No cambió
    assert result.path == update_data.path  # Actualizado

def test_create_config_file_with_defaults(config_file_service, mock_db):
    """Test que verifica que los nuevos archivos se crean con enable=True por defecto"""
    # Configurar datos de prueba
    file_data = ConfigurationFileCreate(
        setup_id=700,
        name="Default Config",
        path="/default/path",
        enable=True
    )
    
    # Configurar el mock para refresh
    def mock_refresh(obj):
        obj.id = 7
    
    # Configurar los mocks
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.side_effect = mock_refresh
    
    # Mockear la validación
    with patch.object(MngConfigurationFileValidator, 'create_validate'):
        # Ejecutar el método
        result = config_file_service.create(obj_in=file_data, db=mock_db)
    
    # Verificar que el archivo se creó habilitado
    assert result.enable is True

def test_update_config_file_enable_status(config_file_service, mock_db):
    """Test para actualizar el estado enable de un archivo"""
    # Configurar datos de prueba
    file_id = 8
    existing_file = MngConfigurationFile(
        id=file_id,
        setup_id=800,
        name="Enable Test",
        path="/enable/path",
        enable=True
    )
    update_data = ConfigurationFileUpdate(enable=False)
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_file
    
    # Ejecutar el método
    result = config_file_service.update(file_id, update_data, db=mock_db)
    
    # Verificar resultados
    assert result.enable is False

def test_get_by_setup_with_relations(config_file_service, mock_db):
    """Test para obtener archivos con relaciones cargadas (aunque no se serializan)"""
    # Configurar datos de prueba
    mock_file = MngConfigurationFile(
        id=9, 
        setup_id=900, 
        name="File with Relation",
        path="/relation/path",
        enable=True
    )
    # Agregar relación ficticia
    mock_file.setup = MagicMock()
    
    # Configurar el mock
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_file]
    
    # Ejecutar el método
    result = config_file_service.get_by_setup(900, db=mock_db)
    
    # Verificar resultados
    assert len(result) == 1
    assert result[0].id == 9
    # La relación no debería estar en el resultado serializado
    assert not hasattr(result[0], 'setup')

def test_delete_config_file_physical_delete(config_file_service, mock_db):
    """Test para verificar que se elimina físicamente si no tiene campo enable"""
    # Configurar datos de prueba (sin campo enable)
    class NoEnableConfigFile:
        id = 10
        setup_id = 1000
        name = "No Enable File"
        path = "/no/enable/path"
    
    # Sobrescribir el método delete del servicio base para este test
    with patch.object(BaseService, 'delete') as mock_base_delete:
        mock_base_delete.return_value = True
        result = config_file_service.delete(10, db=mock_db)
    
    # Verificar que se llama al método base de eliminación física
    mock_base_delete.assert_called_once()

def test_create_config_file_name_length_validation():
    """Test para validar longitud máxima del nombre"""
    # Configurar datos de prueba con nombre demasiado largo
    long_name = "A" * 256  # 256 caracteres (límite es 255)
    with pytest.raises(ValidationError) as excinfo:
        ConfigurationFileCreate(
            setup_id=1100,
            name=long_name,
            path="/long/name/path"
        )
    assert "at most 255 characters" in str(excinfo.value)

def test_update_config_file_setup_id(config_file_service, mock_db):
    """Test que verifica que se puede actualizar el setup_id"""
    # Configurar datos de prueba
    file_id = 11
    existing_file = MngConfigurationFile(
        id=file_id,
        setup_id=1200,
        name="Change Setup",
        path="/change/setup/path",
        enable=True
    )
    update_data = ConfigurationFileUpdate(setup_id=1300)
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_file
    
    # Ejecutar el método
    result = config_file_service.update(file_id, update_data, db=mock_db)
    
    # Verificar que el setup_id se actualizó
    assert result.setup_id == update_data.setup_id

def test_create_config_file_with_minimal_data(config_file_service, mock_db):
    """Test para crear archivo con solo los campos obligatorios"""
    # Configurar datos de prueba
    file_data = ConfigurationFileCreate(
        setup_id=1400,
        name="Minimal Config",
        path="/minimal/path"
    )
    
    # Configurar el mock para refresh
    def mock_refresh(obj):
        obj.id = 12
    
    # Configurar los mocks
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.side_effect = mock_refresh
    
    # Mockear la validación
    with patch.object(MngConfigurationFileValidator, 'create_validate'):
        # Ejecutar el método
        result = config_file_service.create(obj_in=file_data, db=mock_db)
    
    # Verificar resultados
    assert result.id == 12
    # Campos opcionales deben tener valores por defecto
    assert result.enable is True
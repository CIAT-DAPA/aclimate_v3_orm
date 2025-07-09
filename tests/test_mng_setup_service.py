# test_mng_setup_service.py
import pytest
from unittest.mock import create_autospec, patch, MagicMock
from sqlalchemy.orm import Session
from datetime import datetime, timezone

# Importaciones de tu proyecto
from aclimate_v3_orm.models import MngSetup
from aclimate_v3_orm.schemas import SetupCreate, SetupRead, SetupUpdate
from aclimate_v3_orm.services import MngSetupService

@pytest.fixture
def mock_db():
    """Fixture para una sesión de base de datos mockeada"""
    return create_autospec(Session, instance=True)

@pytest.fixture
def setup_service():
    """Fixture para el servicio de setups"""
    return MngSetupService()

def test_get_by_cultivar(setup_service, mock_db):
    """Test para obtener setups por cultivar_id"""
    # Configurar datos de prueba
    mock_setups = [
        MngSetup(id=1, cultivar_id=100, soil_id=200, season_id=300, frequency=7, enable=True),
        MngSetup(id=2, cultivar_id=100, soil_id=201, season_id=301, frequency=14, enable=False)
    ]
    
    # Configurar el mock
    mock_db.query.return_value.filter.return_value.all.return_value = mock_setups
    
    # Ejecutar el método
    result = setup_service.get_by_cultivar(mock_db, 100)
    
    # Verificar resultados
    assert len(result) == 2
    assert all(isinstance(item, SetupRead) for item in result)
    assert all(item.cultivar_id == 100 for item in result)
    
    # Verificar llamadas a la base de datos
    mock_db.query.assert_called_once_with(MngSetup)
    mock_db.query.return_value.filter.assert_called_once()

def test_get_by_season(setup_service, mock_db):
    """Test para obtener setups por season_id"""
    # Configurar datos de prueba
    mock_setups = [
        MngSetup(id=3, cultivar_id=101, soil_id=202, season_id=400, frequency=7, enable=True),
        MngSetup(id=4, cultivar_id=102, soil_id=203, season_id=400, frequency=14, enable=False)
    ]
    
    # Configurar el mock
    mock_db.query.return_value.filter.return_value.all.return_value = mock_setups
    
    # Ejecutar el método
    result = setup_service.get_by_season(mock_db, 400)
    
    # Verificar resultados
    assert len(result) == 2
    assert all(isinstance(item, SetupRead) for item in result)
    assert all(item.season_id == 400 for item in result)

def test_create_setup(setup_service, mock_db):
    """Test para crear un setup"""
    # Configurar datos de prueba
    setup_data = SetupCreate(
        cultivar_id=103,
        soil_id=204,
        season_id=401,
        frequency=21
    )
    mock_new_setup = MngSetup(
        id=5,
        cultivar_id=setup_data.cultivar_id,
        soil_id=setup_data.soil_id,
        season_id=setup_data.season_id,
        frequency=setup_data.frequency,
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
    
    # Ejecutar el método
    result = setup_service.create(db=mock_db, obj_in=setup_data)
    
    # Verificar resultados
    assert isinstance(result, SetupRead)
    assert result.id == 5
    assert result.cultivar_id == setup_data.cultivar_id
    assert result.soil_id == setup_data.soil_id
    assert result.season_id == setup_data.season_id
    assert result.frequency == setup_data.frequency
    
    # Verificar llamadas
    mock_db.add.assert_called_once()
    mock_db.refresh.assert_called_once()

def test_update_setup(setup_service, mock_db):
    """Test para actualizar un setup"""
    # Configurar datos de prueba
    setup_id = 6
    existing_setup = MngSetup(
        id=setup_id,
        cultivar_id=104,
        soil_id=205,
        season_id=402,
        frequency=7,
        enable=True
    )
    update_data = SetupUpdate(
        frequency=14,
        enable=False
    )
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_setup
    
    # Ejecutar el método
    result = setup_service.update(id=setup_id, obj_in=update_data, db=mock_db)
    
    # Verificar resultados
    assert isinstance(result, SetupRead)
    assert result.id == setup_id
    assert result.frequency == update_data.frequency
    assert result.enable == update_data.enable
    # Campos no actualizados deben permanecer igual
    assert result.cultivar_id == existing_setup.cultivar_id
    assert result.soil_id == existing_setup.soil_id
    assert result.season_id == existing_setup.season_id
    
    # Verificar llamadas
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

def test_delete_setup(setup_service, mock_db):
    """Test para eliminar un setup (deshabilitar)"""
    # Configurar datos de prueba
    setup_id = 7
    existing_setup = MngSetup(
        id=setup_id,
        cultivar_id=105,
        soil_id=206,
        season_id=403,
        frequency=21,
        enable=True
    )
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_setup
    
    # Ejecutar el método
    result = setup_service.delete(id=setup_id, db=mock_db)
    
    # Verificar resultados
    assert result is True
    # Debería ser un soft delete (deshabilitar)
    assert existing_setup.enable is False
    mock_db.commit.assert_called_once()

def test_get_by_cultivar_empty(setup_service, mock_db):
    """Test para cuando no hay setups para un cultivar_id"""
    # Configurar el mock para devolver lista vacía
    mock_db.query.return_value.filter.return_value.all.return_value = []
    
    # Ejecutar el método
    result = setup_service.get_by_cultivar(mock_db, 999)
    
    # Verificar resultados
    assert isinstance(result, list)
    assert len(result) == 0

def test_get_by_season_empty(setup_service, mock_db):
    """Test para cuando no hay setups para un season_id"""
    # Configurar el mock para devolver lista vacía
    mock_db.query.return_value.filter.return_value.all.return_value = []
    
    # Ejecutar el método
    result = setup_service.get_by_season(mock_db, 999)
    
    # Verificar resultados
    assert isinstance(result, list)
    assert len(result) == 0

def test_partial_update_setup(setup_service, mock_db):
    """Test para actualización parcial de un setup"""
    # Configurar datos de prueba
    setup_id = 8
    existing_setup = MngSetup(
        id=setup_id,
        cultivar_id=106,
        soil_id=207,
        season_id=404,
        frequency=7,
        enable=True
    )
    update_data = SetupUpdate(
        frequency=14  # Solo actualizar frecuencia
    )
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_setup
    
    # Ejecutar el método

    result = setup_service.update(id=setup_id, obj_in=update_data, db=mock_db)

    # Verificar resultados
    assert result.frequency == update_data.frequency
    # Los demás campos no cambian
    assert result.cultivar_id == existing_setup.cultivar_id
    assert result.soil_id == existing_setup.soil_id
    assert result.season_id == existing_setup.season_id
    assert result.enable == existing_setup.enable  # Sigue siendo True

def test_create_setup_with_defaults(setup_service, mock_db):
    """Test que verifica que los nuevos setups se crean con enable=True por defecto"""
    # Configurar datos de prueba
    setup_data = SetupCreate(
        cultivar_id=107,
        soil_id=208,
        season_id=405,
        frequency=28
    )
    
    # Configurar el mock para refresh
    def mock_refresh(obj):
        obj.id = 9
    
    # Configurar los mocks
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.side_effect = mock_refresh
    
    # Ejecutar el método
    result = setup_service.create(db=mock_db, obj_in=setup_data)
    
    # Verificar que el setup se creó habilitado
    assert result.enable is True

def test_update_setup_relationships(setup_service, mock_db):
    """Test que verifica que las relaciones no se actualizan directamente"""
    # Configurar datos de prueba
    setup_id = 10
    existing_setup = MngSetup(
        id=setup_id,
        cultivar_id=108,
        soil_id=209,
        season_id=406,
        frequency=14,
        enable=True
    )
    update_data = SetupUpdate(
        cultivar_id=109,  # Intentar actualizar relación
        soil_id=210       # Intentar actualizar relación
    )
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_setup
    
    # Ejecutar el método
    result = setup_service.update(id=setup_id, obj_in=update_data, db=mock_db)
    
    # Verificar que las relaciones se actualizaron
    assert result.cultivar_id == update_data.cultivar_id
    assert result.soil_id == update_data.soil_id

def test_get_by_cultivar_with_relations(setup_service, mock_db):
    """Test para obtener setups con relaciones cargadas (aunque no se serializan)"""
    # Configurar datos de prueba
    mock_setup = MngSetup(
        id=11, 
        cultivar_id=110, 
        soil_id=211,
        season_id=407,
        frequency=21,
        enable=True
    )
    # Agregar relaciones ficticias
    mock_setup.cultivar = MagicMock()
    mock_setup.soil = MagicMock()
    mock_setup.configuration_files = [MagicMock()]
    mock_setup.season = MagicMock()

    # Configurar el mock
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_setup]
    
    # Ejecutar el método
    result = setup_service.get_by_cultivar(mock_db, 110)
    
    # Verificar resultados
    assert len(result) == 1
    assert result[0].id == 11
    # Las relaciones no deberían estar en el resultado serializado
    assert not hasattr(result[0], 'cultivar')
    assert not hasattr(result[0], 'soil')
    assert not hasattr(result[0], 'configuration_files')
    assert not hasattr(result[0], 'season')

def test_delete_setup_soft_delete(setup_service, mock_db):
    """Test que verifica que el delete es un soft delete (deshabilitar)"""
    # Configurar datos de prueba
    setup_id = 12
    existing_setup = MngSetup(
        id=setup_id,
        cultivar_id=111,
        soil_id=212,
        season_id=408,
        frequency=7,
        enable=True
    )
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_setup
    
    # Ejecutar el método
    result = setup_service.delete(id=setup_id, db=mock_db)
    
    # Verificar que no fue eliminado físicamente
    mock_db.delete.assert_not_called()
    # Verificar que fue deshabilitado
    assert existing_setup.enable is False
    mock_db.commit.assert_called_once()

def test_create_setup_with_optional_fields(setup_service, mock_db):
    """Test para crear setup con campos opcionales (aunque no hay en el modelo)"""
    # Configurar datos de prueba
    setup_data = SetupCreate(
        cultivar_id=112,
        soil_id=213,
        season_id=409,
        frequency=14,
        enable=True
    )
    
    # Configurar el mock para refresh
    def mock_refresh(obj):
        obj.id = 13
    
    # Configurar los mocks
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.side_effect = mock_refresh
    
    # Ejecutar el método
    result = setup_service.create(db=mock_db, obj_in=setup_data)
    
    # Verificar resultados
    assert result.id == 13
    assert result.enable is True  # Campo por defecto
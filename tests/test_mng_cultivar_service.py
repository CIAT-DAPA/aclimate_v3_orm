# test_mng_cultivar_service.py
import pytest
from unittest.mock import MagicMock, create_autospec, patch
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from pydantic import ValidationError

# Importaciones de tu proyecto
from aclimate_v3_orm.models import MngCultivar
from aclimate_v3_orm.schemas import CultivarCreate, CultivarRead, CultivarUpdate
from aclimate_v3_orm.services import MngCultivarService
from aclimate_v3_orm.validations import MngCultivarValidator

@pytest.fixture
def mock_db():
    """Fixture para una sesión de base de datos mockeada"""
    return create_autospec(Session, instance=True)

@pytest.fixture
def cultivar_service():
    """Fixture para el servicio de cultivares"""
    return MngCultivarService()

def test_get_by_crop(cultivar_service, mock_db):
    """Test para obtener cultivares por crop_id"""
    # Configurar datos de prueba
    mock_cultivars = [
        MngCultivar(id=1, crop_id=100, country_id=200, name="Cultivar A", sort_order=1, rainfed=True, enable=True, register=datetime.now(timezone.utc), updated=datetime.now(timezone.utc)),
        MngCultivar(id=2, crop_id=100, country_id=201, name="Cultivar B", sort_order=2, rainfed=False, enable=True, register=datetime.now(timezone.utc), updated=datetime.now(timezone.utc))
    ]
    
    # Configurar el mock
    mock_db.query.return_value.filter.return_value.all.return_value = mock_cultivars
    
    # Ejecutar el método
    result = cultivar_service.get_by_crop(100, db=mock_db)
    
    # Verificar resultados
    assert len(result) == 2
    assert all(isinstance(item, CultivarRead) for item in result)
    assert all(item.crop_id == 100 for item in result)
    
    # Verificar llamadas a la base de datos
    mock_db.query.assert_called_once_with(MngCultivar)
    mock_db.query.return_value.filter.assert_called_once()

def test_get_by_country(cultivar_service, mock_db):
    """Test para obtener cultivares por country_id"""
    # Configurar datos de prueba
    mock_cultivars = [
        MngCultivar(id=3, crop_id=101, country_id=300, name="Cultivar C", sort_order=3, rainfed=True, enable=True, register=datetime.now(timezone.utc), updated=datetime.now(timezone.utc)),
        MngCultivar(id=4, crop_id=102, country_id=300, name="Cultivar D", sort_order=4, rainfed=False, enable=True, register=datetime.now(timezone.utc), updated=datetime.now(timezone.utc))
    ]
    
    # Configurar el mock
    mock_db.query.return_value.filter.return_value.all.return_value = mock_cultivars
    
    # Ejecutar el método
    result = cultivar_service.get_by_country(300, db=mock_db)
    
    # Verificar resultados
    assert len(result) == 2
    assert all(isinstance(item, CultivarRead) for item in result)
    assert all(item.country_id == 300 for item in result)

def test_create_cultivar_valid(cultivar_service, mock_db):
    """Test para crear un cultivar válido"""
    # Configurar datos de prueba
    cultivar_data = CultivarCreate(
        country_id=400,
        crop_id=103,
        name="New Cultivar",
        sort_order=5,
        rainfed=True
    )
    mock_new_cultivar = MngCultivar(
        id=5, 
        country_id=cultivar_data.country_id,
        crop_id=cultivar_data.crop_id,
        name=cultivar_data.name,
        sort_order=cultivar_data.sort_order,
        rainfed=cultivar_data.rainfed,
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
    with patch.object(MngCultivarValidator, 'create_validate') as mock_validate:
        # Ejecutar el método
        result = cultivar_service.create(obj_in=cultivar_data, db=mock_db)
    
    # Verificar resultados
    assert isinstance(result, CultivarRead)
    assert result.id == 5
    assert result.country_id == cultivar_data.country_id
    assert result.crop_id == cultivar_data.crop_id
    assert result.name == cultivar_data.name
    assert result.sort_order == cultivar_data.sort_order
    assert result.rainfed == cultivar_data.rainfed
    
    # Verificar llamadas
    mock_validate.assert_called_once_with(mock_db, cultivar_data)
    mock_db.add.assert_called_once()
    mock_db.refresh.assert_called_once()

def test_update_cultivar(cultivar_service, mock_db):
    """Test para actualizar un cultivar"""
    # Configurar datos de prueba
    cultivar_id = 6
    existing_cultivar = MngCultivar(
        id=cultivar_id,
        country_id=500,
        crop_id=104,
        name="Old Cultivar",
        sort_order=6,
        rainfed=False,
        enable=True
    )
    update_data = CultivarUpdate(
        name="Updated Cultivar",
        rainfed=True
    )
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_cultivar
    
    # Ejecutar el método
    result = cultivar_service.update(cultivar_id, update_data, db=mock_db)
    
    # Verificar resultados
    assert isinstance(result, CultivarRead)
    assert result.id == cultivar_id
    assert result.name == update_data.name
    assert result.rainfed == update_data.rainfed
    # Campos no actualizados deben permanecer igual
    assert result.country_id == existing_cultivar.country_id
    assert result.crop_id == existing_cultivar.crop_id
    assert result.sort_order == existing_cultivar.sort_order
    assert result.enable == existing_cultivar.enable
    
    # Verificar llamadas
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

def test_delete_cultivar(cultivar_service, mock_db):
    """Test para eliminar (deshabilitar) un cultivar"""
    # Configurar datos de prueba
    cultivar_id = 7
    existing_cultivar = MngCultivar(
        id=cultivar_id,
        country_id=600,
        crop_id=105,
        name="Cultivar to Delete",
        sort_order=7,
        rainfed=True,
        enable=True
    )
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_cultivar
    
    # Ejecutar el método
    result = cultivar_service.delete(cultivar_id, db=mock_db)
    
    # Verificar resultados
    assert result is True
    assert existing_cultivar.enable is False
    mock_db.commit.assert_called_once()

def test_get_by_crop_empty(cultivar_service, mock_db):
    """Test para cuando no hay cultivares para un crop_id"""
    # Configurar el mock para devolver lista vacía
    mock_db.query.return_value.filter.return_value.all.return_value = []
    
    # Ejecutar el método
    result = cultivar_service.get_by_crop(999, db=mock_db)
    
    # Verificar resultados
    assert isinstance(result, list)
    assert len(result) == 0

def test_get_by_country_empty(cultivar_service, mock_db):
    """Test para cuando no hay cultivares para un country_id"""
    # Configurar el mock para devolver lista vacía
    mock_db.query.return_value.filter.return_value.all.return_value = []
    
    # Ejecutar el método
    result = cultivar_service.get_by_country(999, db=mock_db)
    
    # Verificar resultados
    assert isinstance(result, list)
    assert len(result) == 0

def test_create_cultivar_validation_failure(cultivar_service, mock_db):
    """Test para validar fallos en la creación de cultivar"""
    # Configurar datos de prueba
    cultivar_data = CultivarCreate(
        country_id=700,
        crop_id=106,
        name="Invalid Cultivar",
        sort_order=8,
        rainfed=False, 
        enable=True
    )
    
    # Mockear la validación para que lance excepción
    with patch.object(MngCultivarValidator, 'create_validate', 
                     side_effect=ValueError("Name already exists for this crop and country")):
        with pytest.raises(ValueError) as excinfo:
            cultivar_service.create(cultivar_data, db=mock_db)
        
        assert "Name already exists" in str(excinfo.value)
    
    # Verificar que no se llamó a commit
    mock_db.commit.assert_not_called()

def test_partial_update_cultivar(cultivar_service, mock_db):
    """Test para actualización parcial de un cultivar"""
    # Configurar datos de prueba
    cultivar_id = 8
    existing_cultivar = MngCultivar(
        id=cultivar_id,
        country_id=800,
        crop_id=107,
        name="Partial Update",
        sort_order=9,
        rainfed=False,
        enable=True
    )
    update_data = CultivarUpdate(
        rainfed=True  # Solo actualizar rainfed
    )
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_cultivar
    
    # Ejecutar el método
    result = cultivar_service.update(cultivar_id, update_data, db=mock_db)
    
    # Verificar resultados
    assert result.name == existing_cultivar.name  # No cambió
    assert result.sort_order == existing_cultivar.sort_order  # No cambió
    assert result.rainfed == update_data.rainfed  # Actualizado

def test_update_cultivar_country_id(cultivar_service, mock_db):
    """Test que verifica que se puede actualizar country_id"""
    # Configurar datos de prueba
    cultivar_id = 9
    existing_cultivar = MngCultivar(
        id=cultivar_id,
        country_id=900,
        crop_id=108,
        name="Update Country",
        sort_order=10,
        rainfed=True,
        enable=True
    )
    update_data = CultivarUpdate(country_id=901)
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_cultivar
    
    # Ejecutar el método
    result = cultivar_service.update(cultivar_id, update_data, db=mock_db)
    
    # Verificar que el country_id se actualizó
    assert result.country_id == update_data.country_id

def test_create_cultivar_with_defaults(cultivar_service, mock_db):
    """Test que verifica valores por defecto al crear cultivar"""
    # Configurar datos de prueba
    cultivar_data = CultivarCreate(
        country_id=1000,
        crop_id=109,
        name="Default Cultivar",
        sort_order=11
    )
    
    # Configurar el mock para refresh
    def mock_refresh(obj):
        obj.id = 10
    
    # Configurar los mocks
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.side_effect = mock_refresh
    
    # Mockear la validación
    with patch.object(MngCultivarValidator, 'create_validate'):
        # Ejecutar el método
        result = cultivar_service.create(obj_in=cultivar_data, db=mock_db)
    
    # Verificar valores por defecto
    assert result.rainfed is False  # Valor por defecto
    assert result.enable is True    # Valor por defecto

def test_get_by_crop_with_relations(cultivar_service, mock_db):
    """Test para obtener cultivares con relaciones cargadas (aunque no se serializan)"""
    # Configurar datos de prueba
    mock_cultivar = MngCultivar(
        id=11, 
        country_id=1100, 
        crop_id=110,
        name="Cultivar with Relations",
        sort_order=12,
        rainfed=True,
        enable=True
    )
    # Agregar relaciones ficticias
    mock_cultivar.crop = None
    mock_cultivar.setups = []
    mock_cultivar.country = None
    
    # Configurar el mock
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_cultivar]
    
    # Ejecutar el método
    result = cultivar_service.get_by_crop(110, db=mock_db)
    
    # Verificar resultados
    assert len(result) == 1
    assert result[0].id == 11
    assert result[0].crop is None
    assert result[0].country is None

def test_delete_cultivar_soft_delete(cultivar_service, mock_db):
    """Test que verifica que el delete es un soft delete (deshabilitar)"""
    # Configurar datos de prueba
    cultivar_id = 12
    existing_cultivar = MngCultivar(
        id=cultivar_id,
        country_id=1200,
        crop_id=111,
        name="Soft Delete Test",
        sort_order=13,
        rainfed=True,
        enable=True
    )
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_cultivar
    
    # Ejecutar el método
    result = cultivar_service.delete(cultivar_id, db=mock_db)
    
    # Verificar que no fue eliminado físicamente
    # (El servicio base hace soft delete si existe campo enable)
    mock_db.delete.assert_not_called()
    # Verificar que fue deshabilitado
    assert existing_cultivar.enable is False
    mock_db.commit.assert_called_once()

def test_create_cultivar_name_length_validation():
    long_name = "A" * 256  # 256 caracteres (límite es 255)
    with pytest.raises(ValidationError) as excinfo:
        CultivarCreate(
            country_id=1300,
            crop_id=112,
            name=long_name,
            sort_order=14
        )
    assert "at most 255 characters" in str(excinfo.value)

def test_update_cultivar_sort_order(cultivar_service, mock_db):
    """Test para actualizar el sort_order de un cultivar"""
    # Configurar datos de prueba
    cultivar_id = 13
    existing_cultivar = MngCultivar(
        id=cultivar_id,
        country_id=1400,
        crop_id=113,
        name="Update Sort Order",
        sort_order=15,
        rainfed=False,
        enable=True
    )
    update_data = CultivarUpdate(sort_order=16)
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_cultivar
    
    # Ejecutar el método
    result = cultivar_service.update(cultivar_id, update_data, db=mock_db)
    
    # Verificar que el sort_order se actualizó
    assert result.sort_order == update_data.sort_order

def test_get_by_country_with_disabled(cultivar_service, mock_db):
    """Test para obtener cultivares por country_id incluyendo deshabilitados"""
    # Configurar datos de prueba
    mock_cultivars = [
        MngCultivar(id=14, country_id=1500, crop_id=114, name="Enabled Cultivar", sort_order=17, enable=True, rainfed=False),
        MngCultivar(id=15, country_id=1500, crop_id=115, name="Disabled Cultivar", sort_order=18, enable=False, rainfed=True)
    ]
    
    # Configurar el mock
    mock_db.query.return_value.filter.return_value.all.return_value = mock_cultivars
    
    # Ejecutar el método sin filtro de enable (no hay parámetro en el servicio)
    result = cultivar_service.get_by_country(1500, db=mock_db)
    
    # Verificar que devuelve ambos (el servicio no filtra por enable en estos métodos)
    assert len(result) == 2

def test_create_cultivar_with_rainfed_true(cultivar_service, mock_db):
    """Test para crear cultivar con rainfed=True"""
    # Configurar datos de prueba
    cultivar_data = CultivarCreate(
        country_id=1600,
        crop_id=116,
        name="Rainfed Cultivar",
        sort_order=19,
        rainfed=True
    )
    
    # Configurar el mock para refresh
    def mock_refresh(obj):
        obj.id = 16
    
    # Configurar los mocks
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.side_effect = mock_refresh
    
    # Mockear la validación
    with patch.object(MngCultivarValidator, 'create_validate'):
        # Ejecutar el método
        result = cultivar_service.create(obj_in=cultivar_data, db=mock_db)
    
    # Verificar que rainfed es True
    assert result.rainfed is True

def test_update_cultivar_enable_status(cultivar_service, mock_db):
    """Test para actualizar el estado enable de un cultivar"""
    # Configurar datos de prueba
    cultivar_id = 17
    existing_cultivar = MngCultivar(
        id=cultivar_id,
        country_id=1700,
        crop_id=117,
        name="Enable Test",
        sort_order=20,
        rainfed=True,
        enable=True
    )
    update_data = CultivarUpdate(enable=False)
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_cultivar
    
    # Ejecutar el método
    result = cultivar_service.update(cultivar_id, update_data, db=mock_db)
    
    # Verificar resultados
    assert result.enable is False

def test_create_cultivar_minimal_data(cultivar_service, mock_db):
    """Test para crear cultivar con solo campos obligatorios"""
    # Configurar datos de prueba
    cultivar_data = CultivarCreate(
        country_id=1800,
        crop_id=118,
        name="Minimal Cultivar",
        sort_order=21
    )
    
    # Configurar el mock para refresh
    def mock_refresh(obj):
        obj.id = 18
    
    # Configurar los mocks
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.side_effect = mock_refresh
    
    # Mockear la validación
    with patch.object(MngCultivarValidator, 'create_validate'):
        # Ejecutar el método
        result = cultivar_service.create(obj_in=cultivar_data, db=mock_db)
    
    # Verificar resultados
    assert result.id == 18
    # Campos opcionales deben tener valores por defecto
    assert result.rainfed is False
    assert result.enable is True
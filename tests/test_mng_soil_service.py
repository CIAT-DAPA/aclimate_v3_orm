# test_mng_soil_service.py
import pytest
from unittest.mock import create_autospec, patch
from sqlalchemy.orm import Session
from datetime import datetime, timezone

# Importaciones de tu proyecto
from aclimate_v3_orm.models import MngSoil
from aclimate_v3_orm.schemas import SoilCreate, SoilRead, SoilUpdate
from aclimate_v3_orm.services import MngSoilService
from aclimate_v3_orm.validations import MngSoilValidator

@pytest.fixture
def mock_db():
    """Fixture para una sesión de base de datos mockeada"""
    return create_autospec(Session, instance=True)

@pytest.fixture
def soil_service():
    """Fixture para el servicio de suelos"""
    return MngSoilService()

def test_get_by_country_id(soil_service, mock_db):
    """Test para obtener suelos por country_id"""
    # Configurar datos de prueba
    mock_soils = [
        MngSoil(id=1, country_id=100, crop_id=200, name="Soil A", sort_order=1, enable=True),
        MngSoil(id=2, country_id=100, crop_id=201, name="Soil B", sort_order=2, enable=True)
    ]
    
    # Configurar el mock
    mock_db.query.return_value.filter.return_value.all.return_value = mock_soils
    
    # Ejecutar el método
    result = soil_service.get_by_country_id(100, db=mock_db)
    
    # Verificar resultados
    assert len(result) == 2
    assert all(isinstance(item, SoilRead) for item in result)
    assert all(item.country_id == 100 for item in result)
    assert all(item.enable is True for item in result)  # Por defecto enabled=True
    
    # Verificar llamadas a la base de datos
    mock_db.query.assert_called_once_with(MngSoil)
    filter_call = mock_db.query.return_value.filter
    assert filter_call.call_count == 1  # Para country_id y enable

def test_get_by_crop_id(soil_service, mock_db):
    """Test para obtener suelos por crop_id"""
    # Configurar datos de prueba
    mock_soils = [
        MngSoil(id=3, country_id=101, crop_id=300, name="Soil C", sort_order=3, enable=True),
        MngSoil(id=4, country_id=102, crop_id=300, name="Soil D", sort_order=4, enable=True)
    ]
    
    # Configurar el mock
    mock_db.query.return_value.filter.return_value.all.return_value = mock_soils
    
    # Ejecutar el método
    result = soil_service.get_by_crop_id(300, db=mock_db)
    
    # Verificar resultados
    assert len(result) == 2
    assert all(isinstance(item, SoilRead) for item in result)
    assert all(item.crop_id == 300 for item in result)

def test_get_all_enable(soil_service, mock_db):
    """Test para obtener todos los suelos habilitados"""
    # Configurar datos de prueba
    mock_soils = [
        MngSoil(id=5, country_id=103, crop_id=301, name="Soil E", sort_order=5, enable=True),
        MngSoil(id=6, country_id=104, crop_id=302, name="Soil F", sort_order=6, enable=True)
    ]
    
    # Configurar el mock
    mock_db.query.return_value.filter.return_value.all.return_value = mock_soils
    
    # Ejecutar el método sin especificar 'enabled'
    result = soil_service.get_all_enable(db=mock_db)
    
    # Verificar resultados (debería devolver solo habilitados por defecto)
    assert len(result) == 2
    assert all(item.enable is True for item in result)

def test_get_all_enable_disabled(soil_service, mock_db):
    """Test para obtener suelos deshabilitados"""
    # Configurar datos de prueba
    mock_soils = [
        MngSoil(id=7, country_id=105, crop_id=303, name="Soil G", sort_order=7, enable=False)
    ]
    
    # Configurar el mock
    mock_db.query.return_value.filter.return_value.all.return_value = mock_soils
    
    # Ejecutar el método con enabled=False
    result = soil_service.get_all_enable(enabled=False, db=mock_db)
    
    # Verificar resultados
    assert len(result) == 1
    assert result[0].enable is False

def test_get_by_name(soil_service, mock_db):
    """Test para obtener suelos por nombre"""
    # Configurar datos de prueba
    mock_soils = [
        MngSoil(id=8, country_id=106, crop_id=304, name="Clay", sort_order=8, enable=True)
    ]
    
    # Configurar el mock
    mock_db.query.return_value.filter.return_value.all.return_value = mock_soils
    
    # Ejecutar el método
    result = soil_service.get_by_name("Clay", db=mock_db)
    
    # Verificar resultados
    assert len(result) == 1
    assert result[0].name == "Clay"

def test_create_soil_valid(soil_service, mock_db):
    """Test para crear un suelo válido"""
    # Configurar datos de prueba
    soil_data = SoilCreate(
        country_id=107,
        crop_id=305,
        name="New Soil",
        sort_order=9
    )
    mock_new_soil = MngSoil(
        id=9, 
        country_id=soil_data.country_id,
        crop_id=soil_data.crop_id,
        name=soil_data.name,
        sort_order=soil_data.sort_order,
        enable=True,
        register=datetime.now(timezone.utc),
        updated=datetime.now(timezone.utc)
    )
    
    # Configurar el mock para refresh
    def mock_refresh(obj):
        if obj.id is None:
            obj.id = 9
    
    # Configurar los mocks
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.side_effect = mock_refresh
    
    # Mockear la validación
    with patch.object(MngSoilValidator, 'create_validate') as mock_validate:
        # Ejecutar el método
        result = soil_service.create(obj_in=soil_data, db=mock_db)
    
    # Verificar resultados
    assert isinstance(result, SoilRead)
    assert result.id == 9
    assert result.country_id == soil_data.country_id
    assert result.crop_id == soil_data.crop_id
    assert result.name == soil_data.name
    assert result.sort_order == soil_data.sort_order
    
    # Verificar llamadas
    mock_validate.assert_called_once_with(mock_db, soil_data)
    mock_db.add.assert_called_once()
    mock_db.refresh.assert_called_once()

def test_update_soil(soil_service, mock_db):
    """Test para actualizar un suelo"""
    # Configurar datos de prueba
    soil_id = 10
    existing_soil = MngSoil(
        id=soil_id,
        country_id=108,
        crop_id=306,
        name="Old Soil",
        sort_order=10,
        enable=True
    )
    update_data = SoilUpdate(
        name="Updated Soil",
        sort_order=11
    )
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_soil
    
    # Ejecutar el método
    result = soil_service.update(soil_id, update_data, db=mock_db)
    
    # Verificar resultados
    assert isinstance(result, SoilRead)
    assert result.id == soil_id
    assert result.name == update_data.name
    assert result.sort_order == update_data.sort_order
    # Campos no actualizados deben permanecer igual
    assert result.country_id == existing_soil.country_id
    assert result.crop_id == existing_soil.crop_id
    assert result.enable == existing_soil.enable
    
    # Verificar llamadas
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

def test_delete_soil(soil_service, mock_db):
    """Test para eliminar (deshabilitar) un suelo"""
    # Configurar datos de prueba
    soil_id = 11
    existing_soil = MngSoil(
        id=soil_id,
        country_id=109,
        crop_id=307,
        name="Soil to Delete",
        sort_order=12,
        enable=True
    )
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_soil
    
    # Ejecutar el método
    result = soil_service.delete(soil_id, db=mock_db)
    
    # Verificar resultados
    assert result is True
    assert existing_soil.enable is False
    mock_db.commit.assert_called_once()

def test_get_by_country_id_empty(soil_service, mock_db):
    """Test para cuando no hay suelos para un country_id"""
    # Configurar el mock para devolver lista vacía
    mock_db.query.return_value.filter.return_value.all.return_value = []
    
    # Ejecutar el método
    result = soil_service.get_by_country_id(999, db=mock_db)
    
    # Verificar resultados
    assert isinstance(result, list)
    assert len(result) == 0

def test_create_soil_validation_failure(soil_service, mock_db):
    """Test para validar fallos en la creación de suelo"""
    # Configurar datos de prueba
    soil_data = SoilCreate(
        country_id=110,
        crop_id=308,
        name="Invalid Soil",
        sort_order=13
    )
    
    # Mockear la validación para que lance excepción
    with patch.object(MngSoilValidator, 'create_validate', 
                     side_effect=ValueError("Sort order already exists for this country and crop")):
        with pytest.raises(ValueError) as excinfo:
            soil_service.create(soil_data, db=mock_db)
        
        assert "Sort order already exists" in str(excinfo.value)
    
    # Verificar que no se llamó a commit
    mock_db.commit.assert_not_called()

def test_partial_update_soil(soil_service, mock_db):
    """Test para actualización parcial de un suelo"""
    # Configurar datos de prueba
    soil_id = 12
    existing_soil = MngSoil(
        id=soil_id,
        country_id=111,
        crop_id=309,
        name="Partial Update",
        sort_order=14,
        enable=True
    )
    update_data = SoilUpdate(
        sort_order=15  # Solo actualizar sort_order
    )
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_soil
    
    # Ejecutar el método
    result = soil_service.update(soil_id, update_data, db=mock_db)
    
    # Verificar resultados
    assert result.name == existing_soil.name  # No cambió
    assert result.sort_order == update_data.sort_order  # Actualizado

def test_update_soil_country_id(soil_service, mock_db):
    """Test que verifica que se puede actualizar country_id"""
    # Configurar datos de prueba
    soil_id = 13
    existing_soil = MngSoil(
        id=soil_id,
        country_id=112,
        crop_id=310,
        name="Update Country",
        sort_order=16,
        enable=True
    )
    update_data = SoilUpdate(country_id=113)
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_soil
    
    # Ejecutar el método
    result = soil_service.update(soil_id, update_data, db=mock_db)
    
    # Verificar que el country_id se actualizó
    assert result.country_id == update_data.country_id

def test_get_by_name_empty(soil_service, mock_db):
    """Test para cuando no hay suelos con el nombre buscado"""
    # Configurar el mock para devolver lista vacía
    mock_db.query.return_value.filter.return_value.all.return_value = []
    
    # Ejecutar el método
    result = soil_service.get_by_name("Non-existent Soil", db=mock_db)
    
    # Verificar resultados
    assert len(result) == 0

def test_create_soil_with_default_enable(soil_service, mock_db):
    """Test que verifica que los nuevos suelos se crean habilitados por defecto"""
    # Configurar datos de prueba
    soil_data = SoilCreate(
        country_id=114,
        crop_id=311,
        name="Soil with Default",
        sort_order=17
    )
    
    # Configurar el mock para refresh
    def mock_refresh(obj):
        obj.id = 14
    
    # Configurar los mocks
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.side_effect = mock_refresh
    
    # Mockear la validación
    with patch.object(MngSoilValidator, 'create_validate'):
        # Ejecutar el método
        result = soil_service.create(obj_in=soil_data, db=mock_db)
    
    # Verificar que el suelo se creó habilitado
    assert result.enable is True

def test_get_by_crop_id_disabled(soil_service, mock_db):
    """Test para obtener suelos deshabilitados por crop_id"""
    # Configurar datos de prueba
    mock_soils = [
        MngSoil(id=15, country_id=115, crop_id=312, name="Disabled Soil", sort_order=18, enable=False)
    ]
    
    # Configurar el mock
    mock_db.query.return_value.filter.return_value.all.return_value = mock_soils
    
    # Ejecutar el método con enabled=False
    result = soil_service.get_by_crop_id(312, enabled=False, db=mock_db)
    
    # Verificar resultados
    assert len(result) == 1
    assert result[0].enable is False

def test_update_soil_enable_status(soil_service, mock_db):
    """Test para actualizar el estado enable de un suelo"""
    # Configurar datos de prueba
    soil_id = 16
    existing_soil = MngSoil(
        id=soil_id,
        country_id=116,
        crop_id=313,
        name="Enable Test",
        sort_order=19,
        enable=True
    )
    update_data = SoilUpdate(enable=False)
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_soil
    
    # Ejecutar el método
    result = soil_service.update(soil_id, update_data, db=mock_db)
    
    # Verificar resultados
    assert result.enable is False

def test_get_by_name_disabled(soil_service, mock_db):
    """Test para obtener suelos deshabilitados por nombre"""
    # Configurar datos de prueba
    mock_soils = [
        MngSoil(id=17, country_id=117, crop_id=314, name="Disabled Soil", sort_order=20, enable=False)
    ]
    
    # Configurar el mock
    mock_db.query.return_value.filter.return_value.all.return_value = mock_soils
    
    # Ejecutar el método con enabled=False
    result = soil_service.get_by_name("Disabled Soil", enabled=False, db=mock_db)
    
    # Verificar resultados
    assert len(result) == 1
    assert result[0].enable is False

def test_create_soil_with_optional_fields(soil_service, mock_db):
    """Test para crear suelo con solo campos obligatorios"""
    # Configurar datos de prueba
    soil_data = SoilCreate(
        country_id=118,
        crop_id=315,
        name="Minimal Soil",
        sort_order=21
    )
    
    # Configurar el mock para refresh
    def mock_refresh(obj):
        obj.id = 18
        obj.register = datetime.now(timezone.utc)
        obj.updated = datetime.now(timezone.utc)
    
    # Configurar los mocks
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.side_effect = mock_refresh
    
    # Mockear la validación
    with patch.object(MngSoilValidator, 'create_validate'):
        # Ejecutar el método
        result = soil_service.create(obj_in=soil_data, db=mock_db)
    
    # Verificar resultados
    assert result.id == 18
    # Campos opcionales deben tener valores por defecto
    assert result.enable is True
    assert isinstance(result.registered_at, datetime)
    assert isinstance(result.updated_at, datetime)

def test_update_soil_multiple_fields(soil_service, mock_db):
    """Test para actualizar múltiples campos de un suelo"""
    # Configurar datos de prueba
    soil_id = 19
    existing_soil = MngSoil(
        id=soil_id,
        country_id=119,
        crop_id=316,
        name="Multi Update",
        sort_order=22,
        enable=True
    )
    update_data = SoilUpdate(
        name="Updated Multi Soil",
        sort_order=23,
        enable=False
    )
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_soil
    
    # Ejecutar el método
    result = soil_service.update(soil_id, update_data, db=mock_db)
    
    # Verificar resultados
    assert result.name == update_data.name
    assert result.sort_order == update_data.sort_order
    assert result.enable == update_data.enable

def test_get_by_country_id_with_disabled(soil_service, mock_db):
    """Test para obtener suelos por country_id incluyendo deshabilitados"""
    # Configurar datos de prueba
    mock_soils = [
        MngSoil(id=20, country_id=120, crop_id=317, name="Enabled Soil", sort_order=24, enable=True),
        MngSoil(id=21, country_id=120, crop_id=318, name="Disabled Soil", sort_order=25, enable=False)
    ]
    
    # Configurar el mock
    mock_db.query.return_value.filter.return_value.all.return_value = mock_soils
    
    # Ejecutar el método sin filtro de enable
    result = soil_service.get_by_country_id(120, enabled=None, db=mock_db)
    
    # Verificar resultados (debería devolver ambos)
    assert len(result) == 2
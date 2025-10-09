import pytest
from unittest.mock import create_autospec, patch, MagicMock
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List
from pydantic import ValidationError

# Importaciones de tu proyecto
from aclimate_v3_orm.models import MngAdmin1, MngCountry
from aclimate_v3_orm.schemas import Admin1Create, Admin1Read, Admin1Update
from aclimate_v3_orm.services import MngAdmin1Service
from aclimate_v3_orm.validations import MngAdmin1Validator

@pytest.fixture
def mock_db():
    """Fixture para una sesión de base de datos mockeada"""
    return create_autospec(Session, instance=True)

@pytest.fixture
def admin1_service():
    """Fixture para el servicio de Admin1"""
    return MngAdmin1Service()

# ---- Tests para get_by_country_id ----
def test_get_by_country_id(admin1_service, mock_db):
    """Test para obtener regiones Admin1 por country_id"""
    # Configurar datos de prueba
    country_id = 1
    mock_admin1s = [
        MngAdmin1(id=1, country_id=country_id, name="Region 1", ext_id="EXT1", enable=True),
        MngAdmin1(id=2, country_id=country_id, name="Region 2", ext_id="EXT2", enable=True)
    ]
    
    # Configurar el mock
    mock_db.query.return_value.filter.return_value.all.return_value = mock_admin1s
    
    # Ejecutar el método
    result = admin1_service.get_by_country_id(country_id, db=mock_db)
    # Verificar resultados
    assert len(result) == 2
    assert all(isinstance(item, Admin1Read) for item in result)
    assert all(item.country_id == country_id for item in result)
    assert all(item.enable is True for item in result)
    
    # Verificar llamadas a la base de datos
    mock_db.query.assert_called_once_with(MngAdmin1)
    filter_call = mock_db.query.return_value.filter
    assert filter_call.call_count == 1  # Para country_id y enable

def test_get_by_country_id_disabled(admin1_service, mock_db):
    """Test para obtener regiones Admin1 deshabilitadas por country_id"""
    # Configurar datos de prueba
    country_id = 1
    mock_admin1s = [
        MngAdmin1(id=1, country_id=country_id, name="Region 1", ext_id="", enable=False)
    ]
    
    # Configurar el mock
    mock_db.query.return_value.filter.return_value.all.return_value = mock_admin1s
    
    # Ejecutar el método con enabled=False
    result = admin1_service.get_by_country_id(country_id, enabled=False, db=mock_db)
    
    # Verificar resultados
    assert len(result) == 1
    assert result[0].enable is False

# ---- Tests para get_by_country_name ----


def test_get_by_country_name_with_patch(admin1_service, mock_db):
    country_name = "TestCountry"
    
    # Crear mock para country con atributos reales (no MagicMock vacío)
    mock_country = MngCountry(id=1, name=country_name, iso2="TC", enable=True)
    
    mock_admin1 = MngAdmin1(id=1, country_id=1, name="Region 1", ext_id="CTRY1", enable=True, country=mock_country)
    
    mock_db.query.return_value.join.return_value.filter.return_value.all.return_value = [mock_admin1]

    result = admin1_service.get_by_country_name(country_name, db=mock_db)
    assert len(result) == 1
    assert result[0].name == "Region 1"
    assert result[0].country is not None
    assert result[0].country.name == country_name



# ---- Tests para get_all ----
def test_get_all_enabled(admin1_service, mock_db):
    """Test para obtener todas las regiones Admin1 habilitadas"""
    # Configurar datos de prueba
    mock_admin1s = [
        MngAdmin1(id=1, country_id=1, name="Region 1", ext_id="ALL1", enable=True),
        MngAdmin1(id=2, country_id=1, name="Region 2", ext_id="ALL2", enable=True)
    ]
    
    # Configurar el mock
    mock_db.query.return_value.filter.return_value.all.return_value = mock_admin1s
    
    # Ejecutar el método
    result = admin1_service.get_all_enable(db=mock_db)
    
    # Verificar resultados
    assert len(result) == 2
    assert all(item.enable is True for item in result)

def test_get_all_include_disabled(admin1_service, mock_db):
    """Test para obtener todas las regiones Admin1 incluyendo deshabilitadas"""
    # Configurar datos de prueba
    mock_admin1s = [
        MngAdmin1(id=1, country_id=1, name="Region 1", ext_id="EN1", enable=True),
        MngAdmin1(id=2, country_id=1, name="Region 2", ext_id="", enable=False)
    ]
    
    # Configurar el mock sin filtro enable
    mock_db.query.return_value.all.return_value = mock_admin1s
    
    # Ejecutar el método con enabled=None
    result = admin1_service.get_all_enable(enabled=None, db=mock_db)
    
    # Verificar resultados
    assert len(result) == 2
    assert any(item.enable is False for item in result)

# ---- Tests para get_by_name ----
def test_get_by_name(admin1_service, mock_db):
    """Test para obtener regiones Admin1 por nombre"""
    # Configurar datos de prueba
    region_name = "TestRegion"
    mock_admin1s = [
        MngAdmin1(id=1, country_id=1, name=region_name, ext_id="NAME1", enable=True)
    ]
    
    # Configurar el mock
    mock_db.query.return_value.filter.return_value.all.return_value = mock_admin1s
    
    # Ejecutar el método
    result = admin1_service.get_by_name(region_name, db=mock_db)
    
    # Verificar resultados
    assert len(result) == 1
    assert result[0].name == region_name

# ---- Tests para create ----
def test_create_admin1_valid(admin1_service, mock_db):
    """Test para crear una región Admin1 válida"""
    # Configurar datos de prueba
    admin1_data = Admin1Create(country_id=1, name="New Region", ext_id="NEW1")
    mock_new_admin1 = MngAdmin1(
        id=1, 
        country_id=admin1_data.country_id, 
        name=admin1_data.name, 
        ext_id=admin1_data.ext_id,
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
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    # Mockear la validación
    with patch.object(MngAdmin1Validator, 'create_validate') as mock_validate:
        # Ejecutar el método
        result = admin1_service.create(obj_in=admin1_data, db=mock_db)
    
    # Verificar resultados
    assert isinstance(result, Admin1Read)
    assert result.id == 1
    assert result.name == admin1_data.name
    
    # Verificar llamadas
    mock_validate.assert_called_once_with(mock_db, admin1_data)
    mock_db.add.assert_called_once()

# ---- Tests para update ----
def test_update_admin1(admin1_service, mock_db):
    """Test para actualizar una región Admin1"""
    # Configurar datos de prueba
    admin1_id = 1
    update_data = Admin1Update(name="Updated Region")
    existing_admin1 = MngAdmin1(
        id=admin1_id,
        country_id=1,
        name="Old Region",
        ext_id="OLD1",
        enable=True
    )
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_admin1
    
    # Ejecutar el método
    result = admin1_service.update(admin1_id, update_data, db=mock_db)
    
    # Verificar resultados
    assert isinstance(result, Admin1Read)
    assert result.id == admin1_id
    assert result.name == update_data.name
    
    # Verificar llamadas
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

# ---- Tests para delete ----
def test_delete_admin1(admin1_service, mock_db):
    """Test para eliminar (deshabilitar) una región Admin1"""
    # Configurar datos de prueba
    admin1_id = 1
    existing_admin1 = MngAdmin1(
        id=admin1_id,
        country_id=1,
        name="Region to Delete",
        ext_id="DEL1",
        enable=True
    )
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_admin1
    
    # Ejecutar el método
    result = admin1_service.delete(admin1_id, db=mock_db)
    
    # Verificar resultados
    assert result is True
    assert existing_admin1.enable is False
    mock_db.commit.assert_called_once()

# ---- Tests de validación ----
def test_validate_create_duplicate_name(admin1_service, mock_db):
    """Test para validar nombre duplicado al crear Admin1"""
    # Configurar datos de prueba
    admin1_data = Admin1Create(country_id=1, name="Duplicate Region", ext_id="DUP1")
    
    # Configurar el mock para simular que ya existe
    mock_db.query.return_value.filter.return_value.first.return_value = MngAdmin1(id=99, name="Duplicate Region", ext_id="DUP1")
    
    # Mockear la validación para que lance excepción
    with patch.object(MngAdmin1Validator, 'create_validate', side_effect=ValueError("Name already exists")):
        with pytest.raises(ValueError) as excinfo:
            admin1_service.create(admin1_data, db=mock_db)
        
        assert "Name already exists" in str(excinfo.value)

def test_partial_update_admin1(admin1_service, mock_db):
    """Test para actualización parcial de Admin1"""
    # Configurar datos de prueba
    admin1_id = 1
    existing_admin1 = MngAdmin1(
        id=admin1_id,
        country_id=1,
        name="Existing Region",
        ext_id="EXIST1",
        enable=True
    )
    update_data = Admin1Update(enable=False)  # Solo actualizar enable
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_admin1
    
    # Ejecutar el método
    result = admin1_service.update(admin1_id, update_data, db=mock_db)
    
    # Verificar resultados
    assert result.enable is False
    assert result.name == existing_admin1.name  # No debería cambiar
import pytest
from unittest.mock import create_autospec, MagicMock, patch
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List
from pydantic import ValidationError

# Importaciones de tu proyecto
from aclimate_v3_orm.models import MngAdmin2, MngAdmin1, MngCountry
from aclimate_v3_orm.schemas import Admin2Create, Admin2Read, Admin2Update
from aclimate_v3_orm.services import MngAdmin2Service
from aclimate_v3_orm.validations import MngAdmin2Validator

@pytest.fixture
def mock_db():
    """Fixture para una sesión de base de datos mockeada"""
    return create_autospec(Session, instance=True)

@pytest.fixture
def admin2_service():
    """Fixture para el servicio de Admin2"""
    return MngAdmin2Service()

# ---- Tests para get_by_admin1_id ----
def test_get_by_admin1_id(admin2_service, mock_db):
    """Test para obtener regiones Admin2 por admin1_id"""
    admin1_id = 1
    mock_admin2s = [
        MngAdmin2(id=1, admin_1_id=admin1_id, name="Region 2-1", visible=True, enable=True),
        MngAdmin2(id=2, admin_1_id=admin1_id, name="Region 2-2", visible=True, enable=True)
    ]
    
    mock_db.query.return_value.filter.return_value.all.return_value = mock_admin2s
    
    result = admin2_service.get_by_admin1_id(admin1_id, db=mock_db)
    
    assert len(result) == 2
    assert all(isinstance(item, Admin2Read) for item in result)
    assert all(item.admin_1_id == admin1_id for item in result)
    mock_db.query.assert_called_once_with(MngAdmin2)

# ---- Tests para get_by_admin1_name ----
def test_get_by_admin1_name(admin2_service, mock_db):
    """Test para obtener regiones Admin2 por nombre de Admin1"""
    admin1_name = "TestAdmin1"
    mock_admin1 = MngAdmin1(id=1, name=admin1_name, enable=True, country_id=1)
    mock_admin2 = MngAdmin2(id=1, admin_1_id=1, name="Region 2-1", visible=True, enable=True)
    mock_admin2.admin_1 = mock_admin1
    
    # Configurar mocks complejos para el join
    query_mock = MagicMock()
    join_mock = MagicMock()
    filter_mock = MagicMock()
    
    mock_db.query.return_value = query_mock
    query_mock.join.return_value = join_mock
    join_mock.filter.return_value = filter_mock
    filter_mock.all.return_value = [mock_admin2]
    
    result = admin2_service.get_by_admin1_name(admin1_name, db=mock_db)
    
    assert len(result) == 1
    assert result[0].name == "Region 2-1"
    query_mock.join.assert_called_once_with(MngAdmin2.admin_1)

# ---- Tests para get_by_country_id ----
def test_get_by_country_id(admin2_service, mock_db):
    """Test para obtener regiones Admin2 por country_id"""
    country_id = 1

    # Crear objetos mock con relaciones simuladas
    mock_country = MngCountry(id=country_id, name="TestCountry", iso2="CL", enable=True)
    mock_admin1 = MngAdmin1(id=1, country_id=country_id, country=mock_country, name="Test", enable=True)
    mock_admin2 = MngAdmin2(id=1, admin_1_id=1, name="Region 2-1", visible=True, enable=True)
    mock_admin2.admin_1 = mock_admin1

    # Mocks de SQLAlchemy para las llamadas en cadena
    query_mock = MagicMock()
    join1_mock = MagicMock()
    join2_mock = MagicMock()
    filter_mock = MagicMock()

    mock_db.query.return_value = query_mock
    query_mock.join.return_value = join1_mock
    join1_mock.join.return_value = join2_mock
    join2_mock.filter.return_value = filter_mock
    filter_mock.all.return_value = [mock_admin2]

    result = admin2_service.get_by_country_id(country_id, db=mock_db)
    # Validaciones
    assert len(result) == 1
    assert result[0].id == 1
    assert result[0].name == "Region 2-1"

    # Validar la cadena de joins
    query_mock.join.assert_called_once_with(MngAdmin2.admin_1)
    join1_mock.join.assert_called_once_with(MngAdmin1.country)


# ---- Tests para get_by_country_name ----
def test_get_by_country_name(admin2_service, mock_db):
    """Test para obtener regiones Admin2 por nombre de país"""
    country_name = "TestCountry"
    
    # 1. Configurar objetos de prueba con relaciones
    mock_country = MngCountry(id=1, name=country_name, iso2="CL", enable=True)
    mock_admin1 = MngAdmin1(id=1, country_id=1, country=mock_country, enable=True, name="Test")
    mock_admin2 = MngAdmin2(id=1, admin_1_id=1, name="Region 2-1", visible=True, enable=True)
    mock_admin2.admin_1 = mock_admin1
    
    # 2. Configurar mocks para la cadena de llamadas
    query_mock = MagicMock()
    join1_mock = MagicMock()
    join2_mock = MagicMock()
    filter_mock = MagicMock()
    
    # Configurar la cadena de retornos
    mock_db.query.return_value = query_mock
    query_mock.join.return_value = join1_mock
    join1_mock.join.return_value = join2_mock
    join2_mock.filter.return_value = filter_mock
    filter_mock.all.return_value = [mock_admin2]
    
    # 3. Ejecutar el método
    result = admin2_service.get_by_country_name(country_name, db=mock_db)
    # 4. Verificar resultados
    assert len(result) == 1
    assert result[0].admin_1_id == 1
    assert result[0].name == "Region 2-1"
    
    # 5. Verificar llamadas a los joins
    query_mock.join.assert_called_once_with(MngAdmin2.admin_1)
    join1_mock.join.assert_called_once_with(MngAdmin1.country)

# ---- Tests para get_all ----
def test_get_all_enabled(admin2_service, mock_db):
    """Test para obtener todas las regiones Admin2 habilitadas"""
    mock_admin2s = [
        MngAdmin2(id=1, admin_1_id=1, name="Region 2-1", visible=True, enable=True),
        MngAdmin2(id=2, admin_1_id=1, name="Region 2-2", visible=True, enable=True)
    ]
    
    mock_db.query.return_value.filter.return_value.all.return_value = mock_admin2s
    
    result = admin2_service.get_all(db=mock_db)
    
    assert len(result) == 2
    assert all(item.enable is True for item in result)

# ---- Tests para get_by_name ----
def test_get_by_name(admin2_service, mock_db):
    """Test para obtener regiones Admin2 por nombre"""
    region_name = "TestRegion"
    mock_admin2 = [
        MngAdmin2(id=1, admin_1_id=1, name=region_name, visible=True, enable=True)
    ]
    
    mock_db.query.return_value.filter.return_value.all.return_value = mock_admin2
    
    result = admin2_service.get_by_name(region_name, db=mock_db)
    assert len(result) == 1
    assert result[0].name == region_name

# ---- Tests para get_by_visible ----
def test_get_by_visible(admin2_service, mock_db):
    """Test para obtener regiones Admin2 por visibilidad"""
    mock_admin2s = [
        MngAdmin2(id=1, admin_1_id=1, name="Visible Region", visible=True, enable=True)
    ]
    
    mock_db.query.return_value.filter.return_value.all.return_value = mock_admin2s
    
    result = admin2_service.get_by_visible(True, db=mock_db)
    
    assert len(result) == 1
    assert result[0].visible is True

# ---- Tests para create ----
def test_create_admin2_valid(admin2_service, mock_db):
    """Test para crear una región Admin2 válida"""
    admin2_data = Admin2Create(admin_1_id=1, name="New Region")
    mock_new_admin2 = MngAdmin2(
        id=1, 
        admin_1_id=admin2_data.admin_1_id, 
        name=admin2_data.name, 
        enable=True,
        visible=True
    )
    
    # Configurar el mock para refresh
    def mock_refresh(obj):
        if obj.id is None:
            obj.id = 1
    
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.side_effect = mock_refresh
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    # Mockear la validación
    with patch.object(MngAdmin2Validator, 'create_validate') as mock_validate:
        result = admin2_service.create(obj_in=admin2_data, db=mock_db)
    
    assert isinstance(result, Admin2Read)
    assert result.id == 1
    mock_validate.assert_called_once_with(mock_db, admin2_data)

# ---- Tests para update ----
def test_update_admin2(admin2_service, mock_db):
    """Test para actualizar una región Admin2"""
    admin2_id = 1
    update_data = Admin2Update(name="Updated Region", visible=False)
    existing_admin2 = MngAdmin2(
        id=admin2_id,
        admin_1_id=1,
        name="Old Region",
        visible=True,
        enable=True
    )
    
    mock_db.query.return_value.get.return_value = existing_admin2
    
    result = admin2_service.update(admin2_id, update_data, db=mock_db)
    
    assert result.name == "Updated Region"
    assert result.visible is False
    mock_db.commit.assert_called_once()

# ---- Tests para delete ----
def test_delete_admin2(admin2_service, mock_db):
    """Test para eliminar (deshabilitar) una región Admin2"""
    admin2_id = 1
    existing_admin2 = MngAdmin2(
        id=admin2_id,
        admin_1_id=1,
        name="Region to Delete",
        enable=True
    )
    
    mock_db.query.return_value.get.return_value = existing_admin2
    
    result = admin2_service.delete(admin2_id, db=mock_db)
    
    assert result is True
    assert existing_admin2.enable is False
    mock_db.commit.assert_called_once()

# ---- Tests de validación ----
def test_validate_create_duplicate(admin2_service, mock_db):
    """Test para validar duplicados al crear Admin2"""
    admin2_data = Admin2Create(admin_1_id=1, name="Duplicate Region")
    
    # Simular que ya existe
    mock_db.query.return_value.filter.return_value.first.return_value = MngAdmin2(id=99, name="Duplicate Region")
    
    with patch.object(MngAdmin2Validator, 'create_validate', side_effect=ValueError("Name already exists")):
        with pytest.raises(ValueError) as excinfo:
            admin2_service.create(admin2_data, db=mock_db)
        
        assert "Name already exists" in str(excinfo.value)
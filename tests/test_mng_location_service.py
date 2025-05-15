import pytest
from unittest.mock import create_autospec, MagicMock, patch
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List
from pydantic import ValidationError

from aclimate_v3_orm.models import MngLocation, MngAdmin2, MngAdmin1, MngCountry
from aclimate_v3_orm.schemas import LocationCreate, LocationRead, LocationUpdate
from aclimate_v3_orm.services import MngLocationService
from aclimate_v3_orm.validations import MngLocationValidator

@pytest.fixture
def mock_db():
    """Fixture para una sesión de base de datos mockeada"""
    return create_autospec(Session, instance=True)

@pytest.fixture
def location_service():
    """Fixture para el servicio de ubicaciones"""
    return MngLocationService()

# ---- Tests básicos CRUD (heredados de BaseService) ----
def test_create_location(location_service, mock_db):
    """Test para crear una ubicación"""
    # 1. Configurar datos de prueba válidos
    location_data = LocationCreate(
        name="Test Location",
        admin_2_id=1,
        latitude=12.34,
        longitude=56.78,
        visible=True,
        altitude=23,
        ext_id="Test1",
        origin="CHIRPS"
    )
    
    # 2. Configurar mocks
    mock_db.query.return_value.filter.return_value.first.return_value = None
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    
    def mock_refresh(obj):
        obj.id = 1  # Asignar ID simulado
        obj.enable = True  # Asegurar que enable está establecido
    
    mock_db.refresh.side_effect = mock_refresh
    
    # 3. Mockear validación
    with patch.object(MngLocationValidator, 'create_validate'):
        result = location_service.create(location_data, db=mock_db)
    
    # 4. Verificaciones
    assert isinstance(result, LocationRead)
    assert result.id == 1
    assert result.name == "Test Location"
    assert result.enable is True  # Verificar que enable está correctamente establecido
    assert result.visible is True
    assert result.latitude == 12.34

def test_update_location(location_service, mock_db):
    """Test para actualizar una ubicación"""
    location_id = 1
    update_data = LocationUpdate(name="Updated Location", visible=False)
    existing_location = MngLocation(
        id=location_id,
        admin_2_id=1,
        name="Original Location",
        visible=True,
        enable=True
    )
    
    mock_db.query.return_value.get.return_value = existing_location
    
    result = location_service.update(location_id, update_data, db=mock_db)
    
    assert result.name == "Updated Location"
    assert result.visible is False
    mock_db.commit.assert_called_once()

def test_delete_location(location_service, mock_db):
    """Test para eliminar (deshabilitar) una ubicación"""
    location_id = 1
    existing_location = MngLocation(
        id=location_id,
        admin_2_id=1,
        name="Location to Delete",
        enable=True
    )
    
    mock_db.query.return_value.get.return_value = existing_location
    
    result = location_service.delete(location_id, db=mock_db)
    
    assert result is True
    assert existing_location.enable is False
    mock_db.commit.assert_called_once()

# ---- Tests para métodos específicos ----
def test_get_by_visible(location_service, mock_db):
    """Test simplificado para obtener ubicaciones por visibilidad"""
    # Configurar datos de prueba
    visible_location = MngLocation(id=1, 
                    name="Visible Location", 
                    visible=True, 
                    enable=True,
                    altitude=23,
                    ext_id="Test1",
                    origin="CHIRPS",
                    latitude=12.34,
                    longitude=56.78,
                    admin_2_id=1)
    hidden_location = MngLocation(id=2, 
                    name="Hidden Location", 
                    visible=False, 
                    enable=True,
                    altitude=24,
                    ext_id="Test2",
                    origin="CHIRPS",
                    latitude=12.34,
                    longitude=56.78,
                    admin_2_id=1)
    
    # Configurar mocks separados para cada caso de prueba
    with patch.object(location_service, '_session_scope') as mock_scope:
        # Configurar el mock para visibles
        mock_scope.return_value.__enter__.return_value.query.return_value \
            .filter.return_value.all.return_value = [visible_location]
        result = location_service.get_by_visible(True)
        assert len(result) == 1
        assert result[0].visible is True
        
        # Configurar el mock para no visibles
        mock_scope.return_value.__enter__.return_value.query.return_value \
            .filter.return_value.all.return_value = [hidden_location]
        result = location_service.get_by_visible(False)
        assert len(result) == 1
        assert result[0].visible is False

def test_get_by_ext_id(location_service, mock_db):
    """Test para obtener ubicaciones por ID externo"""
    ext_id = "EXT123"
    mock_location = MngLocation(id=1, 
                                ext_id=ext_id, 
                                name="Test Location", 
                                enable=True,
                                latitude=12.34,
                                longitude=56.78,
                                altitude=23,
                                origin="CHIRPS",
                                admin_2_id=1,
                                visible=True)
    
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_location]
    
    result = location_service.get_by_ext_id(ext_id, db=mock_db)
    
    assert len(result) == 1
    assert result[0].ext_id == ext_id

def test_get_by_name(location_service, mock_db):
    """Test para obtener ubicaciones por nombre"""
    location_name = "Test Location"
    mock_location = [
        MngLocation(id=1,
                    name=location_name, 
                    enable=True,
                    latitude=12.34,
                    longitude=56.78,
                    altitude=23,
                    ext_id="Test1",
                    origin="CHIRPS",
                    admin_2_id=1,
                    visible=True)
    ]
    
    mock_db.query.return_value.filter.return_value.all.return_value = mock_location
    
    result = location_service.get_by_name(location_name, db=mock_db)
    assert len(result) == 1
    assert result[0].name == location_name

def test_get_all_enable(location_service, mock_db):
    """Test para obtener todas las ubicaciones habilitadas"""
    mock_locations = [
        MngLocation(id=1, 
                    name="Location 1", 
                    enable=True,admin_2_id=1, 
                    latitude=12.34,
                    longitude=56.78,
                    altitude=23,
                    ext_id="Test1",
                    origin="CHIRPS",
                    visible=True),
        MngLocation(id=2, 
                    name="Location 2", 
                    enable=True,
                    admin_2_id=1,
                    latitude=12.34,
                    longitude=56.78,
                    altitude=23,
                    ext_id="Test1",
                    origin="CHIRPS",
                    visible=True)
    ]
    
    mock_db.query.return_value.filter.return_value.all.return_value = mock_locations
    
    result = location_service.get_all_enable(db=mock_db)
    
    assert len(result) == 2
    assert all(loc.enable is True for loc in result)

# ---- Tests con relaciones complejas ----
def test_get_by_country_id(location_service, mock_db):
    """Test para obtener ubicaciones por country_id"""
    country_id = 1
    mock_country = MngCountry(id=1, name="Test Country", iso2="CC")
    mock_admin1 = MngAdmin1(id=1, country_id=country_id, country=mock_country, enable=True)
    mock_admin2 = MngAdmin2(id=1, admin_1_id=1, admin_1_region=mock_admin1, visible=True, enable=True)
    mock_location = MngLocation(id=1, 
                                admin_2_id=1, 
                                name="Test Location",
                                latitude=12.34,
                                longitude=56.78,
                                altitude=23,
                                ext_id="Test1",
                                origin="CHIRPS",
                                visible=True,
                                enable=True,
                                admin_2_region=mock_admin2)
    
    # Configurar mocks para la cadena de joins
    query_mock = MagicMock()
    join1_mock = MagicMock()
    join2_mock = MagicMock()
    filter_mock = MagicMock()
    
    mock_db.query.return_value = query_mock
    query_mock.join.return_value = join1_mock
    join1_mock.join.return_value = join2_mock
    join2_mock.filter.return_value = filter_mock
    filter_mock.all.return_value = [mock_location]
    
    result = location_service.get_by_country_id(country_id, db=mock_db)
    
    assert len(result) == 1
    assert result[0].name == "Test Location"
    query_mock.join.assert_called_once_with(MngLocation.admin_2_region)

def test_get_by_admin1_id(location_service, mock_db):
    """Test para obtener ubicaciones por admin1_id"""
    admin1_id = 1
    mock_admin2 = MngAdmin2(id=1, admin_1_id=admin1_id, visible=True, enable=True)
    mock_location = MngLocation(id=1, 
                                admin_2_id=1, 
                                name="Test Location",
                                latitude=12.34,
                                longitude=56.78,
                                altitude=23,
                                ext_id="Test1",
                                origin="CHIRPS",
                                visible=True,
                                enable=True,
                                admin_2_region=mock_admin2)
    
    # Configurar mocks
    query_mock = MagicMock()
    join_mock = MagicMock()
    filter_mock = MagicMock()
    
    mock_db.query.return_value = query_mock
    query_mock.join.return_value = join_mock
    join_mock.filter.return_value = filter_mock
    filter_mock.all.return_value = [mock_location]
    
    result = location_service.get_by_admin1_id(admin1_id, db=mock_db)
    
    assert len(result) == 1
    assert result[0].name == "Test Location"
    query_mock.join.assert_called_once_with(MngLocation.admin_2_region)

def test_get_by_country_name(location_service, mock_db):
    """Test para obtener ubicaciones por nombre de país"""
    country_name = "Test Country"
    mock_country = MngCountry(id=1, name=country_name, iso2="CC")
    mock_admin1 = MngAdmin1(id=1, country=mock_country, enable=True, country_id=1)
    mock_admin2 = MngAdmin2(id=1, admin_1_region=mock_admin1, admin_1_id=1, visible=True, enable=True)
    mock_location = MngLocation(id=1, 
                                admin_2_id=1, 
                                name="Test Location",
                                latitude=12.34,
                                longitude=56.78,
                                altitude=23,
                                ext_id="Test1",
                                origin="CHIRPS",
                                visible=True,
                                enable=True,
                                admin_2_region=mock_admin2)
    
    # Configurar mocks para múltiples joins
    query_mock = MagicMock()
    join1_mock = MagicMock()
    join2_mock = MagicMock()
    join3_mock = MagicMock()
    filter_mock = MagicMock()
    
    mock_db.query.return_value = query_mock
    query_mock.join.return_value = join1_mock
    join1_mock.join.return_value = join2_mock
    join2_mock.join.return_value = join3_mock
    join3_mock.filter.return_value = filter_mock
    filter_mock.all.return_value = [mock_location]
    
    result = location_service.get_by_country_name(country_name, db=mock_db)
    
    assert len(result) == 1
    assert result[0].name == "Test Location"
    query_mock.join.assert_called_once_with(MngLocation.admin_2_region)

def test_get_by_admin1_name(location_service, mock_db):
    """Test para obtener ubicaciones por nombre de admin1"""
    admin1_name = "Test Admin1"
    mock_admin1 = MngAdmin1(id=1, name=admin1_name, enable=True, country_id=1)
    mock_admin2 = MngAdmin2(id=1, admin_1_region=mock_admin1, admin_1_id=1, visible=True, enable=True)
    mock_location = MngLocation(id=1, 
                                admin_2_id=1, 
                                name="Test Location",
                                latitude=12.34,
                                longitude=56.78,
                                altitude=23,
                                ext_id="Test1",
                                origin="CHIRPS",
                                visible=True,
                                enable=True,
                                admin_2_region=mock_admin2)
    
    # Configurar mocks
    query_mock = MagicMock()
    join1_mock = MagicMock()
    join2_mock = MagicMock()
    filter_mock = MagicMock()
    
    mock_db.query.return_value = query_mock
    query_mock.join.return_value = join1_mock
    join1_mock.join.return_value = join2_mock
    join2_mock.filter.return_value = filter_mock
    filter_mock.all.return_value = [mock_location]
    
    result = location_service.get_by_admin1_name(admin1_name, db=mock_db)
    
    assert len(result) == 1
    assert result[0].name == "Test Location"
    query_mock.join.assert_called_once_with(MngLocation.admin_2_region)

def test_get_by_admin2_id(location_service, mock_db):
    """Test para obtener ubicaciones por admin2_id"""
    admin2_id = 1
    mock_location = MngLocation(id=1, 
                                admin_2_id=admin2_id, 
                                name="Test Location",
                                latitude=12.34,
                                longitude=56.78,
                                altitude=23,
                                ext_id="Test1",
                                origin="CHIRPS",
                                visible=True,
                                enable=True)
    
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_location]
    
    result = location_service.get_by_admin2_id(admin2_id, db=mock_db)
    
    assert len(result) == 1
    assert result[0].admin_2_id == admin2_id

def test_get_by_admin2_name(location_service, mock_db):
    """Test para obtener ubicaciones por nombre de admin2"""
    admin2_name = "Test Admin2"
    mock_admin2 = MngAdmin2(id=1, name=admin2_name, admin_1_id=1, visible=True, enable=True)
    mock_location = MngLocation(id=1, 
                                admin_2_id=1, 
                                name="Test Location",
                                latitude=12.34,
                                longitude=56.78,
                                altitude=23,
                                ext_id="Test1",
                                origin="CHIRPS",
                                visible=True,
                                enable=True,
                                admin_2_region=mock_admin2)
    
    # Configurar mocks
    query_mock = MagicMock()
    join_mock = MagicMock()
    filter_mock = MagicMock()
    
    mock_db.query.return_value = query_mock
    query_mock.join.return_value = join_mock
    join_mock.filter.return_value = filter_mock
    filter_mock.all.return_value = [mock_location]
    
    result = location_service.get_by_admin2_name(admin2_name, db=mock_db)
    assert len(result) == 1
    assert result[0].name == "Test Location"
    query_mock.join.assert_called_once_with(MngLocation.admin_2_region)

# ---- Tests de validación ----
def test_validate_create_duplicate(location_service, mock_db):
    """Test para validar duplicados al crear ubicación"""
    location_data = LocationCreate(
        admin_2_id=1,
        name="Duplicate Location",
        ext_id="DUPL123"
    )
    
    # Simular que ya existe
    mock_db.query.return_value.filter.return_value.first.return_value = MngLocation(id=99, name="Duplicate Location")
    
    with patch.object(MngLocationValidator, 'create_validate', side_effect=ValueError("Location already exists")):
        with pytest.raises(ValueError) as excinfo:
            location_service.create(location_data, db=mock_db)
        
        assert "Location already exists" in str(excinfo.value)
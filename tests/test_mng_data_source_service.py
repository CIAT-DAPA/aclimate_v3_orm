import pytest
from unittest.mock import create_autospec, MagicMock, patch
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List, Optional

from aclimate_v3_orm.models import MngDataSource
from aclimate_v3_orm.schemas import DataSourceCreate, DataSourceRead
from aclimate_v3_orm.services import MngDataSourceService
from aclimate_v3_orm.validations import MngDataSourceValidator

@pytest.fixture
def mock_db():
    """Fixture para una sesión de base de datos mockeada"""
    return create_autospec(Session, instance=True)

@pytest.fixture
def data_source_service():
    """Fixture para el servicio de fuentes de datos"""
    return MngDataSourceService()

# ---- Tests para métodos específicos de MngDataSourceService ----
def test_get_by_country(data_source_service, mock_db):
    """Test para obtener fuentes de datos por country_id"""
    country_id = 1
    mock_data_sources = [
        MngDataSource(
            id=1, 
            country_id=country_id,
            name="Test Source 1",
            type="API",
            enable=True,
            content="Content 1",
            created_at=datetime.now(timezone.utc)
        ),
        MngDataSource(
            id=2, 
            country_id=country_id,
            name="Test Source 2",
            type="Database",
            enable=True,
            content="Content 2",
            created_at=datetime.now(timezone.utc)
        )
    ]
    
    mock_db.query.return_value.filter.return_value.all.return_value = mock_data_sources
    
    result = data_source_service.get_by_country(country_id, db=mock_db)
    
    assert len(result) == 2
    assert all(ds.country_id == country_id for ds in result)
    assert result[0].name == "Test Source 1"
    assert result[1].name == "Test Source 2"
    mock_db.query.return_value.filter.assert_called_once()

def test_get_by_name_found(data_source_service, mock_db):
    """Test para obtener una fuente de datos por nombre (encontrada)"""
    source_name = "Test Source"
    mock_data_source = MngDataSource(
        id=1,
        country_id=1,
        name=source_name,
        type="API",
        enable=True,
        created_at=datetime.now(timezone.utc),
        content="Test content"
    )

    mock_db.query.return_value.filter.return_value.first.return_value = mock_data_source
    
    result = data_source_service.get_by_name(source_name, db=mock_db)
    
    assert result is not None
    assert result.name == source_name
    assert result.id == 1

def test_get_by_name_not_found(data_source_service, mock_db):
    """Test para obtener una fuente de datos por nombre (no encontrada)"""
    source_name = "Unknown Source"
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    result = data_source_service.get_by_name(source_name, db=mock_db)
    
    assert result is None

# ---- Tests para validación durante la creación ----
def test_create_with_validation(data_source_service, mock_db):
    """Test que verifica que se llama a la validación durante la creación"""
    # 1. Configurar datos de prueba válidos
    data_source_data = DataSourceCreate(
        country_id=1,
        name="Valid Source",
        type="API",
        description="Test description",
        enable=True,
        content="{}"
    )
    
    # 2. Configurar mocks
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    
    def mock_refresh(obj):
        obj.id = 1  # Asignar ID simulado
    
    mock_db.refresh.side_effect = mock_refresh
    
    # 3. Mockear validación y crear
    with patch.object(MngDataSourceValidator, 'create_validate') as mock_validate:
        result = data_source_service.create(data_source_data, db=mock_db)
    
    # 4. Verificaciones
    mock_validate.assert_called_once_with(mock_db, data_source_data)
    assert result.id == 1
    assert result.name == "Valid Source"

def test_create_validation_error(data_source_service, mock_db):
    """Test que verifica el manejo de errores de validación"""
    # 1. Configurar datos inválidos
    invalid_data = DataSourceCreate(
        country_id=1,
        name="",  # Nombre vacío - inválido
        type="API",
        description="Test",
        enable=True,
        content="{}"
    )
    
    # 2. Configurar mock para lanzar excepción
    with patch.object(MngDataSourceValidator, 'create_validate', 
                     side_effect=ValueError("Invalid name")) as mock_validate:
        
        # 3. Verificar que se lanza la excepción
        with pytest.raises(ValueError) as excinfo:
            data_source_service.create(invalid_data, db=mock_db)
        
        assert "Invalid name" in str(excinfo.value)
    
    # 4. Verificar que no se llamó a commit
    mock_db.commit.assert_not_called()

# ---- Tests para operaciones CRUD básicas ----
def test_create_data_source(data_source_service, mock_db):
    """Test para crear una nueva fuente de datos"""
    data_source_data = DataSourceCreate(
        country_id=1,
        name="New Source",
        type="Scraper",
        description="Test description",
        enable=True,
        content="{}"
    )
    
    # Mockear validación y operaciones de DB
    with patch.object(MngDataSourceValidator, 'create_validate'):
        mock_db.add.return_value = None
        mock_db.commit.return_value = None
        
        def mock_refresh(obj):
            obj.id = 1
        
        mock_db.refresh.side_effect = mock_refresh
        
        result = data_source_service.create(data_source_data, db=mock_db)
    
    assert result.id == 1
    assert result.name == "New Source"

def test_update_data_source(data_source_service, mock_db):
    """Test para actualizar una fuente de datos existente"""
    data_source_id = 1
    update_data = {"name": "Updated Source", "description": "Updated description"}
    
    existing_source = MngDataSource(
        id=data_source_id,
        country_id=1,
        name="Original Source",
        type="API",
        description="Original description",
        enable=True,
        content="{}"
    )
    
    mock_db.query.return_value.get.return_value = existing_source
    
    result = data_source_service.update(data_source_id, update_data, db=mock_db)
    
    assert result.name == "Updated Source"
    assert result.description == "Updated description"
    mock_db.commit.assert_called_once()

def test_delete_data_source(data_source_service, mock_db):
    """Test para eliminar (desactivar) una fuente de datos"""
    data_source_id = 1
    existing_source = MngDataSource(
        id=data_source_id,
        country_id=1,
        name="Source to Delete",
        type="API",
        enable=True
    )
    
    mock_db.query.return_value.get.return_value = existing_source
    
    result = data_source_service.delete(data_source_id, db=mock_db)
    
    assert result is True
    assert existing_source.enable is False  # Verificar que se desactivó
    mock_db.commit.assert_called_once()

def test_get_by_id_found(data_source_service, mock_db):
    """Test para obtener una fuente de datos por ID (encontrada)"""
    data_source_id = 1
    mock_source = MngDataSource(
        id=data_source_id,
        country_id=1,
        name="Test Source",
        type="API",
        enable=True
    )
    
    mock_db.query.return_value.get.return_value = mock_source
    
    result = data_source_service.get_by_id(data_source_id, db=mock_db)
    
    assert result.id == data_source_id
    assert result.name == "Test Source"

def test_get_by_id_not_found(data_source_service, mock_db):
    """Test para obtener una fuente de datos por ID (no encontrada)"""
    data_source_id = 999
    mock_db.query.return_value.get.return_value = None
    
    result = data_source_service.get_by_id(data_source_id, db=mock_db)
    
    assert result is None
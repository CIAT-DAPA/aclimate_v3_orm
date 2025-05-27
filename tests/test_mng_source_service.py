import pytest
from unittest.mock import create_autospec, MagicMock, patch
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List
from pydantic import ValidationError

from aclimate_v3_orm.models import MngSource
from aclimate_v3_orm.schemas import MngSourceCreate, MngSourceRead, MngSourceUpdate
from aclimate_v3_orm.services import MngSourceService
from aclimate_v3_orm.validations import MngSourceValidator

@pytest.fixture
def mock_db():
    """Fixture for mocked database session"""
    return create_autospec(Session, instance=True)

@pytest.fixture
def source_service():
    """Fixture for the source service"""
    return MngSourceService()

# ---- Basic CRUD Tests ----
def test_create_source(source_service, mock_db):
    """Test creating a source"""
    # 1. Setup valid test data
    source_data = MngSourceCreate(
        name="Test Source",
        source_type="MA",  # Using MA/AU instead of type
        enable=True
    )
    
    # 2. Configure mocks
    mock_db.query.return_value.filter.return_value.first.return_value = None
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    
    def mock_refresh(obj):
        obj.id = 1
        obj.enable = True
    
    mock_db.refresh.side_effect = mock_refresh
    
    # 3. Mock validation
    with patch.object(MngSourceValidator, 'create_validate'):
        result = source_service.create(source_data, db=mock_db)
    
    # 4. Assertions
    assert isinstance(result, MngSourceRead)
    assert result.id == 1
    assert result.name == "Test Source"
    assert result.source_type == "MA"
    assert result.enable is True

def test_update_source(source_service, mock_db):
    """Test updating a source"""
    source_id = 1
    update_data = MngSourceUpdate(name="Updated Source", source_type="AU")
    existing_source = MngSource(
        id=source_id,
        name="Original Source",
        source_type="MA",
        enable=True
    )
    
    mock_db.query.return_value.get.return_value = existing_source
    
    result = source_service.update(source_id, update_data, db=mock_db)
    
    assert result.name == "Updated Source"
    assert result.source_type == "AU"
    mock_db.commit.assert_called_once()

def test_delete_source(source_service, mock_db):
    """Test deleting (disabling) a source"""
    source_id = 1
    existing_source = MngSource(
        id=source_id,
        name="Source to Delete",
        source_type="MA",
        enable=True
    )
    
    mock_db.query.return_value.get.return_value = existing_source
    
    result = source_service.delete(source_id, db=mock_db)
    
    assert result is True
    assert existing_source.enable is False
    mock_db.commit.assert_called_once()

# ---- Specific Method Tests ----
def test_get_by_source_type(source_service, mock_db):
    """Test getting sources by type (MA/AU)"""
    # Configure test data
    manual_source = MngSource(id=1, name="Manual Source", source_type="MA", enable=True)
    auto_source = MngSource(id=2, name="Auto Source", source_type="AU", enable=True)
    
    with patch.object(source_service, '_session_scope') as mock_scope:
        # Test for manual sources
        mock_scope.return_value.__enter__.return_value.query.return_value \
            .filter.return_value.all.return_value = [manual_source]
        result = source_service.get_by_type("MA")
        assert len(result) == 1
        assert result[0].source_type == "MA"
        
        # Test for automatic sources
        mock_scope.return_value.__enter__.return_value.query.return_value \
            .filter.return_value.all.return_value = [auto_source]
        result = source_service.get_by_type("AU")
        assert len(result) == 1
        assert result[0].source_type == "AU"

def test_get_by_name(source_service, mock_db):
    """Test getting sources by exact name match"""
    source_name = "Test Source"
    mock_source = MngSource(
        id=1,
        name=source_name,
        source_type="MA",
        enable=True
    )
    
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_source]
    
    result = source_service.get_by_name(source_name, db=mock_db)
    
    assert len(result) == 1
    assert result[0].name == source_name

def test_search_by_name(source_service, mock_db):
    """Test searching sources by name (partial match)"""
    search_term = "Test"
    mock_sources = [
        MngSource(id=1, name="Test Source 1", source_type="MA", enable=True),
        MngSource(id=2, name="Test Source 2", source_type="AU", enable=True)
    ]
    
    mock_db.query.return_value.filter.return_value.all.return_value = mock_sources
    
    result = source_service.search_by_name(search_term, db=mock_db)
    
    assert len(result) == 2
    assert all(search_term.lower() in source.name.lower() for source in result)

def test_get_all(source_service, mock_db):
    """Test getting all sources with enabled filter"""
    mock_sources = [
        MngSource(id=1, name="Source 1", source_type="MA", enable=True),
        MngSource(id=2, name="Source 2", source_type="AU", enable=False)
    ]
    
    # Test enabled only
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_sources[0]]
    result = source_service.get_all_enable(enabled=True, db=mock_db)
    assert len(result) == 1
    assert result[0].enable is True
    
    # Test all sources
    mock_db.query.return_value.all.return_value = mock_sources
    result = source_service.get_all_enable(enabled=None, db=mock_db)
    assert len(result) == 2

# ---- Validation Tests ----
def test_validate_create_duplicate(source_service, mock_db):
    """Test validation for duplicate source creation"""
    source_data = MngSourceCreate(
        name="Duplicate Source",
        source_type="MA"
    )
    
    # Simulate existing source
    mock_db.query.return_value.filter.return_value.first.return_value = MngSource(id=99, name="Duplicate Source")
    
    with patch.object(MngSourceValidator, 'create_validate', side_effect=ValueError("Source already exists")):
        with pytest.raises(ValueError) as excinfo:
            source_service.create(source_data, db=mock_db)
        
        assert "Source already exists" in str(excinfo.value)

def test_validate_invalid_source_type(source_service, mock_db):
    """Test validation for invalid source types"""
    # Usa un tipo que pase Pydantic pero falle en tu validador
    invalid_source_data = MngSourceCreate(
        name="Invalid Source",
        source_type="MA"  # Tipo válido para Pydantic
    )
    
    # Configura el mock para simular que el validador encuentra un problema
    with patch.object(MngSourceValidator, 'create_validate', 
                     side_effect=ValueError("Invalid source type: XX")):
        with pytest.raises(ValueError) as excinfo:
            source_service.create(invalid_source_data, db=mock_db)
        
        assert "Invalid source type: XX" in str(excinfo.value)
        
        assert "Invalid source type" in str(excinfo.value)

def test_validate_type_name_combination(source_service, mock_db):
    """Test validation for type-name combination"""
    source_data = MngSourceCreate(
        name="Test Source",
        source_type="MA"
    )
    
    # Simulate existing source with same name and type
    mock_db.query.return_value.filter.return_value.first.return_value = MngSource(
        id=99, 
        name="Test Source", 
        source_type="MA"
    )
    
    with patch.object(MngSourceValidator, 'create_validate', 
                    side_effect=ValueError("A MA source with name 'Test Source' already exists")):
        with pytest.raises(ValueError) as excinfo:
            source_service.create(source_data, db=mock_db)
        
        assert "already exists" in str(excinfo.value)

# ---- Edge Case Tests ----
def test_update_with_partial_data(source_service, mock_db):
    """Test updating with partial data"""
    source_id = 1
    existing_source = MngSource(
        id=source_id,
        name="Original Source",
        source_type="MA",
        enable=True
    )
    
    mock_db.query.return_value.get.return_value = existing_source
    
    # Update only the name
    update_data = MngSourceUpdate(name="Updated Name")
    result = source_service.update(source_id, update_data, db=mock_db)
    
    assert result.name == "Updated Name"
    assert result.source_type == "MA"  # Should remain unchanged

def test_create_with_minimal_data(source_service, mock_db):
    """Test creation with minimal required data"""
    minimal_data = MngSourceCreate(
        name="Minimal Source",
        source_type="AU"
    )
    
    mock_db.query.return_value.filter.return_value.first.return_value = None
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh = lambda obj: setattr(obj, 'id', 1) or setattr(obj, 'enable', True)
    
    with patch.object(MngSourceValidator, 'create_validate'):
        result = source_service.create(minimal_data, db=mock_db)
    
    assert result.id == 1
    assert result.name == "Minimal Source"
    assert result.enable is True  # Should default to True
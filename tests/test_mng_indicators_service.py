import pytest
from unittest.mock import create_autospec, patch
from sqlalchemy.orm import Session
from datetime import datetime, timezone

# Import your project classes
from aclimate_v3_orm.models import MngIndicator
from aclimate_v3_orm.schemas import (
    IndicatorCreate,
    IndicatorRead
)
from aclimate_v3_orm.services import (
    MngIndicatorService
)
from aclimate_v3_orm.validations import (
    IndicatorValidator
)

# ---- Fixtures ----
@pytest.fixture
def mock_db():
    """Fixture for mocked database session"""
    return create_autospec(Session, instance=True)

@pytest.fixture
def indicator_service():
    """Fixture for indicator service"""
    return MngIndicatorService()

# ---- MngIndicatorService Tests ----
def test_create_indicator(indicator_service, mock_db):
    """Test creating a new indicator"""
    indicator_data = IndicatorCreate(
        type="climate",
        name="Temperature",
        short_name="TEMP",
        unit="°C",
        description="Average temperature",
        indicator_category_id=1
    )
    
    # Mock database operations
    mock_db.query.return_value.filter.return_value.first.return_value = None
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    
    def mock_refresh(obj):
        obj.id = 1
        obj.register = datetime.now(timezone.utc)
        obj.updated = datetime.now(timezone.utc)
    
    mock_db.refresh.side_effect = mock_refresh
    
    # Mock validation
    with patch.object(IndicatorValidator, 'validate_name'), \
         patch.object(IndicatorValidator, 'validate_short_name'):
        result = indicator_service.create(indicator_data, db=mock_db)
    
    assert isinstance(result, IndicatorRead)
    assert result.id == 1
    assert result.name == "Temperature"
    assert result.type == "climate"

def test_get_by_name(indicator_service, mock_db):
    """Test getting indicators by name"""
    mock_indicators = [
        MngIndicator(id=1, name="Temperature", type="climate", short_name="TEMP", unit="°C", indicator_category_id=1),
        MngIndicator(id=2, name="Temperature", type="climate", short_name="TEMP2", unit="°C", indicator_category_id=1)
    ]
    
    mock_db.query.return_value.filter.return_value.all.return_value = mock_indicators
    
    results = indicator_service.get_by_name("Temperature", db=mock_db)
    assert len(results) == 2
    assert all(i.name == "Temperature" for i in results)

def test_get_by_type(indicator_service, mock_db):
    """Test getting indicators by type"""
    mock_indicators = [
        MngIndicator(id=1, name="Temp", type="climate", short_name="TEMP", unit="°C", indicator_category_id=1),
        MngIndicator(id=2, name="Rain", type="climate", short_name="RAIN", unit="mm", indicator_category_id=1)
    ]
    
    mock_db.query.return_value.filter.return_value.all.return_value = mock_indicators
    
    results = indicator_service.get_by_type("climate", db=mock_db)
    assert len(results) == 2
    assert all(i.type == "climate" for i in results)

def test_validate_create_duplicate(indicator_service, mock_db):
    """Test validation for duplicate indicator"""
    indicator_data = IndicatorCreate(
        type="climate",
        name="Temperature",
        short_name="TEMP",
        unit="°C",
        indicator_category_id=1
    )
    
    # Mock existing indicator
    mock_db.query.return_value.filter.return_value.first.return_value = MngIndicator(id=99, name="Temperature", indicator_category_id=1)
    
    with patch.object(IndicatorValidator, 'validate_name', side_effect=ValueError("Name exists")):
        with pytest.raises(ValueError) as excinfo:
            indicator_service.create(indicator_data, db=mock_db)
        
        assert "Name exists" in str(excinfo.value)

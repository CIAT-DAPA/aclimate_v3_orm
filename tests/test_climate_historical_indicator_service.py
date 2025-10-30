import pytest
from unittest.mock import create_autospec, MagicMock, patch
from sqlalchemy.orm import Session
from datetime import date
from pydantic import ValidationError

# Import your project classes
from aclimate_v3_orm.models import ClimateHistoricalIndicator, MngIndicator, MngLocation
from aclimate_v3_orm.schemas import (
    ClimateHistoricalIndicatorCreate,
    ClimateHistoricalIndicatorRead
)
from aclimate_v3_orm.services import (
    ClimateHistoricalIndicatorService
)
from aclimate_v3_orm.validations import (
    ClimateHistoricalIndicatorValidator
)

# ---- Fixtures ----
@pytest.fixture
def mock_db():
    """Fixture for mocked database session"""
    return create_autospec(Session, instance=True)


@pytest.fixture
def historical_indicator_service():
    """Fixture for historical indicator service"""
    return ClimateHistoricalIndicatorService()


def test_create_historical_indicator(historical_indicator_service, mock_db):
    """Test creating a historical indicator record"""
    # Crear mock del indicador
    mock_indicator = MngIndicator(
        id=1, 
        type="climate", 
        name="TEMPERATURA",
        temporality="monthly",
        short_name="TEMP", 
        unit="°C", 
        enable=True,
        indicator_category_id=1
    )
    mock_location = MngLocation(id=1, 
                                admin_2_id=1, 
                                name="Test Location",
                                latitude=12.34,
                                longitude=56.78,
                                altitude=23,
                                ext_id="Test1",
                                source_id=1,
                                visible=True,
                                enable=True)
    
    
    # Configurar los mocks para diferentes consultas:
    # 1. Cuando se busque el indicador (para validación)
    # 2. Cuando se verifique si ya existe el registro histórico
    mock_db.query.side_effect = [
        # Para la validación del indicador
        MagicMock(filter=MagicMock(return_value=MagicMock(first=MagicMock(return_value=mock_indicator)))),
        MagicMock(filter=MagicMock(return_value=MagicMock(first=MagicMock(return_value=mock_location)))),
        MagicMock(filter=MagicMock(return_value=MagicMock(first=MagicMock(return_value=None))))
    ]
    
    
    # Configurar mocks para operaciones de guardado
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    
    def mock_refresh(obj):
        obj.id = 1  # Simular el ID asignado por la base de datos
    
    mock_db.refresh.side_effect = mock_refresh

    record_data = ClimateHistoricalIndicatorCreate(
        indicator_id=1,
        location_id=1,
        value=25.5,
        period="monthly",
        start_date=date(2023, 1, 1),
        end_date=date(2023, 1, 31)
    )
    
    # Ejecutar el test sin mockear el validador para probar el flujo completo
    result = historical_indicator_service.create(record_data, db=mock_db)
    
    # Verificaciones
    assert isinstance(result, ClimateHistoricalIndicatorRead)
    assert result.id == 1
    assert result.value == 25.5
    assert result.period == "monthly"
    assert result.indicator_id == 1

def test_get_by_indicator_id(historical_indicator_service, mock_db):
    """Test getting records by indicator ID"""
    mock_records = [
        ClimateHistoricalIndicator(
            id=1,
            indicator_id=1,
            location_id=1,
            value=25.5,
            period="monthly",
            start_date=date(2023, 1, 1)
        ),
        ClimateHistoricalIndicator(
            id=2,
            indicator_id=1,
            location_id=2,
            value=26.0,
            period="monthly",
            start_date=date(2023, 2, 1)
        )
    ]
    
    mock_db.query.return_value.filter.return_value.all.return_value = mock_records
    
    results = historical_indicator_service.get_by_indicator_id(1, db=mock_db)
    assert len(results) == 2
    assert all(r.indicator_id == 1 for r in results)

def test_get_by_period(historical_indicator_service, mock_db):
    """Test getting records by period"""
    mock_records = [
        ClimateHistoricalIndicator(
            id=1,
            indicator_id=1,
            location_id=1,
            value=25.5,
            period="monthly",
            start_date=date(2023, 1, 1)
        )
    ]
    
    mock_db.query.return_value.filter.return_value.all.return_value = mock_records
    
    results = historical_indicator_service.get_by_period("monthly", db=mock_db)
    assert len(results) == 1
    assert results[0].period == "monthly"

def test_validate_invalid_period():
    """Test that invalid enum value for period raises ValidationError"""
    with pytest.raises(ValidationError) as excinfo:
        ClimateHistoricalIndicatorCreate(
            indicator_id=1,
            location_id=1,
            value=25.5,
            period="invalid",  # Valor no permitido por el Enum
            start_date=date(2023, 1, 1),
            end_date=date(2023, 2, 1)
        )

    # Verifica que el mensaje del error contenga el motivo esperado
    assert "Input should be" in str(excinfo.value)
    assert "invalid" in str(excinfo.value)

def test_validate_date_range(historical_indicator_service, mock_db):
    """Test validation for invalid date range"""
    record_data = ClimateHistoricalIndicatorCreate(
        indicator_id=1,
        location_id=1,
        value=25.5,
        period="monthly",
        start_date=date(2023, 2, 1),
        end_date=date(2023, 1, 1)  # Invalid - end before start
    )
    
    with patch.object(ClimateHistoricalIndicatorValidator, 'create_validate',
                    side_effect=ValueError("Start date cannot be after end date")):
        with pytest.raises(ValueError) as excinfo:
            historical_indicator_service.create(record_data, db=mock_db)
        
        assert "Start date cannot be after end date" in str(excinfo.value)

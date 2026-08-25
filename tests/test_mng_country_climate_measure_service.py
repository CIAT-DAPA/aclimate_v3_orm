import pytest
from unittest.mock import create_autospec, MagicMock, patch
from sqlalchemy.orm import Session

# Importaciones de tu proyecto
from aclimate_v3_orm.models import MngCountryClimateMeasure
from aclimate_v3_orm.schemas import CountryClimateMeasureCreate, CountryClimateMeasureRead, CountryClimateMeasureUpdate
from aclimate_v3_orm.services.mng_country_climate_measure_service import MngCountryClimateMeasureService
from aclimate_v3_orm.validations import MngCountryClimateMeasureValidator

@pytest.fixture
def mock_db():
    """Fixture para una sesión de base de datos mockeada"""
    return create_autospec(Session, instance=True)

@pytest.fixture
def country_climate_measure_service():
    """Fixture para el servicio de medidas climáticas a nivel país"""
    return MngCountryClimateMeasureService()


def _create_payload(**overrides):
    """Helper para construir un payload de creación válido."""
    data = {
        "country_id": 1,
        "measure_id": 3,
        "spatial_forecast": False,
        "spatial_climate": True,
        "location_forecast": False,
        "location_climate": True,
        "spatial_climate_conf": [
            {"temporality": "daily", "store": "climate_historical_daily_ni_prec", "workspace": "climate_historical_daily"},
            {"temporality": "monthly", "store": "climate_historical_monthly_ni_prec", "workspace": "climate_historical_monthly"},
        ],
        "location_climate_conf": ["daily", "monthly", "climatology"],
        "description": "Descripción de prueba",
    }
    data.update(overrides)
    return data


# ---- Tests CRUD básicos ----
def test_create_country_climate_measure(country_climate_measure_service, mock_db):
    """Test para crear una configuración de medida climática a nivel país"""
    payload = _create_payload()
    measure_data = CountryClimateMeasureCreate(**payload)

    # Configurar mocks
    mock_db.query.return_value.filter.return_value.first.return_value = None
    mock_db.add.return_value = None
    mock_db.commit.return_value = None

    def mock_refresh(obj):
        obj.id = 1

    mock_db.refresh.side_effect = mock_refresh

    result = country_climate_measure_service.create(measure_data, db=mock_db)

    assert isinstance(result, CountryClimateMeasureRead)
    assert result.id == 1
    assert result.country_id == 1
    assert result.measure_id == 3
    assert result.spatial_climate is True
    assert result.location_climate is True
    assert result.spatial_climate_conf[0].temporality == "daily"
    assert result.location_climate_conf[0] == "daily"
    assert result.description == "Descripción de prueba"


def test_get_by_country(country_climate_measure_service, mock_db):
    """Test para obtener configuraciones por país"""
    mock_obj = MngCountryClimateMeasure(
        id=1,
        country_id=1,
        measure_id=3,
        spatial_forecast=False,
        spatial_climate=True,
        location_forecast=False,
        location_climate=True,
        spatial_climate_conf=[{"temporality": "daily", "store": "s1", "workspace": "w1"}],
        location_climate_conf=["daily"],
    )
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_obj]

    result = country_climate_measure_service.get_by_country(1, db=mock_db)

    assert len(result) == 1
    assert result[0].country_id == 1
    assert result[0].spatial_climate_conf[0].temporality == "daily"
    assert result[0].location_climate_conf == ["daily"]


def test_get_by_country_and_measure(country_climate_measure_service, mock_db):
    """Test para obtener configuración específica país + medida"""
    mock_obj = MngCountryClimateMeasure(
        id=1,
        country_id=1,
        measure_id=3,
        spatial_forecast=False,
        spatial_climate=False,
        location_forecast=False,
        location_climate=False,
        spatial_climate_conf=None,
        location_climate_conf=None,
    )
    mock_db.query.return_value.filter.return_value.first.return_value = mock_obj

    result = country_climate_measure_service.get_by_country_and_measure(1, 3, db=mock_db)

    assert result is not None
    assert result.measure_id == 3
    assert result.spatial_climate_conf is None
    assert result.location_climate_conf is None


def test_update_country_climate_measure(country_climate_measure_service, mock_db):
    """Test para actualizar una configuración"""
    existing = MngCountryClimateMeasure(
        id=1,
        country_id=1,
        measure_id=3,
        spatial_forecast=False,
        spatial_climate=True,
        location_forecast=False,
        location_climate=True,
        spatial_climate_conf=[{"temporality": "daily", "store": "s1", "workspace": "w1"}],
        location_climate_conf=["daily"],
    )
    mock_db.query.return_value.get.return_value = existing

    update_data = CountryClimateMeasureUpdate(
        location_climate_conf=["daily", "monthly"]
    )

    result = country_climate_measure_service.update(1, update_data, db=mock_db)

    assert result is not None
    assert result.location_climate_conf == ["daily", "monthly"]


# ---- Tests de validación ----
def test_validate_create_missing_spatial_conf_when_flag_true(country_climate_measure_service, mock_db):
    """spatial_climate=True sin spatial_climate_conf debe fallar"""
    payload = _create_payload(spatial_climate=True, spatial_climate_conf=None)
    measure_data = CountryClimateMeasureCreate(**payload)

    mock_db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(ValueError) as excinfo:
        country_climate_measure_service.create(measure_data, db=mock_db)

    assert "spatial_climate_conf is required" in str(excinfo.value)


def test_validate_create_missing_location_conf_when_flag_true(country_climate_measure_service, mock_db):
    """location_climate=True sin location_climate_conf debe fallar"""
    payload = _create_payload(location_climate=True, location_climate_conf=None)
    measure_data = CountryClimateMeasureCreate(**payload)

    mock_db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(ValueError) as excinfo:
        country_climate_measure_service.create(measure_data, db=mock_db)

    assert "location_climate_conf is required" in str(excinfo.value)


def test_validate_create_no_conf_when_flags_false(country_climate_measure_service, mock_db):
    """Flags en False sin config no debe fallar"""
    payload = _create_payload(
        spatial_climate=False,
        spatial_climate_conf=None,
        location_climate=False,
        location_climate_conf=None,
    )
    measure_data = CountryClimateMeasureCreate(**payload)

    mock_db.query.return_value.filter.return_value.first.return_value = None
    mock_db.add.return_value = None
    mock_db.commit.return_value = None

    def mock_refresh(obj):
        obj.id = 1

    mock_db.refresh.side_effect = mock_refresh

    result = country_climate_measure_service.create(measure_data, db=mock_db)

    assert result.id == 1
    assert result.spatial_climate_conf is None
    assert result.location_climate_conf is None


def test_validate_create_duplicate(country_climate_measure_service, mock_db):
    """Validar duplicado country_id + measure_id"""
    payload = _create_payload()
    measure_data = CountryClimateMeasureCreate(**payload)

    mock_db.query.return_value.filter.return_value.first.return_value = MngCountryClimateMeasure(id=99, country_id=1, measure_id=3)

    with pytest.raises(ValueError) as excinfo:
        country_climate_measure_service.create(measure_data, db=mock_db)

    assert "already exists" in str(excinfo.value)


# ---- Tests de schema ----
def test_country_climate_measure_schema_validation():
    """Test para validar el esquema CountryClimateMeasureCreate"""
    valid_data = _create_payload()
    measure = CountryClimateMeasureCreate(**valid_data)
    assert measure.spatial_climate_conf[0].temporality == "daily"
    assert measure.location_climate_conf == ["daily", "monthly", "climatology"]

    # Temporality inválido debe fallar
    with pytest.raises(ValueError):
        CountryClimateMeasureCreate(**_create_payload(location_climate_conf=["invalid"]))

    # spatial_climate_conf con temporality inválido debe fallar
    with pytest.raises(ValueError):
        CountryClimateMeasureCreate(
            **_create_payload(spatial_climate_conf=[{"temporality": "invalid", "store": "s1", "workspace": "w1"}])
        )


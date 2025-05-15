import pytest
from unittest.mock import create_autospec, patch, MagicMock
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List
from pydantic import ValidationError

# Importaciones de tu proyecto
from aclimate_v3_orm.models import MngCountry
from aclimate_v3_orm.schemas import CountryCreate, CountryRead, CountryUpdate
from aclimate_v3_orm.services.mng_country_service import MngCountryService
from aclimate_v3_orm.validations import MngCountryValidator

@pytest.fixture
def mock_db():
    """Fixture para una sesión de base de datos mockeada"""
    return create_autospec(Session, instance=True)

@pytest.fixture
def country_service():
    """Fixture para el servicio de países"""
    return MngCountryService()

def test_get_by_name(country_service, mock_db):
    """Test para obtener países por nombre"""
    # Configurar datos de prueba
    mock_countries = [
        MngCountry(id=1, name="Test1", iso2="TC", enable=True)
    ]
    
    # Configurar el mock
    mock_db.query.return_value.filter.return_value.all.return_value = mock_countries
    
    # Ejecutar el método
    result = country_service.get_by_name("Test1", db=mock_db)
    # Verificar resultados
    assert len(result) == 1
    assert all(isinstance(item, CountryRead) for item in result)
    assert all(item.name == "Test1" for item in result)
    
    # Verificar llamadas a la base de datos
    mock_db.query.assert_called_once_with(MngCountry)
    filter_call = mock_db.query.return_value.filter
    assert filter_call.call_count == 1  # Para name y enable

def test_get_all_enable(country_service, mock_db):
    """Test para obtener todos los países habilitados"""
    # Configurar datos de prueba
    mock_countries = [
        MngCountry(id=1, name="Country 1", iso2="CA", enable=True),
        MngCountry(id=2, name="Country 2", iso2="CC", enable=True)
    ]
    
    # Configurar el mock
    mock_db.query.return_value.filter.return_value.all.return_value = mock_countries
    
    # Ejecutar el método
    result = country_service.get_all_enable(db=mock_db)
    # Verificar resultados
    assert len(result) == 2
    assert all(isinstance(item, CountryRead) for item in result)
    assert all(item.enable for item in result)
    
    # Verificar llamadas a la base de datos
    mock_db.query.assert_called_once_with(MngCountry)
    mock_db.query.return_value.filter.assert_called_once()

def test_create_country_valid(country_service, mock_db):
    """Test para crear un país válido"""
    # Configurar datos de prueba
    country_data = CountryCreate(name="New Country", iso2="NC")
    mock_new_country = MngCountry(
        id=1, 
        name=country_data.name, 
        iso2=country_data.iso2, 
        enable=True,
        register=datetime.now(timezone.utc),
        updated=datetime.now(timezone.utc)
    )
    
    # Configurar el mock para que refresh() actualice el objeto
    def mock_refresh(obj):
        # Simular el comportamiento de refresh actualizando el objeto
        if obj.id is None:
            obj.id = 1
    
    # Configurar los mocks
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.side_effect = mock_refresh
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    # Mockear la validación (ya que es interna)
    with patch.object(MngCountryValidator, 'create_validate') as mock_validate:
        # Ejecutar el método
        result = country_service.create(obj_in=country_data, db=mock_db)
    
    # Verificar resultados
    assert isinstance(result, CountryRead)
    assert result.id == 1  # Asegurarse que tiene ID
    assert result.name == country_data.name
    assert result.iso2 == country_data.iso2
    
    # Verificar llamadas
    mock_validate.assert_called_once_with(mock_db, country_data)
    mock_db.add.assert_called_once()
    
    # Verificar commit - ahora permitimos 1 o 2 llamadas
    assert mock_db.commit.call_count >= 1  # Al menos un commit
    assert mock_db.commit.call_count <= 2  # Máximo dos commits
    
    mock_db.refresh.assert_called_once()

def test_update_country(country_service, mock_db):
    """Test para actualizar un país"""
    # Configurar datos de prueba
    country_id = 1
    update_data = CountryUpdate(name="Updated Country", iso2="UC")
    existing_country = MngCountry(
        id=country_id,
        name="Old Country",
        iso2="OC",
        enable=True
    )
    
    # Configurar el mock
    mock_db.query.return_value.filter.return_value.first.return_value = existing_country
    
    # Ejecutar el método
    result = country_service.update(country_id, update_data, db=mock_db)
    
    # Verificar resultados
    assert isinstance(result, CountryRead)
    assert result.id == country_id
    assert result.name == update_data.name
    assert result.iso2 == update_data.iso2
    
    # Verificar llamadas
    mock_db.query.assert_called_once_with(MngCountry)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

def test_delete_country(country_service, mock_db):
    """Test para eliminar (deshabilitar) un país"""
    # Configurar datos de prueba
    country_id = 1
    existing_country = MngCountry(
        id=country_id,
        name="Country to Delete",
        iso2="CD",
        enable=True
    )
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_country
    
    # Ejecutar el método
    result = country_service.delete(country_id, db=mock_db)
    
    # Verificar resultados (ahora esperando un booleano)
    assert isinstance(result, bool)
    assert result is True  # Debería devolver True si la eliminación fue exitosa
    print(existing_country.enable)
    # Verificar que el país fue deshabilitado
    assert existing_country.enable is False
    
    # Verificar llamadas a la base de datos
    mock_db.commit.assert_called_once()

def test_get_by_name_empty(country_service, mock_db):
    """Test para cuando no hay países con el nombre buscado"""
    # Configurar el mock para devolver lista vacía
    mock_db.query.return_value.filter.return_value.all.return_value = []
    
    # Ejecutar el método
    result = country_service.get_by_name("Non-existent Country", db=mock_db)
    
    # Verificar resultados
    assert isinstance(result, list)
    assert len(result) == 0

def test_create_country_duplicate_iso2(country_service, mock_db):
    """Test para validar duplicados al crear país"""
    # Configurar datos de prueba
    country_data = CountryCreate(name="New Country", iso2="NC")
    
    # Configurar el mock para simular que ya existe un país con ese ISO2
    mock_db.query.return_value.filter.return_value.first.return_value = MngCountry(id=99, name="Existing", iso2="NC")
    
    # Mockear la validación para que lance excepción
    with patch.object(MngCountryValidator, 'create_validate', side_effect=ValueError("ISO2 already exists")):
        with pytest.raises(ValueError) as excinfo:
            country_service.create(country_data, db=mock_db)
        
        assert "ISO2 already exists" in str(excinfo.value)

def test_validate_iso2_in_update():
    """Test para validar formato ISO2 en actualización"""
    # Debe fallar al crear el objeto, no al llamar a update()
    with pytest.raises(ValidationError) as excinfo:
        invalid_update = CountryUpdate(iso2="n2")  # Esto ya lanza ValidationError
        # country_service.update nunca se ejecuta
        
    # Verificar que el mensaje de error sea el correcto
    assert "ISO2 code must be 2 uppercase letters" in str(excinfo.value)

def test_partial_update(country_service, mock_db):
    """Test para actualización parcial de un país"""
    # Configurar datos de prueba
    country_id = 1
    existing_country = MngCountry(
        id=country_id,
        name="Existing Country",
        iso2="EC",
        enable=True
    )
    update_data = CountryUpdate(name="Updated Name")  # Solo actualizar nombre
    
    # Configurar el mock
    mock_db.query.return_value.get.return_value = existing_country
    
    # Ejecutar el método
    result = country_service.update(country_id, update_data, db=mock_db)
    
    # Verificar resultados
    assert result.name == update_data.name
    assert result.iso2 == existing_country.iso2  # No debería cambiar
    assert result.enable == existing_country.enable  # No debería cambiar
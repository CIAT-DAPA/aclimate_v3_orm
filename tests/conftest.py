import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from aclimate_v3_orm.database.base import Base  # Adjust this import based on your actual model location

@pytest.fixture(scope="session")
def engine():
    return create_engine("sqlite:///:memory:")

@pytest.fixture(scope="function")
def db_session(engine):
    # Create all tables
    Base.metadata.create_all(engine)
    
    # Create a new session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    
    # Clean up
    session.close()
    Base.metadata.drop_all(engine)

@pytest.fixture
def sample_countries(db_session):
    from aclimate_v3_orm.models import MngCountry  # Adjust import as needed
    
    # Create sample data
    countries = [
        MngCountry(name="Colombia", code="COL", enable=True),
        MngCountry(name="Ecuador", code="ECU", enable=True),
        MngCountry(name="Venezuela", code="VEN", enable=False),
    ]
    
    db_session.add_all(countries)
    db_session.commit()
    
    return countries
from database import engine
from database.base import Base
from models.administrative import Country, Admin1, Admin2, Location
from models.catalog import ClimateMeasure
from models.climate import ClimateHistoricalClimatology, ClimateHistoricalDaily, ClimateHistoricalMonthly

from factory.administrative import Admin1Factory, Admin2Factory, CountryFactory, LocationFactory
from factory.catalog import ClimateMeasureFactory
from factory.climate import ClimateHistoricalClimatologyFactory, ClimateHistoricalDailyFactory, ClimateHistoricalMonthlyFactory

# Crea todas las tablas
Base.metadata.create_all(bind=engine)

print("Tablas creadas correctamente.")

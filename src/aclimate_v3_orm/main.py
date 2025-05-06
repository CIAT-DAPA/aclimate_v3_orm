from database import engine
from database.base import Base
from models.administrative import Country, Admin1, Admin2, Location
from models.catalog import ClimateMeasure
from models.climate import ClimateHistoricalClimatology, ClimateHistoricalDaily, ClimateHistoricalMonthly

from services.administrative import Admin1Service, Admin2Service, CountryService, LocationService
from services.catalog import ClimateMeasureService
from services.climate import ClimateHistoricalClimatologyService, ClimateHistoricalDailyService, ClimateHistoricalMonthlyService

# Crea todas las tablas
Base.metadata.create_all(bind=engine)

print("Tablas creadas correctamente.")

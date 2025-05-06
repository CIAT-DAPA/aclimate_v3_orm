from database import engine
from database.base import Base
from models.administrative.admin1 import Admin1
from models.administrative.location import Location
from models.administrative.country import Country
from models.administrative.admin2 import Admin2
from models.catalog.climate_measure import ClimateMeasure
from models.climate.historical_climatology import ClimateHistoricalClimatology
from models.climate.historical_daily import ClimateHistoricalDaily
from models.climate.historical_monthly import ClimateHistoricalMonthly

# Crea todas las tablas
Base.metadata.create_all(bind=engine)

print("Tablas creadas correctamente.")

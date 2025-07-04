from sqlalchemy.orm import Session
from ..models import ForecastAnalogue, Forecast, MngLocation

class ForecastAnalogueValidator:

    @staticmethod
    def validate_foreign_keys(db: Session, forecast_id: int, location_id: int):
        if not db.query(Forecast).filter(Forecast.id == forecast_id).first():
            raise ValueError(f"Forecast con id '{forecast_id}' no existe.")
        if not db.query(MngLocation).filter(MngLocation.id == location_id).first():
            raise ValueError(f"Location con id '{location_id}' no existe.")

    @staticmethod
    def validate_unique(db: Session, forecast_id: int, location_id: int, year: int, rank: int):
        exists = db.query(ForecastAnalogue).filter(
            ForecastAnalogue.forecast_id == forecast_id,
            ForecastAnalogue.location_id == location_id,
            ForecastAnalogue.year == year,
            ForecastAnalogue.rank == rank
        ).first()
        if exists:
            raise ValueError("Ya existe un registro con estos valores clave.")

    @staticmethod
    def create_validate(db: Session, obj_in):
        ForecastAnalogueValidator.validate_foreign_keys(db, obj_in.forecast_id, obj_in.location_id)
        ForecastAnalogueValidator.validate_unique(db, obj_in.forecast_id, obj_in.location_id, obj_in.year, obj_in.rank)
from sqlalchemy.orm import Session
from ..models import (
    HistoricalAgroclimaticIndicator,
    MngIndicator,
    MngLocation,
    MngPhenologicalStage
)

class HistoricalAgroclimaticIndicatorValidator:

    @staticmethod
    def validate_foreign_keys(db: Session, indicator_id: int, location_id: int, phenological_id: int):
        if not db.query(MngIndicator).filter(MngIndicator.id == indicator_id).first():
            raise ValueError(f"Indicator con id '{indicator_id}' no existe.")
        if not db.query(MngLocation).filter(MngLocation.id == location_id).first():
            raise ValueError(f"Location con id '{location_id}' no existe.")
        if not db.query(MngPhenologicalStage).filter(MngPhenologicalStage.id == phenological_id).first():
            raise ValueError(f"PhenologicalStage con id '{phenological_id}' no existe.")

    @staticmethod
    def validate_dates(start_date, end_date):
        if start_date > end_date:
            raise ValueError("start_date no puede ser después de end_date.")

    @staticmethod
    def create_validate(db: Session, obj_in):
        HistoricalAgroclimaticIndicatorValidator.validate_foreign_keys(
            db, obj_in.indicator_id, obj_in.location_id, obj_in.phenological_id
        )
        HistoricalAgroclimaticIndicatorValidator.validate_dates(obj_in.start_date, obj_in.end_date)
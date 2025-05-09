from sqlalchemy import Date
from sqlalchemy.orm import Session
from models import ClimateHistoricalDaily
from aclimate_v3_orm.models import MngLocation
from models import MngClimateMeasure
from datetime import datetime

class ClimateHistoricalDailyValidator:

    @staticmethod
    def validate_date(date: Date):
        """ Validate if the date is not in the future """
        if date > datetime.today().date():
            raise ValueError("The 'date' field cannot be in the future.")

    @staticmethod
    def validate_value(value: float):
        """ Validate if the value is not None and is a valid numeric value """
        if not isinstance(value, (int, float)):  # Ensure the value is a number
            raise ValueError("The 'value' field must be a numeric value.")

    @staticmethod
    def validate_location_exists(db: Session, location_id: int):
        """ Validate if the location exists in the database """
        existing_location = db.query(MngLocation).filter(MngLocation.id == location_id).first()
        if not existing_location:
            raise ValueError(f"Location with ID {location_id} does not exist.")

    @staticmethod
    def validate_measure_exists(db: Session, measure_id: int):
        """ Validate if the measure exists in the database """
        existing_measure = db.query(MngClimateMeasure).filter(MngClimateMeasure.id == measure_id).first()
        if not existing_measure:
            raise ValueError(f"Climate measure with ID {measure_id} does not exist.")

    @staticmethod
    def validate_unique_data(db: Session, location_id: int, measure_id: int, date: Date):
        """ Validate if data already exists for the given location, measure, and date """
        existing = db.query(ClimateHistoricalDaily).filter(
            ClimateHistoricalDaily.location_id == location_id,
            ClimateHistoricalDaily.measure_id == measure_id,
            ClimateHistoricalDaily.date == date
        ).first()
        if existing:
            raise ValueError(f"Data for location {location_id}, measure {measure_id}, and date {date} already exists.")

    @staticmethod
    def create_validate(db: Session, obj_in: dict):
        """ Validate the fields before creating a new record """
        # Apply validations that SQLAlchemy cannot enforce
        ClimateHistoricalDailyValidator.validate_date(obj_in["date"])
        ClimateHistoricalDailyValidator.validate_value(obj_in["value"])
        ClimateHistoricalDailyValidator.validate_location_exists(db, obj_in["location_id"])
        ClimateHistoricalDailyValidator.validate_measure_exists(db, obj_in["measure_id"])
        ClimateHistoricalDailyValidator.validate_unique_data(db, obj_in["location_id"], obj_in["measure_id"], obj_in["date"])

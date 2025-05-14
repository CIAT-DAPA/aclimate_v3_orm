from sqlalchemy.orm import Session
from ..models import ClimateHistoricalClimatology, MngLocation, MngClimateMeasure

class ClimateHistoricalClimatologyValidator:

    @staticmethod
    def validate_month(month: int):
        """ Validate if the month is between 1 and 12 """
        if month < 1 or month > 12:
            raise ValueError("The 'month' field must be between 1 and 12.")

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
    def validate_unique_data(db: Session, location_id: int, measure_id: int, month: int):
        """ Validate if data already exists for the given location, measure, and month """
        existing = db.query(ClimateHistoricalClimatology).filter(
            ClimateHistoricalClimatology.location_id == location_id,
            ClimateHistoricalClimatology.measure_id == measure_id,
            ClimateHistoricalClimatology.month == month
        ).first()
        if existing:
            raise ValueError(f"Data for location {location_id}, measure {measure_id}, and month {month} already exists.")

    @staticmethod
    def create_validate(db: Session, obj_in: dict):
        """ Validate the fields before creating a new record """
        # Apply validations that SQLAlchemy cannot enforce
        ClimateHistoricalClimatologyValidator.validate_month(obj_in.month)
        ClimateHistoricalClimatologyValidator.validate_value(obj_in.value)
        ClimateHistoricalClimatologyValidator.validate_location_exists(db, obj_in.location_id)
        ClimateHistoricalClimatologyValidator.validate_measure_exists(db, obj_in.measure_id)
        ClimateHistoricalClimatologyValidator.validate_unique_data(db, obj_in.location_id, obj_in.measure_id, obj_in.month)

from sqlalchemy.orm import Session
from ..models import ClimateHistoricalIndicator, MngLocation, MngIndicator
from typing import Optional
from datetime import date
from ..enums import Period

class ClimateHistoricalIndicatorValidator:
    @staticmethod
    def validate_period(period: str):
        """Validate if the period is a valid Period enum value"""
        try:
            Period(period)  # This will raise ValueError if invalid
        except ValueError:
            valid_periods = [e.value for e in Period]
            raise ValueError(
                f"Invalid period '{period}'. Must be one of: {', '.join(valid_periods)}"
            )

    @staticmethod
    def validate_value(value: float):
        """Validate if the value is a valid number"""
        if not isinstance(value, (int, float)):
            raise ValueError("Value must be a numeric value")

    @staticmethod
    def validate_dates(start_date: date, end_date: Optional[date] = None):
        """Validate date consistency"""
        if end_date and start_date > end_date:
            raise ValueError("Start date cannot be after end date")

    @staticmethod
    def validate_indicator_exists(db: Session, indicator_id: int):
        """Validate if the indicator exists"""
        if not db.query(MngIndicator).filter(MngIndicator.id == indicator_id).first():
            raise ValueError(f"No indicator found with ID {indicator_id}")

    @staticmethod
    def validate_location_exists(db: Session, location_id: int):
        """Validate if the location exists"""
        if not db.query(MngLocation).filter(MngLocation.id == location_id).first():
            raise ValueError(f"No location found with ID {location_id}")

    @staticmethod
    def validate_unique_entry(db: Session, indicator_id: int, location_id: int, 
                            start_date: date, period: str):
        """Validate if data already exists for the given parameters"""
        # Convert string period to enum before querying
        period_enum = Period(period)
        existing = db.query(ClimateHistoricalIndicator).filter(
            ClimateHistoricalIndicator.indicator_id == indicator_id,
            ClimateHistoricalIndicator.location_id == location_id,
            ClimateHistoricalIndicator.start_date == start_date,
            ClimateHistoricalIndicator.period == period_enum  # Use enum value here
        ).first()
        if existing:
            raise ValueError("Historical data for these parameters already exists")

    @staticmethod
    def create_validate(db: Session, obj_in: dict):
        """Comprehensive validation for creating new records"""
        # Validate period first
        ClimateHistoricalIndicatorValidator.validate_period(obj_in.period)
        
        # Then validate other fields
        ClimateHistoricalIndicatorValidator.validate_value(obj_in.value)
        ClimateHistoricalIndicatorValidator.validate_dates(
            obj_in.start_date, 
            obj_in.end_date
        )
        ClimateHistoricalIndicatorValidator.validate_indicator_exists(db, obj_in.indicator_id)
        ClimateHistoricalIndicatorValidator.validate_location_exists(db, obj_in.location_id)
        
        # Finally validate uniqueness
        ClimateHistoricalIndicatorValidator.validate_unique_entry(
            db, 
            obj_in.indicator_id, 
            obj_in.location_id,
            obj_in.start_date,
            obj_in.period
        )
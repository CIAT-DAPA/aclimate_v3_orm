from sqlalchemy.orm import Session
from ..models import MngIndicator

class IndicatorValidator:
    @staticmethod
    def validate_name(db: Session, name: str):
        """Validate if an indicator name is unique in the database"""
        existing = db.query(MngIndicator).filter(MngIndicator.name == name).first()
        if existing:
            raise ValueError(f"Indicator with name '{name}' already exists")

    @staticmethod
    def validate_short_name(db: Session, short_name: str):
        """Validate if an indicator short name is unique in the database"""
        existing = db.query(MngIndicator).filter(MngIndicator.short_name == short_name).first()
        if existing:
            raise ValueError(f"Indicator with short name '{short_name}' already exists")
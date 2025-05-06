from sqlalchemy.orm import Session
from models.catalog import ClimateMeasure

class ClimateMeasureNameValidator:
    @staticmethod
    def validate(db: Session, name: str):
        """
        Validate if a ClimateMeasure name is unique in the database.
        """
        existing = db.query(ClimateMeasure).filter(ClimateMeasure.name == name).first()
        if existing:
            raise ValueError(f"The climate measure with the name '{name}' already exists.")

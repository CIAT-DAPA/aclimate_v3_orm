from sqlalchemy.orm import Session
from aclimate_v3_orm.models import MngClimateMeasure

class MngClimateMeasureNameValidator:
    @staticmethod
    def validate(db: Session, name: str):
        """
        Validate if a ClimateMeasure name is unique in the database.
        """
        existing = db.query(MngClimateMeasure).filter(MngClimateMeasure.name == name).first()
        if existing:
            raise ValueError(f"The climate measure with the name '{name}' already exists.")

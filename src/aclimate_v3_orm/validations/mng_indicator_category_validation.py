from sqlalchemy.orm import Session
from ..models import MngIndicatorCategory

class MngIndicatorCategoryValidator:
    @staticmethod
    def validate_name(db: Session, name: str):
        """Validate if a category name is unique in the database"""
        existing = db.query(MngIndicatorCategory).filter(MngIndicatorCategory.name == name).first()
        if existing:
            raise ValueError(f"Indicator category with name '{name}' already exists")

    @staticmethod
    def create_validate(db: Session, obj_in):
        MngIndicatorCategoryValidator.validate_name(db, obj_in.name)

    @staticmethod
    def update_validate(db: Session, obj_in: dict, category_id: int):
        name = obj_in.get('name')
        if name:
            existing = db.query(MngIndicatorCategory).filter(
                MngIndicatorCategory.name == name,
                MngIndicatorCategory.id != category_id
            ).first()
            if existing:
                raise ValueError(f"Indicator category with name '{name}' already exists")

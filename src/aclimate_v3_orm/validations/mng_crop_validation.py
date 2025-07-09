from sqlalchemy.orm import Session
from ..models import MngCrop

class MngCropValidator:

    @staticmethod
    def validate_name(name: str):
        if not name or not name.strip():
            raise ValueError("El campo 'name' es obligatorio.")

    @staticmethod
    def validate_unique_name(db: Session, name: str):
        exists = db.query(MngCrop).filter(MngCrop.name == name).first()
        if exists:
            raise ValueError(f"Ya existe un cultivo con el nombre '{name}'.")

    @staticmethod
    def create_validate(db: Session, obj_in):
        MngCropValidator.validate_name(obj_in.name)
        MngCropValidator.validate_unique_name(db, obj_in.name)
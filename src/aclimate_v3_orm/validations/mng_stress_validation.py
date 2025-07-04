from sqlalchemy.orm import Session
from ..models import MngStress

class MngStressValidator:

    @staticmethod
    def validate_name(name: str):
        if not name or not name.strip():
            raise ValueError("El campo 'name' es obligatorio.")

    @staticmethod
    def validate_short_name(short_name: str):
        if not short_name or not short_name.strip():
            raise ValueError("El campo 'short_name' es obligatorio.")

    @staticmethod
    def validate_unique_name(db: Session, name: str):
        exists = db.query(MngStress).filter(MngStress.name == name).first()
        if exists:
            raise ValueError(f"Ya existe un stress con el nombre '{name}'.")

    @staticmethod
    def create_validate(db: Session, obj_in):
        MngStressValidator.validate_name(obj_in.name)
        MngStressValidator.validate_short_name(obj_in.short_name)
        MngStressValidator.validate_unique_name(db, obj_in.name)
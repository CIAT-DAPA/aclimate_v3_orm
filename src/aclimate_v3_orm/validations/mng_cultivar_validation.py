from sqlalchemy.orm import Session
from ..models import MngCultivar, MngCountry, MngCrop

class MngCultivarValidator:

    @staticmethod
    def validate_name(name: str):
        if not name or not name.strip():
            raise ValueError("El campo 'name' es obligatorio.")

    @staticmethod
    def validate_country_id(db: Session, country_id: int):
        if not db.query(MngCountry).filter(MngCountry.id == country_id).first():
            raise ValueError(f"Country con id '{country_id}' no existe.")

    @staticmethod
    def validate_crop_id(db: Session, crop_id: int):
        if not db.query(MngCrop).filter(MngCrop.id == crop_id).first():
            raise ValueError(f"Crop con id '{crop_id}' no existe.")

    @staticmethod
    def validate_unique_name(db: Session, name: str, crop_id: int, country_id: int):
        exists = db.query(MngCultivar).filter(
            MngCultivar.name == name,
            MngCultivar.crop_id == crop_id,
            MngCultivar.country_id == country_id
        ).first()
        if exists:
            raise ValueError(f"Ya existe un cultivar con el nombre '{name}' para este cultivo y país.")

    @staticmethod
    def create_validate(db: Session, obj_in):
        MngCultivarValidator.validate_name(obj_in.name)
        MngCultivarValidator.validate_country_id(db, obj_in.country_id)
        MngCultivarValidator.validate_crop_id(db, obj_in.crop_id)
        MngCultivarValidator.validate_unique_name(db, obj_in.name, obj_in.crop_id, obj_in.country_id)
from sqlalchemy.orm import Session
from ..models import MngPhenologicalStage, MngCrop

class MngPhenologicalStageValidator:

    @staticmethod
    def validate_name(name: str):
        if not name or not name.strip():
            raise ValueError("El campo 'name' es obligatorio.")

    @staticmethod
    def validate_crop_id(db: Session, crop_id: int):
        if not db.query(MngCrop).filter(MngCrop.id == crop_id).first():
            raise ValueError(f"Crop con id '{crop_id}' no existe.")

    @staticmethod
    def validate_unique_name(db: Session, name: str, crop_id: int):
        exists = db.query(MngPhenologicalStage).filter(
            MngPhenologicalStage.name == name,
            MngPhenologicalStage.crop_id == crop_id
        ).first()
        if exists:
            raise ValueError(f"Ya existe una etapa fenológica con el nombre '{name}' para este cultivo.")

    @staticmethod
    def create_validate(db: Session, obj_in):
        MngPhenologicalStageValidator.validate_name(obj_in.name)
        MngPhenologicalStageValidator.validate_crop_id(db, obj_in.crop_id)
        MngPhenologicalStageValidator.validate_unique_name(db, obj_in.name, obj_in.crop_id)
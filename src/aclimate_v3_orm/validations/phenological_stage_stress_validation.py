from sqlalchemy.orm import Session
from ..models import PhenologicalStageStress, MngStress, MngPhenologicalStage

class PhenologicalStageStressValidator:

    @staticmethod
    def validate_foreign_keys(db: Session, stress_id: int, phenological_stage_id: int):
        if not db.query(MngStress).filter(MngStress.id == stress_id).first():
            raise ValueError(f"Stress con id '{stress_id}' no existe.")
        if not db.query(MngPhenologicalStage).filter(MngPhenologicalStage.id == phenological_stage_id).first():
            raise ValueError(f"MngPhenologicalStage con id '{phenological_stage_id}' no existe.")

    @staticmethod
    def validate_min_max(min_value: float, max_value: float):
        if min_value > max_value:
            raise ValueError("El valor mínimo no puede ser mayor que el máximo.")

    @staticmethod
    def create_validate(db: Session, obj_in):
        PhenologicalStageStressValidator.validate_foreign_keys(db, obj_in.stress_id, obj_in.phenological_stage_id)
        PhenologicalStageStressValidator.validate_min_max(obj_in.min, obj_in.max)
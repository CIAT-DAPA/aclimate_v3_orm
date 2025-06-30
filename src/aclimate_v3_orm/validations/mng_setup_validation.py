# mng_setup_validation.py
from sqlalchemy.orm import Session
from src.aclimate_v3_orm.schemas.mng_setup_schema import MngSetupCreate
from ..models import MngCultivar, MngSoil, Season

class MngSetupValidator:
    @staticmethod
    def validate_frequency(frequency: int):
        if frequency <= 0:
            raise ValueError("Frequency must be a positive integer")
    
    @staticmethod
    def validate_foreign_keys(db: Session, cultivar_id: int, soil_id: int, season_id: int):
        # Validate cultivar exists
        if not db.query(MngCultivar).filter(MngCultivar.id == cultivar_id).first():
            raise ValueError("Invalid cultivar ID")
        
        # Validate soil exists
        if not db.query(MngSoil).filter(MngSoil.id == soil_id).first():
            raise ValueError("Invalid soil ID")
        
        # Validate season exists
        if not db.query(Season).filter(Season.id == season_id).first():
            raise ValueError("Invalid season ID")
    
    @staticmethod
    def create_validate(db: Session, obj_in: MngSetupCreate):
        MngSetupValidator.validate_frequency(obj_in.frequency)
        MngSetupValidator.validate_foreign_keys(db, obj_in.cultivar_id, obj_in.soil_id, obj_in.season_id)
from sqlalchemy.orm import Session
from ..models import Season, MngLocation, MngCrop

class MngSeasonValidator:

    @staticmethod
    def validate_location_id(db: Session, location_id: int):
        if not db.query(MngLocation).filter(MngLocation.id == location_id).first():
            raise ValueError(f"Location con id '{location_id}' no existe.")

    @staticmethod
    def validate_crop_id(db: Session, crop_id: int):
        if not db.query(MngCrop).filter(MngCrop.id == crop_id).first():
            raise ValueError(f"Crop con id '{crop_id}' no existe.")

    @staticmethod
    def validate_dates(planting_start, planting_end, season_start, season_end):
        if planting_start > planting_end:
            raise ValueError("planting_start no puede ser después de planting_end.")
        if season_start > season_end:
            raise ValueError("season_start no puede ser después de season_end.")

    @staticmethod
    def create_validate(db: Session, obj_in):
        MngSeasonValidator.validate_location_id(db, obj_in.location_id)
        MngSeasonValidator.validate_crop_id(db, obj_in.crop_id)
        MngSeasonValidator.validate_dates(obj_in.planting_start, obj_in.planting_end, obj_in.season_start, obj_in.season_end)
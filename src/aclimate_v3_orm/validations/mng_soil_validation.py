from sqlalchemy.orm import Session
from ..models import MngSoil, MngCountry

class MngSoilValidator:

    @staticmethod
    def validate_name(name: str):
        """ Validate if the name field is not empty or null """
        if not name:
            raise ValueError("The 'name' field is required.")

    @staticmethod
    def validate_country_id(db: Session, country_id: int):
        """ Validate if the country_id corresponds to an existing country """
        country = db.query(MngCountry).filter(MngCountry.id == country_id).first()
        if not country:
            raise ValueError(f"Country with id '{country_id}' does not exist.")

    @staticmethod
    def validate_unique_name(db: Session, name: str, country_id: int):
        """ Validate if the name is unique within the same country """
        existing_soil = db.query(MngSoil).filter(MngSoil.name == name, MngSoil.country_id == country_id).first()
        if existing_soil:
            raise ValueError(f"A soil entry with the name '{name}' already exists in this country.")

    @staticmethod
    def create_validate(db: Session, obj_in):
        """ Validate fields before creating a new Soil record """
        MngSoilValidator.validate_name(obj_in.name)
        MngSoilValidator.validate_country_id(db, obj_in.country_id)
        MngSoilValidator.validate_unique_name(db, obj_in.name, obj_in.country_id)
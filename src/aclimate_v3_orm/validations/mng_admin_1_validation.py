from sqlalchemy.orm import Session
from aclimate_v3_orm.models import MngAdmin1, MngCountry

class MngAdmin1Validator:

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
        existing_admin1 = db.query(MngAdmin1).filter(MngAdmin1.name == name, MngAdmin1.country_id == country_id).first()
        if existing_admin1:
            raise ValueError(f"An Admin1 with the name '{name}' already exists in this country.")

    @staticmethod
    def create_validate(db: Session, obj_in: dict):
        """ Validate fields before creating a new Admin1 record """
        # Validate the fields for the new Admin1 entry
        MngAdmin1Validator.validate_name(obj_in["name"])
        MngAdmin1Validator.validate_country_id(db, obj_in["country_id"])
        MngAdmin1Validator.validate_unique_name(db, obj_in["name"], obj_in["country_id"])

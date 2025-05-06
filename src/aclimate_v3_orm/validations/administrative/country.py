from sqlalchemy.orm import Session
from models.administrative import Country

class CountryValidator:

    @staticmethod
    def validate_name(name: str):
        """ Validate if the name is not empty or null """
        if not name:
            raise ValueError("The 'name' field is required.")

    @staticmethod
    def validate_iso2(iso2: str):
        """ Validate if the iso2 field is a valid two-letter country code """
        if not iso2 or len(iso2) != 2:
            raise ValueError("The 'iso2' field must be a valid two-letter ISO country code.")

    @staticmethod
    def validate_unique_iso2(db: Session, iso2: str):
        """ Validate if the iso2 code is unique """
        existing_country = db.query(Country).filter(Country.iso2 == iso2).first()
        if existing_country:
            raise ValueError(f"The country with iso2 code '{iso2}' already exists.")

    @staticmethod
    def create_validate(db: Session, obj_in: dict):
        """ Validate the fields before creating a new record """
        # Apply validations that SQLAlchemy cannot enforce
        CountryValidator.validate_name(obj_in["name"])
        CountryValidator.validate_iso2(obj_in["iso2"])
        CountryValidator.validate_unique_iso2(db, obj_in["iso2"])

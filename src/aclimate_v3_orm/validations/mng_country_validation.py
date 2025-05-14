from sqlalchemy.orm import Session
from aclimate_v3_orm.models import MngCountry
from aclimate_v3_orm.schemas import CountryCreate

class MngCountryValidator:

    @staticmethod
    def validate_name(name: str):
        if not name:
            raise ValueError("The 'name' field is required.")

    @staticmethod
    def validate_iso2(iso2: str):
        if not iso2 or len(iso2) != 2:
            raise ValueError("The 'iso2' field must be a valid two-letter ISO country code.")

    @staticmethod
    def validate_unique_iso2(db: Session, iso2: str, exclude_id: int = None):
        query = db.query(MngCountry).filter(MngCountry.iso2 == iso2)
        if exclude_id:
            query = query.filter(MngCountry.id != exclude_id)
        if query.first():
            raise ValueError(f"The country with iso2 code '{iso2}' already exists.")

    @staticmethod
    def create_validate(db: Session, obj_in: CountryCreate):
        MngCountryValidator.validate_name(obj_in.name)
        MngCountryValidator.validate_iso2(obj_in.iso2)
        MngCountryValidator.validate_unique_iso2(db, obj_in.iso2)

    @staticmethod
    def update_validate(db: Session, obj_in: dict, country_id: int):
        if 'name' in obj_in:
            MngCountryValidator.validate_name(obj_in['name'])
        if 'iso2' in obj_in:
            MngCountryValidator.validate_iso2(obj_in['iso2'])
            MngCountryValidator.validate_unique_iso2(db, obj_in['iso2'], exclude_id=country_id)
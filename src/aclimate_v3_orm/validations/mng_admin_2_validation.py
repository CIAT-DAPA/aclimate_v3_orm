from sqlalchemy.orm import Session
from ..models import MngAdmin2, MngAdmin1

class MngAdmin2Validator:

    @staticmethod
    def validate_name(name: str):
        """ Validate that the name field is not empty """
        if not name:
            raise ValueError("The 'name' field is required.")

    @staticmethod
    def validate_admin_1_id(db: Session, admin_1_id: int):
        """ Validate that the admin_1_id corresponds to an existing Admin1 """
        admin_1 = db.query(MngAdmin1).filter(MngAdmin1.id == admin_1_id).first()
        if not admin_1:
            raise ValueError(f"The 'admin_1_id' '{admin_1_id}' does not correspond to a valid Admin1 record.")

    @staticmethod
    def validate_unique_name(db: Session, name: str, admin_1_id: int):
        """ Validate that the name is unique within the same Admin1 """
        existing_admin2 = db.query(MngAdmin2).filter(MngAdmin2.name == name, MngAdmin2.admin_1_id == admin_1_id).first()
        if existing_admin2:
            raise ValueError(f"An Admin2 with the name '{name}' already exists in this Admin1.")

    @staticmethod
    def validate_unique_ext_id(db: Session, ext_id: str, admin_1_id: int):
        """ Validate that the ext_id is unique within the same country (ignoring empty strings) """
        if ext_id and ext_id.strip():  # Only validate if ext_id is not empty
            # Get the country_id from the parent Admin1
            admin_1 = db.query(MngAdmin1).filter(MngAdmin1.id == admin_1_id).first()
            if admin_1:
                # Search for Admin2 with the same ext_id in the same country
                existing_admin2 = db.query(MngAdmin2).join(MngAdmin1).filter(
                    MngAdmin2.ext_id == ext_id,
                    MngAdmin1.country_id == admin_1.country_id
                ).first()
                if existing_admin2:
                    raise ValueError(f"An Admin2 with the ext_id '{ext_id}' already exists in this country.")

    @staticmethod
    def create_validate(db: Session, obj_in):
        """ Validate all fields before creating a new Admin2 """
        # Validate the name
        MngAdmin2Validator.validate_name(obj_in.name)
        # Validate admin_1_id
        MngAdmin2Validator.validate_admin_1_id(db, obj_in.admin_1_id)
        # Validate name uniqueness
        MngAdmin2Validator.validate_unique_name(db, obj_in.name, obj_in.admin_1_id)
        # Validate ext_id uniqueness
        MngAdmin2Validator.validate_unique_ext_id(db, obj_in.ext_id, obj_in.admin_1_id)

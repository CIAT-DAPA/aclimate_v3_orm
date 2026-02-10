from sqlalchemy.orm import Session
from ..models import MngLocation, MngAdmin2
import re

class MngLocationValidator:

    @staticmethod
    def validate_name(name: str):
        """ Validate if the name field is not empty or null """
        if not name:
            raise ValueError("The 'name' field is required.")

    @staticmethod
    def validate_admin_2_id(db: Session, admin_2_id: int):
        """ Validate if the admin_2_id corresponds to an existing Admin2 """
        admin_2 = db.query(MngAdmin2).filter(MngAdmin2.id == admin_2_id).first()
        if not admin_2:
            raise ValueError(f"Admin2 with id '{admin_2_id}' does not exist.")

    @staticmethod
    def validate_unique_name(db: Session, name: str, admin_2_id: int):
        """ Validate if the name is unique within the same admin_2 """
        existing_location = db.query(MngLocation).filter(MngLocation.name == name, MngLocation.admin_2_id == admin_2_id).first()
        if existing_location:
            raise ValueError(f"A Location with the name '{name}' already exists in this Admin2.")

    @staticmethod
    def validate_machine_name_format(machine_name: str):
        """ Validate if machine_name follows slug format (lowercase letters, numbers, hyphens) """
        if not machine_name:
            raise ValueError("The 'machine_name' field is required.")
        if not re.match(r'^[a-z0-9]+(?:-[a-z0-9]+)*$', machine_name):
            raise ValueError("machine_name must be a slug: lowercase letters, numbers, and hyphens only (e.g., 'station-name-01').")

    @staticmethod
    def validate_unique_machine_name(db: Session, machine_name: str, location_id: int = None):
        """ Validate if machine_name is globally unique """
        query = db.query(MngLocation).filter(MngLocation.machine_name == machine_name)
        if location_id:
            query = query.filter(MngLocation.id != location_id)
        existing_location = query.first()
        if existing_location:
            raise ValueError(f"A Location with machine_name '{machine_name}' already exists.")

    @staticmethod
    def validate_latitude(latitude: float):
        """ Validate if the latitude is in a valid range (-90 to 90) """
        if latitude < -90 or latitude > 90:
            raise ValueError("Latitude must be between -90 and 90.")

    @staticmethod
    def validate_longitude(longitude: float):
        """ Validate if the longitude is in a valid range (-180 to 180) """
        if longitude < -180 or longitude > 180:
            raise ValueError("Longitude must be between -180 and 180.")

    @staticmethod
    def create_validate(db: Session, obj_in: dict):
        """ Validate fields before creating a new Location record """
        # Validate the fields for the new Location entry
        MngLocationValidator.validate_name(obj_in.name)
        MngLocationValidator.validate_machine_name_format(obj_in.machine_name)
        MngLocationValidator.validate_unique_machine_name(db, obj_in.machine_name)
        MngLocationValidator.validate_admin_2_id(db, obj_in.admin_2_id)
        MngLocationValidator.validate_unique_name(db, obj_in.name, obj_in.admin_2_id)
        if "latitude" in obj_in:
            MngLocationValidator.validate_latitude(obj_in.latitude)
        if "longitude" in obj_in:
            MngLocationValidator.validate_longitude(obj_in.longitude)

from sqlalchemy.orm import Session
from ..models import MngAdmin2, MngAdmin1

class MngAdmin2Validator:

    @staticmethod
    def validate_name(name: str):
        """ Validar que el nombre no esté vacío """
        if not name:
            raise ValueError("El campo 'name' es obligatorio.")

    @staticmethod
    def validate_admin_1_id(db: Session, admin_1_id: int):
        """ Validar que el admin_1_id corresponda a un Admin1 existente """
        admin_1 = db.query(MngAdmin1).filter(MngAdmin1.id == admin_1_id).first()
        if not admin_1:
            raise ValueError(f"El 'admin_1_id' '{admin_1_id}' no corresponde a un registro de Admin1 válido.")

    @staticmethod
    def validate_unique_name(db: Session, name: str, admin_1_id: int):
        """ Validar que el nombre sea único dentro del mismo Admin1 """
        existing_admin2 = db.query(MngAdmin2).filter(MngAdmin2.name == name, MngAdmin2.admin_1_id == admin_1_id).first()
        if existing_admin2:
            raise ValueError(f"Ya existe un Admin2 con el nombre '{name}' en este Admin1.")

    @staticmethod
    def create_validate(db: Session, obj_in):
        """ Validar todos los campos antes de crear un nuevo Admin2 """
        # Validar el nombre
        MngAdmin2Validator.validate_name(obj_in.name)
        # Validar admin_1_id
        MngAdmin2Validator.validate_admin_1_id(db, obj_in.admin_1_id)
        # Validar unicidad del nombre
        MngAdmin2Validator.validate_unique_name(db, obj_in.name, obj_in.admin_1_id)

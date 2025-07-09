from sqlalchemy.orm import Session
from ..models import MngDataSource, MngCountry

class MngDataSourceValidator:

    @staticmethod
    def validate_name(name: str):
        if not name or not name.strip():
            raise ValueError("El campo 'name' es obligatorio.")

    @staticmethod
    def validate_type(type_: str):
        if not type_ or not type_.strip():
            raise ValueError("El campo 'type' es obligatorio.")

    @staticmethod
    def validate_country_id(db: Session, country_id: int):
        if not db.query(MngCountry).filter(MngCountry.id == country_id).first():
            raise ValueError(f"Country con id '{country_id}' no existe.")

    @staticmethod
    def validate_unique_name(db: Session, name: str, country_id: int):
        exists = db.query(MngDataSource).filter(
            MngDataSource.name == name,
            MngDataSource.country_id == country_id
        ).first()
        if exists:
            raise ValueError(f"Ya existe una fuente de datos con el nombre '{name}' para este país.")

    @staticmethod
    def create_validate(db: Session, obj_in):
        MngDataSourceValidator.validate_name(obj_in.name)
        MngDataSourceValidator.validate_type(obj_in.type)
        MngDataSourceValidator.validate_country_id(db, obj_in.country_id)
        MngDataSourceValidator.validate_unique_name(db, obj_in.name, obj_in.country_id)
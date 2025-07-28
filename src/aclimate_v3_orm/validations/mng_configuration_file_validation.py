import os
from sqlalchemy.orm import Session
from ..models import MngConfigurationFile, MngSetup

class MngConfigurationFileValidator:

    ALLOWED_EXTENSIONS = {'.crp', '.exp', '.sol', '.csv', '.cul', '.eco', '.spe'}

    @staticmethod
    def validate_setup_id(db: Session, setup_id: int):
        if not db.query(MngSetup).filter(MngSetup.id == setup_id).first():
            raise ValueError(f"Setup con id '{setup_id}' no existe.")

    @staticmethod
    def validate_unique_name(db: Session, name: str, setup_id: int):
        exists = db.query(MngConfigurationFile).filter(
            MngConfigurationFile.name == name,
            MngConfigurationFile.setup_id == setup_id
        ).first()
        if exists:
            raise ValueError(f"Ya existe un archivo de configuración con el nombre '{name}' para este setup.")

    @staticmethod
    def validate_extension(name: str):
        ext = os.path.splitext(name)[1].lower()
        if ext not in MngConfigurationFileValidator.ALLOWED_EXTENSIONS:
            raise ValueError(
                f"Extensión de archivo '{ext}' no permitida. "
                f"Permitidas: {', '.join(MngConfigurationFileValidator.ALLOWED_EXTENSIONS)}"
            )

    @staticmethod
    def create_validate(db: Session, obj_in):
        MngConfigurationFileValidator.validate_setup_id(db, obj_in.setup_id)
        MngConfigurationFileValidator.validate_unique_name(db, obj_in.name, obj_in.setup_id)
        MngConfigurationFileValidator.validate_extension(obj_in.name)
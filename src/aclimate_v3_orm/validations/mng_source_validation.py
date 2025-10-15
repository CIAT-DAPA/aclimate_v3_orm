from sqlalchemy.orm import Session
from ..models import MngSource
from ..schemas import SourceCreate, SourceUpdate
from ..enums import SourceType

class MngSourceValidator:
    @staticmethod
    def validate_name(name: str):
        """Validate source name is not empty"""
        if not name or not name.strip():
            raise ValueError("The 'name' field is required and cannot be empty.")
        if len(name) > 255:
            raise ValueError("Source name cannot exceed 255 characters")

    @staticmethod
    def validate_type(source_type: str):
        """Validate source type is MA, AU, SP, PL, or TP"""
        if source_type not in [SourceType.MANUAL, SourceType.AUTOMATIC, SourceType.SPATIAL, SourceType.PLUVIOMETER, SourceType.THERMOPLUVIOMETER]:
            raise ValueError("Source type must be either 'MA' (Manual), 'AU' (Automatic), 'SP' (Spatial), 'PL' (Pluviometer), or 'TP' (Thermoplviometer)")

    @staticmethod
    def validate_unique_name(db: Session, name: str, exclude_id: int = None):
        """Check if source name already exists in database"""
        query = db.query(MngSource).filter(MngSource.name == name)
        if exclude_id:
            query = query.filter(MngSource.id != exclude_id)
        if query.first():
            raise ValueError(f"A source with name '{name}' already exists")

    @staticmethod
    def validate_unique_type_name_combination(db: Session, name: str, source_type: str, exclude_id: int = None):
        """Check if the same name exists for the same type"""
        query = db.query(MngSource).filter(
            MngSource.name == name,
            MngSource.source_type == source_type
        )
        if exclude_id:
            query = query.filter(MngSource.id != exclude_id)
        if query.first():
            raise ValueError(f"A {source_type} source with name '{name}' already exists")

    @staticmethod
    def create_validate(db: Session, obj_in: SourceCreate):
        """Validation for source creation"""
        MngSourceValidator.validate_name(obj_in.name)
        MngSourceValidator.validate_type(obj_in.source_type)
        MngSourceValidator.validate_unique_name(db, obj_in.name)
        MngSourceValidator.validate_unique_type_name_combination(db, obj_in.name, obj_in.source_type)

    @staticmethod
    def update_validate(db: Session, obj_in: SourceUpdate, source_id: int):
        """Validation for source updates"""
        if hasattr(obj_in, 'name') and obj_in.name is not None:
            MngSourceValidator.validate_name(obj_in.name)
            MngSourceValidator.validate_unique_name(db, obj_in.name, exclude_id=source_id)

        if hasattr(obj_in, 'type') and obj_in.source_type is not None:
            MngSourceValidator.validate_type(obj_in.source_type)
            
            # If both name and type are being updated, check combination
            if hasattr(obj_in, 'name') and obj_in.name is not None:
                MngSourceValidator.validate_unique_type_name_combination(
                    db, obj_in.name, obj_in.source_type, exclude_id=source_id
                )
            else:
                # If only type is being updated, get current name to check combination
                current_source = db.query(MngSource).filter(MngSource.id == source_id).first()
                if current_source:
                    MngSourceValidator.validate_unique_type_name_combination(
                        db, current_source.name, obj_in.source_type, exclude_id=source_id
                    )
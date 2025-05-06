from services.base_service import BaseService
from models.catalog import ClimateMeasure
from validations.catalog import ClimateMeasureNameValidator
from sqlalchemy.orm import Session
from typing import List

class ClimateMeasureService(BaseService[ClimateMeasure]):
    def __init__(self):
        super().__init__(ClimateMeasure)

    def get_by_name(self, db: Session, name: str, enabled: bool = True) -> List[ClimateMeasure]:
        return db.query(self.model).filter(self.model.name == name, self.model.enable == enabled).all()

    def get_by_short_name(self, db: Session, short_name: str, enabled: bool = True) -> List[ClimateMeasure]:
        return db.query(self.model).filter(self.model.short_name == short_name, self.model.enable == enabled).all()

    def get_all(self, db: Session, enabled: bool = True) -> List[ClimateMeasure]:
        return db.query(self.model).filter(self.model.enable == enabled).all()
    
    def validate_create(self, db: Session, obj_in: dict):
        # Validate that the climate measure name is unique before creating
        ClimateMeasureNameValidator.validate(db, obj_in)

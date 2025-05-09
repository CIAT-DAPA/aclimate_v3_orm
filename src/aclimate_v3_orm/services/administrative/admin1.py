from services.base_service import BaseService
from models.administrative import Admin1
from validations.administrative import Admin1Validator
from sqlalchemy.orm import Session
from typing import List

class Admin1Service(BaseService[Admin1]):
    def __init__(self):
        super().__init__(Admin1)

    def get_by_country_id(self, db: Session, country_id: int, enabled: bool = True) -> List[Admin1]:
        return db.query(self.model).filter(self.model.country_id == country_id, self.model.enable == enabled).all()

    def get_by_country_name(self, db: Session, country_name: str, enabled: bool = True) -> List[Admin1]:
        return db.query(self.model).join(self.model.country).filter(self.model.country.name == country_name, self.model.enable == enabled).all()

    def get_all(self, db: Session, enabled: bool = True) -> List[Admin1]:
        return db.query(self.model).filter(self.model.enable == enabled).all()
    
    def get_by_name(self, db: Session, name: str, enabled: bool = True) -> List[Admin1]:
        return db.query(self.model).filter(self.model.name == name, self.model.enable == enabled).all()

    def validate_create(self, db: Session, obj_in: dict):
        # Validate before create
        Admin1Validator.create_validate(db, obj_in)
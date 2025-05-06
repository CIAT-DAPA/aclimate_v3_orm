from services.base_service import BaseService
from models.administrative import Admin2
from validations.administrative import Admin2Validator
from sqlalchemy.orm import Session
from typing import List

class Admin2Service(BaseService[Admin2]):
    def __init__(self):
        super().__init__(Admin2)

    def get_by_admin1_id(self, db: Session, admin1_id: int, enabled: bool = True) -> List[Admin2]:
        return db.query(self.model).filter(self.model.admin_1_id == admin1_id, self.model.enable == enabled).all()

    def get_by_admin1_name(self, db: Session, admin1_name: str, enabled: bool = True) -> List[Admin2]:
        return db.query(self.model).join(self.model.admin_1).filter(self.model.admin_1.name == admin1_name, self.model.enable == enabled).all()

    def get_by_country_id(self, db: Session, country_id: int, enabled: bool = True) -> List[Admin2]:
        return db.query(self.model).join(self.model.admin_1).filter(self.model.admin_1.country_id == country_id, self.model.enable == enabled).all()

    def get_by_country_name(self, db: Session, country_name: str, enabled: bool = True) -> List[Admin2]:
        return db.query(self.model).join(self.model.admin_1).join(self.model.admin_1.country).filter(self.model.admin_1.country.name == country_name, self.model.enable == enabled).all()

    def get_all(self, db: Session, enabled: bool = True) -> List[Admin2]:
        return db.query(self.model).filter(self.model.enable == enabled).all()

    def get_by_name(self, db: Session, name: str, enabled: bool = True) -> List[Admin2]:
        return db.query(self.model).filter(self.model.name == name, self.model.enable == enabled).all()
    
    def get_by_visible(self, db: Session, visible: bool, enabled: bool = True) -> List[Admin2]:
        return db.query(self.model).filter(self.model.visible == visible, self.model.enable == enabled).all()
    
    def validate_create(self, db: Session, obj_in: dict):
        # Validate before create
        Admin2Validator.create_validate(db, obj_in)
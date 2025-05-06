from services.base_service import BaseService
from models.administrative import Country
from validations.administrative import CountryValidator
from sqlalchemy.orm import Session
from typing import List

class CountryService(BaseService[Country]):
    def __init__(self):
        super().__init__(Country)

    def get_by_name(self, db: Session, name: str, enabled: bool = True) -> List[Country]:
        return db.query(self.model).filter(self.model.name == name, self.model.enable == enabled).all()

    def get_all_enable(self, db: Session, enabled: bool = True) -> List[Country]:
        return db.query(self.model).filter(self.model.enable == enabled).all()


    def validate_create(self, db: Session, obj_in: dict):
        # Validate before create
        CountryValidator.create_validate(db, obj_in)
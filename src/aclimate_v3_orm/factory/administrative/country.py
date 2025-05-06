from factory.base_factory import BaseFactory
from models.administrative import Country
from sqlalchemy.orm import Session
from typing import List

class CountryFactory(BaseFactory[Country]):
    def __init__(self):
        super().__init__(Country)

    def get_by_name(self, db: Session, name: str, enabled: bool = True) -> List[Country]:
        return db.query(self.model).filter(self.model.name == name, self.model.enable == enabled).all()

    def get_all_enable(self, db: Session, enabled: bool = True) -> List[Country]:
        return db.query(self.model).filter(self.model.enable == enabled).all()

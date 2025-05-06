from factory.base_factory import BaseFactory
from models.administrative import Location
from sqlalchemy.orm import Session
from typing import List

class LocationFactory(BaseFactory[Location]):
    def __init__(self):
        super().__init__(Location)

    
    def get_by_visible(self, db: Session, visible: bool, enabled: bool = True) -> List[Location]:
        return db.query(self.model).filter(self.model.visible == visible, self.model.enable == enabled).all()

    def get_by_ext_id(self, db: Session, ext_id: str, enabled: bool = True) -> List[Location]:
        return db.query(self.model).filter(self.model.ext_id == ext_id, self.model.enable == enabled).all()

    def get_by_name(self, db: Session, name: str, enabled: bool = True) -> List[Location]:
        return db.query(self.model).filter(self.model.name == name, self.model.enable == enabled).all()
    
    def get_all_enable(self, db: Session, enable: bool = True) -> List[Location]:
        return db.query(self.model).filter(self.model.enable == enable).all()

    def get_by_country_id(self, db: Session, country_id: int, enabled: bool = True) -> List[Location]:
        return (
            db.query(self.model)
            .join(self.model.admin_2)
            .join(self.model.admin_2.admin_1)
            .filter(self.model.admin_2.admin_1.country_id == country_id, self.model.enable == enabled)
            .all()
        )

    def get_by_admin1_id(self, db: Session, admin1_id: int, enabled: bool = True) -> List[Location]:
        return (
            db.query(self.model)
            .join(self.model.admin_2)
            .filter(self.model.admin_2.admin_1_id == admin1_id, self.model.enable == enabled)
            .all()
        )

    def get_by_country_name(self, db: Session, country_name: str, enabled: bool = True) -> List[Location]:
        return (
            db.query(self.model)
            .join(self.model.admin_2)
            .join(self.model.admin_2.admin_1)
            .join(self.model.admin_2.admin_1.country)
            .filter(self.model.admin_2.admin_1.country.name == country_name, self.model.enable == enabled)
            .all()
        )

    def get_by_admin1_name(self, db: Session, admin1_name: str, enabled: bool = True) -> List[Location]:
        return (
            db.query(self.model)
            .join(self.model.admin_2)
            .join(self.model.admin_2.admin_1)
            .filter(self.model.admin_2.admin_1.name == admin1_name, self.model.enable == enabled)
            .all()
        )
    
    def get_by_admin2_id(self, db: Session, admin2_id: int, enabled: bool = True) -> List[Location]:
        return (
            db.query(self.model)
            .filter(self.model.admin_2_id == admin2_id, self.model.enable == enabled)
            .all()
        )

    def get_by_admin2_name(self, db: Session, admin2_name: str, enabled: bool = True) -> List[Location]:
        return (
            db.query(self.model)
            .join(self.model.admin_2)
            .filter(self.model.admin_2.name == admin2_name, self.model.enable == enabled)
            .all()
        )

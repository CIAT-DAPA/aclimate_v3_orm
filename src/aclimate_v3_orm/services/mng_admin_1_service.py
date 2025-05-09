from services.base_service import BaseService
from aclimate_v3_orm.models import MngAdmin1
from schemas.administrative import Admin1CreateSchema, Admin1ReadSchema
from validations.administrative import Admin1Validator
from sqlalchemy.orm import Session
from typing import List

class MngAdmin1Service(BaseService[MngAdmin1, Admin1CreateSchema, Admin1ReadSchema]):
    def __init__(self):
        super().__init__(MngAdmin1, Admin1CreateSchema, Admin1ReadSchema)

    def get_by_country_id(self, db: Session, country_id: int, enabled: bool = True) -> List[Admin1ReadSchema]:
        objs = db.query(self.model).filter(self.model.country_id == country_id, self.model.enable == enabled).all()
        return [self.schema_read.from_orm(obj) for obj in objs]

    def get_by_country_name(self, db: Session, country_name: str, enabled: bool = True) -> List[Admin1ReadSchema]:
        objs = db.query(self.model).join(self.model.country).filter(self.model.country.name == country_name, self.model.enable == enabled).all()
        return [self.schema_read.from_orm(obj) for obj in objs]

    def get_all(self, db: Session, enabled: bool = True) -> List[Admin1ReadSchema]:
        objs = db.query(self.model).filter(self.model.enable == enabled).all()
        return [self.schema_read.from_orm(obj) for obj in objs]

    def get_by_name(self, db: Session, name: str, enabled: bool = True) -> List[Admin1ReadSchema]:
        objs = db.query(self.model).filter(self.model.name == name, self.model.enable == enabled).all()
        return [self.schema_read.from_orm(obj) for obj in objs]

    def validate_create(self, db: Session, obj_in: Admin1CreateSchema):
        Admin1Validator.create_validate(db, obj_in)

from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from ..services.base_service import BaseService
from ..models import MngAdmin1, MngCountry
from ..schemas import Admin1Create, Admin1Update, Admin1Read
from ..validations import MngAdmin1Validator

class MngAdmin1Service(BaseService[MngAdmin1, Admin1Create, Admin1Read, Admin1Update]):
    def __init__(self):
        super().__init__(MngAdmin1, Admin1Create, Admin1Read, Admin1Update)

    def get_by_country_id(self,
                          country_id: int, 
                          enabled: bool = True,
                          db: Optional[Session] = None) -> List[Admin1Read]:
        """Get admin1 regions by country ID"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .filter(
                    self.model.country_id == country_id,
                    self.model.enable == enabled
                )
                .all()
            )
            return [Admin1Read.model_validate(obj) for obj in objs]

    def get_by_country_name(self,
                            country_name: str, 
                            enabled: bool = True,
                            db: Optional[Session] = None) -> List[Admin1Read]:
        """Get admin1 regions by country name"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .join(MngAdmin1.country)
                .filter(
                    MngCountry.name == country_name,
                    self.model.enable == enabled
                )
                .all()
            )
            return [Admin1Read.model_validate(obj) for obj in objs]

    def get_all(self,
                enabled: bool = True,
                db: Optional[Session] = None) -> List[Admin1Read]:
        """Get all admin1 regions, optionally filtered by enabled status"""
        with self._session_scope(db) as session:
            query = session.query(self.model)
            if enabled is not None:
                query = query.filter(self.model.enable == enabled)
            objs = query.all()
            return [Admin1Read.model_validate(obj) for obj in objs]

    def get_by_name(self,
                    name: str, 
                    enabled: bool = True,
                    db: Optional[Session] = None) -> List[Admin1Read]:
        """Get admin1 regions by name"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .filter(
                    self.model.name == name,
                    self.model.enable == enabled
                )
                .all()
            )
            return [Admin1Read.model_validate(obj) for obj in objs]

    def _validate_create(self, obj_in: Admin1Create, db: Optional[Session] = None):
        """Validation hook called automatically from BaseService.create()"""
        MngAdmin1Validator.create_validate(db, obj_in)

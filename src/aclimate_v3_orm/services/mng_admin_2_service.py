from ..services.base_service import BaseService
from ..models import MngAdmin2, MngAdmin1, MngCountry
from ..validations import MngAdmin2Validator
from sqlalchemy.orm import Session
from typing import List, Optional
from ..schemas import Admin2Create, Admin2Read, Admin2Update

class MngAdmin2Service(BaseService[MngAdmin2, Admin2Create, Admin2Read, Admin2Update]):
    def __init__(self):
        super().__init__(MngAdmin2, Admin2Create, Admin2Read, Admin2Update)

    def get_by_admin1_id(self, admin1_id: int, enabled: bool = True, db: Optional[Session] = None) -> List[Admin2Read]:
        """Get admin2 regions by admin1 ID"""
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(self.model.admin_1_id == admin1_id, self.model.enable == enabled).all()
            return [Admin2Read.model_validate(obj) for obj in objs]

    def get_by_admin1_name(self, admin1_name: str, enabled: bool = True, db: Optional[Session] = None) -> List[Admin2Read]:
        """Get admin2 regions by admin1 name"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .join(self.model.admin_1)
                .filter(
                    MngAdmin1.name == admin1_name,
                    self.model.enable == enabled
                )
                .all()
            )
            return [Admin2Read.model_validate(obj) for obj in objs]


    def get_by_country_id(self, country_id: int, enabled: bool = True, db: Optional[Session] = None) -> List[Admin2Read]:
        """Get admin2 regions by country ID"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .join(self.model.admin_1)
                .join(MngAdmin1.country)
                .filter(
                    MngAdmin1.country_id == country_id,
                    self.model.enable == enabled
                )
                .all()
            )
            return [Admin2Read.model_validate(obj) for obj in objs]


    def get_by_country_name(self, country_name: str, enabled: bool = True, db: Optional[Session] = None) -> List[Admin2Read]:
        """Get admin2 regions by country name"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .join(MngAdmin2.admin_1)
                .join(MngAdmin1.country)
                .filter(
                    MngCountry.name == country_name,
                    self.model.enable == enabled
                )
                .all()
            )
            return [Admin2Read.model_validate(obj) for obj in objs]


    def get_all(self, enabled: bool = True, db: Optional[Session] = None) -> List[Admin2Read]:
        """Get all admin2 regions, optionally filtered by enabled status"""
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(self.model.enable == enabled).all()
            return [Admin2Read.model_validate(obj) for obj in objs]

    def get_by_name(self, name: str, enabled: bool = True, db: Optional[Session] = None) -> List[Admin2Read]:
        """Get admin2 regions by name"""
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(self.model.name == name, self.model.enable == enabled).all()
            return [Admin2Read.model_validate(obj) for obj in objs]
    
    def get_by_visible(self, visible: bool, enabled: bool = True, db: Optional[Session] = None) -> List[Admin2Read]:
        """Get admin2 regions by visibility status"""
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(self.model.visible == visible, self.model.enable == enabled).all()
            return [Admin2Read.model_validate(obj) for obj in objs]

    def _validate_create(self, obj_in: Admin2Create, db: Optional[Session] = None):
        """Validate before creating a new admin2 region"""
        MngAdmin2Validator.create_validate(db, obj_in)

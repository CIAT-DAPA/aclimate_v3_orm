from typing import List, Optional
from sqlalchemy.orm import Session
from ..services.base_service import BaseService
from ..models import UserAccess, User, MngCountry
from ..validations import UserAccessValidator
from ..schemas import UserAccessCreate, UserAccessRead, UserAccessUpdate

class UserAccessService(BaseService[UserAccess, UserAccessCreate, UserAccessRead, UserAccessUpdate]):
    def __init__(self):
        super().__init__(UserAccess, UserAccessCreate, UserAccessRead, UserAccessUpdate)

    def get_by_user_id(self, user_id: int, db: Optional[Session] = None) -> List[UserAccessRead]:
        """Get user accesses by user_id"""
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(
                self.model.user_id == user_id
            ).all()
            return [UserAccessRead.model_validate(obj) for obj in objs]

    def get_by_country_id(self, country_id: int, db: Optional[Session] = None) -> List[UserAccessRead]:
        """Get user accesses by country_id"""
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(
                self.model.country_id == country_id
            ).all()
            return [UserAccessRead.model_validate(obj) for obj in objs]

    def get_by_role_id(self, role_id: int, db: Optional[Session] = None) -> List[UserAccessRead]:
        """Get user accesses by role_id"""
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(
                self.model.role_id == role_id
            ).all()
            return [UserAccessRead.model_validate(obj) for obj in objs]

    def get_by_user_country_role(self, country_id: int, role_id: int, db: Optional[Session] = None) -> Optional[UserAccessRead]:
        """Get user access by country_id and role_id (unique combination)"""
        with self._session_scope(db) as session:
            obj = session.query(self.model).filter(
                self.model.country_id == country_id,
                self.model.role_id == role_id
            ).first()
            return UserAccessRead.model_validate(obj) if obj else None

    def get_by_keycloak_ext_id(self, keycloak_ext_id: str, db: Optional[Session] = None) -> List[UserAccessRead]:
        """Get user accesses by keycloak external ID"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .join(self.model.user)
                .filter(
                    User.keycloak_ext_id == keycloak_ext_id
                )
                .all()
            )
            return [UserAccessRead.model_validate(obj) for obj in objs]

    def get_by_country_name(self, country_name: str, db: Optional[Session] = None) -> List[UserAccessRead]:
        """Get user accesses by country name"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .join(self.model.country)
                .filter(
                    MngCountry.name == country_name
                )
                .all()
            )
            return [UserAccessRead.model_validate(obj) for obj in objs]

    def _validate_create(self, obj_in: UserAccessCreate, db: Optional[Session] = None):
        """Automatic validation called from BaseService.create()"""
        UserAccessValidator.create_validate(db, obj_in)
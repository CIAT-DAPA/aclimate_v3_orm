from typing import List, Optional
from sqlalchemy.orm import Session
from ..services.base_service import BaseService
from ..models import User
from ..validations import UserValidator
from ..schemas import UserCreate, UserRead, UserUpdate
from ..models import Role
from ..enums import Apps

class UserService(BaseService[User, UserCreate, UserRead, UserUpdate]):
    def __init__(self):
        super().__init__(User, UserCreate, UserRead, UserUpdate)

    def get_by_keycloak_ext_id(self, keycloak_ext_id: str, enabled: bool = True, db: Optional[Session] = None) -> List[UserRead]:
        """Get users by external Keycloak ID"""
        ext_id = keycloak_ext_id.strip() if keycloak_ext_id else keycloak_ext_id
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(
                self.model.keycloak_ext_id == ext_id,
                self.model.enable == enabled
            ).all()
            return [UserRead.model_validate(obj) for obj in objs]

    def get_all_enable(self, db: Optional[Session] = None, enabled: bool = True) -> List[UserRead]:
        """Get all users, filtered by enabled status"""
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(
                self.model.enable == enabled
            ).all()
            return [UserRead.model_validate(obj) for obj in objs]
        
    def get_by_role_id(self, role_id: int, enabled: bool = True, db: Optional[Session] = None) -> List[UserRead]:
        """Get users by role_id"""
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(
                self.model.role_id == role_id,
                self.model.enable == enabled
            ).all()
            return [UserRead.model_validate(obj) for obj in objs]

    def get_by_role_name(self, role_name: str, enabled: bool = True, db: Optional[Session] = None) -> List[UserRead]:
        """Get users by role name"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .join(Role.users)
                .filter(
                    Role.name == role_name,
                    self.model.enable == enabled
                )
                .all()
            )
            return [UserRead.model_validate(obj) for obj in objs]

    def get_by_app(self, app: str, enabled: bool = True, db: Optional[Session] = None) -> List[UserRead]:
        """Get users by app enum value (accepts string or Apps enum)"""
        if isinstance(app, str):
            try:
                app_enum = Apps(app)
            except ValueError:
                raise ValueError(f"Invalid app value: {app}")
        else:
            app_enum = app
        
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .join(Role)
                .filter(
                    Role.app == app_enum,
                    self.model.enable == enabled
                )
                .all()
            )
            return [UserRead.model_validate(obj) for obj in objs]

    def _validate_create(self, obj_in: UserCreate, db: Optional[Session] = None):
        """Automatic validation called from BaseService.create()"""
        UserValidator.create_validate(db, obj_in)

from typing import List, Optional
from sqlalchemy.orm import Session
from ..services.base_service import BaseService
from ..models import Role
from ..validations import RoleValidator
from ..schemas import RoleCreate, RoleRead, RoleUpdate
from ..enums import Apps

class RoleService(BaseService[Role, RoleCreate, RoleRead, RoleUpdate]):
    def __init__(self):
        super().__init__(Role, RoleCreate, RoleRead, RoleUpdate)

    def get_by_name(self, name: str, enabled: bool = True, db: Optional[Session] = None) -> List[RoleRead]:
        """Get roles by name"""
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(
                self.model.name == name,
                self.model.enable == enabled
            ).all()
            return [RoleRead.model_validate(obj) for obj in objs]

    def get_by_app(self, app: str, enabled: bool = True, db: Optional[Session] = None) -> List[RoleRead]:
        """Get roles by app enum value (accepts string or Apps enum)"""
        if isinstance(app, str):
            try:
                app_enum = Apps(app)
            except ValueError:
                raise ValueError(f"Invalid app value: {app}")
        else:
            app_enum = app
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(
                self.model.app == app_enum,
                self.model.enable == enabled
            ).all()
            return [RoleRead.model_validate(obj) for obj in objs]

    def get_by_name_and_app(self, name: str, app: str, enabled: bool = True, db: Optional[Session] = None) -> Optional[RoleRead]:
        """Get role by name and app (unique combination)"""
        if isinstance(app, str):
            try:
                app_enum = Apps(app)
            except ValueError:
                raise ValueError(f"Invalid app value: {app}")
        else:
            app_enum = app
        with self._session_scope(db) as session:
            obj = session.query(self.model).filter(
                self.model.name == name,
                self.model.app == app_enum,
                self.model.enable == enabled
            ).first()
            return RoleRead.model_validate(obj) if obj else None

    def _validate_create(self, obj_in: RoleCreate, db: Optional[Session] = None):
        """Automatic validation called from BaseService.create()"""
        RoleValidator.create_validate(db, obj_in)

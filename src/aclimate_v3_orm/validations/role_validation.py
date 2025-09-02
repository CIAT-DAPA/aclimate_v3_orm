from sqlalchemy.orm import Session
from ..models import Role
from ..schemas import RoleCreate, RoleUpdate
from ..enums import Apps

class RoleValidator:
    @staticmethod
    def validate_name(name: str):
        if not name:
            raise ValueError("The 'name' field is required.")
        if len(name.strip()) == 0:
            raise ValueError("The 'name' field cannot be empty.")

    @staticmethod
    def validate_app(app: Apps):
        if not app:
            raise ValueError("The 'app' field is required.")
        if app not in Apps:
            raise ValueError(f"Invalid app value: {app}")

    @staticmethod
    def validate_unique_name_and_app(db: Session, name: str, app: Apps, exclude_id: int = None):
        query = db.query(Role).filter(Role.name == name, Role.app == app)
        if exclude_id:
            query = query.filter(Role.id != exclude_id)
        if query.first():
            raise ValueError(f"The role with name '{name}' and app '{app.value}' already exists.")

    @staticmethod
    def create_validate(db: Session, obj_in: RoleCreate):
        RoleValidator.validate_name(obj_in.name)
        RoleValidator.validate_app(obj_in.app)
        RoleValidator.validate_unique_name_and_app(db, obj_in.name, obj_in.app)

    @staticmethod
    def update_validate(db: Session, obj_in: RoleUpdate, role_id: int):
        if obj_in.name:
            RoleValidator.validate_name(obj_in.name)
        if obj_in.app:
            RoleValidator.validate_app(obj_in.app)
        
        name = obj_in.name if obj_in.name else None
        app = obj_in.app if obj_in.app else None
        
        if name and app:
            RoleValidator.validate_unique_name_and_app(db, name, app, exclude_id=role_id)

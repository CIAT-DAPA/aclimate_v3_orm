from sqlalchemy.orm import Session
from ..models import User
from ..schemas import UserCreate, UserUpdate

class UserValidator:
    @staticmethod
    def validate_keycloak_ext_id(keycloak_ext_id: str):
        if not keycloak_ext_id:
            raise ValueError("The 'keycloak_ext_id' field is required.")
        if len(keycloak_ext_id.strip()) == 0:
            raise ValueError("The 'keycloak_ext_id' field cannot be empty.")

    @staticmethod
    def validate_unique_keycloak_ext_id(db: Session, keycloak_ext_id: str, exclude_id: int = None):
        query = db.query(User).filter(User.keycloak_ext_id == keycloak_ext_id)
        if exclude_id:
            query = query.filter(User.id != exclude_id)
        if query.first():
            raise ValueError(f"The user with keycloak_ext_id '{keycloak_ext_id}' already exists.")

    @staticmethod
    def create_validate(db: Session, obj_in: UserCreate):
        UserValidator.validate_keycloak_ext_id(obj_in.keycloak_ext_id)
        UserValidator.validate_unique_keycloak_ext_id(db, obj_in.keycloak_ext_id)

    @staticmethod
    def update_validate(db: Session, obj_in: UserUpdate, user_id: int):
        if obj_in.keycloak_ext_id:
            UserValidator.validate_keycloak_ext_id(obj_in.keycloak_ext_id)
            UserValidator.validate_unique_keycloak_ext_id(db, obj_in.keycloak_ext_id, exclude_id=user_id)

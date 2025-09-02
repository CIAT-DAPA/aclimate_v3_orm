from sqlalchemy.orm import Session
from ..models import UserAccess, User, Role, MngCountry
from ..schemas import UserAccessCreate, UserAccessUpdate

class UserAccessValidator:
    @staticmethod
    def validate_user_id(user_id: int):
        if not user_id or user_id <= 0:
            raise ValueError("The 'user_id' field is required and must be greater than 0.")

    @staticmethod
    def validate_country_id(country_id: int):
        if not country_id or country_id <= 0:
            raise ValueError("The 'country_id' field is required and must be greater than 0.")

    @staticmethod
    def validate_role_id(role_id: int):
        if not role_id or role_id <= 0:
            raise ValueError("The 'role_id' field is required and must be greater than 0.")

    @staticmethod
    def validate_user_exists(db: Session, user_id: int):
        """Check if user exists"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError(f"User with id '{user_id}' does not exist.")
        return user

    @staticmethod
    def validate_country_exists(db: Session, country_id: int):
        """Check if country exists"""
        country = db.query(MngCountry).filter(MngCountry.id == country_id).first()
        if not country:
            raise ValueError(f"Country with id '{country_id}' does not exist.")
        return country

    @staticmethod
    def validate_role_exists(db: Session, role_id: int):
        """Check if role exists"""
        role = db.query(Role).filter(Role.id == role_id).first()
        if not role:
            raise ValueError(f"Role with id '{role_id}' does not exist.")
        return role

    @staticmethod
    def validate_unique_user_country_role(db: Session, user_id: int, country_id: int, role_id: int, exclude_user_id: int = None):
        """Check if the combination user_id + country_id + role_id is unique"""
        query = db.query(UserAccess).filter(
            UserAccess.user_id == user_id,
            UserAccess.country_id == country_id,
            UserAccess.role_id == role_id
        )
        if exclude_user_id:
            query = query.filter(UserAccess.user_id != exclude_user_id)
        if query.first():
            raise ValueError(f"UserAccess with user_id '{user_id}', country_id '{country_id}' and role_id '{role_id}' already exists.")

    @staticmethod
    def create_validate(db: Session, obj_in: UserAccessCreate):
        UserAccessValidator.validate_user_id(obj_in.user_id)
        UserAccessValidator.validate_country_id(obj_in.country_id)
        UserAccessValidator.validate_role_id(obj_in.role_id)
        
        # Check if related entities exist
        UserAccessValidator.validate_user_exists(db, obj_in.user_id)
        UserAccessValidator.validate_country_exists(db, obj_in.country_id)
        UserAccessValidator.validate_role_exists(db, obj_in.role_id)
        
        # Check uniqueness
        UserAccessValidator.validate_unique_user_country_role(db, obj_in.user_id, obj_in.country_id, obj_in.role_id)

    @staticmethod
    def update_validate(db: Session, obj_in: UserAccessUpdate, user_id: int):
        if obj_in.country_id:
            UserAccessValidator.validate_country_id(obj_in.country_id)
            UserAccessValidator.validate_country_exists(db, obj_in.country_id)
        
        if obj_in.role_id:
            UserAccessValidator.validate_role_id(obj_in.role_id)
            UserAccessValidator.validate_role_exists(db, obj_in.role_id)
        
        # For update, get current record to check uniqueness
        current_access = db.query(UserAccess).filter(UserAccess.user_id == user_id).first()
        if current_access:
            new_country_id = obj_in.country_id if obj_in.country_id else current_access.country_id
            new_role_id = obj_in.role_id if obj_in.role_id else current_access.role_id
            UserAccessValidator.validate_unique_user_country_role(db, user_id, new_country_id, new_role_id, exclude_user_id=user_id)

from sqlalchemy.orm import Session
from typing import Type, TypeVar, Generic, List, Optional
from sqlalchemy.exc import SQLAlchemyError

# Define a generic type T for models that will be used with BaseService
T = TypeVar("T")

class BaseService(Generic[T]):
    def __init__(self, model: Type[T]):
        """
        Initialize the service with the model class.
        """
        self.model = model

    def get_by_id(self, db: Session, id: int) -> Optional[T]:
        """
        Retrieve a single record from the database by its ID.
        """
        return db.query(self.model).get(id)

    def get_all(self, db: Session) -> List[T]:
        """
        Retrieve all records of the given model from the database.
        """
        return db.query(self.model).all()

    def create(self, db: Session, obj_in: dict) -> T:
        """
        Create a new record in the database, after validation.
        """
        # Perform validation before creating the object
        self.validate_create(db, obj_in)

        # Create the model object from the provided data
        obj = self.model(**obj_in)
        
        # Add, commit and refresh the object to save it in the database
        db.add(obj)
        db.commit()
        db.refresh(obj)
        
        return obj

    def update(self, db: Session, db_obj: T, obj_in: dict) -> T:
        """
        Update an existing record in the database.
        """
        # Update the object fields with the new data
        for key, value in obj_in.items():
            setattr(db_obj, key, value)
        
        # Add, commit and refresh the object to save the changes
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        return db_obj

    def delete(self, db: Session, db_obj: T) -> T:
        """
        Delete a record from the database (or mark as disabled if it has an 'enabled' attribute).
        """
        try:
            if hasattr(db_obj, "enabled"):
                # If the object has an 'enabled' field, set it to False instead of deleting
                db_obj.enabled = False
            else:
                db.delete(db_obj)  # Permanently delete the object from the database
            
            # Commit the changes to the database
            db.commit()
        except SQLAlchemyError:
            # In case of error, roll back the transaction
            db.rollback()
            raise  # Reraise the exception
        
        return db_obj

    def validate_create(self, db: Session, obj_in: dict):
        """
        Validation function before creating an object. Can be overridden by child services.
        """
        # Default validation can be implemented in subclasses
        pass

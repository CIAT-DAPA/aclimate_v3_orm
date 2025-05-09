from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Type, TypeVar, Generic, List, Optional
from pydantic import BaseModel

# Type variables for SQLAlchemy model and Pydantic schemas
T = TypeVar("T")
SchemaCreateType = TypeVar("SchemaCreateType", bound=BaseModel)
SchemaReadType = TypeVar("SchemaReadType", bound=BaseModel)

class BaseService(Generic[T, SchemaCreateType, SchemaReadType]):
    def __init__(self, model: Type[T], schema_create: Type[SchemaCreateType], schema_read: Type[SchemaReadType]):
        """
        Initialize the service with the model and associated schemas.
        """
        self.model = model
        self.schema_create = schema_create
        self.schema_read = schema_read

    def get_by_id(self, db: Session, id: int) -> Optional[SchemaReadType]:
        """
        Retrieve a single record by ID and return it as a read schema.
        """
        obj = db.query(self.model).get(id)
        return self.schema_read.from_orm(obj) if obj else None

    def get_all(self, db: Session) -> List[SchemaReadType]:
        """
        Retrieve all records and return them as a list of read schemas.
        """
        objs = db.query(self.model).all()
        return [self.schema_read.from_orm(obj) for obj in objs]

    def create(self, db: Session, obj_in: SchemaCreateType) -> SchemaReadType:
        """
        Create a new record using the create schema, validate it, and return the result as a read schema.
        """
        self.validate_create(db, obj_in)

        obj = self.model(**obj_in.dict())
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return self.schema_read.from_orm(obj)

    def update(self, db: Session, db_obj: T, obj_in: dict) -> SchemaReadType:
        """
        Update an existing record with new data and return the updated object as a read schema.
        """
        for key, value in obj_in.items():
            setattr(db_obj, key, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return self.schema_read.from_orm(db_obj)

    def delete(self, db: Session, db_obj: T) -> SchemaReadType:
        """
        Delete or disable a record and return the result as a read schema.
        """
        try:
            if hasattr(db_obj, "enabled"):
                db_obj.enabled = False
            else:
                db.delete(db_obj)

            db.commit()
        except SQLAlchemyError:
            db.rollback()
            raise

        return self.schema_read.from_orm(db_obj)

    def validate_create(self, db: Session, obj_in: SchemaCreateType):
        """
        Validation hook for child services. Override this in subclasses to add custom logic.
        """
        pass

from sqlalchemy.orm import Session
from typing import Type, TypeVar, Generic, List, Optional
from sqlalchemy.exc import SQLAlchemyError

T = TypeVar("T")

class BaseFactory(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    def get_by_id(self, db: Session, id: int) -> Optional[T]:
        return db.query(self.model).get(id)

    def get_all(self, db: Session) -> List[T]:
        return db.query(self.model).all()

    def create(self, db: Session, obj_in: dict) -> T:
        obj = self.model(**obj_in)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, db_obj: T, obj_in: dict) -> T:
        for key, value in obj_in.items():
            setattr(db_obj, key, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: T) -> T:
        try:
            if hasattr(db_obj, "enabled"):
                db_obj.enabled = False
            else:
                db.delete(db_obj)
            db.commit()
        except SQLAlchemyError:
            db.rollback()
            raise
        return db_obj

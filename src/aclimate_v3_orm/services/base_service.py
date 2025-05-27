from typing import TypeVar, Generic, Type, Optional, Any, Dict, List
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from ..database import get_db

T = TypeVar("T")  # Modelo SQLAlchemy
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
ReadSchemaType = TypeVar("ReadSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseService(Generic[T, CreateSchemaType, ReadSchemaType, UpdateSchemaType]):
    def __init__(self, 
                model: Type[T],
                create_schema: Type[CreateSchemaType],
                read_schema: Type[ReadSchemaType],
                update_schema: Type[UpdateSchemaType]):
        self.model = model
        self.create_schema = create_schema
        self.read_schema = read_schema
        self.update_schema = update_schema

    @contextmanager
    def _session_scope(self, db: Optional[Session] = None):
        """
        Safely manages session lifecycle.
        For internal sessions, delegates ALL handling to get_db().
        """
        if db:
            try:
                yield db
                db.commit()
            except SQLAlchemyError as e:
                db.rollback()
                print(f"⚠️ Database error: {str(e)}")
                raise
            except Exception as e:
                db.rollback()
                print(f"⚠️ Unexpected error: {str(e)}")
                raise
        else:
            
            with get_db() as session:
                yield session
                
    def get_by_id(self, id: int, db: Optional[Session] = None) -> Optional[ReadSchemaType]:
        """Obtiene un registro por ID y lo devuelve directamente como ReadSchema"""
        with self._session_scope(db) as session:
            obj = session.query(self.model).get(id)
            return self.read_schema.model_validate(obj) if obj else None

    def get_all(self, db: Optional[Session] = None, filters: Optional[Dict[str, Any]] = None) -> List[ReadSchemaType]:
        """Obtiene todos los registros ya convertidos a ReadSchemas"""
        with self._session_scope(db) as session:
            query = session.query(self.model)
            if filters:
                query = query.filter_by(**filters)
            return [self.read_schema.model_validate(obj) for obj in query.all()]

    def create(self, obj_in: CreateSchemaType, db: Optional[Session] = None) -> ReadSchemaType:
        """Crea un nuevo registro desde un CreateSchema y devuelve ReadSchema"""
        with self._session_scope(db) as session:
            self._validate_create(obj_in, session)
            obj_data = obj_in.model_dump()
            db_obj = self.model(**obj_data)
            session.add(db_obj)
            session.commit()
            session.refresh(db_obj)
            return self.read_schema.model_validate(db_obj)

    def update(self, id: int, obj_in: UpdateSchemaType | Dict[str, Any], db: Optional[Session] = None) -> Optional[ReadSchemaType]:
        """Actualiza un registro y devuelve el ReadSchema actualizado"""
        with self._session_scope(db) as session:
            db_obj = session.query(self.model).get(id)
            if not db_obj:
                return None

            update_data = obj_in.model_dump(exclude_unset=True) if isinstance(obj_in, BaseModel) else obj_in
            for field, value in update_data.items():
                setattr(db_obj, field, value)
                
            session.flush()

            session.refresh(db_obj)
            return self.read_schema.model_validate(db_obj)

    def delete(self, id: int, db: Optional[Session] = None) -> bool:
        """Elimina o desactiva un registro (sin schema)"""
        with self._session_scope(db) as session:
            db_obj = session.query(self.model).get(id)
            if not db_obj:
                return False

            if hasattr(db_obj, "enable"):
                db_obj.enable = False
                session.add(db_obj)
            else:
                session.delete(db_obj)
                session.flush()

            return True

    def _validate_create(self, obj_in: CreateSchemaType, db: Optional[Session] = None):
        """Hook para validaciones adicionales al crear"""
        pass
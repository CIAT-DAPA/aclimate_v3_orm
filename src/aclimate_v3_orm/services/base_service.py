from typing import TypeVar, Generic, Type, Optional, Any, Dict, List
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager

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
    def _session_scope(self, db: Session):
        """Maneja el ciclo de vida de la sesión de forma segura"""
        try:
            yield db
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise e
        finally:
            db.close()


    # Métodos públicos que usan schemas
    def get_by_id(self, db: Session, id: int) -> Optional[ReadSchemaType]:
        """Obtiene un registro por ID y lo devuelve como ReadSchema"""
        obj = self._get_by_id(db, id)
        return ReadSchemaType.model_validate(obj) if obj else None

    def get_all(self, db: Session, filters: Optional[Dict[str, Any]] = None) -> List[ReadSchemaType]:
        """Obtiene todos los registros como ReadSchemas"""
        objs = self._get_all(db, filters)
        return [ReadSchemaType.model_validate(obj) for obj in objs]

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ReadSchemaType:
        """Crea un nuevo registro desde un CreateSchema y devuelve ReadSchema"""
        with self._session_scope(db) as session:
            self._validate_create(session, obj_in)
            obj_data = obj_in.model_dump()
            db_obj = self.model(**obj_data)
            session.add(db_obj)
            session.refresh(db_obj)
            return ReadSchemaType.model_validate(db_obj)

    def update(self, db: Session, *, id: int, obj_in: UpdateSchemaType | Dict[str, Any]) -> Optional[ReadSchemaType]:
        """Actualiza un registro y devuelve el ReadSchema actualizado"""
        with self._session_scope(db) as session:
            db_obj = session.query(self.model).get(id)
            if not db_obj:
                return None

            update_data = obj_in.model_dump(exclude_unset=True) if isinstance(obj_in, BaseModel) else obj_in
            for field, value in update_data.items():
                setattr(db_obj, field, value)
            
            session.refresh(db_obj)
            return ReadSchemaType.model_validate(db_obj)

    def delete(self, db: Session, *, id: int) -> bool:
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
            
            return True

    def _validate_create(self, db: Session, obj_in: CreateSchemaType):
        """Hook para validaciones adicionales al crear"""
        pass
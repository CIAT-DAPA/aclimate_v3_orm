from typing import TypeVar, Generic, Type, Optional, Any, Dict, List
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from ..database import get_db

T = TypeVar("T")  # SQLAlchemy Model
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
        """Get a record by ID and return it as ReadSchema"""
        with self._session_scope(db) as session:
            obj = session.query(self.model).get(id)
            return self.read_schema.model_validate(obj) if obj else None

    def get_by_ids(self, ids: List[int], db: Optional[Session] = None) -> List[ReadSchemaType]:
        """Get multiple records by their IDs"""
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(self.model.id.in_(ids)).all()
            return [self.read_schema.model_validate(obj) for obj in objs]

    def get_all(self, db: Optional[Session] = None, filters: Optional[Dict[str, Any]] = None) -> List[ReadSchemaType]:
        """Get all records already converted to ReadSchemas"""
        with self._session_scope(db) as session:
            query = session.query(self.model)
            if filters:
                query = query.filter_by(**filters)
            return [self.read_schema.model_validate(obj) for obj in query.all()]

    def paginate(self, 
                page: int = 1, 
                per_page: int = 20, 
                filters: Optional[Dict[str, Any]] = None,
                order_by: Optional[str] = None,
                order_dir: str = "asc",
                db: Optional[Session] = None) -> Dict[str, Any]:
        """
        Paginate results with optional filters and sorting
        
        Args:
            page: Page number (starts at 1)
            per_page: Items per page
            filters: Dictionary of filter conditions
            order_by: Field name to order by
            order_dir: "asc" or "desc"
            db: Optional database session
            
        Returns:
            Dictionary with items, total, page, per_page, pages
        """
        with self._session_scope(db) as session:
            query = session.query(self.model)
            
            # Apply filters
            if filters:
                query = query.filter_by(**filters)
            
            # Apply ordering
            if order_by and hasattr(self.model, order_by):
                order_column = getattr(self.model, order_by)
                if order_dir.lower() == "desc":
                    query = query.order_by(order_column.desc())
                else:
                    query = query.order_by(order_column.asc())
            
            # Get total count before pagination
            total = query.count()
            
            # Apply pagination
            objs = query.offset((page - 1) * per_page).limit(per_page).all()
            
            # Calculate total pages
            pages = (total + per_page - 1) // per_page if total > 0 else 0
            
            return {
                "items": [self.read_schema.model_validate(obj) for obj in objs],
                "total": total,
                "page": page,
                "per_page": per_page,
                "pages": pages,
                "has_prev": page > 1,
                "has_next": page < pages
            }

    def create(self, obj_in: CreateSchemaType, db: Optional[Session] = None) -> ReadSchemaType:
        """Create a new record from CreateSchema and return ReadSchema"""
        with self._session_scope(db) as session:
            self._validate_create(obj_in, session)
            obj_data = obj_in.model_dump()
            db_obj = self.model(**obj_data)
            session.add(db_obj)
            session.commit()
            session.refresh(db_obj)
            return self.read_schema.model_validate(db_obj)

    def bulk_create(self, 
                objs_in: List[CreateSchemaType], 
                batch_size: int = 1000,
                db: Optional[Session] = None) -> int:
        """
        Bulk create multiple records efficiently
        
        Args:
            objs_in: List of CreateSchema objects
            batch_size: Number of records to insert per batch
            db: Optional database session
            
        Returns:
            Number of records successfully created
        """
        if not objs_in:
            return 0
        
        created_count = 0
        
        with self._session_scope(db) as session:
            for i in range(0, len(objs_in), batch_size):
                batch = objs_in[i:i + batch_size]
                batch_data = [obj.model_dump() for obj in batch]
                
                session.bulk_insert_mappings(self.model, batch_data)
                session.flush()
                created_count += len(batch)
            
            session.commit()
        
        return created_count

    def update(self, id: int, obj_in: UpdateSchemaType | Dict[str, Any], db: Optional[Session] = None) -> Optional[ReadSchemaType]:
        """Update a record and return the updated ReadSchema"""
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
        """Delete or disable a record"""
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
        """Hook for additional validation during creation"""
        pass
from typing import List, Optional
from sqlalchemy.orm import Session
from ..services.base_service import BaseService
from ..models import MngSource
from ..schemas import MngSourceCreate, MngSourceUpdate, MngSourceRead
from ..validations import MngSourceValidator

class MngSourceService(BaseService[MngSource, MngSourceCreate, MngSourceRead, MngSourceUpdate]):
    def __init__(self):
        super().__init__(MngSource, MngSourceCreate, MngSourceRead, MngSourceUpdate)

    def get_by_type(self,
                   source_type: str,
                   enabled: bool = True,
                   db: Optional[Session] = None) -> List[MngSourceRead]:
        """Get sources by type (MA/AU)"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .filter(
                    self.model.source_type == source_type,
                    self.model.enable == enabled
                )
                .all()
            )
            return [MngSourceRead.model_validate(obj) for obj in objs]

    def get_by_name(self,
                   name: str,
                   enabled: bool = True,
                   db: Optional[Session] = None) -> List[MngSourceRead]:
        """Get sources by exact name match"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .filter(
                    self.model.name == name,
                    self.model.enable == enabled
                )
                .all()
            )
            return [MngSourceRead.model_validate(obj) for obj in objs]

    def search_by_name(self,
                      name: str,
                      enabled: bool = True,
                      db: Optional[Session] = None) -> List[MngSourceRead]:
        """Search sources by name (partial match)"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .filter(
                    self.model.name.ilike(f"%{name}%"),
                    self.model.enable == enabled
                )
                .all()
            )
            return [MngSourceRead.model_validate(obj) for obj in objs]

    def get_all(self,
               enabled: bool = True,
               db: Optional[Session] = None) -> List[MngSourceRead]:
        """Get all sources, optionally filtered by enabled status"""
        with self._session_scope(db) as session:
            query = session.query(self.model)
            if enabled is not None:
                query = query.filter(self.model.enable == enabled)
            objs = query.all()
            return [MngSourceRead.model_validate(obj) for obj in objs]

    def _validate_create(self, obj_in: MngSourceCreate, db: Optional[Session] = None):
        """Validation hook called automatically from BaseService.create()"""
        MngSourceValidator.create_validate(db, obj_in)

from typing import List, Optional
from sqlalchemy.orm import Session
from ..services.base_service import BaseService
from ..models import MngSource
from ..schemas import SourceCreate, SourceUpdate, SourceRead
from ..validations import MngSourceValidator

class MngSourceService(BaseService[MngSource, SourceCreate, SourceRead, SourceUpdate]):
    def __init__(self):
        super().__init__(MngSource, SourceCreate, SourceRead, SourceUpdate)

    def get_by_type(self,
                   source_type: str,
                   enabled: bool = True,
                   db: Optional[Session] = None) -> List[SourceRead]:
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
            return [SourceRead.model_validate(obj) for obj in objs]

    def get_by_name(self,
                   name: str,
                   enabled: bool = True,
                   db: Optional[Session] = None) -> List[SourceRead]:
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
            return [SourceRead.model_validate(obj) for obj in objs]

    def search_by_name(self,
                      name: str,
                      enabled: bool = True,
                      db: Optional[Session] = None) -> List[SourceRead]:
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
            return [SourceRead.model_validate(obj) for obj in objs]

    def get_all_enable(self,
               enabled: bool = True,
               db: Optional[Session] = None) -> List[SourceRead]:
        """Get all sources, optionally filtered by enabled status"""
        with self._session_scope(db) as session:
            query = session.query(self.model)
            if enabled is not None:
                query = query.filter(self.model.enable == enabled)
            objs = query.all()
            return [SourceRead.model_validate(obj) for obj in objs]

    def _validate_create(self, obj_in: SourceCreate, db: Optional[Session] = None):
        """Validation hook called automatically from BaseService.create()"""
        MngSourceValidator.create_validate(db, obj_in)

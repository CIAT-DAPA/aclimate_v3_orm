from typing import List, Optional
from sqlalchemy.orm import Session
from ..services.base_service import BaseService
from ..models import MngIndicator, MngIndicatorCategory
from ..validations import IndicatorValidator
from ..schemas import (
    IndicatorCreate,
    IndicatorRead,
    IndicatorUpdate
)

class MngIndicatorService(
    BaseService[
        MngIndicator,
        IndicatorCreate,
        IndicatorRead,
        IndicatorUpdate
    ]
):
    def __init__(self):
        super().__init__(MngIndicator, IndicatorCreate, IndicatorRead, IndicatorUpdate)

    def get_by_name(self, name: str, enabled: bool = True, db: Optional[Session] = None) -> List[IndicatorRead]:
        """Get indicators by exact name match"""
        with self._session_scope(db) as session:
            objs = session.query(self.model)\
                .filter(
                    self.model.name == name,
                    self.model.enable == enabled
                )\
                .all()
            return [IndicatorRead.model_validate(obj) for obj in objs]

    def get_by_short_name(self, short_name: str, enabled: bool = True, db: Optional[Session] = None) -> List[IndicatorRead]:
        """Get indicators by exact short name match"""
        with self._session_scope(db) as session:
            objs = session.query(self.model)\
                .filter(
                    self.model.short_name == short_name,
                    self.model.enable == enabled
                )\
                .all()
            return [IndicatorRead.model_validate(obj) for obj in objs]

    def get_by_type(self, type: str, enabled: bool = True, db: Optional[Session] = None) -> List[IndicatorRead]:
        """Get indicators by type"""
        with self._session_scope(db) as session:
            objs = session.query(self.model)\
                .filter(
                    self.model.type == type,
                    self.model.enable == enabled
                )\
                .all()
            return [IndicatorRead.model_validate(obj) for obj in objs]

    def get_by_temporality(self, temporality: str, db: Optional[Session] = None) -> List[IndicatorRead]:
        """Get records by temporality type"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .filter(self.model.temporality == temporality)
                .all()
            )
            return [IndicatorRead.model_validate(obj) for obj in objs]

    def get_all_enabled(self, db: Optional[Session] = None, enabled: bool = True) -> List[IndicatorRead]:
        """Get all indicators filtered by enabled status"""
        with self._session_scope(db) as session:
            query = session.query(self.model)
            if enabled is not None:
                query = query.filter(self.model.enable == enabled)
            objs = query.all()
            return [IndicatorRead.model_validate(obj) for obj in objs]
        
    def get_by_category_id(self, category_id: int, enabled: bool = True, db: Optional[Session] = None) -> List[IndicatorRead]:
        """Get indicators by category ID"""
        with self._session_scope(db) as session:
            objs = session.query(self.model)\
                .filter(
                    self.model.indicator_category_id == category_id,
                    self.model.enable == enabled
                )\
                .all()
            return [IndicatorRead.model_validate(obj) for obj in objs]

    def get_by_category_name(self,
                            category_name: str,
                            enabled: bool = True,
                            db: Optional[Session] = None) -> List[IndicatorRead]:
        """Get indicators by category name"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .join(MngIndicatorCategory)
                .filter(
                    MngIndicatorCategory.name == category_name,
                    self.model.enable == enabled
                )
                .all()
            )
            return [IndicatorRead.model_validate(obj) for obj in objs]

    def _validate_create(self, obj_in: IndicatorCreate, db: Optional[Session] = None):
        """Automatic validation called from BaseService.create()"""
        IndicatorValidator.validate_name(db, obj_in.name)
        IndicatorValidator.validate_short_name(db, obj_in.short_name)
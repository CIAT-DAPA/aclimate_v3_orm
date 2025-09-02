from typing import List, Optional
from sqlalchemy.orm import Session
from ..services.base_service import BaseService
from ..models import MngIndicatorCategory
from ..validations import MngIndicatorCategoryValidator
from ..schemas.mng_indicator_category_schema import (
    IndicatorCategoryCreate,
    IndicatorCategoryRead,
    IndicatorCategoryUpdate
)

class MngIndicatorCategoryService(
    BaseService[MngIndicatorCategory, IndicatorCategoryCreate, IndicatorCategoryRead, IndicatorCategoryUpdate]
):
    def __init__(self):
        super().__init__(MngIndicatorCategory, IndicatorCategoryCreate, IndicatorCategoryRead, IndicatorCategoryUpdate)

    def get_by_name(self, name: str, db: Optional[Session] = None) -> Optional[IndicatorCategoryRead]:
        """Get category by name"""
        with self._session_scope(db) as session:
            obj = session.query(self.model).filter(
                self.model.name == name
            ).first()
            return IndicatorCategoryRead.model_validate(obj) if obj else None

    def get_all_enable(self, db: Optional[Session] = None, enabled: bool = True) -> List[IndicatorCategoryRead]:
        """Get all categories filtered by enabled status"""
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(
                self.model.enable == enabled
            ).all()
            return [IndicatorCategoryRead.model_validate(obj) for obj in objs]

    def _validate_create(self, obj_in: IndicatorCategoryCreate, db: Optional[Session] = None):
        """Automatic validation called from BaseService.create()"""
        MngIndicatorCategoryValidator.create_validate(db, obj_in)

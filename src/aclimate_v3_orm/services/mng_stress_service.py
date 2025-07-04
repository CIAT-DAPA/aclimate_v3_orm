from typing import List, Optional
from sqlalchemy.orm import Session
from ..services.base_service import BaseService
from ..models import MngStress
from ..schemas import StressCreate, StressUpdate, StressRead
from ..enums import StressCategory
from ..validations import MngStressValidator

class MngStressService(BaseService[MngStress, StressCreate, StressRead, StressUpdate]):
    def __init__(self):
        super().__init__(MngStress, StressCreate, StressRead, StressUpdate)

    def get_by_category(self, category: StressCategory, db: Optional[Session] = None) -> List[StressRead]:
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(self.model.category == category).all()
            return [StressRead.model_validate(obj) for obj in objs]

    def _validate_create(self, obj_in: StressCreate, db: Optional[Session] = None):
        MngStressValidator.create_validate(db, obj_in)
from typing import List, Optional
from sqlalchemy.orm import Session
from ..services.base_service import BaseService
from ..models import MngPhenologicalStage
from ..schemas import PhenologicalStageCreate, PhenologicalStageUpdate, PhenologicalStageRead
from ..validations import MngPhenologicalStageValidator

class MngPhenologicalStageService(BaseService[MngPhenologicalStage, PhenologicalStageCreate, PhenologicalStageRead, PhenologicalStageUpdate]):
    def __init__(self):
        super().__init__(MngPhenologicalStage, PhenologicalStageCreate, PhenologicalStageRead, PhenologicalStageUpdate)

    def get_by_crop(self, crop_id: int, db: Optional[Session] = None) -> List[PhenologicalStageRead]:
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(self.model.crop_id == crop_id).all()
            return [PhenologicalStageRead.model_validate(obj) for obj in objs]

    def _validate_create(self, obj_in: PhenologicalStageCreate, db: Optional[Session] = None):
        MngPhenologicalStageValidator.create_validate(db, obj_in)
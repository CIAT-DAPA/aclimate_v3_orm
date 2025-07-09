from typing import List, Optional
from sqlalchemy.orm import Session
from ..services.base_service import BaseService
from ..models import PhenologicalStageStress
from ..schemas import (
    PhenologicalStageStressCreate,
    PhenologicalStageStressUpdate,
    PhenologicalStageStressRead
)
from ..validations import PhenologicalStageStressValidator

class PhenologicalStageStressService(
    BaseService[
        PhenologicalStageStress,
        PhenologicalStageStressCreate,
        PhenologicalStageStressRead,
        PhenologicalStageStressUpdate
    ]
):
    def __init__(self):
        super().__init__(
            PhenologicalStageStress,
            PhenologicalStageStressCreate,
            PhenologicalStageStressRead,
            PhenologicalStageStressUpdate
        )

    def get_by_stress(self, stress_id: int, db: Optional[Session] = None) -> List[PhenologicalStageStressRead]:
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(self.model.stress_id == stress_id).all()
            return [PhenologicalStageStressRead.model_validate(obj) for obj in objs]

    def get_by_phenological_stage(self, phenological_stage_id: int, db: Optional[Session] = None) -> List[PhenologicalStageStressRead]:
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(self.model.phenological_stage_id == phenological_stage_id).all()
            return [PhenologicalStageStressRead.model_validate(obj) for obj in objs]

    def _validate_create(self, obj_in: PhenologicalStageStressCreate, db: Optional[Session] = None):
        PhenologicalStageStressValidator.create_validate(db, obj_in)
from typing import List, Optional
from sqlalchemy.orm import Session
from ..services.base_service import BaseService
from ..models import Season
from ..schemas import SeasonCreate, SeasonUpdate, SeasonRead
from ..validations import SeasonValidator

class SeasonService(BaseService[Season, SeasonCreate, SeasonRead, SeasonUpdate]):
    def __init__(self):
        super().__init__(Season, SeasonCreate, SeasonRead, SeasonUpdate)

    def get_by_location(self, location_id: int, db: Optional[Session] = None) -> List[SeasonRead]:
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(self.model.location_id == location_id).all()
            return [SeasonRead.model_validate(obj) for obj in objs]

    def get_by_crop(self, crop_id: int, db: Optional[Session] = None) -> List[SeasonRead]:
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(self.model.crop_id == crop_id).all()
            return [SeasonRead.model_validate(obj) for obj in objs]

    def _validate_create(self, obj_in: SeasonCreate, db: Optional[Session] = None):
        SeasonValidator.create_validate(db, obj_in)
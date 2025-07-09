from typing import List, Optional
from sqlalchemy.orm import Session
from ..services.base_service import BaseService
from ..models import ForecastAnalogue
from ..schemas import ForecastAnalogueCreate, ForecastAnalogueUpdate, ForecastAnalogueRead
from ..validations import ForecastAnalogueValidator

class ForecastAnalogueService(BaseService[ForecastAnalogue, ForecastAnalogueCreate, ForecastAnalogueRead, ForecastAnalogueUpdate]):
    def __init__(self):
        super().__init__(ForecastAnalogue, ForecastAnalogueCreate, ForecastAnalogueRead, ForecastAnalogueUpdate)

    def get_by_forecast(self, forecast_id: int, db: Optional[Session] = None) -> List[ForecastAnalogueRead]:
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(self.model.forecast_id == forecast_id).all()
            return [ForecastAnalogueRead.model_validate(obj) for obj in objs]

    def get_by_location(self, location_id: int, db: Optional[Session] = None) -> List[ForecastAnalogueRead]:
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(self.model.location_id == location_id).all()
            return [ForecastAnalogueRead.model_validate(obj) for obj in objs]

    def _validate_create(self, obj_in: ForecastAnalogueCreate, db: Optional[Session] = None):
        ForecastAnalogueValidator.create_validate(db, obj_in)
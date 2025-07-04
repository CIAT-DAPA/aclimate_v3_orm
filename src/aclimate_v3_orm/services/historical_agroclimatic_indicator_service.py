from typing import List, Optional
from sqlalchemy.orm import Session
from ..services.base_service import BaseService
from ..models import HistoricalAgroclimaticIndicator
from ..schemas import (
    HistoricalAgroclimaticIndicatorCreate,
    HistoricalAgroclimaticIndicatorUpdate,
    HistoricalAgroclimaticIndicatorRead
)
from ..validations import HistoricalAgroclimaticIndicatorValidator

class HistoricalAgroclimaticIndicatorService(
    BaseService[
        HistoricalAgroclimaticIndicator,
        HistoricalAgroclimaticIndicatorCreate,
        HistoricalAgroclimaticIndicatorRead,
        HistoricalAgroclimaticIndicatorUpdate
    ]
):
    def __init__(self):
        super().__init__(
            HistoricalAgroclimaticIndicator,
            HistoricalAgroclimaticIndicatorCreate,
            HistoricalAgroclimaticIndicatorRead,
            HistoricalAgroclimaticIndicatorUpdate
        )

    def get_by_location(self, location_id: int, db: Optional[Session] = None) -> List[HistoricalAgroclimaticIndicatorRead]:
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(self.model.location_id == location_id).all()
            return [HistoricalAgroclimaticIndicatorRead.model_validate(obj) for obj in objs]

    def get_by_indicator(self, indicator_id: int, db: Optional[Session] = None) -> List[HistoricalAgroclimaticIndicatorRead]:
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(self.model.indicator_id == indicator_id).all()
            return [HistoricalAgroclimaticIndicatorRead.model_validate(obj) for obj in objs]

    def _validate_create(self, obj_in: HistoricalAgroclimaticIndicatorCreate, db: Optional[Session] = None):
        HistoricalAgroclimaticIndicatorValidator.create_validate(db, obj_in)
from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Session
from ..services.base_service import BaseService
from ..models import Forecast
from ..schemas import ForecastCreate, ForecastRead, ForecastUpdate
from ..validations import ForecastValidator

class ForecastService(BaseService[Forecast, ForecastCreate, ForecastRead, ForecastUpdate]):
    def __init__(self):
        super().__init__(Forecast, ForecastCreate, ForecastRead, ForecastUpdate)

    def get_by_run_date(self, 
                       run_date: date,
                       enabled: bool = True,
                       db: Optional[Session] = None) -> List[ForecastRead]:
        """Get forecasts by exact run date"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .filter(
                    self.model.run_date == run_date,
                    self.model.enable == enabled
                )
                .all()
            )
            return [ForecastRead.model_validate(obj) for obj in objs]
    
    def get_by_date_range(self,
                         start_date: date,
                         end_date: date,
                         enabled: bool = True,
                         db: Optional[Session] = None) -> List[ForecastRead]:
        """Get forecasts within a date range"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .filter(
                    self.model.run_date >= start_date,
                    self.model.run_date <= end_date,
                    self.model.enable == enabled
                )
                .all()
            )
            return [ForecastRead.model_validate(obj) for obj in objs]

    def _validate_create(self, obj_in: ForecastCreate, db: Optional[Session] = None):
        """Validation hook for create"""
        ForecastValidator.create_validate(db, obj_in)
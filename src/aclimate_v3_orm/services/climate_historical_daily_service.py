from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from services.base_service import BaseService
from models import ClimateHistoricalDaily
from validations import ClimateHistoricalDailyValidator
from schemas import (
    ClimateHistoricalDailyCreate,
    ClimateHistoricalDailyUpdate,
    ClimateHistoricalDailyRead
)

class ClimateHistoricalDailyService(
    BaseService[
        ClimateHistoricalDaily,
        ClimateHistoricalDailyCreate,
        ClimateHistoricalDailyRead,
        ClimateHistoricalDailyUpdate
    ]
):
    def __init__(self):
        super().__init__(ClimateHistoricalDaily, ClimateHistoricalDailyCreate, ClimateHistoricalDailyRead, ClimateHistoricalDailyUpdate)

    def get_by_location_id(self, location_id: int, db: Optional[Session] = None) -> List[ClimateHistoricalDailyRead]:
        with self._session_scope(db) as session:
            results = (
                session.query(self.model)
                .filter(self.model.location_id == location_id)
                .all()
            )
            return [ClimateHistoricalDailyRead.model_validate(obj) for obj in results]

    def get_by_location_name(self, location_name: str, db: Optional[Session] = None) -> List[ClimateHistoricalDailyRead]:
        with self._session_scope(db) as session:
            results = (
                session.query(self.model)
                .join(self.model.location)
                .filter(self.model.location.name == location_name)
                .all()
            )
            return [ClimateHistoricalDailyRead.model_validate(obj) for obj in results]

    def get_by_country_id(self, country_id: int, db: Optional[Session] = None) -> List[ClimateHistoricalDailyRead]:
        with self._session_scope(db) as session:
            results = (
                session.query(self.model)
                .join(self.model.location)
                .join(self.model.location.admin_2)
                .join(self.model.location.admin_2.admin_1)
                .join(self.model.location.admin_2.admin_1.country)
                .filter(self.model.location.admin_2.admin_1.country_id == country_id)
                .all()
            )
            return [ClimateHistoricalDailyRead.model_validate(obj) for obj in results]

    def get_by_country_name(self, country_name: str, db: Optional[Session] = None) -> List[ClimateHistoricalDailyRead]:
        with self._session_scope(db) as session:
            results = (
                session.query(self.model)
                .join(self.model.location)
                .join(self.model.location.admin_2)
                .join(self.model.location.admin_2.admin_1)
                .join(self.model.location.admin_2.admin_1.country)
                .filter(self.model.location.admin_2.admin_1.country.name == country_name)
                .all()
            )
            return [ClimateHistoricalDailyRead.model_validate(obj) for obj in results]

    def get_by_admin1_id(self, admin1_id: int, db: Optional[Session] = None) -> List[ClimateHistoricalDailyRead]:
        with self._session_scope(db) as session:
            results = (
                session.query(self.model)
                .join(self.model.location)
                .join(self.model.location.admin_2)
                .join(self.model.location.admin_2.admin_1)
                .filter(self.model.location.admin_2.admin_1_id == admin1_id)
                .all()
            )
            return [ClimateHistoricalDailyRead.model_validate(obj) for obj in results]

    def get_by_admin1_name(self, admin1_name: str, db: Optional[Session] = None) -> List[ClimateHistoricalDailyRead]:
        with self._session_scope(db) as session:
            results = (
                session.query(self.model)
                .join(self.model.location)
                .join(self.model.location.admin_2)
                .join(self.model.location.admin_2.admin_1)
                .filter(self.model.location.admin_2.admin_1.name == admin1_name)
                .all()
            )
            return [ClimateHistoricalDailyRead.model_validate(obj) for obj in results]

    def get_by_measure_id(self, measure_id: int, db: Optional[Session] = None) -> List[ClimateHistoricalDailyRead]:
        with self._session_scope(db) as session:
            results = (
                session.query(self.model)
                .filter(self.model.measure_id == measure_id)
                .all()
            )
            return [ClimateHistoricalDailyRead.model_validate(obj) for obj in results]

    def get_by_measure_name(self, measure_name: str, db: Optional[Session] = None) -> List[ClimateHistoricalDailyRead]:
        with self._session_scope(db) as session:
            results = (
                session.query(self.model)
                .join(self.model.measure)
                .filter(self.model.measure.name == measure_name)
                .all()
            )
            return [ClimateHistoricalDailyRead.model_validate(obj) for obj in results]

    def get_by_date(self, specific_date: date, db: Optional[Session] = None) -> List[ClimateHistoricalDailyRead]:
        with self._session_scope(db) as session:
            results = (
                session.query(self.model)
                .filter(self.model.date == specific_date)
                .all()
            )
            return [ClimateHistoricalDailyRead.model_validate(obj) for obj in results]

    def get_by_date_range(self, start_date: date, end_date: date, db: Optional[Session] = None) -> List[ClimateHistoricalDailyRead]:
        with self._session_scope(db) as session:
            results = (
                session.query(self.model)
                .filter(
                    self.model.date >= start_date,
                    self.model.date <= end_date
                )
                .all()
            )
            return [ClimateHistoricalDailyRead.model_validate(obj) for obj in results]

    def _validate_create(self, obj_in: ClimateHistoricalDailyCreate, db: Optional[Session] = None):
        ClimateHistoricalDailyValidator.create_validate(db, obj_in)

from typing import List
from datetime import date
from sqlalchemy.orm import Session
from services.base_service import BaseService
from models import ClimateHistoricalMonthly
from validations import ClimateHistoricalMonthlyValidator
from schemas import (
    ClimateHistoricalMonthlyCreate,
    ClimateHistoricalMonthlyUpdate,
    ClimateHistoricalMonthlyRead
)

class ClimateHistoricalMonthlyService(
    BaseService[
        ClimateHistoricalMonthly,
        ClimateHistoricalMonthlyCreate,
        ClimateHistoricalMonthlyRead,
        ClimateHistoricalMonthlyUpdate
    ]
):
    def __init__(self):
        super().__init__(ClimateHistoricalMonthly, ClimateHistoricalMonthlyCreate, ClimateHistoricalMonthlyRead, ClimateHistoricalMonthlyUpdate)

    def get_by_location_id(self, db: Session, location_id: int) -> List[ClimateHistoricalMonthlyRead]:
        """Get monthly records by location ID"""
        with self._session_scope(db) as session:
            results = (
                session.query(self.model)
                .filter(self.model.location_id == location_id)
                .all()
            )
            return [ClimateHistoricalMonthlyRead.model_validate(obj) for obj in results]

    def get_by_location_name(self, db: Session, location_name: str) -> List[ClimateHistoricalMonthlyRead]:
        """Get monthly records by location name"""
        with self._session_scope(db) as session:
            results = (
                session.query(self.model)
                .join(self.model.location)
                .filter(self.model.location.name == location_name)
                .all()
            )
            return [ClimateHistoricalMonthlyRead.model_validate(obj) for obj in results]

    def get_by_country_id(self, db: Session, country_id: int) -> List[ClimateHistoricalMonthlyRead]:
        """Get monthly records by country ID"""
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
            return [ClimateHistoricalMonthlyRead.model_validate(obj) for obj in results]

    def get_by_country_name(self, db: Session, country_name: str) -> List[ClimateHistoricalMonthlyRead]:
        """Get monthly records by country name"""
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
            return [ClimateHistoricalMonthlyRead.model_validate(obj) for obj in results]

    def get_by_admin1_id(self, db: Session, admin1_id: int) -> List[ClimateHistoricalMonthlyRead]:
        """Get monthly records by admin1 region ID"""
        with self._session_scope(db) as session:
            results = (
                session.query(self.model)
                .join(self.model.location)
                .join(self.model.location.admin_2)
                .join(self.model.location.admin_2.admin_1)
                .filter(self.model.location.admin_2.admin_1_id == admin1_id)
                .all()
            )
            return [ClimateHistoricalMonthlyRead.model_validate(obj) for obj in results]

    def get_by_admin1_name(self, db: Session, admin1_name: str) -> List[ClimateHistoricalMonthlyRead]:
        """Get monthly records by admin1 region name"""
        with self._session_scope(db) as session:
            results = (
                session.query(self.model)
                .join(self.model.location)
                .join(self.model.location.admin_2)
                .join(self.model.location.admin_2.admin_1)
                .filter(self.model.location.admin_2.admin_1.name == admin1_name)
                .all()
            )
            return [ClimateHistoricalMonthlyRead.model_validate(obj) for obj in results]

    def get_by_measure_id(self, db: Session, measure_id: int) -> List[ClimateHistoricalMonthlyRead]:
        """Get monthly records by measure ID"""
        with self._session_scope(db) as session:
            results = (
                session.query(self.model)
                .filter(self.model.measure_id == measure_id)
                .all()
            )
            return [ClimateHistoricalMonthlyRead.model_validate(obj) for obj in results]

    def get_by_measure_name(self, db: Session, measure_name: str) -> List[ClimateHistoricalMonthlyRead]:
        """Get monthly records by measure name"""
        with self._session_scope(db) as session:
            results = (
                session.query(self.model)
                .join(self.model.measure)
                .filter(self.model.measure.name == measure_name)
                .all()
            )
            return [ClimateHistoricalMonthlyRead.model_validate(obj) for obj in results]

    def get_by_date(self, db: Session, year: int, month: int) -> List[ClimateHistoricalMonthlyRead]:
        """Get monthly records by specific year and month"""
        with self._session_scope(db) as session:
            target_date = date(year, month, 1)
            results = (
                session.query(self.model)
                .filter(self.model.date == target_date)
                .all()
            )
            return [ClimateHistoricalMonthlyRead.model_validate(obj) for obj in results]

    def get_by_date_range(self, db: Session, 
                        start_date: date, 
                        end_date: date) -> List[ClimateHistoricalMonthlyRead]:
        """Get monthly records within date range (inclusive)"""
        with self._session_scope(db) as session:
            # Ensure we're comparing month-start dates
            start_month = start_date.replace(day=1)
            end_month = end_date.replace(day=1)
            results = (
                session.query(self.model)
                .filter(
                    self.model.date >= start_month,
                    self.model.date <= end_month
                )
                .all()
            )
            return [ClimateHistoricalMonthlyRead.model_validate(obj) for obj in results]

    def _validate_create(self, db: Session, obj_in: ClimateHistoricalMonthlyCreate):
        """Automatic validation called from BaseService.create()"""
        ClimateHistoricalMonthlyValidator.create_validate(db, obj_in)

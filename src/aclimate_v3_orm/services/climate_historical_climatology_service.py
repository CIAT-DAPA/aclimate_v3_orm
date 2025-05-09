from typing import List
from sqlalchemy.orm import Session
from services.base_service import BaseService
from models import ClimateHistoricalClimatology
from validations import ClimateHistoricalClimatologyValidator
from schemas import (
    ClimateHistoricalClimatologyCreate,
    ClimateHistoricalClimatologyUpdate,
    ClimateHistoricalClimatologyRead
)

class ClimateHistoricalClimatologyService(
    BaseService[
        ClimateHistoricalClimatology,
        ClimateHistoricalClimatologyCreate,
        ClimateHistoricalClimatologyRead,
        ClimateHistoricalClimatologyUpdate
    ]
):
    def __init__(self):
        super().__init__(ClimateHistoricalClimatology, ClimateHistoricalClimatologyCreate, ClimateHistoricalClimatologyRead, ClimateHistoricalClimatologyUpdate)

    def get_by_location_id(self, db: Session, location_id: int) -> List[ClimateHistoricalClimatologyRead]:
        """Get records by location ID"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .filter(self.model.location_id == location_id)
                .all()
            )
            return [ClimateHistoricalClimatologyRead.model_validate(obj) for obj in objs]

    def get_by_location_name(self, db: Session, location_name: str) -> List[ClimateHistoricalClimatologyRead]:
        """Get records by location name"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .join(self.model.location)
                .filter(self.model.location.name == location_name)
                .all()
            )
            return [ClimateHistoricalClimatologyRead.model_validate(obj) for obj in objs]

    def get_by_country_id(self, db: Session, country_id: int) -> List[ClimateHistoricalClimatologyRead]:
        """Get records by country ID"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .join(self.model.location)
                .join(self.model.location.admin_2)
                .join(self.model.location.admin_2.admin_1)
                .join(self.model.location.admin_2.admin_1.country)
                .filter(self.model.location.admin_2.admin_1.country_id == country_id)
                .all()
            )
            return [ClimateHistoricalClimatologyRead.model_validate(obj) for obj in objs]

    def get_by_country_name(self, db: Session, country_name: str) -> List[ClimateHistoricalClimatologyRead]:
        """Get records by country name"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .join(self.model.location)
                .join(self.model.location.admin_2)
                .join(self.model.location.admin_2.admin_1)
                .join(self.model.location.admin_2.admin_1.country)
                .filter(self.model.location.admin_2.admin_1.country.name == country_name)
                .all()
            )
            return [ClimateHistoricalClimatologyRead.model_validate(obj) for obj in objs]

    def get_by_admin1_id(self, db: Session, admin1_id: int) -> List[ClimateHistoricalClimatologyRead]:
        """Get records by admin1 region ID"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .join(self.model.location)
                .join(self.model.location.admin_2)
                .join(self.model.location.admin_2.admin_1)
                .filter(self.model.location.admin_2.admin_1_id == admin1_id)
                .all()
            )
            return [ClimateHistoricalClimatologyRead.model_validate(obj) for obj in objs]

    def get_by_admin1_name(self, db: Session, admin1_name: str) -> List[ClimateHistoricalClimatologyRead]:
        """Get records by admin1 region name"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .join(self.model.location)
                .join(self.model.location.admin_2)
                .join(self.model.location.admin_2.admin_1)
                .filter(self.model.location.admin_2.admin_1.name == admin1_name)
                .all()
            )
            return [ClimateHistoricalClimatologyRead.model_validate(obj) for obj in objs]

    def get_by_month(self, db: Session, month: int) -> List[ClimateHistoricalClimatologyRead]:
        """Get records by month (1-12)"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .filter(self.model.month == month)
                .all()
            )
            return [ClimateHistoricalClimatologyRead.model_validate(obj) for obj in objs]

    def get_by_measure_id(self, db: Session, measure_id: int) -> List[ClimateHistoricalClimatologyRead]:
        """Get records by measure id"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .filter(self.model.measure_id == measure_id)
                .all()
            )
            return [ClimateHistoricalClimatologyRead.model_validate(obj) for obj in objs]

    def get_by_measure_name(self, db: Session, measure_name: str) -> List[ClimateHistoricalClimatologyRead]:
        """Get records by measure name"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .join(self.model.measure)
                .filter(self.model.measure.name == measure_name)
                .all()
            )
            return [ClimateHistoricalClimatologyRead.model_validate(obj) for obj in objs]

    def _validate_create(self, db: Session, obj_in: ClimateHistoricalClimatologyCreate):
        """Automatic validation called from BaseService.create()"""
        ClimateHistoricalClimatologyValidator.create_validate(db, obj_in)

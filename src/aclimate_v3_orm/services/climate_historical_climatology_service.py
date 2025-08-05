from typing import List, Optional
from sqlalchemy.orm import Session
from ..services.base_service import BaseService
from ..models import ClimateHistoricalClimatology, MngLocation, MngClimateMeasure, MngAdmin1, MngAdmin2, MngCountry
from ..validations import ClimateHistoricalClimatologyValidator
from sqlalchemy.sql import func
from ..schemas import (
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

    def get_by_location_id(self, location_id: int, db: Optional[Session] = None) -> List[ClimateHistoricalClimatologyRead]:
        """Get records by location ID"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .filter(self.model.location_id == location_id)
                .all()
            )
            return [ClimateHistoricalClimatologyRead.model_validate(obj) for obj in objs]

    def get_by_location_name(self, location_name: str, db: Optional[Session] = None) -> List[ClimateHistoricalClimatologyRead]:
        """Get records by location name"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .join(self.model.location)
                .filter(MngLocation.name == location_name)
                .all()
            )
            return [ClimateHistoricalClimatologyRead.model_validate(obj) for obj in objs]

    def get_by_country_id(self, country_id: int, db: Optional[Session] = None) -> List[ClimateHistoricalClimatologyRead]:
        """Get records by country ID"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .join(self.model.location)
                .join(MngLocation.admin_2)
                .join(MngAdmin2.admin_1)
                .filter(MngAdmin1.country_id == country_id)
                .all()
            )
            return [ClimateHistoricalClimatologyRead.model_validate(obj) for obj in objs]

    def get_by_country_name(self, country_name: str, db: Optional[Session] = None ) -> List[ClimateHistoricalClimatologyRead]:
        """Get records by country name"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .join(self.model.location)
                .join(MngLocation.admin_2)
                .join(MngAdmin2.admin_1)
                .join(MngAdmin1.country)
                .filter(MngCountry.name == country_name)
                .all()
            )
            return [ClimateHistoricalClimatologyRead.model_validate(obj) for obj in objs]

    def get_by_admin1_id(self, admin1_id: int, db: Optional[Session] = None) -> List[ClimateHistoricalClimatologyRead]:
        """Get records by admin1 region ID"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .join(self.model.location)
                .join(MngLocation.admin_2)
                .filter(MngAdmin2.admin_1_id == admin1_id)
                .all()
            )
            return [ClimateHistoricalClimatologyRead.model_validate(obj) for obj in objs]

    def get_by_admin1_name(self, admin1_name: str, db: Optional[Session] = None) -> List[ClimateHistoricalClimatologyRead]:
        """Get records by admin1 region name"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .join(self.model.location)
                .join(MngLocation.admin_2)
                .join(MngAdmin2.admin_1)
                .filter(MngAdmin1.name == admin1_name)
                .all()
            )
            return [ClimateHistoricalClimatologyRead.model_validate(obj) for obj in objs]

    def get_by_month(self, month: int, db: Optional[Session] = None) -> List[ClimateHistoricalClimatologyRead]:
        """Get records by month (1-12)"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .filter(self.model.month == month)
                .all()
            )
            return [ClimateHistoricalClimatologyRead.model_validate(obj) for obj in objs]

    def get_by_measure_id(self, measure_id: int, db: Optional[Session] = None) -> List[ClimateHistoricalClimatologyRead]:
        """Get records by measure id"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .filter(self.model.measure_id == measure_id)
                .all()
            )
            return [ClimateHistoricalClimatologyRead.model_validate(obj) for obj in objs]
    def get_date_range_by_location_id(self, location_id: int, db: Optional[Session] = None):
        """
        Get the minimum and maximum month for a given location ID.
        """
        with self._session_scope(db) as session:
            min_month, max_month = session.query(
                func.min(self.model.month),
                func.max(self.model.month)
            ).filter(self.model.location_id == location_id).one()
            return {"location_id": location_id, "min_month": min_month, "max_month": max_month}

    def get_by_measure_name(self, measure_name: str, db: Optional[Session] = None) -> List[ClimateHistoricalClimatologyRead]:
        """Get records by measure name"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .join(ClimateHistoricalClimatology.measure)
                .filter(MngClimateMeasure.name == measure_name)
                .all()
            )
            return [ClimateHistoricalClimatologyRead.model_validate(obj) for obj in objs]
        
    def get_max_min_by_location_id(self, location_id: int, db: Optional[Session] = None) -> List[dict]:
        """
        Returns a list of dicts with min/max value and month for each measure_id at a given location_id.
        Each dict contains: measure_id, measure_name, location_id, location_name, min_value, min_month, max_value, max_month
        """
        with self._session_scope(db) as session:
            measures = session.query(self.model.measure_id).filter(self.model.location_id == location_id).distinct().all()
            result = []
            for (measure_id,) in measures:
                min_record = session.query(self.model).filter(
                    self.model.location_id == location_id,
                    self.model.measure_id == measure_id
                ).order_by(self.model.month.asc()).first()
                max_record = session.query(self.model).filter(
                    self.model.location_id == location_id,
                    self.model.measure_id == measure_id
                ).order_by(self.model.month.desc()).first()
                if min_record and max_record:
                    result.append({
                        "measure_id": measure_id,
                        "measure_name": getattr(min_record.measure, "name", None),
                        "location_id": location_id,
                        "location_name": getattr(min_record.location, "name", None),
                        "min_value": min_record.value,
                        "min_month": min_record.month,
                        "max_value": max_record.value,
                        "max_month": max_record.month
                    })
            return result

    def _validate_create(self, obj_in: ClimateHistoricalClimatologyCreate, db: Optional[Session] = None):
        """Automatic validation called from BaseService.create()"""
        ClimateHistoricalClimatologyValidator.create_validate(db, obj_in)

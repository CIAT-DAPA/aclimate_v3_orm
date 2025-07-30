from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import date
from ..services.base_service import BaseService
from ..models import ClimateHistoricalIndicator, MngLocation, MngIndicator
from ..validations import MngClimateMeasureNameValidator
from ..schemas import (
    ClimateHistoricalIndicatorCreate,
    ClimateHistoricalIndicatorRead,
    ClimateHistoricalIndicatorUpdate
)

class ClimateHistoricalIndicatorService(
    BaseService[
        ClimateHistoricalIndicator,
        ClimateHistoricalIndicatorCreate,
        ClimateHistoricalIndicatorRead,
        ClimateHistoricalIndicatorUpdate
    ]
):
    def __init__(self):
        super().__init__(ClimateHistoricalIndicator, ClimateHistoricalIndicatorCreate, ClimateHistoricalIndicatorRead, ClimateHistoricalIndicatorUpdate)

    def get_by_indicator_id(self, indicator_id: int, db: Optional[Session] = None) -> List[ClimateHistoricalIndicatorRead]:
        """Get records by indicator ID"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .filter(self.model.indicator_id == indicator_id)
                .all()
            )
            return [ClimateHistoricalIndicatorRead.model_validate(obj) for obj in objs]
        
    def get_by_indicator_name(self, indicator_name: str, db: Optional[Session] = None) -> List[ClimateHistoricalIndicatorRead]:
        """Get records by indicator name"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .join(self.model.indicator)
                .filter(MngIndicator.name == indicator_name)
                .all()
            )
            return [ClimateHistoricalIndicatorRead.model_validate(obj) for obj in objs]

    def get_by_location_and_indicator_name(self, location_name: str, indicator_name: str, db: Optional[Session] = None) -> List[ClimateHistoricalIndicatorRead]:
        """Get records by location name and indicator name"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .join(self.model.indicator)
                .join(self.model.location)
                .filter(
                    MngLocation.name == location_name,
                    MngIndicator.name == indicator_name
                )
                .all()
            )
            return [ClimateHistoricalIndicatorRead.model_validate(obj) for obj in objs]

    def get_by_location_id(self, location_id: int, db: Optional[Session] = None) -> List[ClimateHistoricalIndicatorRead]:
        """Get records by location ID"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .filter(self.model.location_id == location_id)
                .all()
            )
            return [ClimateHistoricalIndicatorRead.model_validate(obj) for obj in objs]

    def get_by_period(self, period: str, db: Optional[Session] = None) -> List[ClimateHistoricalIndicatorRead]:
        """Get records by period type"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .filter(self.model.period == period)
                .all()
            )
            return [ClimateHistoricalIndicatorRead.model_validate(obj) for obj in objs]

    def get_by_date_range(self, start_date: date, end_date: date, db: Optional[Session] = None) -> List[ClimateHistoricalIndicatorRead]:
        """Get records within a date range (inclusive)"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .filter(
                    self.model.start_date >= start_date,
                    self.model.end_date <= end_date
                )
                .all()
            )
            return [ClimateHistoricalIndicatorRead.model_validate(obj) for obj in objs]

    def get_by_indicator_and_location(self, indicator_id: int, location_id: int, db: Optional[Session] = None) -> List[ClimateHistoricalIndicatorRead]:
        """Get records by indicator and location combination"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .filter(
                    self.model.indicator_id == indicator_id,
                    self.model.location_id == location_id
                )
                .all()
            )
            return [ClimateHistoricalIndicatorRead.model_validate(obj) for obj in objs]

    def _validate_create(self, obj_in: ClimateHistoricalIndicatorCreate, db: Optional[Session] = None):
        """Automatic validation called from BaseService.create()"""
        print(obj_in)
        # Validate indicator exists
        if not db.query(ClimateHistoricalIndicator).filter(ClimateHistoricalIndicator.id == obj_in.indicator_id).first():
            raise ValueError(f"No indicator found with ID {obj_in.indicator_id}")
        
        # Validate location exists
        if not db.query(ClimateHistoricalIndicator).filter(ClimateHistoricalIndicator.id == obj_in.location_id).first():
            raise ValueError(f"No location found with ID {obj_in.location_id}")
        
        # Validate date range consistency
        if obj_in.end_date and obj_in.start_date > obj_in.end_date:
            raise ValueError("Start date cannot be after end date")
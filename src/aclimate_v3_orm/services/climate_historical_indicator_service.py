from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import date
from ..services.base_service import BaseService
from ..models import ClimateHistoricalIndicator, MngLocation, MngIndicator, MngIndicatorCategory
from ..enums import Period
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
    
    def get_by_category_id(self, category_id: int, db: Optional[Session] = None) -> List[ClimateHistoricalIndicatorRead]:
        """Get records by indicator category ID"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .join(MngIndicator)
                .filter(MngIndicator.indicator_category_id == category_id)
                .all()
            )
            return [ClimateHistoricalIndicatorRead.model_validate(obj) for obj in objs]
    
    def get_by_category_name(self, category_name: str, db: Optional[Session] = None) -> List[ClimateHistoricalIndicatorRead]:
        """Get records by indicator category name"""
        
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .join(MngIndicator)
                .join(MngIndicatorCategory)
                .filter(MngIndicatorCategory.name == category_name)
                .all()
            )
            return [ClimateHistoricalIndicatorRead.model_validate(obj) for obj in objs]
        
    def get_max_min_by_location_id(self, location_id: int, db: Optional[Session] = None) -> List[dict]:
        """
        Returns a list of dicts with min/max value and date for each indicator_id at a given location_id.
        Each dict contains: indicator_id, indicator_name, location_id, location_name, min_value, min_start_date, max_value, max_end_date
        """
        with self._session_scope(db) as session:
            indicators = session.query(self.model.indicator_id).filter(self.model.location_id == location_id).distinct().all()
            result = []
            for (indicator_id,) in indicators:
                min_record = session.query(self.model).filter(
                    self.model.location_id == location_id,
                    self.model.indicator_id == indicator_id
                ).order_by(self.model.start_date.asc()).first()
                max_record = session.query(self.model).filter(
                    self.model.location_id == location_id,
                    self.model.indicator_id == indicator_id
                ).order_by(self.model.end_date.desc()).first()
                if min_record and max_record:
                    result.append({
                        "indicator_id": indicator_id,
                        "indicator_name": getattr(min_record.indicator, "name", None),
                        "location_id": location_id,
                        "location_name": getattr(min_record.location, "name", None),
                        "min_value": min_record.value,
                        "min_start_date": min_record.start_date,
                        "max_value": max_record.value,
                        "max_end_date": max_record.end_date
                    })
            return result
            

    def get_by_location_date_period(self, location_id: int, start_date: date, end_date: date, period: Period, db: Optional[Session] = None) -> List[ClimateHistoricalIndicatorRead]:
        """
        Get climate historical indicators by location, date range and period.
        
        Args:
            location_id: ID of the location
            start_date: Start date for filtering
            end_date: End date for filtering  
            period: Period enum (DAILY, MONTHLY, etc.)
            db: Database session
            
        Returns:
            List of climate historical indicators filtered by criteria
        """
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .filter(
                    self.model.location_id == location_id,
                    self.model.period == period,
                    self.model.start_date >= start_date,
                    self.model.end_date <= end_date
                )
                .order_by(self.model.start_date)
                .all()
            )
            return [ClimateHistoricalIndicatorRead.model_validate(obj) for obj in objs]
        
    def _validate_create(self, obj_in: ClimateHistoricalIndicatorCreate, db: Optional[Session] = None):
        """Automatic validation called from BaseService.create()"""
        # Validate indicator exists
        if not db.query(ClimateHistoricalIndicator).filter(ClimateHistoricalIndicator.id == obj_in.indicator_id).first():
            raise ValueError(f"No indicator found with ID {obj_in.indicator_id}")
        
        # Validate location exists
        if not db.query(ClimateHistoricalIndicator).filter(ClimateHistoricalIndicator.id == obj_in.location_id).first():
            raise ValueError(f"No location found with ID {obj_in.location_id}")
        
        # Validate date range consistency
        if obj_in.end_date and obj_in.start_date > obj_in.end_date:
            raise ValueError("Start date cannot be after end date")
    
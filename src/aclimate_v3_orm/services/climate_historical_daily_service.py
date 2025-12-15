from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from ..services.base_service import BaseService
from ..models import ClimateHistoricalDaily, MngLocation, MngClimateMeasure, MngAdmin1, MngAdmin2, MngCountry
from ..validations import ClimateHistoricalDailyValidator
from sqlalchemy.sql import func
from ..schemas import (
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
                .filter(MngLocation.name == location_name)
                .all()
            )
            return [ClimateHistoricalDailyRead.model_validate(obj) for obj in results]

    def get_by_country_id(self, country_id: int, db: Optional[Session] = None) -> List[ClimateHistoricalDailyRead]:
        with self._session_scope(db) as session:
            results = (
                session.query(self.model)
                .join(self.model.location)
                .join(MngLocation.admin_2)
                .join(MngAdmin2.admin_1)
                .filter(MngAdmin1.country_id == country_id)
                .all()
            )            
            return [ClimateHistoricalDailyRead.model_validate(obj) for obj in results]

    def get_by_country_name(self, country_name: str, db: Optional[Session] = None) -> List[ClimateHistoricalDailyRead]:
        with self._session_scope(db) as session:
            results = (
                session.query(self.model)
                .join(self.model.location)
                .join(MngLocation.admin_2)
                .join(MngAdmin2.admin_1)
                .join(MngAdmin1.country)
                .filter(MngCountry.name == country_name)
                .all()
            )
            return [ClimateHistoricalDailyRead.model_validate(obj) for obj in results]

    def get_by_admin1_id(self, admin1_id: int, db: Optional[Session] = None) -> List[ClimateHistoricalDailyRead]:
        with self._session_scope(db) as session:
            results = (
                session.query(self.model)
                .join(self.model.location)
                .join(MngLocation.admin_2)
                .filter(MngAdmin2.admin_1_id == admin1_id)
                .all()
            )
            return [ClimateHistoricalDailyRead.model_validate(obj) for obj in results]

    def get_by_admin1_name(self, admin1_name: str, db: Optional[Session] = None) -> List[ClimateHistoricalDailyRead]:
        with self._session_scope(db) as session:
            results = (
                session.query(self.model)
                .join(self.model.location)
                .join(MngLocation.admin_2)
                .join(MngAdmin2.admin_1)
                .filter(MngAdmin1.name == admin1_name)
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
                .filter(MngClimateMeasure.name == measure_name)
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
    def get_date_range_by_location_id(self, location_id: int, db: Optional[Session] = None):
        
        with self._session_scope(db) as session:
            min_date, max_date = session.query(
                func.min(self.model.date),
                func.max(self.model.date)
            ).filter(self.model.location_id == location_id).one()
            return {"location_id": location_id, "min_date": min_date, "max_date": max_date}
    

    def get_max_min_by_location_id(self, location_id: int, db: Optional[Session] = None) -> List[dict]:
        """
        Returns a list of dicts with min/max value and date for each measure_id at a given location_id.
        Each dict contains: measure_id, measure_name, location_id, location_name, min_value, min_date, max_value, max_date
        """
        with self._session_scope(db) as session:
            measures = session.query(self.model.measure_id).filter(self.model.location_id == location_id).distinct().all()
            result = []
            for (measure_id,) in measures:
                min_record = session.query(self.model).filter(
                    self.model.location_id == location_id,
                    self.model.measure_id == measure_id
                ).order_by(self.model.date.asc()).first()
                max_record = session.query(self.model).filter(
                    self.model.location_id == location_id,
                    self.model.measure_id == measure_id
                ).order_by(self.model.date.desc()).first()
                if min_record and max_record:
                    result.append({
                        "measure_id": measure_id,
                        "measure_name": getattr(min_record.measure, "name", None),
                        "location_id": location_id,
                        "location_name": getattr(min_record.location, "name", None),
                        "min_value": min_record.value,
                        "min_date": min_record.date,
                        "max_value": max_record.value,
                        "max_date": max_record.date
                    })
            return result
        
    def get_latest_by_location(self, location_id: int, days: int = 1, db: Optional[Session] = None) -> Optional[dict]:
        """
        Get the latest climate data for a location within the last N days.
        Returns a dict with the most recent date and all available climate measures.
        
        Args:
            location_id: ID of the location
            days: Number of days to look back (default: 1, use 0 for no date limit)
            db: Database session
            
        Returns:
            Dict with date and measures list containing all climate data, or None if no data found
        """
        with self._session_scope(db) as session:
            from datetime import datetime, timedelta
            
            # Get the most recent date with data
            if days > 0:
                # Calculate the date range
                end_date = datetime.now().date()
                start_date = end_date - timedelta(days=days)
                
                latest_date_query = (
                    session.query(func.max(self.model.date))
                    .filter(
                        self.model.location_id == location_id,
                        self.model.date >= start_date,
                        self.model.date <= end_date
                    )
                    .scalar()
                )
            else:
                # No date limit - get the most recent date overall
                latest_date_query = (
                    session.query(func.max(self.model.date))
                    .filter(self.model.location_id == location_id)
                    .scalar()
                )
            
            if not latest_date_query:
                return None
            
            # Get all measures for that date with JOIN to load measure relationship
            records = (
                session.query(self.model)
                .join(self.model.measure)
                .filter(
                    self.model.location_id == location_id,
                    self.model.date == latest_date_query
                )
                .all()
            )
            
            if not records:
                return None
            
            # Build result dict with date and measures list
            measures = []
            for record in records:
                if record.measure:
                    measures.append({
                        "measure_id": record.measure_id,
                        "measure_name": record.measure.name,
                        "measure_short_name": record.measure.short_name,
                        "measure_unit": record.measure.unit,
                        "value": record.value
                    })
            
            result = {
                "date": latest_date_query,
                "measures": measures
            }
            
            return result
        
    def _validate_create(self, obj_in: ClimateHistoricalDailyCreate, db: Optional[Session] = None):
        ClimateHistoricalDailyValidator.create_validate(db, obj_in)

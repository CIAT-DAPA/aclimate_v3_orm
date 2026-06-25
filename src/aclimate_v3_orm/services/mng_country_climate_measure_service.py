from typing import List, Optional
from sqlalchemy.orm import Session
from ..services.base_service import BaseService
from ..models import MngCountryClimateMeasure
from ..validations import MngCountryClimateMeasureValidator
from ..schemas.mng_country_climate_measure_schema import (
    CountryClimateMeasureCreate,
    CountryClimateMeasureRead,
    CountryClimateMeasureUpdate,
)


class MngCountryClimateMeasureService(
    BaseService[MngCountryClimateMeasure, CountryClimateMeasureCreate, CountryClimateMeasureRead, CountryClimateMeasureUpdate]
):
    def __init__(self):
        super().__init__(MngCountryClimateMeasure, CountryClimateMeasureCreate, CountryClimateMeasureRead, CountryClimateMeasureUpdate)

    def get_by_country(self, country_id: int, db: Optional[Session] = None) -> List[CountryClimateMeasureRead]:
        """Get all climate measures for a given country"""
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(
                self.model.country_id == country_id
            ).all()
            return [CountryClimateMeasureRead.model_validate(obj) for obj in objs]

    def get_by_measure(self, measure_id: int, db: Optional[Session] = None) -> List[CountryClimateMeasureRead]:
        """Get all countries for a given climate measure"""
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(
                self.model.measure_id == measure_id
            ).all()
            return [CountryClimateMeasureRead.model_validate(obj) for obj in objs]

    def get_by_country_and_measure(self, country_id: int, measure_id: int, db: Optional[Session] = None) -> Optional[CountryClimateMeasureRead]:
        """Get configuration for a given country and climate measure"""
        with self._session_scope(db) as session:
            obj = session.query(self.model).filter(
                self.model.country_id == country_id,
                self.model.measure_id == measure_id
            ).first()
            return CountryClimateMeasureRead.model_validate(obj) if obj else None

    def _validate_create(self, obj_in: CountryClimateMeasureCreate, db: Optional[Session] = None):
        """Automatic validation called from BaseService.create()"""
        MngCountryClimateMeasureValidator.create_validate(db, obj_in)
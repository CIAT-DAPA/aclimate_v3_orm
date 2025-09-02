from typing import List, Optional
from sqlalchemy.orm import Session
from ..services.base_service import BaseService
from ..models import MngCountryIndicator
from ..validations import MngCountryIndicatorValidator
from ..schemas.mng_country_indicator_schema import (
    CountryIndicatorCreate,
    CountryIndicatorRead,
    CountryIndicatorUpdate,
)

class MngCountryIndicatorService(
    BaseService[MngCountryIndicator, CountryIndicatorCreate, CountryIndicatorRead, CountryIndicatorUpdate]
):
    def __init__(self):
        super().__init__(MngCountryIndicator, CountryIndicatorCreate, CountryIndicatorRead, CountryIndicatorUpdate)

    def get_by_country(self, country_id: int, db: Optional[Session] = None) -> List[CountryIndicatorRead]:
        """Get all indicators for a given country"""
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(
                self.model.country_id == country_id
            ).all()
            return [CountryIndicatorRead.model_validate(obj) for obj in objs]

    def get_by_indicator(self, indicator_id: int, db: Optional[Session] = None) -> List[CountryIndicatorRead]:
        """Get all countries for a given indicator"""
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(
                self.model.indicator_id == indicator_id
            ).all()
            return [CountryIndicatorRead.model_validate(obj) for obj in objs]

    def get_by_country_and_indicator(self, country_id: int, indicator_id: int, db: Optional[Session] = None) -> Optional[CountryIndicatorRead]:
        """Get configuration for a given country and indicator"""
        with self._session_scope(db) as session:
            obj = session.query(self.model).filter(
                self.model.country_id == country_id,
                self.model.indicator_id == indicator_id
            ).first()
            return CountryIndicatorRead.model_validate(obj) if obj else None

    def _validate_create(self, obj_in: CountryIndicatorCreate, db: Optional[Session] = None):
        """Automatic validation called from BaseService.create()"""
        MngCountryIndicatorValidator.create_validate(db, obj_in)

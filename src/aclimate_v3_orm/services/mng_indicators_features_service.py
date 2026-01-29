from typing import List, Optional
from sqlalchemy.orm import Session
from ..services.base_service import BaseService
from ..models import MngIndicatorsFeatures
from ..validations import MngIndicatorsFeaturesValidator
from ..schemas.mng_indicators_features_schema import (
    IndicatorFeatureCreate,
    IndicatorFeatureRead,
    IndicatorFeatureUpdate,
)


class MngIndicatorsFeaturesService(
    BaseService[MngIndicatorsFeatures, IndicatorFeatureCreate, IndicatorFeatureRead, IndicatorFeatureUpdate]
):
    def __init__(self):
        super().__init__(MngIndicatorsFeatures, IndicatorFeatureCreate, IndicatorFeatureRead, IndicatorFeatureUpdate)

    def get_by_country_indicator(self, country_indicator_id: int, db: Optional[Session] = None) -> List[IndicatorFeatureRead]:
        """Get all features for a given country indicator"""
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(
                self.model.country_indicator_id == country_indicator_id
            ).all()
            return [IndicatorFeatureRead.model_validate(obj) for obj in objs]

    def get_by_type(self, feature_type: str, db: Optional[Session] = None) -> List[IndicatorFeatureRead]:
        """Get all features by type (recommendation or feature)"""
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(
                self.model.type == feature_type
            ).all()
            return [IndicatorFeatureRead.model_validate(obj) for obj in objs]

    def get_by_country_indicator_and_type(
        self, 
        country_indicator_id: int, 
        feature_type: str, 
        db: Optional[Session] = None
    ) -> List[IndicatorFeatureRead]:
        """Get features for a given country indicator filtered by type"""
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(
                self.model.country_indicator_id == country_indicator_id,
                self.model.type == feature_type
            ).all()
            return [IndicatorFeatureRead.model_validate(obj) for obj in objs]

    def _validate_create(self, obj_in: IndicatorFeatureCreate, db: Optional[Session] = None):
        """Automatic validation called from BaseService.create()"""
        MngIndicatorsFeaturesValidator.create_validate(db, obj_in)

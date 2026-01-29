from sqlalchemy.orm import Session
from ..models import MngIndicatorsFeatures, MngCountryIndicator
from ..schemas.mng_indicators_features_schema import IndicatorFeatureCreate


class MngIndicatorsFeaturesValidator:
    @staticmethod
    def validate_country_indicator_exists(db: Session, country_indicator_id: int):
        """Validate that the country indicator exists"""
        country_indicator = db.query(MngCountryIndicator).filter(
            MngCountryIndicator.id == country_indicator_id
        ).first()
        if not country_indicator:
            raise ValueError(f"Country indicator with id={country_indicator_id} does not exist.")

    @staticmethod
    def validate_unique_title_per_country_indicator(
        db: Session, 
        country_indicator_id: int, 
        title: str, 
        exclude_id: int = None
    ):
        """Validate that the title is unique within the same country indicator"""
        query = db.query(MngIndicatorsFeatures).filter(
            MngIndicatorsFeatures.country_indicator_id == country_indicator_id,
            MngIndicatorsFeatures.title == title
        )
        if exclude_id:
            query = query.filter(MngIndicatorsFeatures.id != exclude_id)
        if query.first():
            raise ValueError(
                f"A feature with title='{title}' already exists for country_indicator_id={country_indicator_id}."
            )

    @staticmethod
    def create_validate(db: Session, obj_in: IndicatorFeatureCreate):
        """Validation for creating a new indicator feature"""
        MngIndicatorsFeaturesValidator.validate_country_indicator_exists(db, obj_in.country_indicator_id)
        MngIndicatorsFeaturesValidator.validate_unique_title_per_country_indicator(
            db, 
            obj_in.country_indicator_id, 
            obj_in.title
        )

    @staticmethod
    def update_validate(db: Session, obj_in: dict, feature_id: int):
        """Validation for updating an indicator feature"""
        country_indicator_id = obj_in.get('country_indicator_id')
        title = obj_in.get('title')
        
        if country_indicator_id:
            MngIndicatorsFeaturesValidator.validate_country_indicator_exists(db, country_indicator_id)
        
        if title and country_indicator_id:
            MngIndicatorsFeaturesValidator.validate_unique_title_per_country_indicator(
                db, 
                country_indicator_id, 
                title, 
                exclude_id=feature_id
            )

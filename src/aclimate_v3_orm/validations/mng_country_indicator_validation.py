from sqlalchemy.orm import Session
from ..models import MngCountryIndicator
from ..schemas.mng_country_indicator_schema import CountryIndicatorCreate

class MngCountryIndicatorValidator:
    @staticmethod
    def validate_unique_country_indicator(db: Session, country_id: int, indicator_id: int, exclude_id: int = None):
        query = db.query(MngCountryIndicator).filter(
            MngCountryIndicator.country_id == country_id,
            MngCountryIndicator.indicator_id == indicator_id
        )
        if exclude_id:
            query = query.filter(MngCountryIndicator.id != exclude_id)
        if query.first():
            raise ValueError(f"A configuration for country_id={country_id} and indicator_id={indicator_id} already exists.")

    @staticmethod
    def create_validate(db: Session, obj_in: CountryIndicatorCreate):
        MngCountryIndicatorValidator.validate_unique_country_indicator(db, obj_in.country_id, obj_in.indicator_id)

    @staticmethod
    def update_validate(db: Session, obj_in: dict, config_id: int):
        country_id = obj_in.get('country_id')
        indicator_id = obj_in.get('indicator_id')
        if country_id and indicator_id:
            MngCountryIndicatorValidator.validate_unique_country_indicator(db, country_id, indicator_id, exclude_id=config_id)

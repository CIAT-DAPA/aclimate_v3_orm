from sqlalchemy.orm import Session
from ..models import MngCountryClimateMeasure
from ..schemas.mng_country_climate_measure_schema import CountryClimateMeasureCreate


class MngCountryClimateMeasureValidator:
    @staticmethod
    def validate_unique_country_measure(db: Session, country_id: int, measure_id: int, exclude_id: int = None):
        query = db.query(MngCountryClimateMeasure).filter(
            MngCountryClimateMeasure.country_id == country_id,
            MngCountryClimateMeasure.measure_id == measure_id
        )
        if exclude_id:
            query = query.filter(MngCountryClimateMeasure.id != exclude_id)
        if query.first():
            raise ValueError(f"A configuration for country_id={country_id} and measure_id={measure_id} already exists.")

    @staticmethod
    def create_validate(db: Session, obj_in: CountryClimateMeasureCreate):
        MngCountryClimateMeasureValidator.validate_unique_country_measure(db, obj_in.country_id, obj_in.measure_id)

    @staticmethod
    def update_validate(db: Session, obj_in: dict, config_id: int):
        country_id = obj_in.get('country_id')
        measure_id = obj_in.get('measure_id')
        if country_id and measure_id:
            MngCountryClimateMeasureValidator.validate_unique_country_measure(db, country_id, measure_id, exclude_id=config_id)
from services.base_service import BaseService
from models import ClimateHistoricalClimatology
from validations.climate import ClimateHistoricalClimatologyValidator
from sqlalchemy.orm import Session
from typing import List

class ClimateHistoricalClimatologyService(BaseService[ClimateHistoricalClimatology]):
    def __init__(self):
        super().__init__(ClimateHistoricalClimatology)

    def get_by_location_id(self, db: Session, location_id: int) -> List[ClimateHistoricalClimatology]:
        return db.query(self.model).filter(self.model.location_id == location_id).all()

    def get_by_location_name(self, db: Session, location_name: str) -> List[ClimateHistoricalClimatology]:
        return db.query(self.model).join(self.model.location).filter(self.model.location.name == location_name).all()

    def get_by_country_id(self, db: Session, country_id: int) -> List[ClimateHistoricalClimatology]:
        return (
            db.query(self.model)
            .join(self.model.location)
            .join(self.model.location.admin_2)
            .join(self.model.location.admin_2.admin_1)
            .join(self.model.location.admin_2.admin_1.country)
            .filter(self.model.location.admin_2.admin_1.country_id == country_id)
            .all()
        )

    def get_by_country_name(self, db: Session, country_name: str) -> List[ClimateHistoricalClimatology]:
        return (
            db.query(self.model)
            .join(self.model.location)
            .join(self.model.location.admin_2)
            .join(self.model.location.admin_2.admin_1)
            .join(self.model.location.admin_2.admin_1.country)
            .filter(self.model.location.admin_2.admin_1.country.name == country_name)
            .all()
        )

    def get_by_admin1_id(self, db: Session, admin1_id: int) -> List[ClimateHistoricalClimatology]:
        return (
            db.query(self.model)
            .join(self.model.location)
            .join(self.model.location.admin_2)
            .join(self.model.location.admin_2.admin_1)
            .filter(self.model.location.admin_2.admin_1_id == admin1_id)
            .all()
        )

    def get_by_admin1_name(self, db: Session, admin1_name: str) -> List[ClimateHistoricalClimatology]:
        return (
            db.query(self.model)
            .join(self.model.location)
            .join(self.model.location.admin_2)
            .join(self.model.location.admin_2.admin_1)
            .filter(self.model.location.admin_2.admin_1.name == admin1_name)
            .all()
        )

    def get_by_month(self, db: Session, month: int) -> List[ClimateHistoricalClimatology]:
        return db.query(self.model).filter(self.model.month == month).all()

    def get_by_measure_id(self, db: Session, measure_id: int) -> List[ClimateHistoricalClimatology]:
        return db.query(self.model).filter(self.model.measure_id == measure_id).all()

    def get_by_measure_name(self, db: Session, measure_name: str) -> List[ClimateHistoricalClimatology]:
        return (
            db.query(self.model)
            .join(self.model.measure)
            .filter(self.model.measure.name == measure_name)
            .all()
        )
    
    def validate_create(self, db: Session, obj_in: dict):
        # Validate before create
        ClimateHistoricalClimatologyValidator.create_validate(db, obj_in)

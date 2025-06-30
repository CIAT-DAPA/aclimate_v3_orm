from sqlalchemy.orm import Session
from ..models import Forecast
from ..schemas import ForecastCreate, ForecastUpdate
from datetime import date

class ForecastValidator:
    @staticmethod
    def validate_run_date(run_date: date):
        """Validate run date is not in the future"""
        if run_date > date.today():
            raise ValueError("Forecast run date cannot be in the future")

    @staticmethod
    def validate_unique_run_date(db: Session, run_date: date, exclude_id: int = None):
        """Check if forecast with same run date already exists"""
        query = db.query(Forecast).filter(Forecast.run_date == run_date)
        if exclude_id:
            query = query.filter(Forecast.id != exclude_id)
        if query.first():
            raise ValueError(f"A forecast with run date {run_date} already exists")

    @staticmethod
    def create_validate(db: Session, obj_in: ForecastCreate):
        """Validation for forecast creation"""
        ForecastValidator.validate_run_date(obj_in.run_date)
        ForecastValidator.validate_unique_run_date(db, obj_in.run_date)

    @staticmethod
    def update_validate(db: Session, obj_in: ForecastUpdate, forecast_id: int):
        """Validation for forecast updates"""
        if hasattr(obj_in, 'run_date') and obj_in.run_date is not None:
            ForecastValidator.validate_run_date(obj_in.run_date)
            ForecastValidator.validate_unique_run_date(db, obj_in.run_date, exclude_id=forecast_id)
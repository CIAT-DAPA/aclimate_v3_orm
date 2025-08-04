from typing import List, Optional
from sqlalchemy.orm import Session
from ..services.base_service import BaseService
from ..models import MngCountry
from ..validations import MngCountryValidator
from ..schemas import CountryCreate, CountryRead, CountryUpdate

class MngCountryService(BaseService[MngCountry, CountryCreate, CountryRead, CountryUpdate]):
    def __init__(self):
        super().__init__(MngCountry, CountryCreate, CountryRead, CountryUpdate)

    def get_by_name(self, name: str, enabled: bool = True, db: Optional[Session] = None) -> List[CountryRead]:
        """Get countries by name (always uppercase)"""
        name_upper = name.upper() if name else name
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(
                self.model.name == name_upper,
                self.model.enable == enabled
            ).all()
            return [CountryRead.model_validate(obj) for obj in objs]

    def get_all_enable(self, db: Optional[Session] = None, enabled: bool = True) -> List[CountryRead]:
        """Get all countries, filtered by enabled status"""
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(
                self.model.enable == enabled
            ).all()
            return [CountryRead.model_validate(obj) for obj in objs]

    def _validate_create(self, obj_in: CountryCreate, db: Optional[Session] = None):
        """Automatic validation called from BaseService.create()"""
        # Validate before creating
        MngCountryValidator.create_validate(db, obj_in)

    def create(self, obj_in: CountryCreate, db: Optional[Session] = None) -> CountryRead:
        """Create a new country, forcing the name to uppercase"""
        if obj_in.name:
            obj_in.name = obj_in.name.upper()
        with self._session_scope(db) as session:
            self._validate_create(obj_in, session)
            obj_data = obj_in.model_dump()
            db_obj = self.model(**obj_data)
            session.add(db_obj)
            session.commit()
            session.refresh(db_obj)
            return self.read_schema.model_validate(db_obj)

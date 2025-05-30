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
        """Obtiene países por nombre"""
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(
                self.model.name == name, 
                self.model.enable == enabled
            ).all()
            return [CountryRead.model_validate(obj) for obj in objs]

    def get_all_enable(self, db: Optional[Session] = None, enabled: bool = True) -> List[CountryRead]:
        """Obtiene todos los países, filtrados por estado habilitado"""
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(
                self.model.enable == enabled
            ).all()
            return [CountryRead.model_validate(obj) for obj in objs]

    def _validate_create(self, obj_in: CountryCreate, db: Optional[Session] = None):
        """Validación automática llamada desde create() del BaseService"""
        # Validar antes de crear
        MngCountryValidator.create_validate(db, obj_in)

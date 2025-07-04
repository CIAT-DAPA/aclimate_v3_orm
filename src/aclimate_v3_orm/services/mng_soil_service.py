from typing import List, Optional
from sqlalchemy.orm import Session
from ..services.base_service import BaseService
from ..models import MngSoil
from ..schemas import SoilCreate, SoilUpdate, SoilRead
from ..validations import MngSoilValidator

class MngSoilService(BaseService[MngSoil, SoilCreate, SoilRead, SoilUpdate]):
    def __init__(self):
        super().__init__(MngSoil, SoilCreate, SoilRead, SoilUpdate)

    def get_by_country_id(self,
                          country_id: int, 
                          enabled: bool = True,
                          db: Optional[Session] = None) -> List[SoilRead]:
        """Get soil records by country ID"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .filter(
                    self.model.country_id == country_id,
                    self.model.enable == enabled
                )
                .all()
            )
            return [SoilRead.model_validate(obj) for obj in objs]

    def get_by_crop_id(self,
                       crop_id: int, 
                       enabled: bool = True,
                       db: Optional[Session] = None) -> List[SoilRead]:
        """Get soil records by crop ID"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .filter(
                    self.model.crop_id == crop_id,
                    self.model.enable == enabled
                )
                .all()
            )
            return [SoilRead.model_validate(obj) for obj in objs]

    def get_all_enable(self,
                       enabled: bool = True,
                       db: Optional[Session] = None) -> List[SoilRead]:
        """Get all soil records, optionally filtered by enabled status"""
        with self._session_scope(db) as session:
            query = session.query(self.model)
            if enabled is not None:
                query = query.filter(self.model.enable == enabled)
            objs = query.all()
            return [SoilRead.model_validate(obj) for obj in objs]

    def get_by_name(self,
                    name: str, 
                    enabled: bool = True,
                    db: Optional[Session] = None) -> List[SoilRead]:
        """Get soil records by name"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .filter(
                    self.model.name == name,
                    self.model.enable == enabled
                )
                .all()
            )
            return [SoilRead.model_validate(obj) for obj in objs]

    def _validate_create(self, obj_in: SoilCreate, db: Optional[Session] = None):
        """Validation hook called automatically from BaseService.create()"""
        MngSoilValidator.create_validate(db, obj_in)
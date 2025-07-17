from typing import List, Optional
from sqlalchemy.orm import Session
from ..services.base_service import BaseService
from ..models import MngCultivar
from ..schemas import CultivarCreate, CultivarUpdate, CultivarRead
from ..validations import MngCultivarValidator

class MngCultivarService(BaseService[MngCultivar, CultivarCreate, CultivarRead, CultivarUpdate]):
    def __init__(self):
        super().__init__(MngCultivar, CultivarCreate, CultivarRead, CultivarUpdate)

    def get_by_crop(self, crop_id: int, db: Optional[Session] = None) -> List[CultivarRead]:
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(self.model.crop_id == crop_id).all()
            return [CultivarRead.model_validate(obj) for obj in objs]

    def get_by_country(self, country_id: int, db: Optional[Session] = None) -> List[CultivarRead]:
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(self.model.country_id == country_id).all()
            return [CultivarRead.model_validate(obj) for obj in objs]

    def get_all_enable(self, db: Optional[Session] = None) -> List[CultivarRead]:
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(self.model.enable == True).all()
            return [CultivarRead.model_validate(obj) for obj in objs]

    def _validate_create(self, obj_in: CultivarCreate, db: Optional[Session] = None):
        MngCultivarValidator.create_validate(db, obj_in)
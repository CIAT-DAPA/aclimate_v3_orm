from typing import List, Optional
from sqlalchemy.orm import Session
from ..services.base_service import BaseService
from ..models import MngCrop
from ..schemas import CropCreate, CropUpdate, CropRead
from ..validations import MngCropValidator

class MngCropService(BaseService[MngCrop, CropCreate, CropRead, CropUpdate]):
    def __init__(self):
        super().__init__(MngCrop, CropCreate, CropRead, CropUpdate)

    def get_by_name(self, name: str, db: Optional[Session] = None) -> Optional[CropRead]:
        with self._session_scope(db) as session:
            obj = session.query(self.model).filter(self.model.name == name).first()
            return CropRead.model_validate(obj) if obj else None

    def get_all_enable(self, enabled: bool = True, db: Optional[Session] = None) -> List[CropRead]:
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(self.model.enable == enabled).all()
            return [CropRead.model_validate(obj) for obj in objs]

    def _validate_create(self, obj_in: CropCreate, db: Optional[Session] = None):
        MngCropValidator.create_validate(db, obj_in)
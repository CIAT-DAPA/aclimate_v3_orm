from typing import List, Optional
from sqlalchemy.orm import Session
from ..services.base_service import BaseService
from ..models import MngConfigurationFile
from ..schemas import ConfigurationFileCreate, ConfigurationFileUpdate, ConfigurationFileRead
from ..validations import MngConfigurationFileValidator

class MngConfigurationFileService(BaseService[MngConfigurationFile, ConfigurationFileCreate, ConfigurationFileRead, ConfigurationFileUpdate]):
    def __init__(self):
        super().__init__(MngConfigurationFile, ConfigurationFileCreate, ConfigurationFileRead, ConfigurationFileUpdate)

    def get_by_setup(self, setup_id: int, db: Optional[Session] = None) -> List[ConfigurationFileRead]:
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(self.model.setup_id == setup_id).all()
            return [ConfigurationFileRead.model_validate(obj) for obj in objs]

    def _validate_create(self, obj_in: ConfigurationFileCreate, db: Optional[Session] = None):
                MngConfigurationFileValidator.create_validate(db, obj_in)
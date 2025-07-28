# mng_setup_service.py
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, joinedload
from ..services.base_service import BaseService
from ..models import MngSetup
from ..schemas import SetupCreate, SetupRead, SetupUpdate

class MngSetupService(BaseService[MngSetup, SetupCreate, SetupRead, SetupUpdate]):
    def __init__(self):
        super().__init__(MngSetup, SetupCreate, SetupRead, SetupUpdate)
    
    def get_by_cultivar(self, db: Session, cultivar_id: int) -> List[SetupRead]:
        objs = db.query(MngSetup).filter(MngSetup.cultivar_id == cultivar_id).all()
        return [SetupRead.model_validate(obj) for obj in objs]
    
    def get_by_season(self, db: Session, season_id: int) -> List[SetupRead]:
        objs = db.query(MngSetup).filter(MngSetup.season_id == season_id).all()
        return [SetupRead.model_validate(obj) for obj in objs]
    
    def get_by_id(self, id: int, db: Optional[Session] = None) -> Optional[SetupRead]:
        with self._session_scope(db) as session:
            obj = session.query(self.model).options(
                joinedload(MngSetup.configuration_files)
            ).get(id)
            return self.read_schema.model_validate(obj) if obj else None
    
    def get_all(self, db: Optional[Session] = None, filters: Optional[Dict[str, Any]] = None) -> List[SetupRead]:
        with self._session_scope(db) as session:
            query = session.query(self.model).options(
                joinedload(MngSetup.configuration_files)
            )
            if filters:
                query = query.filter_by(**filters)
            return [self.read_schema.model_validate(obj) for obj in query.all()]
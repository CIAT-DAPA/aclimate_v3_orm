# mng_setup_service.py
from typing import List, Optional
from sqlalchemy.orm import Session
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
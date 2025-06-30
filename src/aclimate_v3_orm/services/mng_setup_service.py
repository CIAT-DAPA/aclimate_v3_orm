# mng_setup_service.py
from typing import List, Optional
from sqlalchemy.orm import Session
from ..services.base_service import BaseService
from ..models import MngSetup
from ..schemas import MngSetupCreate, MngSetupRead, MngSetupUpdate

class MngSetupService(BaseService[MngSetup, MngSetupCreate, MngSetupRead, MngSetupUpdate]):
    def __init__(self):
        super().__init__(MngSetup)
    
    def get_by_cultivar(self, db: Session, cultivar_id: int) -> List[MngSetupRead]:
        objs = db.query(MngSetup).filter(MngSetup.cultivar_id == cultivar_id).all()
        return [MngSetupRead.model_validate(obj) for obj in objs]
    
    def get_by_season(self, db: Session, season_id: int) -> List[MngSetupRead]:
        objs = db.query(MngSetup).filter(MngSetup.season_id == season_id).all()
        return [MngSetupRead.model_validate(obj) for obj in objs]
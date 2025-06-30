from typing import List, Optional
from sqlalchemy.orm import Session
from ..services.base_service import BaseService
from ..models import MngDataSource
from ..schemas import DataSourceCreate, DataSourceUpdate, DataSourceRead
from ..validations import MngDataSourceValidator

class MngDataSourceService(BaseService[MngDataSource, DataSourceCreate, DataSourceRead, DataSourceUpdate]):
    def __init__(self):
        super().__init__(MngDataSource, DataSourceCreate, DataSourceRead, DataSourceUpdate)

    def get_by_country(self, country_id: int, db: Optional[Session] = None) -> List[DataSourceRead]:
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(self.model.country_id == country_id).all()
            return [DataSourceRead.model_validate(obj) for obj in objs]

    def get_by_name(self, name: str, db: Optional[Session] = None) -> Optional[DataSourceRead]:
        with self._session_scope(db) as session:
            obj = session.query(self.model).filter(self.model.name == name).first()
            return DataSourceRead.model_validate(obj) if obj else None

    def _validate_create(self, obj_in: DataSourceCreate, db: Optional[Session] = None):
        MngDataSourceValidator.create_validate(db, obj_in)
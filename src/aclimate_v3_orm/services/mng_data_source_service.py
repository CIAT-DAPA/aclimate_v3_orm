from typing import List, Optional
from sqlalchemy.orm import Session
from ..services.base_service import BaseService
from ..models import MngDataSource, MngCountry
from ..schemas import DataSourceCreate, DataSourceUpdate, DataSourceRead
from ..validations import MngDataSourceValidator

class MngDataSourceService(BaseService[MngDataSource, DataSourceCreate, DataSourceRead, DataSourceUpdate]):
    def __init__(self):
        super().__init__(MngDataSource, DataSourceCreate, DataSourceRead, DataSourceUpdate)

    def get_by_country(self, country_id: int, enabled: bool = True, db: Optional[Session] = None) -> List[DataSourceRead]:
        """Get data sources by country ID"""
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(
                self.model.country_id == country_id,
                self.model.enable == enabled
            ).all()
            return [DataSourceRead.model_validate(obj) for obj in objs]

    def get_by_name(self, name: str, enabled: bool = True, db: Optional[Session] = None) -> Optional[DataSourceRead]:
        """Get data source by name"""
        with self._session_scope(db) as session:
            obj = session.query(self.model).filter(
                self.model.name == name,
                self.model.enable == enabled
            ).first()
            return DataSourceRead.model_validate(obj) if obj else None

    def get_by_name_and_country(self, name: str, country_name: str, enabled: bool = True, db: Optional[Session] = None) -> Optional[DataSourceRead]:
        """Get data source by name and country name"""
        with self._session_scope(db) as session:
            obj = (
                session.query(self.model)
                .join(MngDataSource.country)
                .filter(
                    self.model.name == name,
                    MngCountry.name == country_name,
                    self.model.enable == enabled
                )
                .first()
            )
            return DataSourceRead.model_validate(obj) if obj else None

    def get_by_country_name(self, country_name: str, enabled: bool = True, db: Optional[Session] = None) -> List[DataSourceRead]:
        """Get data sources by country name"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .join(MngDataSource.country)
                .filter(
                    MngCountry.name == country_name,
                    self.model.enable == enabled
                )
                .all()
            )
            return [DataSourceRead.model_validate(obj) for obj in objs]

    def get_all_enable(self, enabled: bool = True, db: Optional[Session] = None) -> List[DataSourceRead]:
        """Get all data sources, optionally filtered by enabled status"""
        with self._session_scope(db) as session:
            query = session.query(self.model)
            if enabled is not None:
                query = query.filter(self.model.enable == enabled)
            objs = query.all()
            return [DataSourceRead.model_validate(obj) for obj in objs]

    def _validate_create(self, obj_in: DataSourceCreate, db: Optional[Session] = None):
        MngDataSourceValidator.create_validate(db, obj_in)
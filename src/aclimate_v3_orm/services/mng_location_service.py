from typing import List, Optional
from sqlalchemy.orm import Session
from ..services.base_service import BaseService
from ..models import MngLocation, MngCountry, MngAdmin1, MngAdmin2, MngSource
from ..validations import MngLocationValidator
from ..schemas import LocationCreate, LocationRead, LocationUpdate

class MngLocationService(BaseService[MngLocation, LocationCreate, LocationRead, LocationUpdate]):
    def __init__(self):
        super().__init__(MngLocation, LocationCreate, LocationRead, LocationUpdate)

    def get_by_visible(self, visible: bool, enabled: bool = True, db: Optional[Session] = None) -> List[LocationRead]:
        """Obtiene ubicaciones por visibilidad y habilitación"""
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(
                self.model.visible == visible, 
                self.model.enable == enabled
            ).all()
            return [LocationRead.model_validate(obj) for obj in objs]

    def get_by_ext_id(self, ext_id: str, enabled: bool = True, db: Optional[Session] = None) -> List[LocationRead]:
        """Obtiene ubicaciones por ID externo"""
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(
                self.model.ext_id == ext_id, 
                self.model.enable == enabled
            ).all()
            return [LocationRead.model_validate(obj) for obj in objs]

    def get_by_name(self, name: str, enabled: bool = True, db: Optional[Session] = None) -> List[LocationRead]:
        """Obtiene ubicaciones por nombre"""
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(
                self.model.name == name, 
                self.model.enable == enabled
            ).all()
            return [LocationRead.model_validate(obj) for obj in objs]

    def get_by_machine_name(self, machine_name: str, enabled: bool = True, db: Optional[Session] = None) -> Optional[LocationRead]:
        """Obtiene ubicación por machine_name"""
        with self._session_scope(db) as session:
            obj = session.query(self.model).filter(
                self.model.machine_name == machine_name, 
                self.model.enable == enabled
            ).first()
            return LocationRead.model_validate(obj) if obj else None

    def get_all_enable(self, db: Optional[Session] = None, enable: bool = True) -> List[LocationRead]:
        """Obtiene todas las ubicaciones filtradas por estado habilitado"""
        with self._session_scope(db) as session:
            objs = session.query(self.model).filter(
                self.model.enable == enable
            ).all()
            return [LocationRead.model_validate(obj) for obj in objs]

    def get_by_country_id(self, country_id: int, enabled: bool = True, db: Optional[Session] = None) -> List[LocationRead]:
        """Obtiene ubicaciones por ID de país"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .join(self.model.admin_2)
                .join(MngAdmin2.admin_1)
                .filter(MngAdmin1.country_id == country_id, self.model.enable == enabled)
                .all()
            )
            return [LocationRead.model_validate(obj) for obj in objs]

    def get_by_admin1_id(self, admin1_id: int, enabled: bool = True, db: Optional[Session] = None) -> List[LocationRead]:
        """Obtiene ubicaciones por ID de admin1"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .join(self.model.admin_2)
                .filter(MngAdmin2.admin_1_id == admin1_id, self.model.enable == enabled)
                .all()
            )
            return [LocationRead.model_validate(obj) for obj in objs]

    def get_by_country_name(self, country_name: str, enabled: bool = True, db: Optional[Session] = None) -> List[LocationRead]:
        """Obtiene ubicaciones por nombre de país"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .join(self.model.admin_2)
                .join(MngAdmin2.admin_1)
                .join(MngAdmin1.country)
                .filter(MngCountry.name == country_name, self.model.enable == enabled)
                .all()
            )
            return [LocationRead.model_validate(obj) for obj in objs]

    def get_by_admin1_name(self, admin1_name: str, enabled: bool = True, db: Optional[Session] = None) -> List[LocationRead]:
        """Obtiene ubicaciones por nombre de admin1"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .join(self.model.admin_2)
                .join(MngAdmin2.admin_1)
                .filter(MngAdmin1.name == admin1_name, self.model.enable == enabled)
                .all()
            )
            return [LocationRead.model_validate(obj) for obj in objs]

    def get_by_admin2_id(self, admin2_id: int, enabled: bool = True, db: Optional[Session] = None) -> List[LocationRead]:
        """Obtiene ubicaciones por ID de admin2"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .filter(self.model.admin_2_id == admin2_id, self.model.enable == enabled)
                .all()
            )
            return [LocationRead.model_validate(obj) for obj in objs]

    def get_by_admin2_name(self, admin2_name: str, enabled: bool = True, db: Optional[Session] = None) -> List[LocationRead]:
        """Obtiene ubicaciones por nombre de admin2"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .join(self.model.admin_2)
                .filter(MngAdmin2.name == admin2_name, self.model.enable == enabled)
                .all()
            )
            return [LocationRead.model_validate(obj) for obj in objs]
        
    def get_by_source_id(self, 
                        source_id: int, 
                        enabled: bool = True,
                        db: Optional[Session] = None) -> List[LocationRead]:
        """Get by source id"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .filter(
                    self.model.source_id == source_id,
                    self.model.enable == enabled
                )
                .all()
            )
            return [LocationRead.model_validate(obj) for obj in objs]

    def get_by_source_type(self,
                         source_type: str,
                         enabled: bool = True,
                         db: Optional[Session] = None) -> List[LocationRead]:
        """Get by source type (MA/AU)"""
        with self._session_scope(db) as session:
            objs = (
                session.query(self.model)
                .join(self.model.source)
                .filter(
                    MngSource.source_type == source_type,
                    self.model.enable == enabled
                )
                .all()
            )
            return [LocationRead.model_validate(obj) for obj in objs]

    def _validate_create(self, obj_in: LocationCreate, db: Optional[Session] = None):
        """Validación automática llamada desde create() del BaseService"""
        MngLocationValidator.create_validate(db, obj_in)

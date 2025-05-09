from typing import List
from sqlalchemy.orm import Session
from services.base_service import BaseService
from models import MngLocation
from validations import MngLocationValidator
from schemas import LocationCreate, LocationRead, LocationUpdate

class MngLocationService(BaseService[MngLocation, LocationCreate, LocationRead, LocationUpdate]):
    def __init__(self):
        super().__init__(MngLocation, LocationCreate, LocationRead, LocationUpdate)

    def get_by_visible(self, db: Session, visible: bool, enabled: bool = True) -> List[LocationRead]:
        """Obtiene ubicaciones por visibilidad y habilitación"""
        with self._session_scope(db) as session:
            objs = db.query(self.model).filter(
                self.model.visible == visible, 
                self.model.enable == enabled
            ).all()
            return [LocationRead.model_validate(obj) for obj in objs]

    def get_by_ext_id(self, db: Session, ext_id: str, enabled: bool = True) -> List[LocationRead]:
        """Obtiene ubicaciones por ID externo"""
        with self._session_scope(db) as session:
            objs = db.query(self.model).filter(
                self.model.ext_id == ext_id, 
                self.model.enable == enabled
            ).all()
            return [LocationRead.model_validate(obj) for obj in objs]

    def get_by_name(self, db: Session, name: str, enabled: bool = True) -> List[LocationRead]:
        """Obtiene ubicaciones por nombre"""
        with self._session_scope(db) as session:
            objs = db.query(self.model).filter(
                self.model.name == name, 
                self.model.enable == enabled
            ).all()
            return [LocationRead.model_validate(obj) for obj in objs]

    def get_all_enable(self, db: Session, enable: bool = True) -> List[LocationRead]:
        """Obtiene todas las ubicaciones filtradas por estado habilitado"""
        with self._session_scope(db) as session:
            objs = db.query(self.model).filter(
                self.model.enable == enable
            ).all()
            return [LocationRead.model_validate(obj) for obj in objs]

    def get_by_country_id(self, db: Session, country_id: int, enabled: bool = True) -> List[LocationRead]:
        """Obtiene ubicaciones por ID de país"""
        with self._session_scope(db) as session:
            objs = (
                db.query(self.model)
                .join(self.model.admin_2)
                .join(self.model.admin_2.admin_1)
                .filter(self.model.admin_2.admin_1.country_id == country_id, self.model.enable == enabled)
                .all()
            )
            return [LocationRead.model_validate(obj) for obj in objs]

    def get_by_admin1_id(self, db: Session, admin1_id: int, enabled: bool = True) -> List[LocationRead]:
        """Obtiene ubicaciones por ID de admin1"""
        with self._session_scope(db) as session:
            objs = (
                db.query(self.model)
                .join(self.model.admin_2)
                .filter(self.model.admin_2.admin_1_id == admin1_id, self.model.enable == enabled)
                .all()
            )
            return [LocationRead.model_validate(obj) for obj in objs]

    def get_by_country_name(self, db: Session, country_name: str, enabled: bool = True) -> List[LocationRead]:
        """Obtiene ubicaciones por nombre de país"""
        with self._session_scope(db) as session:
            objs = (
                db.query(self.model)
                .join(self.model.admin_2)
                .join(self.model.admin_2.admin_1)
                .join(self.model.admin_2.admin_1.country)
                .filter(self.model.admin_2.admin_1.country.name == country_name, self.model.enable == enabled)
                .all()
            )
            return [LocationRead.model_validate(obj) for obj in objs]

    def get_by_admin1_name(self, db: Session, admin1_name: str, enabled: bool = True) -> List[LocationRead]:
        """Obtiene ubicaciones por nombre de admin1"""
        with self._session_scope(db) as session:
            objs = (
                db.query(self.model)
                .join(self.model.admin_2)
                .join(self.model.admin_2.admin_1)
                .filter(self.model.admin_2.admin_1.name == admin1_name, self.model.enable == enabled)
                .all()
            )
            return [LocationRead.model_validate(obj) for obj in objs]

    def get_by_admin2_id(self, db: Session, admin2_id: int, enabled: bool = True) -> List[LocationRead]:
        """Obtiene ubicaciones por ID de admin2"""
        with self._session_scope(db) as session:
            objs = (
                db.query(self.model)
                .filter(self.model.admin_2_id == admin2_id, self.model.enable == enabled)
                .all()
            )
            return [LocationRead.model_validate(obj) for obj in objs]

    def get_by_admin2_name(self, db: Session, admin2_name: str, enabled: bool = True) -> List[LocationRead]:
        """Obtiene ubicaciones por nombre de admin2"""
        with self._session_scope(db) as session:
            objs = (
                db.query(self.model)
                .join(self.model.admin_2)
                .filter(self.model.admin_2.name == admin2_name, self.model.enable == enabled)
                .all()
            )
            return [LocationRead.model_validate(obj) for obj in objs]

    def _validate_create(self, db: Session, obj_in: LocationCreate):
        """Validación automática llamada desde create() del BaseService"""
        MngLocationValidator.create_validate(db, obj_in)

from typing import List
from sqlalchemy.orm import Session
from services.base_service import BaseService
from models import MngClimateMeasure
from validations import MngClimateMeasureNameValidator
from schemas import (
    ClimateMeasureCreate,
    ClimateMeasureUpdate,
    ClimateMeasureRead
)

class MngClimateMeasureService(
    BaseService[
        MngClimateMeasure,
        ClimateMeasureCreate,
        ClimateMeasureRead,
        ClimateMeasureUpdate
    ]
):
    def __init__(self):
        super().__init__(MngClimateMeasure, ClimateMeasureCreate, ClimateMeasureRead, ClimateMeasureUpdate)

    def get_by_name(self, db: Session, name: str, enabled: bool = True) -> List[ClimateMeasureRead]:
        """Obtiene medidas climáticas por nombre"""
        with self._session_scope(db) as session:
            objs = session.query(self.model)\
                .filter(
                    self.model.name == name,
                    self.model.enable == enabled
                )\
                .all()
            return [ClimateMeasureRead.model_validate(obj) for obj in objs]

    def get_by_short_name(self, db: Session, short_name: str, enabled: bool = True) -> List[ClimateMeasureRead]:
        """Obtiene medidas climáticas por nombre corto"""
        with self._session_scope(db) as session:
            objs = session.query(self.model)\
                .filter(
                    self.model.short_name == short_name,
                    self.model.enable == enabled
                )\
                .all()
            return [ClimateMeasureRead.model_validate(obj) for obj in objs]

    def get_all(self, db: Session, enabled: bool = True) -> List[ClimateMeasureRead]:
        """Obtiene todas las medidas climáticas, filtradas por estado"""
        with self._session_scope(db) as session:
            query = session.query(self.model)
            if enabled is not None:
                query = query.filter(self.model.enable == enabled)
            objs = query.all()
            return [ClimateMeasureRead.model_validate(obj) for obj in objs]

    def _validate_create(self, db: Session, obj_in: ClimateMeasureCreate):
        """Validación automática llamada desde create() del BaseService"""
        # Validar unicidad del nombre
        MngClimateMeasureNameValidator.validate(db, obj_in.name)
        
        # Validar unicidad del short_name
        if db.query(self.model)\
           .filter(self.model.short_name == obj_in.short_name)\
           .first():
            raise ValueError(f"El nombre corto '{obj_in.short_name}' ya existe")

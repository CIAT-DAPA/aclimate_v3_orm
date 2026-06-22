from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from ..database.base import Base


class MngCountryClimateMeasure(Base):
    __tablename__ = 'mng_country_climate_measure'

    id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey('mng_country.id'), nullable=False)
    measure_id = Column(Integer, ForeignKey('mng_climate_measure.id'), nullable=False)
    description = Column(Text, nullable=True)
    store = Column(String(255), nullable=True)
    workspace = Column(String(255), nullable=True)

    country = relationship('MngCountry', back_populates='country_climate_measures')
    measure = relationship('MngClimateMeasure', back_populates='country_climate_measures')
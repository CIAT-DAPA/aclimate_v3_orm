from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import relationship
from ..database.base import Base
from ..enums import Period


class MngCountryClimateMeasure(Base):
    __tablename__ = 'mng_country_climate_measure'

    id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey('mng_country.id'), nullable=False)
    measure_id = Column(Integer, ForeignKey('mng_climate_measure.id'), nullable=False)
    spatial_forecast = Column(Boolean, default=False)
    spatial_climate = Column(Boolean, default=False)
    location_forecast = Column(Boolean, default=False)
    location_climate = Column(Boolean, default=False)
    spatial_climate_conf = Column(JSONB, nullable=True)
    location_climate_conf = Column(ARRAY(Enum(Period)), nullable=True)
    description = Column(Text, nullable=True)

    country = relationship('MngCountry', back_populates='country_climate_measures')
    measure = relationship('MngClimateMeasure', back_populates='country_climate_measures')
from sqlalchemy import Column, Integer, Boolean, String, Text, ForeignKey
import sqlalchemy
from sqlalchemy.orm import relationship
from ..database.base import Base

class MngCountryIndicator(Base):
    __tablename__ = 'mng_country_indicator'

    id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey('mng_country.id'), nullable=False)
    indicator_id = Column(Integer, ForeignKey('mng_indicators.id'), nullable=False)
    spatial_forecast = Column(Boolean, default=False)
    spatial_climate = Column(Boolean, default=False)
    location_forecast = Column(Boolean, default=False)
    location_climate = Column(Boolean, default=False)
    criteria = Column('criteria', sqlalchemy.JSON, nullable=True)
    description = Column(Text, nullable=True)
    store = Column(String(255), nullable=True)
    workspace = Column(String(255), nullable=True)

    country = relationship('MngCountry', back_populates='country_indicators')
    indicator = relationship('MngIndicator', back_populates='country_indicators')
    indicator_features = relationship('MngIndicatorsFeatures', back_populates='country_indicator', cascade="all, delete-orphan")

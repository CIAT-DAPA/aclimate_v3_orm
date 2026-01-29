from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from ..database.base import Base
from ..enums import IndicatorFeatureType


class MngIndicatorsFeatures(Base):
    __tablename__ = 'mng_indicators_features'

    id = Column(Integer, primary_key=True)
    country_indicator_id = Column(Integer, ForeignKey('mng_country_indicator.id'), nullable=False)
    title = Column(String(150), nullable=False)
    description = Column(Text)
    type = Column(Enum(IndicatorFeatureType), nullable=False)

    country_indicator = relationship('MngCountryIndicator', back_populates='indicator_features')

from enum import Enum

class Period(str, Enum):
    DAILY = "daily"
    MONTHLY = "monthly"
    ANNUAL = "annual"
    SEASONAL = "seasonal"
    DECADAL = "decadal"
    OTHER = "other"
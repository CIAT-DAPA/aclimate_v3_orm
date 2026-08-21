from enum import Enum

class Period(str, Enum):
    DAILY = "daily"
    MONTHLY = "monthly"
    CLIMATOLOGY = "climatology"
    ANNUAL = "annual"
    MULTIYEAR_MONTHLY = "multiyear_monthly"
    SEASONAL = "seasonal"
    DECADAL = "decadal"
    OTHER = "other"
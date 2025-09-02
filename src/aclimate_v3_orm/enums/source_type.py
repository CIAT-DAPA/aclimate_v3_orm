from enum import Enum

class SourceType(str, Enum):
    MANUAL = "MA"
    AUTOMATIC = "AU"
    SPATIAL = "SP"
    PLUVIOMETER = "PL"
    THERMOPLUVIOMETER = "TP"
from enum import Enum

class Modules(str, Enum):
    GEOGRAPHIC = "GEOGRAPHIC"  # Países, ADM1, ADM2, Localizaciones
    CLIMATE_DATA = "CLIMATE_DATA"  # Datos climáticos 
    CROP_DATA = "CROP_DATA"  # Datos de cultivos 
    INDICATORS_DATA = "INDICATORS_DATA"  # Datos de indicadores 
    STRESS_DATA = "STRESS_DATA"  # Datos de estreses
    PHENOLOGICAL_STAGE = "PHENOLOGICAL_STAGE"  # Etapas fenológicas 
    USER_MANAGEMENT = "USER_MANAGEMENT"  # Usuarios y roles
    CONFIGURATION = "CONFIGURATION"  # Configuración del sistema
    

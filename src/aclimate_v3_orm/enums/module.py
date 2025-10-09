from enum import Enum

class Modules(str, Enum):
    GEOGRAPHIC = "geographic"  # Países, ADM1, ADM2, Localizaciones
    CLIMATE_DATA = "climate_data"  # Datos climáticos 
    CROP_DATA = "crop_data"  # Datos de cultivos 
    INDICATORS_DATA = "indicators_data"  # Datos de indicadores 
    STRESS_DATA = "stress_data"  # Datos de estreses
    PHENOLOGICAL_STAGE = "phenological_stage"  # Etapas fenológicas 
    USER_MANAGEMENT = "user_management"  # Usuarios y roles
    CONFIGURATION = "configuration"  # Configuración del sistema
    

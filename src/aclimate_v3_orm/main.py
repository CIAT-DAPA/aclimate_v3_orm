from database import engine, SessionLocal
from database.base import Base
from models import *
#from services import *


# Crea todas las tablas
Base.metadata.create_all(bind=engine)

print("Tablas creadas correctamente.")



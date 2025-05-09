from database import engine, SessionLocal
from database.base import Base
from models import *
from services import *
from schemas import *


# Crea todas las tablas
Base.metadata.create_all(bind=engine)

print("Tablas creadas correctamente.")


# db = SessionLocal()

# country_service = MngAdmin1Service()

# test_country = Admin1Create(
#     name="Valle del Cauca",
#     enable=True,
#     country_id=1
# )

# print("=== Creando país ===")
# created_country = country_service.create(db, obj_in=test_country)
# print(f"País creado - ID: {created_country.id}, Nombre: {created_country.name}, ISO2: {created_country.country_id}")

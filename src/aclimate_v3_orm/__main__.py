from .database.base import Base, create_tables
from .database import engine, get_db
from .models import *
from .services import *
from .schemas import *

def main():
    service = MngAdmin1Service()

    test = service.get_all_enable()
    print(test)
    print("ORM Installed")

if __name__ == "__main__":
    main()


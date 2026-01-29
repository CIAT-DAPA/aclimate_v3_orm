from .database.base import Base, create_tables
from .database import engine, get_db
from .models import *
from .services import *
from .schemas import *
from .migrations import upgrade, downgrade, current

def main():
    print("ORM Installed")

if __name__ == "__main__":
    main()


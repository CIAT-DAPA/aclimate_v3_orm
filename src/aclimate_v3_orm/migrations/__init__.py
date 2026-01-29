"""
Alembic migrations for AClimate V3 ORM

This module provides helpers to execute database migrations programmatically.
"""
import os
from pathlib import Path
from alembic import command
from alembic.config import Config


def get_alembic_config():
    """Get Alembic configuration object"""
    migrations_dir = Path(__file__).parent
    alembic_ini = migrations_dir.parent / "alembic.ini"
    
    config = Config(str(alembic_ini))
    config.set_main_option("script_location", str(migrations_dir))
    
    # Load DATABASE_URL from environment
    from dotenv import load_dotenv
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        config.set_main_option("sqlalchemy.url", database_url)
    
    return config


def upgrade(revision: str = "head"):
    """
    Run migrations up to a specific revision.
    
    Args:
        revision: Target revision (default: "head" for latest)
        
    Example:
        from aclimate_v3_orm.migrations import upgrade
        upgrade()  # Upgrade to latest
    """
    config = get_alembic_config()
    command.upgrade(config, revision)
    print(f"✅ Migrations upgraded to: {revision}")


def downgrade(revision: str):
    """
    Rollback migrations to a specific revision.
    
    Args:
        revision: Target revision or "-1" for previous
        
    Example:
        from aclimate_v3_orm.migrations import downgrade
        downgrade("-1")  # Rollback one migration
    """
    config = get_alembic_config()
    command.downgrade(config, revision)
    print(f"✅ Migrations downgraded to: {revision}")


def current():
    """
    Display current migration revision.
    
    Example:
        from aclimate_v3_orm.migrations import current
        current()
    """
    config = get_alembic_config()
    command.current(config)


def history():
    """
    Display migration history.
    
    Example:
        from aclimate_v3_orm.migrations import history
        history()
    """
    config = get_alembic_config()
    command.history(config)


def stamp(revision: str = "head"):
    """
    Mark the database as being at a specific revision without running migrations.
    Useful for initial setup on existing databases.
    
    Args:
        revision: Target revision (default: "head")
        
    Example:
        from aclimate_v3_orm.migrations import stamp
        stamp()  # Mark as current
    """
    config = get_alembic_config()
    command.stamp(config, revision)
    print(f"✅ Database stamped at revision: {revision}")

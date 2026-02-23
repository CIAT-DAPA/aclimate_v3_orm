"""Add new enum in period

Revision ID: 0bd5be9ceceb
Revises: 5eb3fabe7aa8
Create Date: 2026-02-23 10:44:47.172303

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0bd5be9ceceb'
down_revision: Union[str, Sequence[str], None] = '5eb3fabe7aa8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add new value to Period enum
    # Note: This operation cannot be run inside a transaction in PostgreSQL
    op.execute("COMMIT")  # Commit the current transaction
    op.execute("ALTER TYPE period ADD VALUE IF NOT EXISTS 'multiyear_monthly'")


def downgrade() -> None:
    """Downgrade schema."""
    # PostgreSQL doesn't support removing enum values directly
    # We need to recreate the enum type without 'multiyear_monthly'
    
    # Step 1: Create a new temporary enum type without 'multiyear_monthly'
    op.execute("""
        CREATE TYPE period_old AS ENUM (
            'daily', 'monthly', 'annual', 'seasonal', 'decadal', 'other'
        )
    """)
    
    # Step 2: Alter columns that use the period enum to use the new type
    # Using USING clause to cast the values
    op.execute("""
        ALTER TABLE climate_historical_indicator 
        ALTER COLUMN period TYPE period_old 
        USING period::text::period_old
    """)
    
    op.execute("""
        ALTER TABLE mng_indicators 
        ALTER COLUMN temporality TYPE period_old 
        USING temporality::text::period_old
    """)
    
    # Step 3: Drop the old enum type
    op.execute("DROP TYPE period")
    
    # Step 4: Rename the new enum type to the original name
    op.execute("ALTER TYPE period_old RENAME TO period")

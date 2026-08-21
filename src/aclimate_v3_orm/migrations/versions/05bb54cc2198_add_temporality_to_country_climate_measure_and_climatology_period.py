"""Add temporality to mng_country_climate_measure and add CLIMATOLOGY to period enum

Revision ID: 05bb54cc2198
Revises: 50e6e27abd69
Create Date: 2026-08-21 11:44:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '05bb54cc2198'
down_revision: Union[str, Sequence[str], None] = '50e6e27abd69'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add new value to Period enum
    # Note: This operation cannot be run inside a transaction in PostgreSQL
    op.execute("COMMIT")  # Commit the current transaction
    op.execute("ALTER TYPE period ADD VALUE IF NOT EXISTS 'CLIMATOLOGY'")

    # Add temporality column as an array of the existing period enum type
    op.add_column(
        'mng_country_climate_measure',
        sa.Column(
            'temporality',
            postgresql.ARRAY(postgresql.ENUM(name='period', create_type=False)),
            nullable=False,
            server_default='{}'
        )
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop the added column
    op.drop_column('mng_country_climate_measure', 'temporality')

    # PostgreSQL doesn't support removing enum values directly.
    # The CLIMATOLOGY value is left in the period enum type.
    # To fully remove it, the enum type would need to be recreated without it
    # and all columns referencing it altered accordingly.
"""Add description, store, workspace to mng_country_indicator and create mng_country_climate_measure table

Revision ID: 50e6e27abd69
Revises: 0bd5be9ceceb
Create Date: 2026-06-22 16:22:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '50e6e27abd69'
down_revision: Union[str, Sequence[str], None] = '0bd5be9ceceb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # --- Step 1: Add columns to mng_country_indicator ---
    op.add_column('mng_country_indicator',
                  sa.Column('description', sa.Text(), nullable=True))
    op.add_column('mng_country_indicator',
                  sa.Column('store', sa.String(length=255), nullable=True))
    op.add_column('mng_country_indicator',
                  sa.Column('workspace', sa.String(length=255), nullable=True))

    # --- Step 2: Data migration: copy description from mng_indicators to mng_country_indicator ---
    connection = op.get_bind()
    connection.execute(text("""
        UPDATE mng_country_indicator
        SET description = mng_indicators.description
        FROM mng_indicators
        WHERE mng_country_indicator.indicator_id = mng_indicators.id
    """))

    # --- Step 3: Create mng_country_climate_measure table ---
    op.create_table('mng_country_climate_measure',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('country_id', sa.Integer(), nullable=False),
        sa.Column('measure_id', sa.Integer(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('store', sa.String(length=255), nullable=True),
        sa.Column('workspace', sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(['country_id'], ['mng_country.id'], ),
        sa.ForeignKeyConstraint(['measure_id'], ['mng_climate_measure.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop the new table
    op.drop_table('mng_country_climate_measure')

    # Remove added columns from mng_country_indicator
    op.drop_column('mng_country_indicator', 'workspace')
    op.drop_column('mng_country_indicator', 'store')
    op.drop_column('mng_country_indicator', 'description')
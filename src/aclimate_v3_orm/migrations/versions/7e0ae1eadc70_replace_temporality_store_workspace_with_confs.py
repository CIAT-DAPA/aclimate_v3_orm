"""Replace temporality/store/workspace with spatial_climate_conf and location_climate_conf

Revision ID: 7e0ae1eadc70
Revises: 05bb54cc2198
Create Date: 2026-08-21 12:10:00.000000

"""
import json
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '7e0ae1eadc70'
down_revision: Union[str, Sequence[str], None] = '05bb54cc2198'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _parse_pg_array(value) -> list:
    """Parse a PostgreSQL array literal like '{DAILY,MONTHLY}' into a Python list."""
    if value is None:
        return []
    if isinstance(value, list):
        return value
    s = str(value).strip()
    if s.startswith('{') and s.endswith('}'):
        s = s[1:-1]
    if s == '':
        return []
    return [item.strip() for item in s.split(',')]


def upgrade() -> None:
    """Upgrade schema."""
    # --- Step 1: Rename temporality to location_climate_conf ---
    op.alter_column(
        'mng_country_climate_measure',
        'temporality',
        new_column_name='location_climate_conf',
    )
    # Make it nullable (config is optional when location_climate is False)
    op.alter_column(
        'mng_country_climate_measure',
        'location_climate_conf',
        existing_type=postgresql.ARRAY(postgresql.ENUM(name='period', create_type=False)),
        nullable=True,
    )

    # --- Step 2: Add spatial_climate_conf (JSONB, nullable) ---
    op.add_column(
        'mng_country_climate_measure',
        sa.Column('spatial_climate_conf', postgresql.JSONB(), nullable=True),
    )

    # --- Step 3: Data migration ---
    # For each row build:
    #   - location_climate_conf = old temporality ONLY if location_climate is True (else NULL)
    #   - spatial_climate_conf  = per-temporality {temporality, store, workspace} ONLY if spatial_climate is True (else NULL)
    # store/workspace were stored as dash-separated values, one per temporality.
    connection = op.get_bind()

    result = connection.execute(text(
        "SELECT id, location_climate, spatial_climate, location_climate_conf, store, workspace "
        "FROM mng_country_climate_measure"
    ))
    rows = result.fetchall()

    for row in rows:
        row_id, location_climate, spatial_climate = row[0], row[1], row[2]
        temporality = _parse_pg_array(row[3])   # list of period enum names, e.g. ['DAILY', 'MONTHLY', ...]
        store = row[4]                          # dash-separated stores or None
        workspace = row[5]                      # dash-separated workspaces or None

        # location_climate_conf: only meaningful when location_climate is enabled
        location_conf = "{" + ",".join(temporality) + "}" if (location_climate and temporality) else None

        # spatial_climate_conf: only meaningful when spatial_climate is enabled
        spatial_conf = None
        if spatial_climate:
            stores = store.split('-') if store else []
            workspaces = workspace.split('-') if workspace else []
            spatial_conf = [
                {
                    "temporality": period_name.lower(),
                    "store": stores[i] if i < len(stores) else None,
                    "workspace": workspaces[i] if i < len(workspaces) else None,
                }
                for i, period_name in enumerate(temporality)
            ] or None

        connection.execute(
            text(
                "UPDATE mng_country_climate_measure "
                "SET location_climate_conf = CAST(:location_conf AS period[]), "
                "spatial_climate_conf = CAST(:spatial_conf AS JSONB) "
                "WHERE id = :row_id"
            ),
            {
                "location_conf": location_conf,
                "spatial_conf": json.dumps(spatial_conf) if spatial_conf is not None else None,
                "row_id": row_id,
            },
        )

    # --- Step 4: Drop legacy columns ---
    op.drop_column('mng_country_climate_measure', 'store')
    op.drop_column('mng_country_climate_measure', 'workspace')


def downgrade() -> None:
    """Downgrade schema."""
    # Recreate legacy columns
    op.add_column(
        'mng_country_climate_measure',
        sa.Column('workspace', sa.String(length=255), nullable=True),
    )
    op.add_column(
        'mng_country_climate_measure',
        sa.Column('store', sa.String(length=255), nullable=True),
    )

    # Best-effort reconstruction of store/workspace from spatial_climate_conf
    connection = op.get_bind()
    result = connection.execute(text(
        "SELECT id, spatial_climate_conf, location_climate_conf "
        "FROM mng_country_climate_measure"
    ))
    rows = result.fetchall()

    for row in rows:
        row_id, spatial_conf, location_conf = row[0], row[1] or [], row[2] or []
        stores = [c.get('store') for c in spatial_conf if isinstance(c, dict) and c.get('store')]
        workspaces = [c.get('workspace') for c in spatial_conf if isinstance(c, dict) and c.get('workspace')]
        store_value = '-'.join(stores) if stores else None
        workspace_value = '-'.join(workspaces) if workspaces else None

        connection.execute(
            text(
                "UPDATE mng_country_climate_measure "
                "SET store = :store, workspace = :workspace "
                "WHERE id = :row_id"
            ),
            {"store": store_value, "workspace": workspace_value, "row_id": row_id},
        )

    # Drop the new conf columns
    op.drop_column('mng_country_climate_measure', 'spatial_climate_conf')

    # Rename back to temporality and restore NOT NULL + default '{}'
    op.alter_column(
        'mng_country_climate_measure',
        'location_climate_conf',
        new_column_name='temporality',
    )
    op.alter_column(
        'mng_country_climate_measure',
        'temporality',
        existing_type=postgresql.ARRAY(postgresql.ENUM(name='period', create_type=False)),
        nullable=False,
        server_default='{}',
    )

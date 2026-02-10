"""add_machine_name_to_mng_location

Revision ID: a41a6a421185
Revises: 11c21a19c29e
Create Date: 2026-02-10 11:25:15.143755

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = 'a41a6a421185'
down_revision: Union[str, Sequence[str], None] = '11c21a19c29e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Step 1: Add machine_name column as nullable first
    op.add_column('mng_location', 
                  sa.Column('machine_name', sa.String(length=255), nullable=True))
    
    # Step 2: Populate machine_name for existing records
    # Generate unique machine_name from name field (slugified)
    connection = op.get_bind()
    
    # Get all locations
    result = connection.execute(text(
        "SELECT id, name FROM mng_location"
    ))
    
    locations = result.fetchall()
    
    # Helper function to slugify text
    def slugify(text_value: str, location_id: int) -> str:
        """Convert text to slug format"""
        if not text_value:
            return f"location-{location_id}"
        
        # Convert to lowercase
        slug = text_value.lower()
        
        # Replace spaces and special characters with hyphens
        import re
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug)
        
        # Remove leading/trailing hyphens
        slug = slug.strip('-')
        
        # If empty after cleaning, use id
        if not slug:
            slug = f"location-{location_id}"
        
        return slug
    
    # Update each location with a unique machine_name
    used_slugs = set()
    for location_id, name in locations:
        base_slug = slugify(name, location_id)
        slug = base_slug
        counter = 1
        
        # Ensure uniqueness
        while slug in used_slugs:
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        used_slugs.add(slug)
        
        # Update the record
        connection.execute(
            text("UPDATE mng_location SET machine_name = :slug WHERE id = :id"),
            {"slug": slug, "id": location_id}
        )
    
    # Step 3: Make machine_name NOT NULL
    op.alter_column('mng_location', 'machine_name',
                    existing_type=sa.String(length=255),
                    nullable=False)
    
    # Step 4: Add unique constraint
    op.create_unique_constraint('uq_mng_location_machine_name', 
                                'mng_location', 
                                ['machine_name'])


def downgrade() -> None:
    """Downgrade schema."""
    # Remove unique constraint
    op.drop_constraint('uq_mng_location_machine_name', 'mng_location', type_='unique')
    
    # Remove machine_name column
    op.drop_column('mng_location', 'machine_name')

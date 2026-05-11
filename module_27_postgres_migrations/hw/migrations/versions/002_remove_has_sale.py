"""Remove has_sale from users

Revision ID: 002_remove_has_sale
Revises: 001_init_migration
Create Date: 2024-01-02 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002_remove_has_sale'
down_revision = '001_init_migration'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column('users', 'has_sale')


def downgrade() -> None:
    op.add_column('users', sa.Column('has_sale', sa.Boolean(), nullable=True))

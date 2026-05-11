"""Add patronymic to users

Revision ID: 005_add_patronymic
Revises: 001_init_migration
Create Date: 2024-01-05 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '005_add_patronymic'
down_revision = '001_init_migration'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('patronymic', sa.String(length=50), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'patronymic')

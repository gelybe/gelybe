"""Add surname to users

Revision ID: 004_add_surname
Revises: 002_remove_has_sale
Create Date: 2024-01-04 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '004_add_surname'
down_revision = '002_remove_has_sale'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('surname', sa.String(length=50), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'surname')

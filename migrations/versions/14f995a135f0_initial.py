"""initial

Revision ID: 14f995a135f0
Revises: a0ea238626e8
Create Date: 2023-05-16 12:50:19.020422

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '14f995a135f0'
down_revision = 'a0ea238626e8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tokens', 'token',
               existing_type=sa.UUID(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tokens', 'token',
               existing_type=sa.UUID(),
               nullable=False)
    # ### end Alembic commands ###
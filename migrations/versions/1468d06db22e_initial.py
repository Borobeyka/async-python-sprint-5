"""initial

Revision ID: 1468d06db22e
Revises: a752d6bf1597
Create Date: 2023-05-16 12:44:40.300874

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '1468d06db22e'
down_revision = 'a752d6bf1597'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('files', sa.Column('user_id', sa.Integer(), nullable=True))
    op.drop_constraint('files_author_id_fkey', 'files', type_='foreignkey')
    op.create_foreign_key(None, 'files', 'users', ['user_id'], ['id'])
    op.drop_column('files', 'author_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('files', sa.Column('author_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'files', type_='foreignkey')
    op.create_foreign_key('files_author_id_fkey', 'files', 'users', ['author_id'], ['id'])
    op.drop_column('files', 'user_id')
    # ### end Alembic commands ###
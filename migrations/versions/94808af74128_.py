"""empty message

Revision ID: 94808af74128
Revises: eaaf061e4c3c
Create Date: 2019-12-26 15:15:14.768427

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94808af74128'
down_revision = 'eaaf061e4c3c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('date_modified', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'date_modified')
    # ### end Alembic commands ###
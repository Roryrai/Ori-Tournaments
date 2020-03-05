"""added tournament format

Revision ID: 432777ee02a5
Revises: 381918c99b68
Create Date: 2020-03-05 09:06:03.422565

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '432777ee02a5'
down_revision = '381918c99b68'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tournament', sa.Column('format', sa.String(length=10), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tournament', 'format')
    # ### end Alembic commands ###
"""unique tournament group constraint

Revision ID: 480eec781a4e
Revises: 066e5a410888
Create Date: 2019-11-28 11:35:24.367108

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '480eec781a4e'
down_revision = '066e5a410888'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('unique_tournament_group_constraint', 'runner_groups', ['user_id', 'tournament_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('unique_tournament_group_constraint', 'runner_groups', type_='unique')
    # ### end Alembic commands ###

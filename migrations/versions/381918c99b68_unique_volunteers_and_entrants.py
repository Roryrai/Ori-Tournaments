"""unique volunteers and entrants

Revision ID: 381918c99b68
Revises: 16a307f414aa
Create Date: 2019-12-27 16:40:01.175168

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '381918c99b68'
down_revision = '16a307f414aa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('unique_tournament_entrant_constraint', 'tournament_entrant', ['user_id', 'tournament_id'])
    op.create_unique_constraint('unique_tournament_volunteer_constraint', 'tournament_volunteer', ['user_id', 'tournament_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('unique_tournament_volunteer_constraint', 'tournament_volunteer', type_='unique')
    op.drop_constraint('unique_tournament_entrant_constraint', 'tournament_entrant', type_='unique')
    # ### end Alembic commands ###
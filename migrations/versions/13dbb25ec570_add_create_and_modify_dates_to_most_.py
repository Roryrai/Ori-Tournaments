"""add create and modify dates to most things

Revision ID: 13dbb25ec570
Revises: aa748327e114
Create Date: 2019-12-26 15:42:48.137854

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13dbb25ec570'
down_revision = 'aa748327e114'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bracket_node', sa.Column('date_created', sa.DateTime(), nullable=True))
    op.add_column('bracket_node', sa.Column('date_modified', sa.DateTime(), nullable=True))
    op.add_column('group_member', sa.Column('date_created', sa.DateTime(), nullable=True))
    op.add_column('question', sa.Column('date_created', sa.DateTime(), nullable=True))
    op.add_column('question', sa.Column('date_modified', sa.DateTime(), nullable=True))
    op.add_column('question_response', sa.Column('date_created', sa.DateTime(), nullable=True))
    op.add_column('question_response', sa.Column('date_modified', sa.DateTime(), nullable=True))
    op.add_column('race', sa.Column('date_modified', sa.DateTime(), nullable=True))
    op.add_column('race_result', sa.Column('date_created', sa.DateTime(), nullable=True))
    op.add_column('race_result', sa.Column('date_modified', sa.DateTime(), nullable=True))
    op.add_column('tournament', sa.Column('date_created', sa.DateTime(), nullable=True))
    op.add_column('tournament', sa.Column('date_modified', sa.DateTime(), nullable=True))
    op.add_column('tournament_entrant', sa.Column('date_created', sa.DateTime(), nullable=True))
    op.add_column('tournament_volunteer', sa.Column('date_created', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tournament_volunteer', 'date_created')
    op.drop_column('tournament_entrant', 'date_created')
    op.drop_column('tournament', 'date_modified')
    op.drop_column('tournament', 'date_created')
    op.drop_column('race_result', 'date_modified')
    op.drop_column('race_result', 'date_created')
    op.drop_column('race', 'date_modified')
    op.drop_column('question_response', 'date_modified')
    op.drop_column('question_response', 'date_created')
    op.drop_column('question', 'date_modified')
    op.drop_column('question', 'date_created')
    op.drop_column('group_member', 'date_created')
    op.drop_column('bracket_node', 'date_modified')
    op.drop_column('bracket_node', 'date_created')
    # ### end Alembic commands ###

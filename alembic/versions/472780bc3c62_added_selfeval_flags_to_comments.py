"""added selfeval flags to comments

Revision ID: 472780bc3c62
Revises: 3b053548b60f
Create Date: 2014-10-30 16:31:09.871401

"""

# revision identifiers, used by Alembic.
revision = '472780bc3c62'
down_revision = '3b053548b60f'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('PostsForAnswersAndPostsForComments', sa.Column('evaluation', sa.Boolean(), nullable=False))
    op.add_column('PostsForAnswersAndPostsForComments', sa.Column('selfeval', sa.Boolean(), nullable=False))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('PostsForAnswersAndPostsForComments', 'selfeval')
    op.drop_column('PostsForAnswersAndPostsForComments', 'evaluation')
    ### end Alembic commands ###
"""empty message

Revision ID: 3f79c30fe037
Revises: 0cccbd78c1f3
Create Date: 2018-04-29 13:53:08.860204

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f79c30fe037'
down_revision = '0cccbd78c1f3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('note', sa.Column('title', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('note', 'title')
    # ### end Alembic commands ###
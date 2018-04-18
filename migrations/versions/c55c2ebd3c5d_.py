"""empty message

Revision ID: c55c2ebd3c5d
Revises: aa1ebe1193a4
Create Date: 2018-04-18 22:01:54.836202

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c55c2ebd3c5d'
down_revision = 'aa1ebe1193a4'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('note', 'book_id', existing_type=sa.Integer, type_=sa.Text)


def downgrade():
    op.alter_column('note', 'book_id', existing_type=sa.Text, type_=sa.Integer)

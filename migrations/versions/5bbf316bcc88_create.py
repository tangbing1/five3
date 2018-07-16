"""create

Revision ID: 5bbf316bcc88
Revises: 402f24533b82
Create Date: 2018-07-15 11:47:08.300412

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5bbf316bcc88'
down_revision = '402f24533b82'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('city', sa.String(length=10), nullable=True))
    op.add_column('user', sa.Column('sex', sa.String(length=3), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'sex')
    op.drop_column('user', 'city')
    # ### end Alembic commands ###

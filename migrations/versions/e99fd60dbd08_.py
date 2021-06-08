"""empty message

Revision ID: e99fd60dbd08
Revises: 
Create Date: 2020-12-02 14:52:20.600567

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e99fd60dbd08'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('message', sa.Text(), nullable=True),
    sa.Column('sender_id', sa.Integer(), nullable=False, foreign_key='User.id'),
    sa.Column('timestamp', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_message'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('message')
    # ### end Alembic commands ###
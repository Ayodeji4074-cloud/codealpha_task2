"""Initial migration

Revision ID: fe77d1f39002
Revises: 
Create Date: 2024-08-01 01:21:33.799536

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe77d1f39002'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('menu',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('description', sa.String(length=250), nullable=True),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('is_discounted', sa.Boolean(), nullable=True),
    sa.Column('is_drink', sa.Boolean(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sample',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('is_staff', sa.Boolean(), nullable=True),
    sa.Column('registered_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('menu_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['menu_id'], ['menu.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order')
    op.drop_table('user')
    op.drop_table('sample')
    op.drop_table('menu')
    # ### end Alembic commands ###

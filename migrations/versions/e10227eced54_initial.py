"""initial

Revision ID: e10227eced54
Revises: 
Create Date: 2024-08-12 07:31:11.189259

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e10227eced54'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admins',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('tg_id', sa.BigInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('campaigns',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('hashtag', sa.String(length=255), nullable=False),
    sa.Column('goal', sa.BigInteger(), nullable=False),
    sa.Column('collected', sa.BigInteger(), nullable=False),
    sa.Column('user_count', sa.BigInteger(), nullable=False),
    sa.Column('status', sa.BigInteger(), nullable=False),
    sa.Column('charity_id', sa.BigInteger(), nullable=False),
    sa.Column('help_receiver_count', sa.BigInteger(), nullable=False),
    sa.Column('link_open_event_count', sa.BigInteger(), nullable=False),
    sa.Column('published_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('finished_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('finish_payment_id', sa.BigInteger(), nullable=True),
    sa.Column('title', sa.String(length=500), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('tg_id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reviews',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('tg_id', sa.BigInteger(), nullable=False),
    sa.Column('text', sa.String(length=500), nullable=False),
    sa.Column('type', sa.SmallInteger(), nullable=False),
    sa.ForeignKeyConstraint(['tg_id'], ['users.tg_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reviews')
    op.drop_table('users')
    op.drop_table('campaigns')
    op.drop_table('admins')
    # ### end Alembic commands ###

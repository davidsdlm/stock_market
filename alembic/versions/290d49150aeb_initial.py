"""initial

Revision ID: 290d49150aeb
Revises: 
Create Date: 2024-07-15 18:40:55.214723

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '290d49150aeb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('companies',
    sa.Column('pk', sa.String(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('content', sa.String(), nullable=False),
    sa.Column('tokens', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('embedding', sa.ARRAY(sa.Float()), nullable=True),
    sa.PrimaryKeyConstraint('pk', 'id')
    )
    op.create_table('news',
    sa.Column('pk', sa.String(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('content', sa.String(), nullable=False),
    sa.Column('tokens', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('embedding', sa.ARRAY(sa.Float()), nullable=True),
    sa.PrimaryKeyConstraint('pk', 'id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('news')
    op.drop_table('companies')
    # ### end Alembic commands ###

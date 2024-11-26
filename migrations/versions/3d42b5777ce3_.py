"""empty message

Revision ID: 3d42b5777ce3
Revises: 
Create Date: 2024-11-26 22:36:10.560122

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d42b5777ce3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('service',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=128), nullable=False),
    sa.Column('title', sa.VARCHAR(length=256), nullable=False),
    sa.Column('price', sa.DECIMAL(scale=2), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=32), nullable=False),
    sa.Column('is_admin', sa.BOOLEAN(), nullable=True),
    sa.Column('phone', sa.VARCHAR(length=16), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('entry',
    sa.Column('entry_time', sa.TIMESTAMP(), nullable=False),
    sa.Column('user_id', sa.BIGINT(), nullable=False),
    sa.Column('service_id', sa.BIGINT(), nullable=False),
    sa.ForeignKeyConstraint(['service_id'], ['service.id'], onupdate='CASCADE', ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], onupdate='CASCADE', ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('entry_time')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('entry')
    op.drop_table('user')
    op.drop_table('service')
    # ### end Alembic commands ###
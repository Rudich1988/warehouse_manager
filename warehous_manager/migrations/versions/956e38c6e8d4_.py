"""empty message

Revision ID: 956e38c6e8d4
Revises: 3723d36aa159
Create Date: 2024-10-04 15:29:45.713364

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '956e38c6e8d4'
down_revision: Union[str, None] = '3723d36aa159'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('product_count', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('orders', 'product_count')
    # ### end Alembic commands ###

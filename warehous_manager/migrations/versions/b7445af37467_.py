"""empty message

Revision ID: b7445af37467
Revises: 316fa0e14b58
Create Date: 2024-10-14 18:33:42.120720

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7445af37467'
down_revision: Union[str, None] = '316fa0e14b58'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_order_items_order_id', table_name='order_items')
    op.drop_index('ix_order_items_product_id', table_name='order_items')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_order_items_product_id', 'order_items', ['product_id'], unique=False)
    op.create_index('ix_order_items_order_id', 'order_items', ['order_id'], unique=False)
    # ### end Alembic commands ###

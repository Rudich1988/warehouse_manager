'''
import os

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from dotenv import load_dotenv

from warehous_manager.db.db import ModelBase
from warehous_manager.models import *

load_dotenv()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)
database_url = os.getenv("DATABASE_URL") + "?async_fallback=True"
config.set_main_option("sqlalchemy.url", database_url)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = ModelBase.metadata

from sqlalchemy import orm

from warehous_manager.config.base import Config
from warehous_manager.models.orders import Order
from warehous_manager.models.order_items import OrderItem
from warehous_manager.models.products import Product
'''




'''
op.create_check_constraint(
        'check_positive_price', 'products', 'price > 0'
    )
    op.create_check_constraint(
        'check_non_negative_quantity', 'products', 'quantity >= 0'
    )

op.create_check_constraint(
        'check_positive_quantity', 'order_items', 'quantity > 0'
    )
'''
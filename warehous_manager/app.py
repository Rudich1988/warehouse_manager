from fastapi import FastAPI


app = FastAPI()

from warehous_manager.routers.orders import router as router_orders
from warehous_manager.routers.products import router as router_products


app.include_router(router_orders)
app.include_router(router_products)

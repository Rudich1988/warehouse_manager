from decimal import Decimal


class InventoryManagerService:
    def get_product_count(self, products: list):
        products_quantity = 0
        for product in products:
            products_quantity += product['quantity']
        return products_quantity

    def prepare_products_data(self, data: list):
        products_data = {}
        ids = []
        for product in data:
            ids.append(product['id'])
        products_data['ids'] = ids
        products_data['data'] = data
        return products_data

    def get_order_data(
            self,
            products: list,
            data: dict
    ):
        products_data = data['products']
        order_id = data['order_id']
        quantities = {product['id']: product['quantity'] for product in products_data}
        order_cost = Decimal(0)
        orders_items_data = []

        for product in products:
            quantity = quantities.get(product.id)
            order_item = {
                'product_id': product.id,
                'order_id': order_id,
                'product_price': product.price,
                'quantity': quantity,
                'product_name': product.name
            }
            orders_items_data.append(order_item)
            order_cost += (product.price * quantity)

        order_data = {
            'order_cost': order_cost,
            'order_items': orders_items_data
        }
        return order_data

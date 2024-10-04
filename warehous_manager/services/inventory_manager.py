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

    def get_order_data(self, products: list, products_data: list):
        quantities = {product['id']: product['quantity'] for product in products_data}
        products_data = []
        order_cost = Decimal(0)
        for product in products:
            quantity = quantities.get(product.id)
            product_data = {
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'quantity': quantity
            }
            order_cost += (product.price * quantity)
            products_data.append(product_data)
        order_data = {
            'order_cost': order_cost,
            'products': products_data
        }
        return order_data

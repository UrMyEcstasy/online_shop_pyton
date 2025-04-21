from shop.models import Product

CART_SESSION_ID = 'cart'


class Cart:
    """
    A shopping cart class that manages cart data in the user's session.

    Supports adding, updating, removing products, and calculating the total price.
    """

    def __init__(self, request):
        """
        Initialize the cart with the given request session.
        Creates an empty cart dictionary in session if not already present.
        """
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Iterate over cart items and attach corresponding Product instances.
        Also calculates total price per item.
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            pid = str(product.id)
            if pid in cart:
                cart[pid]['product'] = product

        for item in cart.values():
            if 'product' in item:
                item['total_price'] = int(item['price']) * int(item['quantity'])
                yield item

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add or update a product in the cart.

        Args:
            product (Product): The product to add or update.
            quantity (int): Quantity to add or set.
            override_quantity (bool): If True, sets quantity directly; otherwise, increments it.
        """
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        if self.cart[product_id]['quantity'] <= 0:
            del self.cart[product_id]

        self.save()

    def remove(self, product):
        """
        Remove a product from the cart.

        Args:
            product (Product): The product to remove.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        """
        Clear all items from the cart.
        """
        self.session[CART_SESSION_ID] = {}
        self.save()

    def save(self):
        """
        Mark the session as modified to ensure it's saved.
        """
        self.session.modified = True

    def get_total_price(self):
        """
        Return the total price of all items in the cart.
        """
        return sum(
            int(item['price']) * item['quantity'] for item in self.cart.values()
        )

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from shop.models import Product


class Order(models.Model):
    """
    Model representing a customer's order.

    Each order is linked to a user and may contain multiple items and an optional discount.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    discount = models.IntegerField(blank=True, null=True, default=None)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        """
        Return a readable string representation of the order.
        """
        return f"{self.user} - {self.id}"

    @property
    def get_total_price(self):
        """
        Calculate the total price of the order, applying discount if available.
        """
        total = sum(item.get_cost() for item in self.items.all())
        if self.discount:
            discount_price = (self.discount / 100) * total
            return int(total - discount_price)
        return total


class OrderItem(models.Model):
    """
    Model representing a single item within an order.

    Stores the product, its price at the time of ordering, and quantity.
    """

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_items'
    )
    price = models.IntegerField()
    quantity = models.SmallIntegerField(default=1)

    def __str__(self):
        """
        Return the ID of the order item.
        """
        return str(self.id)

    def get_cost(self):
        """
        Calculate and return the total cost for this item.
        """
        return self.price * self.quantity


class Coupon(models.Model):
    """
    Model representing a discount coupon.

    Includes validity range, percentage discount, and whether it's currently active.
    """

    code = models.CharField(max_length=30, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    status = models.BooleanField(default=False)

    def __str__(self):
        """
        Return the coupon code.
        """
        return self.code

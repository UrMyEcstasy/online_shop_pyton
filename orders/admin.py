from django.contrib import admin
from orders.models import Order, OrderItem, Coupon


class OrderItemInline(admin.TabularInline):
    """
    Inline admin interface for OrderItem within the Order admin view.
    Allows editing order items directly on the Order page.
    """
    model = OrderItem
    raw_id_fields = ('product',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Order model.
    Displays basic order information and allows filtering by status.
    """
    list_display = ('id', 'user', 'created', 'status')
    list_filter = ('status',)
    inlines = (OrderItemInline,)


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Coupon model.
    Enables searching and filtering of coupons by status and validity dates.
    """
    list_display = ('code', 'valid_from', 'valid_to', 'discount', 'status')
    list_filter = ('status', 'valid_from', 'valid_to')
    search_fields = ('code',)

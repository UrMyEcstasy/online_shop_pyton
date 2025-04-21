from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone

from cart.utils.cart import Cart
from orders.forms import CouponForm
from orders.models import Order, OrderItem, Coupon


@login_required()
def order_create(request):
    """
    Create a new order for the authenticated user using the items in the cart.

    Creates an Order and corresponding OrderItems, then clears the cart.
    Redirects to the order detail page.
    """
    cart = Cart(request)
    order = Order.objects.create(user=request.user)
    for item in cart:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            price=item['price'],
            quantity=item['quantity']
        )
    cart.clear()
    return redirect('orders:detail', order.id)


@login_required()
def detail(request, order_id):
    """
    Display the detail page for a specific order, including coupon form.

    Args:
        order_id (int): ID of the order to display.
    """
    order = get_object_or_404(Order, id=order_id)
    form = CouponForm()
    return render(request, 'orders/order.html', {'order': order, 'form': form})


@login_required()
def payment(request, order_id, price):
    """
    Simulate a successful payment for demonstration purposes.

    Displays a static confirmation page with order ID.
    """
    return render(request, 'orders/payment_success.html', {'order_id': order_id})


@require_POST
def coupon_apply(request, order_id):
    """
    Apply a valid coupon to an order if it exists and is within its validity period.

    Displays error message if coupon is invalid or expired.
    """
    now = timezone.now()
    form = CouponForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(
                code__iexact=code,
                valid_from__lte=now,
                valid_to__gt=now,
                status=True
            )
        except Coupon.DoesNotExist:
            messages.error(request, 'This coupon does not exist.', extra_tags='danger')
            return redirect('orders:detail', order_id)

        order = Order.objects.get(id=order_id)
        order.discount = coupon.discount
        order.save()
        return redirect('orders:detail', order_id)

from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from shop.models import Product
from .utils.cart import Cart
from .forms import Add2CartForm


def cart_detail(request):
    """
    Display the contents of the shopping cart.
    """
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})


@require_POST
def cart_add(request, product_id):
    """
    Add a product to the cart or update its quantity.

    This view only accepts POST requests and uses Add2CartForm for validation.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = Add2CartForm(request.POST)

    if form.is_valid():
        data = form.cleaned_data
        cart.add(product=product, quantity=data['quantity'], override_quantity=True)

    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    """
    Remove a product entirely from the cart.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_increment(request, product_id):
    """
    Increment the quantity of a product in the cart by 1.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product, quantity=1, override_quantity=False)
    return redirect('cart:cart_detail')


def cart_decrement(request, product_id):
    """
    Decrement the quantity of a product in the cart by 1.
    If the quantity reaches 0, the product is removed from the cart.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product, quantity=-1, override_quantity=False)
    return redirect('cart:cart_detail')

from django.shortcuts import render, get_object_or_404
from cart.forms import Add2CartForm
from shop.models import Product, Category


def home(request, slug=None):
    """
    Display the homepage with a list of active products.

    If a category slug is provided, filters products by that category.
    Shows only top-level categories (is_sub=False).
    """
    products = Product.objects.filter(status=True).distinct()
    categories = Category.objects.filter(is_sub=False)

    if slug:
        category = get_object_or_404(Category, slug=slug)
        products = products.filter(category=category).distinct()

    return render(request, 'shop/home.html', {
        'products': products,
        'categories': categories
    })


def product_detail(request, slug):
    """
    Display the detail page for a specific product.

    Includes the form to add the product to the cart.
    """
    product = get_object_or_404(Product, slug=slug)
    form = Add2CartForm()

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'form': form
    })

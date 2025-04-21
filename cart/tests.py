import pytest
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from shop.models import Product
from cart.utils.cart import Cart

@pytest.mark.django_db
def get_request_with_session():
    factory = RequestFactory()
    request = factory.get('/')
    middleware = SessionMiddleware(lambda x: None)
    middleware.process_request(request)
    request.session.save()
    return request

@pytest.mark.django_db
def test_cart_add(client):
    request = RequestFactory().get('/')
    request.session = client.session
    cart = Cart(request)
    product = Product.objects.create(name='Test', slug='test', price=100, description='desc', image='img.jpg', status=True)
    cart.add(product, quantity=2)
    assert str(product.id) in cart.cart


@pytest.mark.django_db
def test_cart_increment(client):
    request = RequestFactory().get('/')
    request.session = client.session
    cart = Cart(request)
    product = Product.objects.create(name='Test2', slug='test2', price=100, description='desc', image='img.jpg', status=True)
    cart.add(product)
    cart.add(product)
    assert cart.cart[str(product.id)]['quantity'] == 2


@pytest.mark.django_db
def test_cart_add_and_total_price():
    request = get_request_with_session()
    cart = Cart(request)
    product = Product.objects.create(
        name='Product A', slug='product-a', price=100,
        description='desc', image='img.jpg', status=True
    )
    cart.add(product, quantity=3)
    assert cart.get_total_price() == 300
    assert str(product.id) in cart.cart


@pytest.mark.django_db
def test_cart_remove():
    request = get_request_with_session()
    cart = Cart(request)
    product = Product.objects.create(
        name='Product B', slug='product-b', price=50,
        description='desc', image='img.jpg', status=True
    )
    cart.add(product, quantity=1)
    cart.remove(product)
    assert str(product.id) not in cart.cart


@pytest.mark.django_db
def test_cart_clear():
    request = get_request_with_session()
    cart = Cart(request)
    product = Product.objects.create(
        name='Product C', slug='product-c', price=20,
        description='desc', image='img.jpg', status=True
    )
    cart.add(product, quantity=2)
    cart.clear()


    cart = Cart(request)
    assert cart.cart == {}


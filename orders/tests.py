import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from shop.models import Product
from orders.models import Order, OrderItem, Coupon
from accounts.models import User


@pytest.mark.django_db
def test_order_total_price_with_discount():
    User = get_user_model()
    user = User.objects.create_user('user@test.com', 'Test User', '1234567890', 'password123')
    product = Product.objects.create(
        name='Item', slug='item', price=100, description='desc', image='img.jpg', status=True
    )
    order = Order.objects.create(user=user, discount=10)
    OrderItem.objects.create(order=order, product=product, price=100, quantity=2)

    assert order.get_total_price == 180  # 200 - 10%

@pytest.mark.django_db
def test_order_create_view(client):
    user = User.objects.create_user(email='a@a.com', full_name='User', phone_number='123', password='pass')
    client.login(email='a@a.com', password='pass')
    session = client.session
    product = Product.objects.create(name='Tool', slug='tool', price=50, description='desc', image='img.jpg', status=True)
    session['cart'] = {str(product.id): {'quantity': 1, 'price': '50'}}
    session.save()
    response = client.get(reverse('orders:order_create'))
    assert response.status_code == 302
    assert Order.objects.count() == 1


@pytest.mark.django_db
def test_coupon_apply_valid(client):
    user = User.objects.create_user(email='a@a.com', full_name='User', phone_number='123', password='pass')
    client.login(email='a@a.com', password='pass')
    order = Order.objects.create(user=user)
    Coupon.objects.create(code='SAVE10', discount=10, status=True, valid_from='2020-01-01', valid_to='2099-01-01')
    response = client.post(reverse('orders:coupon_apply', args=[order.id]), {'code': 'SAVE10'})
    order.refresh_from_db()
    assert order.discount == 10

import pytest
from django.urls import reverse
from shop.models import Product, Category


@pytest.mark.django_db
def test_category_creation():
    category = Category.objects.create(name='Chainsaws', slug='chainsaws')
    assert str(category) == 'Chainsaws'


@pytest.mark.django_db
def test_product_category_association(client):
    category = Category.objects.create(name='Tools', slug='tools')
    product = Product.objects.create(
        name='Drill', slug='drill', price=120,
        description='Power drill', image='img.jpg', status=True
    )
    product.category.add(category)

    response = client.get(reverse('shop:category_filter', args=[category.slug]))
    assert response.status_code == 200
    assert product.name.encode() in response.content

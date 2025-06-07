import pytest
from django.urls import reverse
from store_app.models import Product, Category


def test_index(client):
    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 200
    assert 'Это главная страница' in response.content.decode('utf-8')


@pytest.mark.django_db
def test_product_list(client, product, category):
    url = reverse('products')
    response = client.get(url)

    assert response.status_code == 200

    assert product.name.encode() in response.content


@pytest.mark.django_db
def test_product_detail(client, product, category):
    url = reverse('product_detail', args=[product.id])
    response = client.get(url)

    assert response.status_code == 200

    assert product.name.encode() in response.content
    assert category.name.encode() in response.content


@pytest.mark.django_db
def test_product_filter(client, product, category):
    url = reverse('products')
    response = client.get(url, {"price": 10.1})
    assert response.status_code == 200

    assert product.name in response.content.decode('utf-8')

    low_price_product = Product.objects.create(
        name='Низкая цена',
        description='Тут низкая цена',
        price=2,
        category=category,
    )
    assert low_price_product.name not in response.content.decode('utf-8')
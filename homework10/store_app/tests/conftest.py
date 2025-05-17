import pytest
from store_app.models import Product, Category


@pytest.fixture
def category():
    return Category.objects.create(name='Тестовая категория')


@pytest.fixture
def product(category):
    return Product.objects.create(
        name='Тестовый товар',
        description='Описание тестового товара',
        price=10.1,
        author=category,
    )


@pytest.fixture
def product2(category):
    return Product.objects.create(
        name='Другой тестовый товар',
        description='Описание другого тестового товара',
        price=50.5,
        author=category,
    )

import pytest
from store_app.models import Product, Category


@pytest.mark.django_db
def test_category_creation(category):
    assert Category.objects.count() == 1
    assert category.name == 'Тестовая категория'
    assert str(category) == 'Тестовая категория'


@pytest.mark.django_db
def test_product_creation(product):
    assert Product.objects.count() == 1
    assert product.name == 'Тестовый товар'
    assert product.category.name == 'Тестовая категория'
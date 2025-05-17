import pytest
from store_app.forms import ProductForm, ProductModelForm



@pytest.mark.django_db
def test_product_form_valid(category):
    form_data = {
        'name': 'Test form',
        'description': 'Test form',
        'category': category,
        'price': 3,
    }

    form = ProductForm(data=form_data)
    assert form.is_valid()

    cleaned_data = form.cleaned_data
    assert cleaned_data['name'] == form_data['name']


@pytest.mark.django_db
def test_product_model_form_name(category):
    form_data = {
        'name': 'Ts',
        'description': 'Test form',
        'category': category,
        'price': 3,
    }

    form = ProductModelForm(data=form_data)
    assert not form.is_valid()


@pytest.mark.django_db
def test_product_model_form_description(category):
    form_data = {
        'name': 'Test form',
        'description': 'казино',
        'category': category,
        'price': 3,
    }

    form = ProductModelForm(data=form_data)
    assert not form.is_valid()
import pytest
from django.urls import reverse
from bs4 import BeautifulSoup


@pytest.mark.django_db
def test_product_list_template_bs(client, category, product, product2):
    url = reverse('products')
    response = client.get(url)
    assert response.status_code == 200

    soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')

    titles = [h5.get_text() for h5 in soup.find_all('h5')]
    assert len(titles) == 2
    assert 'Тестовый товар' in titles
    assert 'Другой тестовый товар' in titles
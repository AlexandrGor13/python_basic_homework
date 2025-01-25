import sys
from io import StringIO

import pytest

from homework3.phonebook.exception import InputError
from homework3.phonebook.view import View


@pytest.fixture(params=[('Владимир', 'Сидоров', '89110363982', 'рабочий'),
                        ('Владимир', 'Петров', '89287364851', 'мобильный'),
                        ('Иван', 'Иванов', '89287364851', 'мобильный')])
def fixture_get_data(request):
    return request.param


@pytest.fixture(params=[('Владимир', 'Сидоров', ' ', 'рабочий'),
                        ('Владимир', 'Петров', '8(928)736-48-51', 'мобильный'),
                        ('Иван', 'Иванов', '89287364851v', 'мобильный')])
def fail_fixture_get_data(request):
    return request.param


def test_get_data(fixture_get_data):
    """Функция тестирования для view.get_data()"""
    name, surname, phone, comment = fixture_get_data
    input_data = '\n'.join([name, surname, phone, comment])
    sys.stdin = StringIO(input_data)
    view = View()
    result = view.get_data()
    assert result == {'name': name, 'surname': surname, 'phone': phone, 'comment': comment}


@pytest.mark.xfail()
def test_fail_get_data(fail_fixture_get_data):
    """Функция тестирования для view.get_data() с неправильными данными"""
    name, surname, phone, comment = fail_fixture_get_data
    input_data = '\n'.join([name, surname, phone, comment])
    sys.stdin = StringIO(input_data)
    view = View()
    result = view.get_data()
    assert result == {'name': name, 'surname': surname, 'phone': phone, 'comment': comment}


def test_get_id():
    """Функция тестирования для view.get_id()"""
    input_data = '1\n'
    sys.stdin = StringIO(input_data)
    view = View()
    result = view.get_id()
    assert result == '1'
    input_data = 'd\n'
    sys.stdin = StringIO(input_data)
    view = View()
    with pytest.raises(InputError):
        view.get_id()


def test_get_number_operation():
    """Функция тестирования для view.get_number_operation()"""
    input_data = '1\n'
    sys.stdin = StringIO(input_data)
    view = View()
    result = view.get_number_operation()
    assert result == 1
    input_data = 'd\n'
    sys.stdin = StringIO(input_data)
    view = View()
    with pytest.raises(InputError):
        view.get_number_operation()

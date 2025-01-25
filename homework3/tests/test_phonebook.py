import pytest

from homework3.phonebook.model import PhoneBook, Abonent


@pytest.fixture(params=[('Владимир', 'Сидоров', '89110363982', 'рабочий'),
                        ('Владимир', 'Петров', '89287364851', 'мобильный')])
def add_phonebook(request):
    """Фикстура для проверки метода Controller.add"""
    pb = PhoneBook()
    name, surname, phone, comment = 'Иван', 'Петров', '89042379836', 'рабочий'
    pb.add(Abonent(name, surname, phone, comment))
    name, surname, phone, comment = request.param
    return pb, {'name': name, 'surname': surname, 'phone': phone, 'comment': comment}


def test_add(add_phonebook):
    pb, param = add_phonebook
    pb.add(Abonent(**param))
    for i in pb.get_id:
        if {k[1:]: v for k, v in pb.get(i).__dict__.items()} == param:
            break
    else:
        assert False

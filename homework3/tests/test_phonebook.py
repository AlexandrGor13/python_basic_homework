import pytest

from homework3.phonebook.model import PhoneBook, Abonent


@pytest.fixture(params=[('Владимир', 'Сидоров', '89110363982', 'рабочий'),
                        ('Владимир', 'Петров', '89287364851', 'мобильный')])
def add_phonebook(request):
    """Фикстура для проверки метода add класса PhoneBook"""
    pb = PhoneBook()
    name, surname, phone, comment = 'Иван', 'Петров', '89042379836', 'рабочий'
    pb.add(Abonent(name, surname, phone, comment))
    name, surname, phone, comment = request.param
    return pb, {'name': name, 'surname': surname, 'phone': phone, 'comment': comment}


def test_add(add_phonebook):
    """Функция проверяет добавление абонента в телефонный справочник"""
    pb, param = add_phonebook
    ab_added = Abonent(**param)
    pb.add(ab_added)
    assert pb.get(str(max(map(int, pb.get_id)))) == ab_added


@pytest.fixture(params=[('1',), ('3',)])
def delete_phonebook(request):
    """Фикстура для проверки метода delete класса PhoneBook"""
    pb = PhoneBook()
    pb.add(Abonent('Иван', 'Петров', '89042379836', 'рабочий'))
    pb.add(Abonent('Владимир', 'Сидоров', '89110363982', 'рабочий'))
    pb.add(Abonent('Иван', 'Иванов', '89287364851', 'мобильный'))
    ab_id, = request.param
    return pb, ab_id


def test_delete(delete_phonebook):
    """Функция проверяет удаление абонента из телефонного справочника"""
    pb, ab_id = delete_phonebook
    pb.delete(ab_id)
    assert ab_id not in pb.get_id


@pytest.fixture(params=[('Владимир', 'Сидоров', '89110363982', 'рабочий'),
                        ('Владимир', '', '', 'мобильный')])
def update_phonebook(request):
    """Фикстура для проверки метода update телефонного справочника"""
    pb = PhoneBook()
    name, surname, phone, comment = 'Иван', 'Петров', '89042379836', 'рабочий'
    pb.add(Abonent(name, surname, phone, comment))
    name, surname, phone, comment = request.param
    return pb, {'abonent_id': '1', 'name': name, 'surname': surname, 'phone': phone, 'comment': comment}


def test_update(update_phonebook):
    pb, param = update_phonebook
    ab_id = param.pop('abonent_id')
    pb.update(ab_id, Abonent(**param))
    ab_updated = pb.get(ab_id)
    assert ab_updated == Abonent(**param)


@pytest.fixture(params=[('Влади',), ('87',), ('моб',)])
def find_phonebook(request):
    """Фикстура для проверки метода find телефонного справочника"""
    pb = PhoneBook()
    pb.add(Abonent('Иван', 'Петров', '89042387836', 'рабочий'))
    pb.add(Abonent('Владимир', 'Сидоров', '87110363982', 'рабочий'))
    pb.add(Abonent('Иван', 'Иванов', '89287364851', 'мобильный'))
    find_string, = request.param
    return pb, {'find_string': find_string}


def test_find(find_phonebook):
    pb, param = find_phonebook
    find_string = param.pop('find_string')
    pb_find = pb.find(find_string)
    assert_flag = True
    for ab in pb_find:
        if not (
                find_string in ab.name or
                find_string in ab.surname or
                find_string in ab.phone or
                find_string in ab.comment):
            assert_flag = False
            break
    for id_str in set(pb.get_id) - set(pb_find.get_id):
        ab = pb.get(id_str)
        if find_string in ab.name or \
                find_string in ab.surname or \
                find_string in ab.phone or \
                find_string in ab.comment:
            assert_flag = False
    assert assert_flag

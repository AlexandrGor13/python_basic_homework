import pytest

from controller import Controller
from model import PhoneBook, Abonent


@pytest.fixture(params=[('Владимир', 'Сидоров', '89110363982', 'рабочий'),
                        ('Владимир', 'Петров', '89287364851', 'мобильный')])
def add_phonebook(request):
    """Фикстура для проверки метода Controller.add_abonent"""
    pb = PhoneBook()
    name, surname, phone, comment = 'Иван', 'Петров', '89042379836', 'рабочий'
    pb.add(Abonent(name, surname, phone, comment))
    pb_new = PhoneBook()
    pb_new.add(Abonent(name, surname, phone, comment))
    name, surname, phone, comment = request.param
    pb_new.add(Abonent(name, surname, phone, comment))
    return pb, {'name': name, 'surname': surname, 'phone': phone, 'comment': comment}, pb_new


def test_add_abonent(add_phonebook):
    pb, param, pb_new = add_phonebook
    assert Controller.add_abonent(pb, **param) == pb_new


@pytest.fixture(params=[('Владимир', 'Сидоров', '89110363982', 'рабочий'),
                        ('Владимир', '', '', 'мобильный')])
def update_phonebook(request):
    """Фикстура для проверки метода Controller.update_phonebook"""
    pb = PhoneBook()
    name_old, surname_old, phone_old, comment_old = 'Иван', 'Петров', '89042379836', 'рабочий'
    pb.add(Abonent(name_old, surname_old, phone_old, comment_old))
    pb_new = PhoneBook()
    name, surname, phone, comment = request.param
    pb_new.add(Abonent(name.strip() if name else name_old,
                       surname.strip() if surname else surname_old,
                       phone.strip() if phone else phone_old,
                       comment.strip() if comment else comment_old))
    return pb, {'abonent_id': '1', 'name': name, 'surname': surname, 'phone': phone, 'comment': comment}, pb_new


def test_update_abonent(update_phonebook):
    pb, param, pb_new = update_phonebook
    assert Controller.update_abonent(pb, **param) == pb_new


@pytest.fixture(params=[('1',), ('2',)])
def del_phonebook(request):
    """Фикстура для проверки метода Controller.del_phonebook"""
    pb = PhoneBook()
    pb.add(Abonent('Иван', 'Петров', '89042379836', 'рабочий'))
    pb.add(Abonent('Владимир', 'Сидоров', '89110363982', 'рабочий'))
    pb_new = PhoneBook()
    pb_new.add(Abonent('Иван', 'Петров', '89042379836', 'рабочий'))
    pb_new.add(Abonent('Владимир', 'Сидоров', '89110363982', 'рабочий'))
    ab_id, = request.param
    pb_new.delete(ab_id)
    return pb, {'abonent_id': ab_id}, pb_new


def test_del_abonent(del_phonebook):
    pb, param, pb_new = del_phonebook
    assert Controller.del_abonent(pb, **param) == pb_new


@pytest.fixture(params=[('Влади',), ('87',)])
def find_phonebook(request):
    """Фикстура для проверки метода Controller.find_phonebook"""
    pb = PhoneBook()
    pb.add(Abonent('Иван', 'Петров', '89042387836', 'рабочий'))
    pb.add(Abonent('Владимир', 'Сидоров', '87110363982', 'рабочий'))
    find_string, = request.param
    pb_new = pb.find(find_string.lower())
    return pb, {'find_string': find_string}, pb_new


def test_find_abonent(find_phonebook):
    pb, param, pb_new = find_phonebook
    assert Controller.find_abonent(pb, **param) == pb_new


@pytest.fixture(params=[('True'), ('False',)])
def isempty_phonebook(request):
    """Фикстура для проверки метода Controller.isempty_phonebook"""
    pb = PhoneBook()
    flag = bool(request.param)
    if flag:
        pb.add(Abonent('Иван', 'Петров', '89042387836', 'рабочий'))
        pb.add(Abonent('Владимир', 'Сидоров', '87110363982', 'рабочий'))

    flag_new = len(pb.get_id) == 0
    return pb, {}, flag_new


def test_isempty_phonebook(isempty_phonebook):
    pb, param, flag_new = isempty_phonebook
    assert Controller.isempty_phonebook(pb) == flag_new


@pytest.fixture(params=[('1',), ('3',)])
def id_in_phonebook(request):
    """Фикстура для проверки метода Controller.id_in_phonebook"""
    pb = PhoneBook()
    pb.add(Abonent('Иван', 'Петров', '89042387836', 'рабочий'))
    pb.add(Abonent('Владимир', 'Сидоров', '87110363982', 'рабочий'))
    ab_id = request.param
    flag = ab_id in pb.get_id
    return pb, {'abonent_id': ab_id}, flag


def test_in_phonebook(id_in_phonebook):
    pb, param, flag = id_in_phonebook
    assert Controller.id_in_phonebook(pb, **param) == flag



if __name__ == '__main__':
    pytest.main(['-v'])
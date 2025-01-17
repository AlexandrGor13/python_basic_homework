"""
Программа создает телефонный справочник, данные которого находятся
в json-файле с адресом указанным в константе BOOK_FILE_NAME

Программа имеет меню

===============================================
========= Меню телефонного справочника =========
===============================================
Для выбора операции укажите её номер:
    1 - Вывести телефонный справочник на экран
    2 - Найти контакт
    3 - Добавить контакт
    4 - Редактировать контакт
    5 - Удалить контакт
    0 - Выход

"""

import json
import os

BOOK_FILE_NAME = 'phone_book.json'


def write_phone_book(file_name: str, phone_book: dict) -> None:
    """Запись в файл телефонного справочника.

    Ключевые аргументы:
    file_name -- строка с именем json-файла (путь к файлу)
    phone_book -- аргумент типа dict, который будет записан в json-файл (телефонный справочник)
    """
    with open(file_name, 'w') as write_file:
        json.dump(phone_book, write_file,
                  ensure_ascii=False, indent=4)


def read_phone_book(file_name: str) -> dict:
    """Чтение из файла телефонного справочника.

    Ключевые аргументы:
    file_name -- строка с именем json-файла (путь к файлу)
    """
    result = dict()
    if not os.path.isfile(file_name):
        write_phone_book(BOOK_FILE_NAME, result)
    try:
        with open(file_name, 'r') as read_file:
            result = json.load(read_file)
    except json.decoder.JSONDecodeError:
        print('Ошибка чтения файла. Неверный формат.')
    return result


def phone_book_file(func: callable) -> callable:
    """Декоратор для чтения данных из файла и автосохранения после изменения
    содержимого справочника. Если передаваемая функция func вызывается с именованным
    аргументом, то результат ее выполнения не сохраняется в файл.
    """

    def wrapper(*args, **kwargs):
        if kwargs:
            updated_book = func(*args, **kwargs)
        else:
            book = read_phone_book(BOOK_FILE_NAME)
            arg = (book,) + args
            updated_book = func(*arg)
        if updated_book:
            write_phone_book(BOOK_FILE_NAME, updated_book)
        return updated_book

    return wrapper


@phone_book_file
def print_phone_book(phone_book: dict) -> None:
    """Вывод всех контактов на экран.

    Ключевые аргументы:
    phone_book -- аргумент типа dict, содержащий телефонный справочник
    """
    head = ('\n' + '-' * 90 + '\n' +
            '№ (ID)'.ljust(10) +
            'Фамилия'.ljust(20) +
            'Имя'.ljust(20) +
            'Номер телефона'.ljust(24) +
            'Коментарий' +
            '\n' + '-' * 90)
    print(head)
    for abonent_id, abonent_info in phone_book.items():
        print(f"{abonent_id}".ljust(10) + \
              f"{abonent_info['surname']}".ljust(20) + \
              f"{abonent_info['name']}".ljust(20) + \
              f"{abonent_info['phone']}".ljust(24) + \
              f"{abonent_info['comment']}")


@phone_book_file
def add_abonent(phone_book: dict) -> dict:
    """Добавление контакта в справочник.

    Ключевые аргументы:
    phone_book -- аргумент типа dict, содержащий телефонный справочник
    """
    print('Введите нужное значение и нажмите Enter.')
    name = input('Name:')
    surname = input('Surname:')
    phone = input('Phone:')
    while not phone.isdigit():
        print('Номер телефона должен состоять из цифр!')
        phone = input('Phone:')
    comment = input('Comment:')
    abonent_id = '1'
    if len(phone_book):
        *_, last = phone_book.keys()
        abonent_id = str(int(last) + 1)

    abonent = {abonent_id: {
        'name': name.strip(),
        'surname': surname.strip(),
        'phone': phone.strip(),
        'comment': comment.strip()
    }
    }
    phone_book.update(abonent)
    print('Новый контакт добавлен.')
    return phone_book


@phone_book_file
def edit_abonent(phone_book: dict) -> dict:
    """Изменение контакта в справочнике.

    Ключевые аргументы:
    phone_book -- аргумент типа dict, содержащий телефонный справочник
    """
    abonent_id = ''
    while not abonent_id.isdigit() or \
            abonent_id.isdigit() and abonent_id not in phone_book.keys():
        abonent_id = input('Укажите ID контакта, который требуется изменить:')
    print('Если требуется изменить поле, введите нужное значение, иначе нажмите Enter.')

    name_old = phone_book[abonent_id]['name']
    name = input(f'Name: ({name_old}) ')
    name = name_old if not name else name

    surname_old = phone_book[abonent_id]['surname']
    surname = input(f'Surname: ({surname_old}) ')
    surname = surname_old if not surname else surname

    phone_old = phone_book[abonent_id]['phone']
    phone = input(f'Phone: ({phone_old}) ')
    while not phone.isdigit() and phone:
        print('Номер телефона должен состоять из цифр!')
        phone = input(f'Phone: ({phone_old}) ')
    phone = phone_old if not phone else phone

    comment_old = phone_book[abonent_id]['comment']
    comment = input(f'Comment: ({comment_old}) ')
    comment = comment_old if not comment else comment

    abonent = {abonent_id.strip(): {
        'name': name.strip(),
        'surname': surname.strip(),
        'phone': phone.strip(),
        'comment': comment.strip()
    }
    }
    phone_book.update(abonent)
    print('Контакт изменен.')
    return phone_book


@phone_book_file
def del_abonent(phone_book: dict) -> dict:
    """Удаление контакта из справочника.

    Ключевые аргументы:
    phone_book -- аргумент типа dict, содержащий телефонный справочник
    """
    abonent_id = ''
    while not abonent_id.isdigit() or \
            abonent_id.isdigit() and abonent_id not in phone_book.keys():
        abonent_id = input('Укажите ID контакта, который хотите удалить:')
    del phone_book[abonent_id]
    print('Контакт удален.')
    return phone_book


@phone_book_file
def find_abonent(phone_book: dict, find_string: str) -> None:
    """Поиск по всем полям справочника.

    Ключевые аргументы:
    phone_book -- аргумент типа dict, содержащий телефонный справочник
    find_string -- строка с шаблоном поиска
    """
    print(f"Поиск строки '{find_string}' в имеющихся полях телефонного справочника.")
    find_string = find_string.lower()
    book_find = {}
    for abonent_id, abonent_info in phone_book.items():
        if find_string in abonent_id or \
                find_string in abonent_info['surname'].lower() or \
                find_string in abonent_info['name'].lower() or \
                find_string in abonent_info['comment'].lower() or \
                find_string in abonent_info['phone'].lower():
            book_find.update({abonent_id: abonent_info})
    if book_find:
        print_phone_book(phone_book=book_find)
    else:
        print('Ничего не найдено.')


code_operation = True
menu_dict = {
    0: 'Выход',
    1: 'Вывести телефонный справочник на экран',
    2: 'Найти контакт',
    3: 'Добавить контакт',
    4: 'Редактировать контакт',
    5: 'Удалить контакт'
}
while code_operation:
    os.system('cls' if os.name == 'nt' else 'clear')
    operation = input(f'''
================================================
========= Меню телефонного справочника =========
================================================
Для выбора операции укажите её номер:
    1 - {menu_dict[1]}
    2 - {menu_dict[2]}
    3 - {menu_dict[3]}
    4 - {menu_dict[4]}
    5 - {menu_dict[5]}
    0 - {menu_dict[0]}

Ваш выбор: ''')
    if operation.isdigit():
        code_operation = int(operation)
        match code_operation:
            case 0:
                break
            case 1:
                print_phone_book()
            case 2:
                find_abonent(input('Введите шаблон для поиска: '))
            case 3:
                add_abonent()
            case 4:
                edit_abonent()
            case 5:
                edit_abonent()
        input('\nДля продолжения нажмите Enter\n')
    else:
        print('Вы указали неправильную операцию. Попробуйте снова.')

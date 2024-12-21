import os
import json

BOOK_FILE_NAME = 'phone_book.json'


def write_phone_book(file_name, phone_book):  # Запись в файл телефонного мправочника
    with open(file_name, 'w') as write_file:
        json.dump(phone_book, write_file, ensure_ascii=False,
                  indent=4)  # ensure_ascii=False и indent=4 для читабельности json-файла


def read_phone_book(file_name):  # Чтение из файла телефонного справочника
    result = dict()
    if not os.path.isfile(file_name):
        write_phone_book(BOOK_FILE_NAME, result)
    try:
        with open(file_name, 'r') as read_file:
            result = json.load(read_file)
    except json.decoder.JSONDecodeError:
        print('Ошибка чтения файла. Неверный формат.')
    return result


def phone_book_file(func):  # Декоратор для автосохранения после изменения содержимого справочника

    def wrapper(*arg, **kvarg):
        # Reading phone book from a file
        book = read_phone_book(BOOK_FILE_NAME)
        arg = (book,) + arg
        updated_book = func(*arg)
        # Writing phone book to a file
        if updated_book:
            write_phone_book(BOOK_FILE_NAME, updated_book)
        return updated_book

    return wrapper


@phone_book_file
def print_phone_book(phone_book):  # Вывод всех контактов на экран
    head = '\n' + '-' * 90 + '\n' + \
           '№ (ID)'.ljust(10)+'Фамилия'.ljust(20)+'Имя'.ljust(20) +'Номер телефона'.ljust(24)+'Коментарий\n' + \
           '-' * 90
    print(head)
    for abonent_id, abonent_info in phone_book.items():
        print(f"{abonent_id}".ljust(10) + \
              f"{abonent_info['surname']}".ljust(20) + \
              f"{abonent_info['name']}".ljust(20) + \
              f"{abonent_info['phone']}".ljust(24) + \
              f"{abonent_info['comment']}")


@phone_book_file
def add_abonent(phone_book):  # Добавление контакта в справочнике
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
def edit_abonent(phone_book):  # Изменение контакта в справочнике
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
def del_abonent(phone_book):  # Удаление контакта из справочника
    abonent_id = ''
    while not abonent_id.isdigit() or \
            abonent_id.isdigit() and abonent_id not in phone_book.keys():
        abonent_id = input('Укажите ID контакта, который хотите удалить:')
    del phone_book[abonent_id]
    print('Контакт удален.')
    return phone_book


@phone_book_file
def find_abonent(phone_book, find_string):  # Поиск по всем полям справочника
    print(f"Поиск строки '{find_string}' в имеющихся полях телефонного справочника.")
    head = '\n' + '-' * 90 + '\n' + \
           '№ (ID)'.ljust(10) + 'Фамилия'.ljust(20) + 'Имя'.ljust(20) + 'Номер телефона'.ljust(24) + 'Коментарий\n' + \
           '-' * 90
    find_string = find_string.lower()
    res_string = ''
    for abonent_id, abonent_info in phone_book.items():
        if find_string in abonent_id.lower() or \
                find_string in abonent_info['surname'].lower() or \
                find_string in abonent_info['name'].lower() or \
                find_string in abonent_info['comment'].lower() or \
                find_string in abonent_info['phone'].lower():
            res_string += f"{abonent_id}".ljust(10)  + \
                          f"{abonent_info['surname']}".ljust(20)  + \
                          f"{abonent_info['name']}".ljust(20)  + \
                          f"{abonent_info['phone']}".ljust(24)  + \
                          f"{abonent_info['comment']}\n"
    if res_string:
        print(head, res_string, sep='\n')
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
===============================================
========= Меню телефонного справчника =========
===============================================
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
        # if code_operation in menu_dict.keys():
        #     if code_operation == 1:
        #         print_phone_book()
        #     elif code_operation == 2:
        #         find_abonent(input('Введите шаблон для поиска: '))
        #     elif code_operation == 3:
        #         add_abonent()
        #     elif code_operation == 4:
        #         edit_abonent()
        #     elif code_operation == 5:
        #         del_abonent()
        #     elif not code_operation:
        #         break

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

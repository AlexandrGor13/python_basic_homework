"""Модуль view"""

from controller import Controller
from model import *


class View:

    @classmethod
    def setup_view(cls) -> None:
        """Настраивает меню справочника."""

        cls.menu_dict = {
            1: 'Вывести телефонный справочник на экран',
            2: 'Найти контакт',
            3: 'Добавить контакт',
            4: 'Редактировать контакт',
            5: 'Удалить контакт',
            0: 'Выход'
        }

    @classmethod
    def get_menu(cls) -> str:
        """Выводит строку меню"""

        cls.setup_view()
        menu = '''
===============================================
========= Меню телефонного справочника =========
===============================================
Для выбора операции укажите её номер:\n'''
        for k, v in cls.menu_dict.items():
            menu += f'\t{k} - {v}\n'
        menu += '\nВаш выбор: '
        return menu

    @classmethod
    def input_operation_number(cls) -> int:
        """Ввод номера операции с клавиатуры"""

        str_operation = input()
        if not str_operation.isdigit():
            raise InputError('Неправильный ввод')
        return int(str_operation)

    @classmethod
    def input_phone_number(cls) -> str:
        """Ввод номера телефона с клавиатуры"""

        str_phone = input('Телефон: ')
        if not str_phone.isdigit():
            raise InputError('Неправильный ввод')
        return str_phone

    @classmethod
    def start_menu(cls) -> None:
        """Запускает цикл выполнения программы."""

        operation = True
        while operation:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(cls.get_menu())
            try:
                operation = cls.input_operation_number()
                if operation in cls.menu_dict.keys():
                    if operation:
                        cls.get_command(operation - 1)()
                    else:
                        break
                    input('\nДля продолжения нажмите Enter\n')
                else:
                    print('Вы указали неправильную операцию. Попробуйте снова.')
            except InputError as ex:
                continue
            except (FileError, JSONError, Exception) as ex:
                print('\nПроизошла непредвиденная ошибка. ' + \
                      f'{ex.message if type(ex) == type(FileError) or type(ex) == type(JSONError) else ex}\n' + \
                      'Программа будет закрыта.')
                break

    @classmethod
    def print_abonents(cls) -> None:
        """Выводит на экран справочник."""

        if Controller.command('empty')[0]:
            print('Справочник пуст.')
        print(Controller.command('print')[1])

    @classmethod
    def find_abonents(cls) -> None:
        """Получает строку поиска и выводит результат поиска."""

        if Controller.command('empty')[0]:
            print('Справочник пуст.')
        else:
            find_string = input('Введите шаблон для поиска: ')
            print(f"Поиск строки '{find_string}' в имеющихся полях телефонного справочника.")
            print(Controller.command('find', find_string=find_string)[1])

    @classmethod
    def add_abonent(cls) -> None:
        """Получает данные для добавления контакта и добавляет его в справочник."""

        print('Введите нужное значение и нажмите Enter.')
        name = input('Имя: ')
        surname = input('Фамилия: ')
        phone = '_'
        while not phone.isdigit():
            try:
                phone = cls.input_phone_number()
            except InputError as ex:
                print('Номер телефона должен состоять из цифр!')
                continue
        comment = input('Комментарий: ')
        print(Controller.command('add', name=name, surname=surname, phone=phone, comment=comment)[1])

    @classmethod
    def edit_abonent(cls) -> None:
        """Получает данные для изменения контакта и его ID. Изменяет контакт."""

        if Controller.command('empty')[0]:
            print('Справочник пуст. Редактировать нечего.')
        else:
            abonent_id = input('Укажите ID контакта, который требуется изменить:')
            while not Controller.command('in', abonent_id=abonent_id)[0]:
                abonent_id = input(
                    'Такого ID в справочнике нет. Укажите существующий ID контакта, который требуется изменить:')
            print('Если требуется изменить поле, введите нужное значение, иначе нажмите Enter.')
            name = input(f'Имя: ')
            surname = input(f'Фамилия: ')
            phone = '_'
            while not phone.isdigit() and phone:
                try:
                    phone = cls.input_phone_number()
                except InputError as ex:
                    print('Номер телефона должен состоять из цифр!')
                    continue
            comment = input(f'Комментарий: ')
            print(Controller.command('update', abonent_id=abonent_id, name=name, surname=surname, phone=phone,
                                     comment=comment)[1])

    @classmethod
    def del_abonent(cls) -> None:
        """Получает ID удаляемого контакта. Удаляет контакт."""

        if Controller.command('empty')[0]:
            print('Справочник пуст. Удалять нечего.')
        else:
            abonent_id = input('Укажите ID контакта, который требуется удалить:')
            while not Controller.command('in', abonent_id=abonent_id)[0]:
                abonent_id = input(
                    'Такого ID в справочнике нет. Укажите существующий ID контакта, который требуется удалить:')
            print(Controller.command('del', abonent_id=abonent_id)[1])

    @classmethod
    def get_command(cls, number: int) -> callable:
        """Вызывает команду из списка меню по вводимому номеру команды."""

        func_list = [
            cls.print_abonents,
            cls.find_abonents,
            cls.add_abonent,
            cls.edit_abonent,
            cls.del_abonent, ]
        if number in range(len(func_list)):
            return func_list[number]
        else:
            return None

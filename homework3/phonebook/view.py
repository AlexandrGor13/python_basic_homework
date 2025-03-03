"""Модуль view (представление)"""

from phonebook.exception import *


class View:

    def __init__(self):
        self.menu_str = ''

    def show(self, str_book: str) -> None:
        """Выводит на экран текстовую информацию о телефонном справочнике

        Ключевые аргументы:
        str_book -- справочник в виде текстовой строки
        """
        print(str_book)

    def waiting(self) -> None:
        """Ожидает ввода пользователем"""
        input('\nДля продолжения нажмите Enter\n')

    def get_data(self) -> dict:
        """Запрашивает у пользователя данные о контакте"""
        print('Введите нужное значение и нажмите Enter.')
        name = input('Имя: ')
        surname = input('Фамилия: ')
        phone = input('Телефон: ')
        while not phone.isdigit() and phone:
            try:
                phone = input('Телефон: ')
            except InputError:
                print('Номер телефона должен состоять из цифр!')
                continue
        comment = input('Комментарий:')
        return {'name': name, 'surname': surname, 'phone': phone, 'comment': comment}

    def get_id(self) -> str:
        """Запрашивает у пользователя ID контакта"""
        abonent_id = input('Укажите ID контакта, который требуется изменить/удалить:')
        if not abonent_id.isdigit():
            raise InputError('Неправильное значение')
        return abonent_id

    def get_str(self) -> str:
        """Запрашивает у пользователя строку для поиска"""
        find_string = input('Введите шаблон для поиска: ')
        print(f"Поиск строки '{find_string}' в имеющихся полях телефонного справочника.")
        return find_string

    def show_menu(self, menu: dict) -> None:
        """Выводит меню на экран

        Ключевые аргументы:
        menu -- словарь со строками меню
        """
        print(f'''
===============================================
========= Меню телефонного справчника =========
===============================================
Для выбора операции укажите её номер:\n''')
        for k, v in menu.items():
            print(f'\t{k} - {v}')
        print('\nВаш выбор: ')

    def get_number_operation(self) -> int:
        """Запрашивает у пользователя номер операции из меню"""
        number_operation = input()
        print()
        if not number_operation.isdigit():
            raise InputError('Неправильное значение')
        return int(number_operation)

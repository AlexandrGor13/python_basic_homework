"""Модуль controller (контроллер)"""

from phonebook.exception import *
from phonebook.model import Abonent, PhoneBook
from phonebook.view import View


class Controller:

    def __init__(self):
        self.__phonebook = PhoneBook()
        self.__view = View()

    def start(self) -> None:
        """Запускает выполнение программы"""
        code_operation = True
        while code_operation:
            try:
                self.__view.show_menu(self.get_menu)
                code_operation = int(self.__view.get_number_operation())
                if code_operation > 0 and code_operation in self.get_menu.keys():
                    self.get_operation[code_operation - 1]()
                    self.__view.waiting()
            except InputError:
                print('Вы указали неправильную операцию. Попробуйте снова.')
                continue
            except (FileError, JSONError, Exception) as ex:
                self.__view.show('\nПроизошла непредвиденная ошибка. ' + \
                                 f'{ex.message if type(ex) == type(FileError) or type(ex) == type(JSONError) else ex}\n' + \
                                 'Программа будет закрыта.')
                break

    @property
    def get_menu(self) -> dict:
        """Выдает словарь со строками меню"""
        return {
            1: 'Вывести телефонный справочник на экран',
            2: 'Найти контакт',
            3: 'Добавить контакт',
            4: 'Редактировать контакт',
            5: 'Удалить контакт',
            0: 'Выход',
        }

    @property
    def phonebook(self) -> PhoneBook:
        """Выдает телефонный справочник"""
        return self.__phonebook

    @phonebook.setter
    def phonebook(self, value) -> None:
        """Получает значение телефонного справочника"""
        self.__phonebook = value

    @property
    def view(self) -> View:
        """Выдает экземпляр объекта представления"""
        return self.__view

    @view.setter
    def view(self, value) -> None:
        """Получает значение экземпляра объекта представления"""
        self.__view = value

    def show(self) -> None:
        """Вызывает вывод на экран телефонного справочника через представление"""
        self.__phonebook.read_phone_book()
        self.__view.show(str(self.__phonebook))

    def add(self) -> None:
        """Добавляет контакт в справочник через представление"""
        self.__phonebook.read_phone_book()
        dct = self.__view.get_data()
        ab = Abonent(**dct)
        self.__phonebook.add(ab)
        self.__phonebook.write_phone_book()

    def update(self) -> None:
        """Обновляет контакт в справочнике через представление"""
        self.__phonebook.read_phone_book()
        str_id = ''
        while str_id not in self.__phonebook.get_id:
            try:
                str_id = self.__view.get_id()
            except InputError:
                continue
        dct = self.__view.get_data()
        for k, v in dct.items():
            if v == '':
                dct[k] = dct[k] if dct[k] else self.__phonebook.get(str_id).__dict__[k]
        self.__phonebook.update(str_id, Abonent(**dct))
        self.__phonebook.write_phone_book()

    def delete(self) -> None:
        """Удаляет контакт из справочника через представление"""
        self.__phonebook.read_phone_book()
        str_id = ''
        while not str_id and str_id not in self.__phonebook.get_id:
            try:
                str_id = self.__view.get_id()
            except InputError:
                continue
        self.__phonebook.delete(str_id)
        self.__phonebook.write_phone_book()

    def find(self) -> None:
        """Ищет контакты в справочнике через представление"""
        self.__phonebook.read_phone_book()
        find_string = self.__view.get_str()
        findbook = self.__phonebook.find(find_string)
        self.__view.show(str(findbook))

    @property
    def get_operation(self) -> list:
        """Выдает список функций для выполнения операций"""
        return [self.show,
                self.find,
                self.add,
                self.update,
                self.delete]

"""Модуль model"""

import json
import os

from homework3.phonebook.exception import *


class FileReader:
    """Класс для чтения JSON-файла"""

    def __init__(self, filename: str):
        self._filename = filename

    def read(self) -> dict:
        """Функция для чтения JSON-файла"""
        try:
            with open(self._filename, 'r') as file:
                return json.load(file)
        except OSError as ex:
            raise FileError('Ошибка открытия файла.')
        except json.JSONDecodeError:
            raise JSONError('Ошибка чтения json-файла.')


class FileWriter:
    """Класс для записи в JSON-файл"""

    def __init__(self, filename: str):
        self._filename = filename

    def write(self, obj: dict) -> None:
        """Функция для записи в JSON-файл"""
        try:
            with open(self._filename, 'w') as file:
                json.dump(obj, file, ensure_ascii=False, indent=4)
        except OSError:
            raise FileError('Ошибка открытия файла.')


class Abonent:
    """Класс пользователя (абонента) из телефонного справочника"""

    def __init__(self, name: str, surname: str, phone: str = '', comment: str = ''):
        self._name = name
        self._surname = surname
        self._phone = phone
        self._comment = comment

    def __str__(self) -> str:
        return f'surname: {self.surname.ljust(12)}' + \
            f'name: {self.name.ljust(12)}' + \
            f'phone: {self.phone.ljust(16)}' + \
            f'comment: {self.comment}'

    def __eq__(self, other: 'Abonent') -> bool:
        self_dict = self.__dict__
        other_dict = other.__dict__
        for k in self_dict.keys():
            if self_dict[k] != other_dict[k]:
                return False
        return True

    @property
    def name(self) -> str:
        """Получение имени пользователя"""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Присвоение имени пользователя"""
        self._name = value

    @property
    def surname(self) -> str:
        """Получение фамилии пользователя"""
        return self._surname

    @surname.setter
    def surname(self, value: str) -> None:
        """Присвоение фамилии пользователя"""
        self._surname = value

    @property
    def phone(self) -> str:
        """Получение номера телефона пользователя"""
        return self._phone

    @phone.setter
    def phone(self, value: str) -> None:
        """Присвоение номера телефона пользователя"""
        self._phone = value

    @property
    def comment(self) -> str:
        """Получение комментария о пользователе"""
        return self._comment

    @comment.setter
    def comment(self, value: str) -> None:
        """Присвоение комментария о пользователе"""
        self._comment = value


class PhoneBook:
    """Класс телефонного справочника"""

    def __init__(self):
        self._abonents = {}
        self._file_name = 'phone_book.json'
        self.__last_id = 0
        self.__ab_value = 0

    def __str__(self) -> str:
        res_str = '\n' + '-' * 85 + '\n' + \
                  'Номер (ID)'.ljust(16) + \
                  'Фамилия'.ljust(16) + \
                  'Имя'.ljust(16) + \
                  'Номер телефона'.ljust(24) + \
                  'Коментарий' + \
                  '\n' + '-' * 85 + '\n'
        for ab_id, ab in self._abonents.items():
            res_str += (str(ab_id)).ljust(16) + \
                       ab['surname'].ljust(16) + \
                       ab['name'].ljust(16) + \
                       ab['phone'].ljust(24) + \
                       ab['comment'] + \
                       '\n'
        return res_str

    def __iter__(self):
        self.__ab_value = 0
        return self

    def __next__(self):
        if self.__ab_value < self.__last_id:
            self.__ab_value += 1
            while not str(self.__ab_value) in self.get_id:
                self.__ab_value += 1
            abonent = Abonent(**self._abonents[str(self.__ab_value)])
            return abonent
        raise StopIteration

    def __eq__(self, other: 'PhoneBook') -> bool:
        for self_ab in self._abonents.values():
            if self_ab not in other._abonents.values():
                return False
        return True

    def __contains__(self, item: 'Abonent') -> bool:
        for i in self.get_id:
            if self.get(i) == item:
                return True
        return False

    @property
    def file_name(self) -> str:
        """Получение имени файла справочника"""
        return self._file_name

    @file_name.setter
    def file_name(self, value: str) -> None:
        """Присвоение нового имени файла для справочника"""
        self._file_name = value

    @property
    def get_id(self) -> tuple:
        """Получение кортежа всех ID в справочнике"""
        return tuple(self._abonents.keys())

    def get(self, abonent_id: str) -> Abonent:
        """Получение контакта по ID из справочника

        Ключевые аргументы:
        abonent_id -- ID пользователя
        """
        return Abonent(**self._abonents[abonent_id])

    def add(self, abonent: Abonent) -> None:
        """Добавление контакта в справочник

        Ключевые аргументы:
        abonent -- объект класса Abonent (пользователь)
        """
        self.__last_id += 1
        self._abonents[str(self.__last_id)] = {k[1:]: v for k, v in abonent.__dict__.items()}

    def delete(self, abonent_id: str) -> None:
        """Удаление контакта из справочника

        Ключевые аргументы:
        abonent_id -- ID пользователя
        """
        del self._abonents[abonent_id]
        self.__last_id = max(map(int, self.get_id))

    def update(self, abonent_id: str, abonent: Abonent) -> None:
        """Изменение контакта в справочнике

        Ключевые аргументы:
        abonent_id -- ID пользователя
        abonent -- объект класса Abonent (пользователь)
        """
        self._abonents[abonent_id] = {k[1:]: v for k, v in abonent.__dict__.items()}

    def find(self, find_string: str) -> 'PhoneBook':
        """Поиск по всем полям справочника

        Ключевые аргументы:
        find_string -- искомая строка
        """
        find_book = PhoneBook()
        for ab_id, ab in self._abonents.items():
            if find_string in ab_id.lower() or \
                    find_string.lower() in ab['surname'].lower() or \
                    find_string.lower() in ab['name'].lower() or \
                    find_string.lower() in ab['comment'].lower() or \
                    find_string.lower() in ab['phone'].lower():
                find_book._abonents[ab_id] = ab
        return find_book

    def write_phone_book(self) -> None:
        """Запись в файл телефонного справочника"""
        try:
            writer = FileWriter(self.file_name)
            writer.write(self._abonents)
        except Exception as ex:
            raise

    def read_phone_book(self) -> None:
        """Чтение из файла телефонного справочника"""
        try:
            if not os.path.isfile(self.file_name):
                self.write_phone_book()
            reader = FileReader(self.file_name)
            self._abonents = reader.read()
            if len(self._abonents):
                *_, last = self._abonents.keys()
                self.__last_id = int(last)
        except AttributeError as ex:
            raise JSONError('Ошибка распаковки json-файла.')
        except Exception as ex:
            raise

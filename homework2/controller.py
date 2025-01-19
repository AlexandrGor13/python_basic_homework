"""Модуль controller"""

from model import *


class Controller:

    @classmethod
    def command(cls, name_command: str, **kwargs) -> tuple[bool, str]:
        """Обрабатывает команды от модуля view

        Ключевые аргументы:
        name_command -- аргумент с названием команды
        kwargs -- дополнительные аргументы
        """
        result = (False, '')
        try:
            phone_book = PhoneBook()
            if 'phone_book' in kwargs.keys():
                phone_book = kwargs['phone_book']
            else:
                phone_book.read_phone_book()
            match name_command:
                case 'print':
                    result = True, cls.print_phonebook(phone_book)
                case 'find':
                    find_book = cls.find_abonent(phone_book, **kwargs)
                    result = True, cls.print_phonebook(find_book) if len(
                        find_book.get_id) else '\nНичего не найдено.'
                case 'add':
                    result = False, '\nКонтакт не был добавлен.'
                    phone_book = cls.add_abonent(phone_book, **kwargs)
                    phone_book.write_phone_book()
                    result = True, '\nНовый контакт добавлен.'
                case 'update':
                    result = False, '\nКонтакт не был изменен.'
                    phone_book = cls.update_abonent(phone_book, **kwargs)
                    phone_book.write_phone_book()
                    result = True, '\nКонтакт изменен.'
                case 'del':
                    result = False, '\nКонтакт не был удален.'
                    phone_book = cls.del_abonent(phone_book, **kwargs)
                    phone_book.write_phone_book()
                    result = True, '\nКонтакт удален.'
                case 'empty':
                    result = len(phone_book.get_id) == 0, ''
                case 'in':
                    result = kwargs['abonent_id'] in phone_book.get_id, ''
        except:
            raise
        finally:
            return result

    @classmethod
    def print_phonebook(cls, phone_book: PhoneBook) -> str:
        """Выводит список контактов из справочника

        Ключевые аргументы:
        phone_book -- аргумент типа PhoneBook, содержащий телефонный справочник
        """
        return str(phone_book)

    @classmethod
    def add_abonent(cls, phone_book: PhoneBook, **kwargs) -> PhoneBook:
        """Добавление контакта в справочник

        Ключевые аргументы:
        phone_book -- аргумент типа PhoneBook, содержащий телефонный справочник
        """
        ab = Abonent(kwargs['name'].strip(),
                     kwargs['surname'].strip(),
                     kwargs['phone'].strip(),
                     kwargs['comment'].strip())
        phone_book.add(ab)
        return phone_book

    @classmethod
    def update_abonent(cls, phone_book: PhoneBook, **kwargs) -> PhoneBook:
        """Изменение контакта в справочнике.

        Ключевые аргументы:
        phone_book -- аргумент типа PhoneBook, содержащий телефонный справочник
        """
        ab_old = phone_book.get(kwargs['abonent_id'])
        ab = Abonent(
            kwargs['name'].strip() if kwargs['name'] else ab_old.name,
            kwargs['surname'].strip() if kwargs['surname'] else ab_old.surname,
            kwargs['phone'].strip() if kwargs['phone'] else ab_old.phone,
            kwargs['comment'].strip() if kwargs['comment'] else ab_old.comment)
        phone_book.update(kwargs['abonent_id'], ab)
        return phone_book

    @classmethod
    def del_abonent(cls, phone_book: PhoneBook, **kwargs) -> PhoneBook:
        """Удаление контакта из справочника.

        Ключевые аргументы:
        phone_book -- аргумент типа PhoneBook, содержащий телефонный справочник
        """
        phone_book.delete(kwargs['abonent_id'])
        return phone_book

    @classmethod
    def find_abonent(cls, phone_book: PhoneBook, **kwargs) -> PhoneBook:
        """Поиск по всем полям справочника.

        Ключевые аргументы:
        phone_book -- аргумент типа PhoneBook, содержащий телефонный справочник
        find_string -- строка с шаблоном поиска
        """
        find_book = phone_book.find(kwargs['find_string'].lower())
        return find_book

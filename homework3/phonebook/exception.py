
class InputError(Exception):
    """Класс исключения для обработки ошибок связанных с неправильным вводом данных"""

    def __init__(self, message: str):
        super().__init__()
        self.message = message


class JSONError(Exception):
    """Класс исключения для обработки ошибок связанных с JSON-форматированием
    и чтением содержимого JSON-файла"""

    def __init__(self, message: str):
        super().__init__()
        self.message = message


class FileError(Exception):
    """Класс исключения для обработки ошибок связанных с доступом к файлу"""

    def __init__(self, message: str):
        super().__init__()
        self.message = message

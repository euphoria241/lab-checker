class Person:
#определяет студента по файлу (дописать функцию извлечения кода)
    def __init__(self, filename, dict_db):
        self.filename = filename
        self.dict_db = dict_db


    def key_from_file(self):
        """
        С названия файлы получает ключ и возвращает название задачи из базы данных
        """
        key = self.filename
        # print('файл:', self.filename, 'ключ:', end='')
        return self.dict_db.get(key[:-3],'Такого студента нет в базе')

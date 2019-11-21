from Connected import Connected
from Person import Person
import time
import glob
import os


def txt_to_dict(file_db):
    """
    Считывает текстовый файл, и записывает его данные в словарь
    """
    dict_db = dict()
    with open(file_db, encoding="utf8") as file:
        for line in file:
            key, value = line.split()
            dict_db[key] = value
    print(dict_db)
    return dict_db

connected = Connected()
connected.authorization()

dict_db = txt_to_dict("../main/db.txt")
#создание словаря из базы Студент-задача
os.chdir('../DB')
#Указание директории, где лежат файлы студентов

for filename in glob.glob( '*.py'):
#последовательное открытие нужных файлов в заданной директории
    Person1 = Person(filename, dict_db)
    decision_json = {"question_id": "",
                      "lang": "python3",
                      "typed_code": ""}
    typed_code = "class Solution:\n"
    with open(str("../DB/"+filename), encoding="utf8") as file:
        for line in file:
            typed_code += "\t" + line
    decision_json["typed_code"] = typed_code
    connected.solve(decision_json, Person1.key_from_file())
    time.sleep(5)

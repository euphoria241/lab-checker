import os.path
import configparser

class LogSave:
    def __init__(self):
        config = configparser.ConfigParser()
        print(os.path.dirname())
        print(config.read('../yuzu.ini'))
        self.path = config['PATH']['LogFile']
        if os.path.isfile(self.path):
            print('Есть файл такой епта')
            mode = 'a'

        else:
            print('Нет такого файла епта')
            mode = 'w'

        self.file_log = open(self.path, mode, encoding='utf-8')


    def write_log(self, string):
        self.file_log.write(string)

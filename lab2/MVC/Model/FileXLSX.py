import pyexcel


class FileXLSX:
    def __init__(self):
        return

    def saveFile(self, file, pars):
        pyexcel.save_as(array=pars, dest_file_name=file)

    def dataPars(self, data, names):
        keys = data[0].keys()
        i = 0
        pars = []
        pars.append(
            ["Студент", "Время", "Статус", "Время выполнения", "Быстрее, чем", "Память", "Меньше, чем", "Входные",
             "Выходные", "Ожидаемые", "Ошибка"])
        for element in data:
            p = [names[i]]
            for k in keys:
                p.append(element[k])
            pars.append(p)
            i += 1
        print(pars)
        return pars

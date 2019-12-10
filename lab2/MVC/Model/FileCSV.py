import csv

class FileCSV:
    def __init__(self):
        return

    def saveFile(self, file, pars):
        with open(file, "w", newline="") as f:
            writer = csv.writer(f, delimiter=';')
            for line in pars:
                writer.writerow(line)

    def dataPars(self, data, names):
        keys = data[0].keys()
        i = 0
        pars = []
        pars.append(["Студент", "Статус", "Время выполнения", "Память", "Input", "Output",
                                                "Expected", "Error"])
        for element in data:
            p = [names[i]]
            for k in keys:
                p.append(element[k])
            pars.append(p)
            i += 1
        print(pars)
        return pars

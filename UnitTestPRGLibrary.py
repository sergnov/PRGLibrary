"""
Программа для просмотра prg файлов
Автор: Новиков С. В.
Лицензия: еще не выбрал
Поддержка формата v2
ToDo распознавание форматов
ToDo поддержка формата v1
"""
from sys import exit
from csv import reader as csvreader
# from prgLibrary import prg

class prgv1(object):
    """Обработка файлов формата prg"""
    def __init__(self, path):
        self.program = None
        self.progdigit = None
        self.progscreen = None
        self.title = None
        self.path2prg = path
        self.format = None
    
    def _down(self,indelimeter):
        """скачивает данные формата 1"""
        try:
            reader = csvreader(open(self.path2prg, 'r'), delimiter=indelimeter, skipinitialspace=True)
            self.program = list()
            self.title = list()
            for row in reader:
                #команда
                if (len(row)>=5):
                    line=row[0]
                    if (line[0]!=";"):
                        self.program.append(row)
                #заголовок или комментарий
                if len(row)>0 and ";" in row[0]:
                    self.title.append(row)
        except OSError as err:
            print(err)
            self.program = None
            self.title = None
        
    def download(self):
        """
        убирает зависимость от формата
        """
        if self.format == None:
            self.format = self.testversion()
        if self.format == "v1":
            self._down(" ")
        elif self.format == "v2":
            self._down("\t")
        
    def testversion(self):
        """открыть файл на чтение и найти там строку ;FILE_FORMAT=1, ;FILE_FORMAT=2
        если ни одна строка не будет найдена, проверить следующие три предположения
        1. может быть файл пуст
        2. в файле нет программы
        3. файл содержит некорректный формат
        """
        try:
            file = open(self.path2prg, 'r')
            self.format = None
            for line in file:
                if ";FILE_FORMAT=1" in line:
                    self.format = "v1"
                elif ";FILE_FORMAT=2" in line:
                    self.format = "v2"
        except OSError as err:
            print(err)
        return self.format

    def extract(self):
        """Извлекает данные в список"""
        if self.program != None:
            self.progdigit = list()
            #создаем выборку в зависимости от формата
            if self.format == "v2":
                extdigit = lambda line: line[-3:]
                extother = lambda line: line[0:-3]
            elif self.format == "v1":
                extdigit = lambda line: line[2:5]
                extother = lambda line: line[0:2]+line[-1:]
            else:
                print("Not program in memory or bad file format")
                return
            
            for line in self.program:
                testdigit = extdigit(line)
                try:
                    digit = list()
                    digit = [float(x) for x in testdigit]
                    digit.append(extother(line))
                    self.progdigit.append(digit)
                except ValueError:
                    print("Line is corrupted")

def main():
    """Базовая точка для запуска скрипта при непосредственном запуске"""
    print("Test prgv1 class")
    
    def testtitle(title, path):
        try:
            _test = prgv1(path)
            _test.download()
            
            print("\n",title)
            print("The file's version is: ",_test.format)
            print("Title:")
            for line in _test.title:
                print(line)
        except Exception as err:
            print(err)
        print("---------------")
    
    #проверяем работу с файлом версии v1 имеющим заголовок
    testtitle("Проверяем работу с файлом версии v1 имеющим заголовок","ex-v1.prg")
    
    #проверяем работу с файлом версии v1 без заголовка
    testtitle("Проверяем работу с файлом версии v1 без заголовка", "ex-v1-notitle.prg")
    
    #проверяем работу с файлом версии v2 имеющим заголовок
    testtitle("Проверяем работу с файлом версии v2 имеющим заголовок", "ex-v2.prg")
    
    #Проверяем работу с файлом версии v1 без комментариев
    testtitle("Проверяем работу с файлом версии v1 без комментариев", "ex-v1-nocomment.prg")
    
    input()
    
if __name__ == "__main__":
    exit(main())
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap

import sqlite3
import sys
from test1re import Ui_Form
from test2 import Ui_MainWindow


class AnotherWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, chartist):
        super().__init__()
        self.chartist = chartist
        self.setupUi(self)
        self.setFixedSize(800, 600)
        self.setWindowTitle('Тест')
        self.setStyleSheet('QMessageBox { color: rgb(255, 255, 255); }')
        self.correctanswer = 0
        con = sqlite3.connect('dbase.db')
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM intro WHERE artist like '{}'""".format(self.chartist)).fetchall()
        result2 = cur.execute("""SELECT * FROM questions WHERE artist1 like '{}'""".format(self.chartist)).fetchall()
        self.list1 = result[0]
        self.list2 = result2[0]
        con.close()
        self.count = 1
        self.radioButton.setHidden(True)
        self.radioButton_2.setHidden(True)
        self.radioButton_5.setHidden(True)
        self.radioButton_6.setHidden(True)
        self.pixmap = QPixmap(self.list1[1])
        self.label_2.setPixmap(self.pixmap)
        self.label_3.setText(self.list1[2])
        self.pushButton.clicked.connect(self.next)

    def findcorrectanswer(self):
        self.all = [self.list2[(self.count - 10) * 5 - 3], self.list2[(self.count - 10) * 5 - 2],
                    self.list2[(self.count - 10) * 5 - 1], self.list2[(self.count - 10) * 5]]
        for ind, i in enumerate(self.all):
            if i[-1] == "*":
                self.answ = i[:-1]
                self.all[ind] = self.answ

    def okno(self):
        if self.radioButton.isChecked() and self.answ == self.all[0]:
            self.correctanswer += 1
        elif self.radioButton_2.isChecked() and self.answ == self.all[1]:
            self.correctanswer += 1
        elif self.radioButton_5.isChecked() and self.answ == self.all[2]:
            self.correctanswer += 1
        elif self.radioButton_6.isChecked() and self.answ == self.all[3]:
            self.correctanswer += 1
        temp = 'Ваш результат: {}/10'.format(self.correctanswer)
        QMessageBox.about(self, 'Итоги', temp)

    def next(self):
        if self.count < 10:
            self.count += 1
            self.pixmap = QPixmap(self.list1[self.count * 2 - 1])
            self.label_2.setPixmap(self.pixmap)
            self.label_3.setText(self.list1[self.count * 2])

        elif self.count < 20:
            try:
                if self.count != 10:
                    if self.radioButton.isChecked() and self.answ == self.all[0]:
                        self.correctanswer += 1
                    elif self.radioButton_2.isChecked() and self.answ == self.all[1]:
                        self.correctanswer += 1
                    elif self.radioButton_5.isChecked() and self.answ == self.all[2]:
                        self.correctanswer += 1
                    elif self.radioButton_6.isChecked() and self.answ == self.all[3]:
                        self.correctanswer += 1

                if self.count == 19:
                    self.pushButton.setText('Итоги')
                self.count += 1
                self.radioButton.setHidden(False)
                self.radioButton_2.setHidden(False)
                self.radioButton_5.setHidden(False)
                self.radioButton_6.setHidden(False)
                if self.radioButton.isChecked():
                    self.radioButton.setAutoExclusive(False)
                    self.radioButton.setChecked(False)
                    self.radioButton.setAutoExclusive(True)
                if self.radioButton_2.isChecked():
                    self.radioButton_2.setAutoExclusive(False)
                    self.radioButton_2.setChecked(False)
                    self.radioButton_2.setAutoExclusive(True)
                if self.radioButton_5.isChecked():
                    self.radioButton_5.setAutoExclusive(False)
                    self.radioButton_5.setChecked(False)
                    self.radioButton_5.setAutoExclusive(True)
                if self.radioButton_6.isChecked():
                    self.radioButton_6.setAutoExclusive(False)
                    self.radioButton_6.setChecked(False)
                    self.radioButton_6.setAutoExclusive(True)
                self.label_3.setText('Выберите правильный ответ')
                self.label.setText('Тест')
                self.pixmap = QPixmap(self.list2[(self.count - 10) * 5 - 4])
                self.label_2.setPixmap(self.pixmap)
                self.findcorrectanswer()
                self.radioButton.setText(self.all[0])
                self.radioButton_2.setText(self.all[1])
                self.radioButton_5.setText(self.all[2])
                self.radioButton_6.setText(self.all[3])
            except Exception as e:
                print(e)
        else:
            self.okno()


class MainWindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(800, 600)
        self.setWindowTitle('Тест')
        self.chartist = "Винсент Ван Гог"
        self.pushButton_2.clicked.connect(self.starttest)
        self.pushButton.clicked.connect(self.choose)

    def choose(self):

        artist, ok_presed = QInputDialog.getItem(self, 'Выберите художника',
                                                 'Художники:',
                                                 ('Винсент Ван Гог', 'Иван Константинович Айвазовский', 'Пабло Пикассо',
                                                  'Сальвадор Дали', 'Грант Вуд'),
                                                 1, False)
        if ok_presed:
            self.chartist = artist

    def starttest(self):
        self.w = AnotherWindow(self.chartist)
        self.w.show()


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec_()
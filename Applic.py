# Импорт библиотек
# GUI
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import os
import math
class Slice(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Расчёт на срез")
        self.setFixedSize(780,600)
        self.initUI()
        self.show()

    def initUI(self):
        self.tabWidget = QTabWidget(self)
        self.tabWidget.setGeometry(QRect(0, 0, 801, 601))
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabWidget.addTab(self.tab1, "Тип крепления")
        self.tabWidget.addTab(self.tab2, "Вывод")
        self.TypeMountC = QComboBox(self.tab1)
        self.TypeMountC.setGeometry(QRect(20, 10, 291, 31))
        self.TypeMountC.addItems(["Резьбовое метрическое","Резьбовое дюймовое","Заклепочное","Заклепочное, с полой заклепкой","Заклепочное, резьбовой заклепкой","Штифтовое продольное","Штифтовое поперечное","Призматической шпонкой","Сегментной шпонкой","Клиновой шпонкой","Шлицевое" ])
        self.MountingSize = QLabel('Типоразмер крепления',self.tab1)
        self.MountingSize.setGeometry(QRect(380, 10, 250, 31))
        self.MountingSizeC = QComboBox(self.tab1)
        self.MountingSizeC.setGeometry(QRect(550, 10, 200, 31))
        self.NumberMounts = QLabel('Количество креплений ',self.tab1)
        self.NumberMounts.setGeometry(QRect(20, 50, 200, 31))
        self.NumberMountsE = QLineEdit('1',self.tab1)
        self.NumberMountsE.setGeometry(QRect(210, 50, 100, 31))
        self.Material = QLabel('Материал крепления',self.tab1)
        self.Material.setGeometry(QRect(380, 50, 250, 31))
        self.MaterialC = QComboBox(self.tab1)
        self.MaterialC.setGeometry(QRect(550, 50, 200, 31))
        self.groupBox1 = QGroupBox("Для резьбового и заклепочного соединений ", self.tab1)
        self.groupBox1.setGeometry(QRect(0, 110, 770, 264))
        self.groupBox1.isFlat(1)
        # self.groupBox1.alignment('AlignCenter')




if __name__ == '__main__':
    # для списоков аргументов командной строки
    App = QApplication(sys.argv)
    # Конструктор
    window = Slice()
    # Реакция на крестик
    sys.exit(App.exec())

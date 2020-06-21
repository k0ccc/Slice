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
        self.setFixedSize(780,420)
        self.initUI()
        self.show()

    def initUI(self):
        self.tabWidget = QTabWidget(self)
        self.tabWidget.setGeometry(QRect(0, 0, 801, 601))
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabWidget.addTab(self.tab1, "Тип крепления")
        self.tabWidget.addTab(self.tab2, "Вывод")
        self.typeMountC = QComboBox(self.tab1)
        self.typeMountC.setGeometry(QRect(20, 10, 291, 25))
        self.typeMountC.addItems(["Резьбовое метрическое","Резьбовое дюймовое","Заклепочное","Заклепочное, с полой заклепкой","Заклепочное, резьбовой заклепкой","Штифтовое продольное","Штифтовое поперечное","Призматической шпонкой","Сегментной шпонкой","Клиновой шпонкой","Шлицевое" ])
        self.mountingSize = QLabel('Типоразмер крепления',self.tab1)
        self.mountingSize.setGeometry(QRect(390, 10, 250, 25))
        self.mountingSizeC = QComboBox(self.tab1)
        self.mountingSizeC.setGeometry(QRect(550, 10, 200, 25))
        self.numberMounts = QLabel('Количество креплений ',self.tab1)
        self.numberMounts.setGeometry(QRect(20, 50, 200, 25))
        self.numberMountsE = QLineEdit('1',self.tab1)
        self.numberMountsE.setGeometry(QRect(210, 50, 100, 25))
        self.material = QLabel('Материал крепления',self.tab1)
        self.material.setGeometry(QRect(390, 50, 250, 25))
        self.materialC = QComboBox(self.tab1)
        self.materialC.setGeometry(QRect(550, 50, 200, 25))
        self.groupBox1 = QGroupBox("Для резьбового и заклепочного соединений ", self.tab1)
        self.groupBox1.setGeometry(QRect(10, 110, 350, 264))
        self.diameter = QLabel('Диаметр отверстия',self.groupBox1)
        self.diameter.setGeometry(QRect(20, 25, 200, 25))
        self.diameterC = QComboBox(self.groupBox1)
        self.diameterC.setGeometry(QRect(175, 25, 140, 25))
        self.plate = QLabel('Пластины',self.groupBox1)
        self.plate.setGeometry(QRect(20, 60, 150, 25))
        self.plateT= QTableWidget(self.groupBox1)
        self.plateT.setColumnCount(2)
        self.plateT.setRowCount(1)
        self.plateT.setHorizontalHeaderLabels(['Толщина пластины, мм  ','Поперечная сила, Н '])
        self.plateT.setGeometry(QRect(20, 80, 295, 170))
        self.plateT.resizeColumnsToContents()
        self.groupBox2 = QGroupBox("Вал", self.tab1)
        self.groupBox2.setGeometry(QRect(390, 110, 360, 134))
        self.shaftDiameter = QLabel('Диаметр вала, мм',self.groupBox2)
        self.shaftDiameter.setGeometry(QRect(20, 25, 200, 25))
        self.shaftDiameterC = QLineEdit(self.groupBox2)
        self.shaftDiameterC.setGeometry(QRect(175, 25, 140, 25))
        self.torque = QLabel('Крутящий момент в H*мм',self.groupBox2)
        self.torque.setGeometry(QRect(20, 65, 200, 25))
        self.torqueC = QLineEdit(self.groupBox2)
        self.torqueC.setGeometry(QRect(175, 65, 140, 25))
        self.calculation = QPushButton('Расчитать',self.tab1)
        self.calculation.setGeometry(QRect (391, 278, 100, 35))
        self.outputInW = QPushButton('Вывести',self.tab1)
        self.outputInW.setGeometry(QRect (391, 338, 100, 35))
        self.exitApp = QPushButton('Выход',self.tab1)
        self.exitApp.setGeometry(QRect (650, 338, 100, 35))

        self.shaftDiameter.setEnabled(False)
        self.shaftDiameterC.setEnabled(False)
        self.torque.setEnabled(False)
        self.torqueC.setEnabled(False)

        self.exitApp.pressed.connect(self.exitA)
        self.plateT.activated.connect(self.plusRow)
        self.calculation.pressed.connect(self.raschet)
        self.typeMountC.currentTextChanged.connect(self.changeForm)

    @pyqtSlot()
    def plusRow(self):
        self.rowPosition = self.plateT.rowCount()
        self.plateT.insertRow(self.rowPosition)


    @pyqtSlot()
    def raschet(self):
        pass

    @pyqtSlot()
    def changeForm(self):
        if self.typeMountC.currentText() == "Резьбовое метрическое"or self.typeMountC.currentText() =="Резьбовое дюймовое"or self.typeMountC.currentText() =="Заклепочное"or self.typeMountC.currentText() =="Заклепочное, с полой заклепкой"or self.typeMountC.currentText() =="Заклепочное, резьбовой заклепкой":
            self.shaftDiameter.setEnabled(False)
            self.shaftDiameterC.setEnabled(False)
            self.torque.setEnabled(False)
            self.torqueC.setEnabled(False)
            self.diameter.setEnabled(True)
            self.diameterC.setEnabled(True)
            self.plate.setEnabled(True)
            self.plateT.setEnabled(True)
        else:
            self.shaftDiameter.setEnabled(True)
            self.shaftDiameterC.setEnabled(True)
            self.torque.setEnabled(True)
            self.torqueC.setEnabled(True)

            self.diameter.setEnabled(False)
            self.diameterC.setEnabled(False)
            self.plate.setEnabled(False)
            self.plateT.setEnabled(False)


    @pyqtSlot()
    def exitA(self):
        sys.exit()


if __name__ == '__main__':
    # для списоков аргументов командной строки
    App = QApplication(sys.argv)
    # Конструктор
    window = Slice()
    # Реакция на крестик
    sys.exit(App.exec())

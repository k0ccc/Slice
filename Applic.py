# Импорт библиотек
# GUI
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import math
import sqlite3
from itertools import groupby

class Slice(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Расчёт на срез")
        self.setFixedSize(780,420)

        self.con = sqlite3.connect('MaterialT.db')
        self.cursor = self.con.cursor()
        self.cursor.execute('select MaterialGOST from MaterialGOST')
        self.materialsGost = self.cursor.fetchall()
        self.cursor.execute('select DiametrRezbi from RezbaMetricheskayaGOST')
        self.diamRezbiMetr = self.cursor.fetchall()
        self.cursor.execute('select Shag from RezbaMetricheskayaGOST')
        self.shagRezbiMetr = self.cursor.fetchall()
        self.cursor.execute('select Naprejenie from MaterialGOST WHERE MaterialGOST ="Ст2 ГОСТ 380-94"')
        self.materialsZnach = self.cursor.fetchall()
        # print(self.rezbiMetr)
        self.initUI()
        self.show()

    def initUI(self):
        self.tabWidget = QTabWidget(self)
        self.tabWidget.setGeometry(QRect(0, 0, 801, 601))
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        # TAB 1
        self.tabWidget.addTab(self.tab1, "Тип крепления")
        self.tabWidget.addTab(self.tab2, "Вывод")
        self.typeMountC = QComboBox(self.tab1)
        self.typeMountC.setGeometry(QRect(20, 10, 291, 25))
        self.typeMountC.addItems(["Резьбовое метрическое","Резьбовое дюймовое","Заклепочное","Заклепочное, с полой заклепкой","Заклепочное, резьбовой заклепкой","Штифтовое продольное","Штифтовое поперечное","Призматической шпонкой","Сегментной шпонкой","Клиновой шпонкой","Шлицевое" ])
        self.mountingSize = QLabel('Диаметр резьбы',self.tab1)
        self.mountingSize.setGeometry(QRect(390, 10, 250, 25))
        self.mountingSizeC = QComboBox(self.tab1)
        self.sortDiamRezbiMetr = [el for el, _ in groupby(self.diamRezbiMetr)]
        for self.diamMetr  in self.sortDiamRezbiMetr:
            self.mountingSizeC.addItems(self.diamMetr)
        self.mountingSizeC.setGeometry(QRect(500, 10, 100, 25))
        self.shagRezbi = QLabel('Шаг',self.tab1)
        self.shagRezbi.setGeometry(QRect(660, 10, 100, 25))
        self.shagRezbiC = QComboBox(self.tab1)
        self.shagRezbiC.addItem("0,075")
        self.shagRezbiC.setGeometry(QRect(690, 10, 60, 25))
        self.numberMounts = QLabel('Количество креплений ',self.tab1)
        self.numberMounts.setGeometry(QRect(20, 50, 200, 25))
        self.numberMountsE = QLineEdit('1',self.tab1)
        self.numberMountsE.setGeometry(QRect(210, 50, 100, 25))
        self.material = QLabel('Материал крепления',self.tab1)
        self.material.setGeometry(QRect(390, 50, 250, 25))
        self.materialC = QComboBox(self.tab1)
        for self.materialGost in self.materialsGost:
            self.materialC.addItems(self.materialGost)
        self.materialC.setGeometry(QRect(550, 50, 200, 25))
        # groupBox1
        self.groupBox1 = QGroupBox("Для резьбового и заклепочного соединений ", self.tab1)
        self.groupBox1.setGeometry(QRect(10, 110, 350, 264))
        self.diameter = QLabel('Диаметр отверстия',self.groupBox1)
        self.diameter.setGeometry(QRect(20, 25, 200, 25))
        self.diameterE = QLineEdit('23',self.groupBox1)
        self.diameterE.setGeometry(QRect(175, 25, 140, 25))
        self.plate = QLabel('Пластины',self.groupBox1)
        self.plate.setGeometry(QRect(20, 60, 150, 25))
        self.plateT= QTableWidget(self.groupBox1)
        self.plateT.setColumnCount(2)
        self.plateT.setRowCount(1)
        self.plateT.setHorizontalHeaderLabels(['Толщина пластины, мм  ','Поперечная сила, Н '])
        self.plateT.setGeometry(QRect(20, 80, 295, 170))
        self.plateT.resizeColumnsToContents()
        # groupBox2
        self.groupBox2 = QGroupBox("Вал", self.tab1)
        self.groupBox2.setGeometry(QRect(390, 110, 360, 134))
        self.shaftDiameter = QLabel('Диаметр вала, мм',self.groupBox2)
        self.shaftDiameter.setGeometry(QRect(20, 25, 200, 25))
        self.shaftDiameterC = QLineEdit('70',self.groupBox2)
        self.shaftDiameterC.setGeometry(QRect(175, 25, 140, 25))
        self.torque = QLabel('Крутящий момент в H*мм',self.groupBox2)
        self.torque.setGeometry(QRect(20, 65, 200, 25))
        self.torqueC = QLineEdit('166440',self.groupBox2)
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
        self.materialC.currentTextChanged.connect(self.materialChanged)
        self.mountingSizeC.currentTextChanged.connect(self.diametrChanged)
        self.typeMountC.currentTextChanged.connect(self.chengeDiam)

    # Добавление сторик для таблицы
    @pyqtSlot()
    def plusRow(self):
        self.rowPosition = self.plateT.rowCount()
        self.plateT.insertRow(self.rowPosition)
    # Изменинее "Диаметр резьбы" и "шаг"
    @pyqtSlot()
    def diametrChanged(self):
        if self.typeMountC.currentText() == 'Резьбовое метрическое' or self.typeMountC.currentText() == 'Штифтовое продольное' or self.typeMountC.currentText() =='Штифтовое поперечное' or self.typeMountC.currentText() =='Призматической шпонкой' or self.typeMountC.currentText() =='Сегментной шпонкой' or self.typeMountC.currentText() =='Клиновой шпонкой' or self.typeMountC.currentText() == 'Шлицевое':
            self.shagRezbiC.clear()
            self.cursor.execute('select Shag from RezbaMetricheskayaGOST WHERE DiametrRezbi = ?' ,(self.mountingSizeC.currentText(),))
            self.metrShagi = self.cursor.fetchall()
            for self.metrShag  in self.metrShagi:
                self.shagRezbiC.addItems(self.metrShag)
        elif self.typeMountC.currentText() == 'Резьбовое дюймовое':
            self.shagRezbiC.clear()
            self.cursor.execute('select Shag from RezbaDuimovayaBoltGOST WHERE DiametrRezbi = ?' ,(self.mountingSizeC.currentText(),))
            self.duimShagi = self.cursor.fetchall()
            for self.duimShag  in self.duimShagi:
                self.shagRezbiC.addItems(self.duimShag)
        else:
            self.shagRezbiC.clear()
            self.cursor.execute('select Shag from DuimovayaRezbaZaklepok WHERE DiametrRezbi = ?' ,(self.mountingSizeC.currentText(),))
            self.duimZaklShagi = self.cursor.fetchall()
            for self.duimZaklShag  in self.duimZaklShagi:
                self.shagRezbiC.addItems(self.duimZaklShag)
    # Подсос материала
    @pyqtSlot()
    def materialChanged(self):
        self.gostMaterialCombo = self.materialC.currentText()
        self.cursor.execute('select Naprejenie from MaterialGOST WHERE MaterialGOST = ?' ,(self.gostMaterialCombo,))
        self.materialsZnach = self.cursor.fetchall()
        print (self.materialsZnach)
    # Изменение формы заглушить вал и тд
    @pyqtSlot()
    def changeForm(self):
        if self.typeMountC.currentText() == "Резьбовое метрическое"or self.typeMountC.currentText() =="Резьбовое дюймовое"or self.typeMountC.currentText() =="Заклепочное"or self.typeMountC.currentText() =="Заклепочное, с полой заклепкой"or self.typeMountC.currentText() =="Заклепочное, резьбовой заклепкой":
            self.shaftDiameter.setEnabled(False)
            self.shaftDiameterC.setEnabled(False)
            self.torque.setEnabled(False)
            self.torqueC.setEnabled(False)
            self.diameter.setEnabled(True)
            self.diameterE.setEnabled(True)
            self.plate.setEnabled(True)
            self.plateT.setEnabled(True)
        else:
            self.shaftDiameter.setEnabled(True)
            self.shaftDiameterC.setEnabled(True)
            self.torque.setEnabled(True)
            self.torqueC.setEnabled(True)
            self.diameter.setEnabled(False)
            self.diameterE.setEnabled(False)
            self.plate.setEnabled(False)
            self.plateT.setEnabled(False)
    @pyqtSlot()
    def chengeDiam(self):
        if self.typeMountC.currentText() == 'Резьбовое метрическое' or self.typeMountC.currentText() == 'Штифтовое продольное' or self.typeMountC.currentText() =='Штифтовое поперечное' or self.typeMountC.currentText() =='Призматической шпонкой' or self.typeMountC.currentText() =='Сегментной шпонкой' or self.typeMountC.currentText() =='Клиновой шпонкой' or self.typeMountC.currentText() == 'Шлицевое':
            print(self.typeMountC.currentText())
            self.mountingSizeC.clear()
            self.cursor.execute('select DiametrRezbi from RezbaMetricheskayaGOST')
            self.changeMDiametri=self.cursor.fetchall()
            self.sortMChangeDiametri = [el for el, _ in groupby(self.changeMDiametri)]
            for self.sortMChangeDiametr in self.sortMChangeDiametri:
                self.mountingSizeC.addItems(self.sortMChangeDiametr)
        elif self.typeMountC.currentText() == 'Резьбовое дюймовое':
            self.mountingSizeC.clear()
            self.cursor.execute('select DiametrRezbi from RezbaDuimovayaBoltGOST')
            self.changeDDiametri=self.cursor.fetchall()
            self.sortDChangeDiametri = [el for el, _ in groupby(self.changeDDiametri)]
            for self.sortDChangeDiametr in self.sortDChangeDiametri:
                self.mountingSizeC.addItems(self.sortDChangeDiametr)
        else:
            self.mountingSizeC.clear()
            self.cursor.execute('select DiametrRezbi from DuimovayaRezbaZaklepok')
            self.duimZaklepki=self.cursor.fetchall()
            self.sortduimZaklepki = [el for el, _ in groupby(self.duimZaklepki)]
            for self.sortduimZaklepk in self.sortduimZaklepki:
                self.mountingSizeC.addItems(self.sortduimZaklepk)
    @pyqtSlot()
    def raschet(self):
        # kolRow = self.plateT.rowCount()
        # if kolRow == 1:
        #     i = self.plateT.item(0,0).text()
        #     secCol = self.plateT.item(0,1).text()

        p=self.materialsZnach
        # i =
        # pass
    # выход
    @pyqtSlot()
    def exitA(self):
        self.con.close()
        sys.exit()


if __name__ == '__main__':
    # для списоков аргументов командной строки
    App = QApplication(sys.argv)
    # Конструктор
    window = Slice()
    # Реакция на крестик
    sys.exit(App.exec())

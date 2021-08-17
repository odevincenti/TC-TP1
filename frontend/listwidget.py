from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

class ListWidget(QWidget):

    def __init__(self, nombre = None):
        QMainWindow.__init__(self)
        loadUi("ListWidget.ui", self)

        self.nombre_list.setText(nombre)
        #self.color.setStyleSheet("background-color:"+color)
        self.visibilidad_list.clicked.connect(self.goto_visibilidad)
        self.color_list.clicked.connect(self.goto_color)
        self.datos_list.clicked.connect(self.goto_datos)
        self.borrar_list.clicked.connect(self.goto_borrar)

    def goto_visibilidad (self):
        print("messi")

    def goto_color(self):
        print("messi")

    def goto_datos(self):
        print("messi")

    def goto_borrar(self):
        print("messi")



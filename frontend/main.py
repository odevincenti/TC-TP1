from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from backend import *
from mplwidget import MplWidget

import numpy as np
import random


class Input_Teorico_Window(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        loadUi("input_teorico.ui", self)

        self.mplwid = MplWidget()
        self.show()
        self.ok_teorico_pushButton.clicked.connect(self.display_ok)
        self.cancel_teorico_pushButton.clicked.connect(self.close)

    def display_ok(self):
        print("entraste a display_ok")
        nombre_input = self.nombre_graph_teorico.text()
        numerador_input = self.numerador_teorico.text()
        denominador_input = self.denominador_teorico.text()
        cs.add_curve(1, [numerador_input, denominador_input], nombre_input)
        self.show_graph()
        self.close()

    def show_graph(self):
        self.mplwid.canvas.axes.clear()
        print(len(cs.curves))
        if len(cs.curves) != 0:
            cs.plot_mod(self.mplwid.canvas.axes)
            self.mplwid.canvas.draw()


class Input_Simulacion_Window(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        loadUi("input_simulacion.ui", self)

        self.upload_simulacion_pushButton.clicked.connect(self.get_simulation_file)

    def displayInfo(self):
        self.show()

    def get_simulation_file(self):
        filename = QFileDialog.getOpenFileNames()
        print(filename)
        path = filename[0]
        print(path)
        with open(path, "r") as f:
            print(f.readline())


class Input_Medicion_Window(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        loadUi("input_medicion.ui", self)

        self.upload_medicion_pushButton.clicked.connect(self.get_medicion_file)

    def displayInfo(self):
        self.show()

    def get_medicion_file(self):
        filename = QFileDialog.getOpenFileNames()
        print(filename)
        path = filename[0]
        print(path)
        with open(path, "r") as f:
            print(f.readline())


class MatplotlibWidget(QtWidgets.QMainWindow):

    def __init__(self):

        QMainWindow.__init__(self)

        loadUi("menu.ui", self)

        self.setWindowTitle("ejemplo")

        self.Input_Simulacion = Input_Simulacion_Window()
        self.Input_Medicion = Input_Medicion_Window()

        self.teoricoButton.clicked.connect(self.goto_graphInfoTeorico)
        self.simulacionButton.clicked.connect(self.goto_graphInfoSimulacion)
        self.medicionButton.clicked.connect(self.goto_graphInfoMedicion)

        self.moduloButton.clicked.connect(self.goto_graphModulo_Axis)
        self.faseButton.clicked.connect(self.goto_graphFase_Axis)

        # self.mostrar_teorico_Button.clicked.connect(self.show_graph)
        # self.ocultar_teorico_Button.clicked.connect(self.hide_graph)

    def goto_graphInfoTeorico(self):
        self.Input_Teorico = Input_Teorico_Window()

    def goto_graphInfoSimulacion(self):
        self.Input_Simulacion.displayInfo()

    def goto_graphInfoMedicion(self):
        self.Input_Medicion.displayInfo()

    def goto_graphModulo_Axis(self):
        if len(self.ejextextEdit.text()) == 0:
            ax_x = "Eje X"
        if len(self.ejeytextEdit.text()) == 0:
            ax_y = "Eje Y"
        if len(self.ejextextEdit.text()) != 0:
            ax_x = self.ejextextEdit.text()
        if len(self.ejeytextEdit.text()) != 0:
            ax_y = self.ejeytextEdit.text()
        # mandar al graph
        self.MplWidget.canvas.draw()

    def goto_graphFase_Axis(self):
        if len(self.ejextextEdit.text()) == 0:
            ax_x = "Eje X"
        if len(self.ejeytextEdit.text()) == 0:
            ax_y = "Eje Y"
        if len(self.ejextextEdit.text()) != 0:
            ax_x = self.ejextextEdit.text()
        if len(self.ejeytextEdit.text()) != 0:
            ax_y = self.ejeytextEdit.text()
        # mandar al graph


"""
    def hide_graph(self):
        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.draw()"""

cs = Curvespace()
app = QApplication([])
window = MatplotlibWidget()
window.show()
app.exec_()
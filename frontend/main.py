from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from backend import *
from mplwidget import MplWidget
from mplwidget import MplWidget2

import numpy as np
import random


class Input_Teorico_Window(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        loadUi("input_teorico.ui", self)

        self.show()
        self.ok_teorico_pushButton.clicked.connect(self.display_ok)
        self.cancel_teorico_pushButton.clicked.connect(self.close)

    def display_ok(self):
        print("entraste a display_ok")
        nombre_input = self.nombre_graph_teorico.text()
        numerador_input = self.numerador_teorico.text()
        denominador_input = self.denominador_teorico.text()
        cs.add_curve(1, [numerador_input, denominador_input], nombre_input)
        self.close()



class Input_Simulacion_Window(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        loadUi("input_simulacion.ui", self)

        self.show()
        self.upload_simulacion_pushButton.clicked.connect(self.get_simulation_file)
        self.ok_simulacion_pushButton_2.clicked.connect(self.display_ok)

    def get_simulation_file(self):
        filename = QFileDialog.getOpenFileNames()
        self.path = filename[0][0]


    def display_ok(self):
        cs.add_curve(2, self.path)
        self.close()


class Input_Medicion_Window(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        loadUi("input_medicion.ui", self)

        self.show()
        self.upload_medicion_pushButton.clicked.connect(self.get_medicion_file)
        self.ok_medicion_pushButton_2.clicked.connect(self.display_ok)

    def get_medicion_file(self):
        filename = QFileDialog.getOpenFileNames()
        self.path = filename[0][0]

    def display_ok(self):
        cs.add_curve(3, self.path)
        self.close()


class MatplotlibWidget(QtWidgets.QMainWindow):

    def __init__(self):

        QMainWindow.__init__(self)

        loadUi("menu.ui", self)

        self.setWindowTitle("ejemplo")

        self.teoricoButton.clicked.connect(self.goto_graphInfoTeorico)
        self.simulacionButton.clicked.connect(self.goto_graphInfoSimulacion)
        self.medicionButton.clicked.connect(self.goto_graphInfoMedicion)
        self.borrarpushButton.clicked.connect(self.goto_borrar)

        self.moduloButton.clicked.connect(self.goto_graphModulo_Axis)
        self.faseButton.clicked.connect(self.goto_graphFase_Axis)

        self.mostrar_teorico_Button.clicked.connect(self.show_graph)
        self.ocultar_teorico_Button.clicked.connect(self.hide_graph)


    def goto_graphInfoTeorico(self):
        self.Input_Teorico = Input_Teorico_Window()
        self.Input_Teorico.ok_teorico_pushButton.clicked.connect(self.show_graph)
        self.Input_Teorico.cancel_teorico_pushButton.clicked.connect(self.close)

    def goto_graphInfoSimulacion(self):
        self.Input_Simulacion = Input_Simulacion_Window()
        self.Input_Simulacion.ok_simulacion_pushButton_2.clicked.connect(self.show_graph)

    def goto_graphInfoMedicion(self):
        self.Input_Medicion = Input_Medicion_Window()
        self.Input_Medicion.ok_medicion_pushButton_2.clicked.connect(self.show_graph)

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

    def show_graph(self):
        self.MplWidget.canvas.axes.clear()
        self.MplWidget2.canvas.axes.clear()
        print(len(cs.curves))
        if len(cs.curves) != 0:
            cs.plot_mod(self.MplWidget.canvas.axes)
            cs.plot_ph(self.MplWidget2.canvas.axes)
            self.MplWidget.canvas.draw()
            self.MplWidget2.canvas.draw()

    def hide_graph(self):
        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.draw()
        self.MplWidget2.canvas.axes.clear()
        self.MplWidget2.canvas.draw()

    def goto_borrar(self):
        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.draw()
        self.MplWidget2.canvas.axes.clear()
        self.MplWidget2.canvas.draw()

cs = Curvespace()
app = QApplication([])
window = MatplotlibWidget()
window.show()
app.exec_()
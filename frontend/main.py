from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi



import numpy as np
import random

class Input_Teorico_Window(QWidget):

    def __init__(self, parent = None):

        QWidget.__init__(self, parent)
        loadUi("input_teorico.ui", self)

        self.ok_teorico_pushButton.clicked.connect(self.close)
        self.cancel_teorico_pushButton.clicked.connect(self.close)

    def displayInfo(self):
        self.show()

class Input_Simulacion_Window(QWidget):

    def __init__(self, parent = None):

        QWidget.__init__(self, parent)
        loadUi("input_simulacion.ui", self)

        self.upload_simulacion_pushButton.clicked.connect(self.close)

    def displayInfo(self):
        self.show()


class Input_Medicion_Window(QWidget):

    def __init__(self, parent = None):

        QWidget.__init__(self, parent)
        loadUi("input_medicion.ui", self)

        self.upload_medicion_pushButton.clicked.connect(self.close)

    def displayInfo(self):
        self.show()


class MatplotlibWidget(QtWidgets.QMainWindow):

    def __init__(self):

        QMainWindow.__init__(self)

        loadUi("menu.ui",self)

        self.setWindowTitle("ejemplo")

        self.Input_Teorico = Input_Teorico_Window()
        self.Input_Simulacion = Input_Simulacion_Window()
        self.Input_Medicion = Input_Medicion_Window()

        self.teoricoButton.clicked.connect(self.goto_graphInfoTeorico)
        self.simulacionButton.clicked.connect(self.goto_graphInfoSimulacion)
        self.medicionButton.clicked.connect(self.goto_graphInfoMedicion)

        self.mostrar_teorico_Button.clicked.connect(self.show_graph)
        self.ocultar_teorico_Button.clicked.connect(self.hide_graph)

    def goto_graphInfoTeorico(self):
        self.Input_Teorico.displayInfo()

    def goto_graphInfoSimulacion(self):
        self.Input_Simulacion.displayInfo()

    def goto_graphInfoMedicion(self):
        self.Input_Medicion.displayInfo()

    def show_graph(self):
        fs = 500
        f = random.randint(1, 100)
        ts = 1/fs
        length_of_signal = 100
        t = np.linspace(0,1,length_of_signal)

        cosinus_signal = np.cos(2*np.pi*f*t)
        sinus_signal = np.sin(2*np.pi*f*t)

        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot(t, cosinus_signal)
        self.MplWidget.canvas.axes.plot(t, sinus_signal)
        self.MplWidget.canvas.axes.legend(('cosinus', 'sinus'),loc='upper right')
        self.MplWidget.canvas.axes.set_title('Cosinus - Sinus Signal')
        self.MplWidget.canvas.draw()

    def hide_graph(self):
        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.draw()




app = QApplication([])
window = MatplotlibWidget()
window.show()
app.exec_()
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from backend import *
from mplwidget import MplWidget

class MainScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainScreen, self).__init__()
        loadUi("menu.ui", self)
        self.setWindowTitle("Plot Tool")

        self.Input_Teorico = Input_Teorico_Window()
        self.Input_Simulacion = Input_Simulacion_Window()
        self.Input_Medicion = Input_Medicion_Window()

        self.teoricoButton.clicked.connect(self.goto_input_teorico)
        self.simulacionButton.clicked.connect(self.goto_input_simulacion)
        self.medicionButton.clicked.connect(self.goto_input_medicion)
        self.moduloButton.clicked.connect(self.goto_graphModulo_Axis)
        self.faseButton.clicked.connect(self.goto_graphFase_Axis)

    def goto_input_teorico(self):
        self.Input_Teorico.show()

    def goto_input_simulacion(self):
        self.Input_Simulacion.show()

    def goto_input_medicion(self):
        self.Input_Medicion.show()

    def goto_graphModulo_Axis(self):
        if len(self.ejex_lineEdit.text()) == 0:
            ax_x = "Eje X"
        else:
            ax_x = self.ejex_lineEdit.text()

        if len(self.ejey_lineEdit.text()) == 0:
            ax_y = "Eje Y"
        else:
            ax_y = self.ejey_lineEdit.text()

        # mandar al graph
        print(ax_y, ax_x)

    def goto_graphFase_Axis(self):
        if len(self.ejex_lineEdit.text()) == 0:
            ax_x = "Eje X"
        else:
            ax_x = self.ejex_lineEdit.text()

        if len(self.ejey_lineEdit.text()) == 0:
            ax_y = "Eje Y"
        else:
            ax_y = self.ejey_lineEdit.text()

        # mandar al graph
        print(ax_y, ax_x)

class Input_Teorico_Window(QWidget):
    def __init__(self):
        super(Input_Teorico_Window, self).__init__()
        loadUi("input_teorico.ui", self)
        self.setWindowTitle("Input Teórico")

        self.ploteo = MatplotlibWidget()

        self.ok_teorico_pushButton.clicked.connect(self.display_ok)
        self.cancel_teorico_pushButton.clicked.connect(self.close)

    def display_ok(self):
        nombre_input = self.nombre_graph_teorico.text()
        numerador_input = self.numerador_teorico.text()
        denominador_input = self.denominador_teorico.text()
        cs.add_curve(1, [numerador_input, denominador_input], nombre_input)
        self.ploteo.show_graph()
        self.close()

class Input_Simulacion_Window(QWidget):
    def __init__(self):
        super(Input_Simulacion_Window, self).__init__()
        loadUi("input_simulacion.ui", self)
        self.setWindowTitle("Input Simulación")
        self.upload_simulacion_pushButton.clicked.connect(self.get_simulation_file)

    def get_simulation_file(self):
        filename = QFileDialog.getOpenFileNames()
        print(filename)
        path = filename[0]
        print(path)
        with open(path,"r") as f:
            print(f.readline())

class Input_Medicion_Window(QWidget):
    def __init__(self):
        super(Input_Medicion_Window, self).__init__()
        loadUi("input_medicion.ui", self)
        self.setWindowTitle("Input Medición")
        self.upload_medicion_pushButton.clicked.connect(self.get_medicion_file)

    def get_medicion_file(self):
        filename = QFileDialog.getOpenFileNames()
        print(filename)
        path = filename[0]
        print(path)
        with open(path,"r") as f:
            print(f.readline())

class MatplotlibWidget(QWidget):
    def __init__(self):
        super(MatplotlibWidget, self).__init__()
        self.mplwidget = MplWidget()

    def show_graph(self):
        if len(cs.curves) != 0:
            cs.plot_mod(self.mplwidget.canvas.axes)
            self.mplwidget.canvas.draw()

    def hide_graph(self):
        self.mplwidget.canvas.axes.clear()
        self.mplwidget.canvas.draw()

#main
cs = Curvespace()
app = QApplication(sys.argv)
mainScreen = MainScreen()
mainScreen.show()
try:
    sys.exit(app.exec_())
except:
    print("saliendo")
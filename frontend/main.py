import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from backend import *

class Input_Teorico_Window(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        loadUi("input_teorico.ui", self)
        self.setWindowTitle("Input Teórico")

        self.show()
        self.ok_teorico_pushButton.clicked.connect(self.display_ok)
        self.cancel_teorico_pushButton.clicked.connect(self.close)


    def display_ok(self):
        self.nombre_input = self.nombre_graph_teorico.text()
        numerador_input = self.numerador_teorico.text()
        denominador_input = self.denominador_teorico.text()
        self.color_t = self.teorico_color_comboBox.currentText()
        unidad_frec = self.teorico_frec_comboBox.currentText()
        unidad_modulo = self.teorico_modulo_comboBox.currentText()
        unidad_fase = self.teorico_fase_comboBox.currentText()
        if unidad_fase == "grados":
            unidad_fase = "°"
        cs.add_curve(1, [numerador_input, denominador_input], self.nombre_input, self.color_t, unidad_frec, unidad_modulo, unidad_fase)
        self.close()


class Input_Simulacion_Window(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        loadUi("input_simulacion.ui", self)
        self.setWindowTitle("Input Simulación")

        self.show()
        self.upload_simulacion_pushButton.clicked.connect(self.get_simulation_file)
        self.ok_simulacion_pushButton_2.clicked.connect(self.display_ok)

    def get_simulation_file(self):
        filename = QFileDialog.getOpenFileNames()
        self.path = filename[0][0]


    def display_ok(self):
        self.nombre_input = self.nombre_graph_simulacion.text()
        #color = self.teorico_color_comboBox.currentText()
        unidad_frec = self.simulacion_frec_comboBox.currentText()
        unidad_modulo = self.simulacion_modulo_comboBox.currentText()
        unidad_fase = self.simulacion_fase_comboBox.currentText()
        if unidad_fase == "grados":
            unidad_fase = "°"
        cs.add_curve(2, self.path, self.nombre_input, "",unidad_frec, unidad_modulo, unidad_fase)
        self.close()


class Input_Medicion_Window(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        loadUi("input_medicion.ui", self)
        self.setWindowTitle("Input Medición")

        self.show()
        self.upload_medicion_pushButton.clicked.connect(self.get_medicion_file)
        self.ok_medicion_pushButton_2.clicked.connect(self.display_ok)

    def get_medicion_file(self):
        filename = QFileDialog.getOpenFileNames()
        self.path = filename[0][0]

    def display_ok(self):
        self.nombre_input = self.nombre_graph_medicion.text()
        #color = self.teorico_color_comboBox.currentText()
        unidad_frec = self.medicion_frec_comboBox.currentText()
        unidad_modulo = self.medicion_modulo_comboBox.currentText()
        unidad_fase = self.medicion_fase_comboBox.currentText()
        if unidad_fase == "grados":
            unidad_fase = "°"
        cs.add_curve(3, self.path, self.nombre_input, "", unidad_frec, unidad_modulo, unidad_fase)
        self.close()

class Input_Montecarlo_Window(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        loadUi("input_montecarlo.ui", self)
        self.setWindowTitle("Input Montecarlo")

        self.show()
        self.upload_montecarlo_pushButton.clicked.connect(self.get_montecarlo_file)
        self.ok_montecarlo_pushButton_2.clicked.connect(self.display_ok)

    def get_montecarlo_file(self):
        filename = QFileDialog.getOpenFileNames()
        self.path = filename[0][0]

    def display_ok(self):
        self.nombre_input = self.nombre_graph_montecarlo.text()
        #color = self.teorico_color_comboBox.currentText()
        unidad_frec = self.montecarlo_frec_comboBox.currentText()
        unidad_modulo = self.montecarlo_modulo_comboBox.currentText()
        unidad_fase = self.montecarlo_fase_comboBox.currentText()
        if unidad_fase == "grados":
            unidad_fase = "°"
        cs.add_curve(4, self.path, self.nombre_input, "", unidad_frec, unidad_modulo, unidad_fase)
        self.close()



class MatplotlibWidget(QtWidgets.QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        loadUi("menu.ui", self)
        self.setWindowTitle("Plot Tool")

        self.Curve_0.hide()

        self.teoricoButton.clicked.connect(self.goto_graphInfoTeorico)
        self.simulacionButton.clicked.connect(self.goto_graphInfoSimulacion)
        self.medicionButton.clicked.connect(self.goto_graphInfoMedicion)
        self.montecarloButton.clicked.connect(self.goto_graphInfoMontecarlo)
        self.borrarpushButton.clicked.connect(self.goto_borrar)
        self.aplicar_button_ejes1.clicked.connect(self.goto_graphModulo_Axis)
        self.aplicar_button_ejes2.clicked.connect(self.goto_graphFase_Axis)

    def goto_graphInfoTeorico(self):
        self.Input_Teorico = Input_Teorico_Window()
        self.Input_Teorico.ok_teorico_pushButton.clicked.connect(self.addCurveTeorico)
        self.Input_Teorico.cancel_teorico_pushButton.clicked.connect(self.close)


    def goto_graphInfoSimulacion(self):
        self.Input_Simulacion = Input_Simulacion_Window()
        self.Input_Simulacion.ok_simulacion_pushButton_2.clicked.connect(self.addCurveSimulacion)

    def goto_graphInfoMedicion(self):
        self.Input_Medicion = Input_Medicion_Window()
        self.Input_Medicion.ok_medicion_pushButton_2.clicked.connect(self.addCurveMedicion)

    def goto_graphInfoMontecarlo(self):
        self.Input_Montecarlo = Input_Montecarlo_Window()
        self.Input_Montecarlo.ok_montecarlo_pushButton_2.clicked.connect(self.addCurveMontecarlo)


    def addCurveTeorico(self):
        aux_curve = ListWidget()
        self.CurveList.layout().addWidget(aux_curve)
        self.aux_curve.visibilidad_list.clicked.connect(self.show_graph)
        self.show_graph()

    def addCurveSimulacion(self):
        aux_curve = ListWidget()
        self.CurveList.layout().addWidget(aux_curve)
        self.show_graph()

    def addCurveMedicion(self):
        aux_curve = ListWidget()
        self.CurveList.layout().addWidget(aux_curve)
        self.show_graph()

    def addCurveMontecarlo(self):
        aux_curve = ListWidget()
        self.CurveList.layout().addWidget(aux_curve)
        self.show_graph()


    def goto_graphModulo_Axis(self):
        if len(self.ejex_lineEdit.text()) == 0:
            ax_x = "Eje X"
        else:
            ax_x = self.ejex_lineEdit.text()
        if len(self.ejey_lineEdit.text()) == 0:
            ax_y = "Eje Y"
        else:
            ax_y = self.ejey_lineEdit.text()

        #self.ejex_lineEdit.setPlainText("")
        #self.ejey_lineEdit.setPlainText("")
        cs.change_x_mod_label(ax_x)
        cs.change_y_mod_label(ax_y)
        self.show_graph()

    def goto_graphFase_Axis(self):
        if len(self.ejex2_lineEdit.text()) == 0:
            ax_x = "Eje X"
        else:
            ax_x = self.ejex2_lineEdit.text()
        if len(self.ejey2_lineEdit.text()) == 0:
            ax_y = "Eje Y"
        else:
            ax_y = self.ejey2_lineEdit.text()

        #self.ejex2_lineEdit.setPlainText(" ")
        #self.ejey2_lineEdit.setPlainText(" ")
        cs.change_x_ph_label(ax_x)
        cs.change_y_ph_label(ax_y)
        self.show_graph()

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

class ListWidget(QWidget):

    def __init__(self):
        QMainWindow.__init__(self)
        loadUi("ListWidget.ui", self)

        self.nombre_list.setText(cs.curves[-1].name)
        #self.color.setStyleSheet("background-color:" + color)
        self.visibilidad_list.clicked.connect(self.goto_visibilidad)
        self.color_list.clicked.connect(self.goto_color)
        self.datos_list.clicked.connect(self.goto_datos)
        self.borrar_list.clicked.connect(self.goto_borrar)

    def goto_visibilidad (self):
        cs.curves[-1].change_visibility()

    def goto_color(self):
        print("messi")

    def goto_datos(self):
        print("messi")

    def goto_borrar(self):
        print("messi")


cs = Curvespace()
app = QApplication([])
window = MatplotlibWidget()
window.show()
try:
    sys.exit(app.exec_())
except:
    print("saliendo")
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'input_teorico.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(441, 300)
        self.ok_teorico_pushButton = QtWidgets.QPushButton(Form)
        self.ok_teorico_pushButton.setGeometry(QtCore.QRect(230, 260, 75, 23))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.ok_teorico_pushButton.setFont(font)
        self.ok_teorico_pushButton.setObjectName("ok_teorico_pushButton")
        self.cancel_teorico_pushButton = QtWidgets.QPushButton(Form)
        self.cancel_teorico_pushButton.setGeometry(QtCore.QRect(340, 260, 75, 23))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.cancel_teorico_pushButton.setFont(font)
        self.cancel_teorico_pushButton.setObjectName("cancel_teorico_pushButton")
        self.nombre_graph_teorico = QtWidgets.QPlainTextEdit(Form)
        self.nombre_graph_teorico.setGeometry(QtCore.QRect(150, 70, 151, 41))
        self.nombre_graph_teorico.setObjectName("nombre_graph_teorico")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(40, 80, 101, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(70, 140, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(60, 200, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.numerador_teorico = QtWidgets.QPlainTextEdit(Form)
        self.numerador_teorico.setGeometry(QtCore.QRect(150, 130, 151, 41))
        self.numerador_teorico.setObjectName("numerador_teorico")
        self.denominador_teorico = QtWidgets.QPlainTextEdit(Form)
        self.denominador_teorico.setGeometry(QtCore.QRect(150, 190, 151, 41))
        self.denominador_teorico.setObjectName("denominador_teorico")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(20, 10, 401, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.teorico_comboBox = QtWidgets.QComboBox(Form)
        self.teorico_comboBox.setGeometry(QtCore.QRect(148, 260, 51, 22))
        self.teorico_comboBox.setObjectName("teorico_comboBox")
        self.teorico_comboBox.addItem("")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.ok_teorico_pushButton.setText(_translate("Form", "OK"))
        self.cancel_teorico_pushButton.setText(_translate("Form", "CANCEL"))
        self.label.setText(_translate("Form", "Ingrese Nombre:"))
        self.label_2.setText(_translate("Form", "Numerador:"))
        self.label_3.setText(_translate("Form", "Denominador:"))
        self.label_4.setText(_translate("Form", "Ingrese los coeficientes separados por coma (\",\")"))
        self.teorico_comboBox.setItemText(0, _translate("Form", "H(s)"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

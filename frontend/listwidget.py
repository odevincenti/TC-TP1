from PyQt5.QtWidgets import *

class listWidget(QListWidget):

    def __init__(self, parent=None):
        QListWidget.__init__(self, parent)

        self.add_item()
        vbox = QVBoxLayout()
        self.list = QListWidget()
        self.list.insertItem(0, "curva 1")
        vbox.addWidget(self.list)
        self.setLayout(vbox)
        #vbox.addItem(QListWidgetItem("curva 1"))


#def add_curve(self):
        #for i in range(len(cs.curves)):
        #    self.addItem("curva"+str(i))
        #    self.addItem(QListWidgetItem("curva"+str(i)))
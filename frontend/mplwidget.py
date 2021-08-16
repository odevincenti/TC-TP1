from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import *

class MplWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.canvas = FigureCanvas(Figure())

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        vertical_layout.addWidget(NavigationToolbar(self.canvas, self))

        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)

class MplWidget2(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.canvas = FigureCanvas(Figure())

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        vertical_layout.addWidget(NavigationToolbar(self.canvas, self))

        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)

class latexWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        # Get window background color
        bg = self.palette().window().color()
        cl = (bg.redF(), bg.greenF(), bg.blueF())

        # Create figure, using window bg color
        self.fig = Figure(edgecolor=cl, facecolor=cl)

        # Add FigureCanvasQTAgg widget to form
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.tex_label_placeholder.layout().addWidget(self.canvas)

        # Clear figure
        self.fig.clear()

        # Set figure title
        self.fig.suptitle('$TeX$',
                          x=0.0, y=0.5,
                          horizontalalignment='left',
                          verticalalignment='center')
        self.canvas.draw()
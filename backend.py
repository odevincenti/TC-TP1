import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as ss

########################################################################################################################
# Clase Curve: Contiene toda la información para graficar la curva. Necesita:
#    - Tipo de curva: - 1 si es teórica (función transferencia)
#                     - 2 si es simulada (LTSpice)
#                     - 3 si es medida (Digilent)
#                     - 0 si es otra cosa (error)
#    - Datos: Dependerán del tipo de curva, en cada caso se especifica mejor (mirar funciones)
#    - Nombre: Si no se especifica, se le asignará uno según el orden
#    - Color: Se permitirá elegir el color de la curva, si no se especifica se tomará naranja todo ver como hace esto la gui
# Para cada tipo se accede una función particular, estas devuelven 0 si se creó bien o 1 si hubo un error
# ----------------------------------------------------------------------------------------------------------------------

class Curve:
    def __init__(self, c_type, data, name="", color='orange'):
        self.type = c_type          # Tipo de curva
        self.data = data
        self.color = color          # Color de la curva
        if name != "": self.name = name
        else: self.name = "curva1"
        self.update()

    def update(self):
        r = self.switch_ctypes.get(self.type, self.c_type_error)(self)
        return r

    def data_check(self, data):
        return 1

    def teorica(self):
        print("teórica")
        return 0

    def simulada(self):
        print("simulada")
        return 0

    def medida(self):
        print("medida")
        return 0

    def c_type_error(self):
        print("Si llegó hasta acá es porque se rompió algo")
        return 1

    # SWITCH
    switch_ctypes = {
        1: teorica,
        2: simulada,
        3: medida
    }
########################################################################################################################






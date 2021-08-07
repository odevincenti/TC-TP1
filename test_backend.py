import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as ss
from backend import Curve

# ARCHIVO PARA PROBAR LAS FUNCIONALIDADES DEL BACKEND ANTES DE AGREGAR EL FRONT

c1 = Curve(1, [1, 2, 3], color="blue")
print(c1.type)
print(c1.name)
print(c1.color)


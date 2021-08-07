import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as ss
from backend import Curvespace

# ARCHIVO PARA PROBAR LAS FUNCIONALIDADES DEL BACKEND ANTES DE AGREGAR EL FRONT

def plot_bode_mod(c, ax):
    w, mod, ph = ss.bode(c.H)#, np.linspace(F.w0*10**-2, F.w0*10**2, 10**4))       # Obtengo valores de frecuencia y módulo
    ax.semilogx(w, mod, c.color)  # Grafico bode del módulo de la transferencia
    plt.legend(c.name)
    ax.set_xlabel("$\omega$ $[log(s)]$")
    ax.set_ylabel("$|H(S)|$ $[dB]$")
    ax.grid()
    return

def plot_bode_ph(c, ax):
    w, mod, ph = ss.bode(c.H)#, np.linspace(F.w0*10**-2, F.w0*10**2, 10**4))       # Obtengo valores de frecuencia y fase
    ax.semilogx(w, ph, c.color)   # Grafico bode de la fase de la transferencia
    plt.legend(c.name)
    ax.set_xlabel("$\omega$ $[log(s)]$")
    ax.set_ylabel("$\phi(H(s))$ $[°]$")
    ax.grid()
    return

# TEST
C = Curvespace()
C.addCurve(1, [",1, 2, 3,", "10  , 20 , 30"], name="Prueba teórica", color="blue")
print(C.curves[0].name)
print(C.curves[0].H)
print(C.curves[0].color)

fig, ax = plt.subplots(2, 1)
fig.suptitle("Bode plot")
plot_bode_mod(C.curves[0], ax[0])        # Grafico módulo
plot_bode_ph(C.curves[0], ax[1])         # Grafico fase
fig.tight_layout()
plt.show()






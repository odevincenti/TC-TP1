import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as ss
from backend import Curvespace

# ARCHIVO PARA PROBAR LAS FUNCIONALIDADES DEL BACKEND ANTES DE AGREGAR EL FRONT

def plot_bode_mod(c, ax):
    #w, mod, ph = ss.bode(c.H)#, np.linspace(F.w0*10**-2, F.w0*10**2, 10**4))       # Obtengo valores de frecuencia y módulo
    ax.semilogx(c.w, c.mod, c.color)  # Grafico bode del módulo de la transferencia
    plt.legend(c.name)
    ax.set_xlabel("$\omega$ $\\left[" + c.w_unit + "\\right]$")
    ax.set_ylabel("$|H(S)|$ $\\left[" + c.mod_unit + "\\right]$")
    ax.grid()
    return

def plot_bode_ph(c, ax):
    w, mod, ph = ss.bode(c.H)#, np.linspace(F.w0*10**-2, F.w0*10**2, 10**4))       # Obtengo valores de frecuencia y fase
    ax.semilogx(w, ph, c.color)   # Grafico bode de la fase de la transferencia
    plt.legend(c.name)
    ax.set_xlabel("$\omega$ $\\left[" + c.w_unit + "\\right]$")
    ax.set_ylabel("$\phi(H(s))$ $\\left[" + c.ph_unit + "\\right]$")
    ax.grid()
    return

'''
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
'''

'''
def check_data():
    data = "Ejemplo1-simulacion.txt"
    file = open(data, "r")
    count = 0
    w_name, V_name = file.readline().split("\t")
    aux = file.readline().split("\t")
    aux_mod, aux_ph = aux[1][1:-2].split(",")

    mod_unit = get_unit(aux_mod)
    ph_unit = get_unit(aux_ph)
    for line in file:
        if line != "\n":
            count += 1
    file.close()

    w = np.zeros(count - 1)
    mod = np.zeros(count - 1)
    ph = np.zeros(count - 1)

    l = open(data, "r")

    l.readline()
    for i in range(count - 1):
        aux = l.readline().split("\t")
        w[i] = aux[0]
        aux_mod, aux_ph = aux[1][1:-2].split(",")
        mod[i] = aux_mod.replace(mod_unit, "")
        ph[i] = aux_ph.replace(ph_unit, "")

    l.close()

    return w, mod, ph
'''
def get_unit(s):
    unit = ""
    for i in range(len(s)-1, 0, -1):
        if not s[i].isdigit():
            unit = s[i] + unit
            # s = s[:i]
        else: break
    return unit
'''
w, mod, ph = check_data()
for i in range(len(w)):
    print(w[i], mod[i], ph[i])
'''
'''
# TEST
a = "dB"
fig, ax = plt.subplots(2, 1)
fig.suptitle("Bode plot")
ax[0].semilogx(w, mod)  # Grafico bode del módulo de la transferencia
ax[0].set_xlabel("$\omega$ $\\left[\\frac{rad}{s}\\right]$")
ax[0].set_ylabel("$|H(S)|$ $[" + a + "]$")
ax[0].grid()
ax[1].semilogx(w, ph)  # Grafico bode de la fase de la transferencia
ax[1].set_xlabel("$\omega$ $\\left[\\frac{rad}{s}\\right]$")
ax[1].set_ylabel("$\phi(H(s))$ $[°]$")
ax[1].grid()
fig.tight_layout()
plt.show()
'''


def check_data(path):
    file = open(path, "r")
    count = 0
    for line in file:
        if line != "\n":
            count += 1
    file.close()

    w = np.zeros(count - 1)
    mod = np.zeros(count - 1)
    ph = np.zeros(count - 1)

    l = open(path, "r")

    aux = l.readline()
    units = []
    for i in range(3):
        j1 = aux.find("(")
        j2 = aux.find(")")
        units.append(aux[j1 + 1: j2])
        aux = aux[j2 + 1:]

    for i in range(count - 1):
        aux = l.readline().split(",")
        w[i] = aux[0]
        mod[i] = aux[1]
        ph[i] = aux[2]
    l.close()

    return w, mod, ph





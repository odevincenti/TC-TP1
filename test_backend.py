import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as ss
from backend import Curvespace

# ARCHIVO PARA PROBAR LAS FUNCIONALIDADES DEL BACKEND ANTES DE AGREGAR EL FRONT

def plot_bode_mod(c, ax):
    ls = get_ls(c)
    if ls == '':
        print("Hubo un error, no se puede graficar la curva")
        return
    if c.type != 4:
        ax.semilogx(c.w, c.mod, c.color, linestyle=ls)   # Grafico el módulo de la transferencia
    else:
        for i in range(len(c.w)):
            ax.semilogx(c.w[i], c.mod[i], c.color, linestyle=ls)  # Grafico el módulo de la transferencia
    ax.legend([c.name + " (mod)"])
    ax.set_xlabel("$f$ $\\left[" + c.w_unit + "\\right]$")
    ax.set_ylabel("$|H(s)|$ $\\left[" + c.mod_unit + "\\right]$")
    ax.grid()
    return

def plot_bode_ph(c, ax):
    ls = get_ls(c)
    if ls == '':
        print("Hubo un error, no se puede graficar la curva")
        return
    if c.type != 4:
        ax.semilogx(c.w, c.ph, c.color, linestyle=ls)   # Grafico la fase de la transferencia
    else:
        for i in range(len(c.w)):
            ax.semilogx(c.w[i], c.ph[i], c.color, linestyle=ls)  # Grafico la fase de la transferencia
    ax.legend([c.name + " (ph)"])
    ax.set_xlabel("$f$ $\\left[" + c.w_unit + "\\right]$")
    ax.set_ylabel("$\phi(H(s))$ $\\left[" + c.ph_unit + "\\right]$")
    ax.grid()
    return

# get_ls: Obtiene el linestyle correcto para graficar según el timpo de curva
def get_ls(c):
    if c.type == 1 or c.type == 2 or c.type == 4:
        ls = 'solid'
    elif c.type == 3:
        ls = 'dotted'
    else:
        ls = ''
    return ls

# TEST
C = Curvespace()
C.addCurve(1, ["1, 2,3", "2,  +4,6 "], name="Prueba", color="blue")
print(C.curves[0].name)
print(C.curves[0].color)

fig, ax = plt.subplots(2, 1)
fig.suptitle("Transferencia")
plot_bode_mod(C.curves[0], ax[0])        # Grafico módulo
plot_bode_ph(C.curves[0], ax[1])         # Grafico fase
fig.tight_layout()
plt.show()

'''
def check_data():
    data = "Ejemplo1-simulacion.txt"
    file = open(data, "r")
    count = 2
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

'''
def check_mc_data(path):
    file = open(path, "r")
    file.readline()
    aux = file.readline()
    j1 = aux.find("/")
    j2 = aux.find(")")
    runs = int(aux[j1 + 1: j2])
    aux = file.readline().split("\t")
    aux_mod, aux_ph = aux[1][1:-2].split(",")

    count = 2
    mod_unit = get_unit(aux_mod)
    ph_unit = get_unit(aux_ph)
    for line in file:
        if line != 'Step Information: Run=2  (Run: 2/100)\n':
            count += 1
        else: break
    file.close()

    w = np.zeros((runs, count - 1))
    mod = np.zeros((runs, count - 1))
    ph = np.zeros((runs, count - 1))

    l = open(path, "r")

    l.readline()
    for k in range(runs):
        l.readline()
        for i in range(count - 1):
            aux = l.readline().split("\t")
            w[k][i] = aux[0]
            aux_mod, aux_ph = aux[1][1:-2].split(",")
            mod[k][i] = aux_mod.replace(mod_unit, "")
            ph[k][i] = aux_ph.replace(ph_unit, "")
    l.close()

    if ph_unit == 'Â°': ph_unit = '°'

    return w, mod, ph

import os
def check_file(path):
    r = True
    ext = os.path.splitext(path)[1]
    if ext != ".txt":
        print("El archivo de la simulación no está en formato .txt")
        r = False
        return r
    if not os.path.isfile(path):
        print("El archivo no existe")
        r = False
    else:
        if not os.access(path, os.R_OK):
            print("El archivo no es legible")
            r = False
        else:
            file = open(path, "r")
            if len(file.readline().split("\t")) != 2:
                print("El archivo no cumple con el formato adecuado")
                r = False
            elif file.readline() != 'Step Information: Run=1  (Run: 1/100)\n':
                print("El archivo no cumple con el formato adecuado")
                r = False
    return r

if check_file("montecarlo-simulacion.txt"):
    w, mod, ph = check_mc_data("montecarlo-simulacion.txt")
    for i in range(len(w[0])):
        print(w[16][i], mod[16][i], ph[16][i])
    print(len(w[0]))
'''

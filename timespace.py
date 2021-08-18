import numpy as np
import scipy.signal as ss
import os
import matplotlib.lines as mlines
from curvespace import Curvespace, Curve

########################################################################################################################
# Calse Timespace: Contiene la lista de curvas de tiempo y métodos para modificarla
# ----------------------------------------------------------------------------------------------------------------------
class Timespace(Curvespace):
    def __init__(self):
        super().__init__()

        self.t_unit = "s"       # Unidad del tiempo del gráfico
        self.y_unit = "V"       # Unidad de la curva de salida del gráfico
        self.x_unit = "V"       # Unidad de la curva de entrada del gráfico
        self.title = "Respuesta temporal"       # Título del gráfico de respuesta temporal
        self.t_label = "$t$"       # Label del eje x del gráfico de respuesta temporal. Es t por defecto
        self.y_label = "$y$"       # Label del eje y del gráfico de respuesta temporal. Es y por defecto
        self.x_label = "$x$"            # Label del eje y(2) del gráfico de respuesta temporal. Corresponde a la entrada y es x por defecto
        # todo agregar para que se pueda graficar la entrada con la salida

    # update: Método para actualizar los valores de la curva sin tener que borrarla y crearla de vuelta
    # OJO: En vez de recibir el tipo de curva, recibe el índice
    def update(self, index, data, name="", color="", t_unit="s", y_unit="V", x_unit="V"):
        self.change_curve_name(index, name)
        self.change_curve_color(index, color)
        self.curves[index].change_t_unit(t_unit)
        self.curves[index].change_y_unit(y_unit)
        self.curves[index].change_x_unit(x_unit)
        self.curves[index].change_data(data)
        return

    # addCurve: Método para agregar una curva. Para más detalles mirar clase Curva
    def add_curve(self, c_type, data, name="", color="", t_unit="s", y_unit="V", x_unit="V"):
        if name == "" or not self.check_name(name):
            for i in range(len(self.curves) + 1):
                name = "Curve " + str(len(self.curves) - i)
                if self.check_name(name):
                    print("Se tomará como nombre: " + name)
                    break
        # SWITCH DE COLORES
        switch_colors = ["blue", "orange", "green", "red", "cyan", "magenta", "gold", "violet"]
        if color == "":# and c_type != 4:
            color = switch_colors[len(self.curves) % 8]
            print("Para la curva", name, "se tomará el color: " + color)

        if c_type == 0:
            self.simulada(c_type, data, name, color, t_unit, y_unit, x_unit)
        elif 1 <= c_type <= 6:
            self.teorica(c_type, data, name, color, t_unit, y_unit, x_unit)

    # plot_time: grafica la curvas de respuesta temporal, si alguna da error deja de ser visible
    def plot_time(self, ax):
        # self.fix_units()
        h = []
        for i in range(len(self.curves)):
            if self.curves[i].visibility:
                if self.curves[i].plot_timecurve(ax):  # Grafico fase
                    h.append(mlines.Line2D([], [], color=self.curves[i].color, label=self.curves[i].name))
                else: self.curves[i].visibility = False
        ax.legend(handles=h)
        ax.legend(self.get_names(True))
        ax.set_title(self.title)
        ax.set_xlabel(self.t_label + " $\\left[" + self.curves[0].t_unit + "\\right]$")
        ax.set_ylabel(self.y_label + " $\\left[" + self.curves[0].y_unit + "\\right]$")
        ax.grid()
        return

    # change_t_label: Cambia el label del eje x del gráfico del tiempo
    def change_t_label(self, label):
        if label == "t":
            self.x_mod_label = "$t$"
        else:
            self.x_mod_label = label

    # change_x_mod_label: Cambia el label del eje y del gráfico temporal
    def change_y_label(self, label):
        if label == "V":
            self.y_label = "$V$"
        elif label == "Y":
            self.y_label = "$Y$"
        else:
            self.y_label = label

    # change_x_label: Cambia el label del segundo eje y del gráfico temporal
    def change_x_label(self, label):
        if label == "V":
            self.y_label = "$V$"
        elif label == "X":
            self.y_label = "$X$"
        else:
            self.y_label = label

    # change_title: Setter para el título del gráfico
    # Devuelve False en caso de error
    def change_title(self, title):
        r = False
        if isinstance(title, str):
            self.title = title
            r = True
        return r

    def simulada(self, r_type, data, name, color, t_unit="s", y_unit="V", x_unit="V"):
        # print("simulada")
        r = True
        s = tSim(0, data, name, color, t_unit="s", y_unit="V", x_unit="V")
        if s.t != [] and s.y != []:
            self.curves.append(s)
        else:
            print("Los datos ingresados no son válidos")
            r = False
        return r

    def teorica(self, r_type, data, name, color, t_unit="s", y_unit="V", x_unit="V"):
        # print("teorica")
        r = True
        s = tTeo(r_type, data, name, color, t_unit="s", y_unit="V", x_unit="V")
        if s.t != [] and s.y != [] and s.x != []:
            self.curves.append(s)
        else:
            print("Los datos ingresados no son válidos")
            r = False
        return r
########################################################################################################################

########################################################################################################################
# Clase Timecurve: Clase de curva de respuesta temporal. Contiene toda la información para graficar la curva. Necesita:
#    - Tipo de curva: - 0 si es simulada (LTSpice)
#                     - 1 si es respuesta a la senoidal (teórica)
#                     - 2 si es respuesta a la función escalón (teórica)
#                     - 3 si es respuesta al tren de pulsos (teórica)
#                     - 4 si es respuesta al impulso (teórica)
#                     - 5 si es respuesta a la rampa (teórica)
#                     - 6 si es respuesta a la exponencial (teórica)
#    - Raw Data: Dependerá del tipo de curva, será el path del archivo si es simulada o datos si es teórica (mirar casos)
#    - Nombre: Si no se especifica, se le asignará uno según el orden
#    - Color: Se permitirá elegir el color de la curva, si no se especifica se tomará naranja
#    - Visibilidad: True si la curva está visible, False si está oculta
#    - t: Intervalo de tiempo (Arreglo vacío si hubo error)
#    - y: Señal de salida (Arreglo vacío si hubo error)
#    - x: Señal de entrada (Arreglo vacío si hubo error)
#    - t_unit: Unidad del tiempo, por defecto es s
#    - y_unit: Unidad de la salida, por defecto es V
#    - x_unit: Unidad de la entrada, por defecto es V
# ----------------------------------------------------------------------------------------------------------------------
class Timecurve(Curve):
    def __init__(self, c_type, data, name="", color="", t_unit="s", y_unit="V", x_unit="V"):
        super().__init__(c_type, data, name, color)

        self.t = []
        self.y = []
        self.x = []
        self.t_unit = t_unit    # Unidad del tiempo, se asume s
        self.y_unit = y_unit    # Unidad de la señal de salida, se asume V
        self.x_unit = x_unit    # Unidad de la señal de entrada, se asume V

    # plot_timecurve: Grafica la curva en el tiempo
    #todo: Si se especifica graphx = True, grafica la entrada superpuesta con la salida
    def plot_timecurve(self, ax, graphx=False):
        '''ls = get_ls(self.type)
        if ls == '':
            print("Hubo un error, no se puede graficar la curva")
            return False'''
        ax.plot(self.t, self.y, self.color) #, linestyle=ls)  # Grafico el módulo de la transferencia
        return True

    # change_t_unit: Cambia la unidad de la frecuencia de s a min o viceversa
    # Si no se especifica la unidad a la que se quiere cambiar o es una que no existe, hace un switch
    def change_t_unit(self, unit=""):
        if self.t_unit != unit:
            if self.t_unit == "s":
                self.t_unit = "min"
                self.t = self.t/60.0
            else:
                self.t_unit = "s"
                self.t = 60.0 * self.t
        return

    # change_y_unit: Cambia la unidad de la señal de salida de V a ?? o viceversa
    def change_y_unit(self, unit=""):
        if self.y_unit != unit:
            self.y_unit = unit
        return

    # change_x_unit: Cambia la unidad de la señal de entrada de V a ?? o viceversa
    def change_x_unit(self, unit=""):
        if self.x_unit != unit:
            self.x_unit = unit
        return

    # check_data: Método para la verificación de datos (método virtual)
    def check_data(self, data):
        return

    # change_data: Setter para la modificación de datos (método virtual)
    def change_data(self, data):
        return
########################################################################################################################

########################################################################################################################
# Clase tSim: Representa una curva de tiempo simulada, hija de la clase Timecurve
# En data recibe el path al archivo con los datos
# ----------------------------------------------------------------------------------------------------------------------
class tSim(Timecurve):
    def __init__(self, c_type, data, name="", color="", t_unit="s", y_unit="V", x_unit="V"):
        super().__init__(c_type, data, name, color, t_unit, y_unit, x_unit)
        if self.check_file(data):
            self.t, self.y, self.x = self.check_data(data)

    # change_data: Revisa la validez de los datos nuevos.
    # Devuelve False si hubo error.
    def change_data(self, path):
        r = False
        if self.check_file(path):
            self.rawdata = path
            self.t, self.y, self.x = self.check_data(self.rawdata)
            r = True
        return r

    # check_data: Parsea el txt de la simulación de LTSpice
    # Acepta 2 formatos: t|y o t|y|x
    # todo: que acepte también t|x|y. Habría que pedirle al front que aclare
    # Devuelve t, y o t, y, x dependiendo del caso
    def check_data(self, path):
        file = open(path, "r")
        file.readline()
        aux = file.readline().split("\t")
        n = len(aux)
        count = 2

        for line in file:
            if line != "\n":
                count += 1
        file.close()

        t = np.zeros(count - 1)
        y = np.zeros(count - 1)
        x = np.zeros(count - 1)

        l = open(path, "r")

        l.readline()
        for i in range(count - 1):
            aux = l.readline().split("\t")
            t[i] = aux[0]
            y[i] = aux[1]
            if n == 3: x[i] = aux[2]
        l.close()

        return t, y, x

    # check_file: Revisa que el archivo exista, que sea .txt y que tenga el formato adecuado
    # Devuelve False en caso de error
    def check_file(self, path):
        r = True
        ext = os.path.splitext(path)[1]
        if self.type == 2 and ext != ".txt":
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
                if len(file.readline().split("\t")) != 2 and len(file.readline().split("\t")) != 3:
                    print("El archivo no cumple con el formato adecuado")
                    r = False
        return r

########################################################################################################################

########################################################################################################################
# Clase tTeo: Representa una curva de tiempo teórica, hija de la clase Timecurve
# En data recibe un arreglo con: - curve: La curva a partir de la cual fue creada
#                                - t: El intervalo de tiempo a graficar (si no se aclara asume de 0 a 10ms)
#                                - param: Valores de A, f, dc, t0 necesarios para los cálculos (ver cada caso)
# ----------------------------------------------------------------------------------------------------------------------
class tTeo(Timecurve):
    def __init__(self, c_type, data, name="", color="", t_unit="s", y_unit="V", x_unit="V"):
        super().__init__(c_type, data, name, color, t_unit, y_unit, x_unit)

        if self.check_data(data):
            curve = data[0]
            if data[1].any(): self.t = data[1]
            else:
                self.t = np.linspace(0.0, 10E-3, 1000)
                self.t_unit = "s"
            self.params = data[2]

            self.x = switch_rta_types.get(self.type)(self.t, self.params)
            self.t, self.y, self.x = ss.lsim(curve.H, self.x, self.t)
        else:
            print("Los datos ingresados no son válidos")

    # change_data: Revisa la validez de los datos nuevos.
    # Devuelve False si hubo error.
    def change_data(self, data):
        r = True
        if self.check_data(self.rawdata):        # Revisa los datos nuevos
            self.x = switch_rta_types.get(self.type)(self.t, self.params)
            self.t, self.y, self.x = ss.lsim(data[0].H, self.x, self.t)
        else:
            print("Los datos ingresados no son válidos")
            r = False
        return r

    # check_data: Revisa la validez los datos de la curva de tiempo teórica
    # Devuelve False si hubo error
    def check_data(self, data):
        r = True
        if len(data) != 3:
            print("El vector de datos para curvas de tiempo teóricas está incompleto")
        else:
            if not isinstance(data[0], Curve):
                print("Acá va una curva de frecuencia existente")
                r = False
            if data[1].any() and not isinstance(data[1], (list, np.ndarray)):
                print("Se ingresó el intervalo de tiempo en otro formato")
                r = False
        return r
########################################################################################################################

########################################################################################################################
# ----------------------------------------------------------------------------------------------------------------------
# sine: Devuelve una senoide en el intervalo dado con la frecuencia y amplitud determinada
# Parámetros: - t: intervalo de tiempo que se tomará en cuenta
#             - A: amplitud de la senoide
#             - f: frecuencia de la senoide
# ----------------------------------------------------------------------------------------------------------------------
def sine(t, params):
    if len(params) == 0:
        A, f = (1.0, 1.0)
    elif len(params) == 1:
        A, f = (params, 1.0)
    elif len(params) == 2:
        A, f = params
    else:
        print("ERROR: El seno sólo acepta 2 parámetros: amplitud y frecuencia. Se tomarán los primeros 2 valores respectivamente")
        A, f = params[0:2]
    x = A * np.sin(2 * np.pi * f * t)
    return x
# ----------------------------------------------------------------------------------------------------------------------
# heaviside: Devuelve la función escalón en el intervalo dado con la amplitud dada
# Parámetros: - t: intervalo de tiempo que se tomará en cuenta
#             - A: amplitud de la señal
def heaviside(t, params):
    if len(params) == 0:
        A = 1.0
    elif len(params) == 1:
        A = params
    else:
        print("ERROR: La función escalón sólo acepta 1 parámetro: amplitud. Se tomará el primer valor")
        A = params[0]
    x = A * (np.sign(t))
    return x
# ----------------------------------------------------------------------------------------------------------------------
# pulse_ train: Devuelve un tren de pulsos en el intervalo dado con la amplitud, frecuencia y DC dados
# Parámetros: - t: intervalo de tiempo que se tomará en cuenta
#             - A: amplitud de la señal
#             - f: frecuencia del tren
#             - Dc: duty cycle
def pulse_train(t, params):
    if len(params) == 0:
        A, f, dc = (1.0, 1.0, 0.5)
    elif len(params) == 1:
        A, f, dc = (params, 1.0, 0.5)
    elif len(params) == 2:
        A, f = params
        dc = 0.5
    elif len(params) == 3:
        A, f, dc = params
    else:
        print("ERROR: El tren de pulsos sólo acepta 3 parámetros: amplitud, frecuencia y Duty Cycle. Se tomarán los primeros 3 valores respectivamente")
        A, f, dc = params[0:3]
    x = A * ss.square(2 * np.pi * f * t, dc)
    return x
# ----------------------------------------------------------------------------------------------------------------------
# impulse: Devuelve un impulso en el intervalo dado en el instante t0 y con una la amplitud dada
def impulse(t, params):
    if len(params) == 0:
        t0, A = (0.0, 1.0)
    elif len(params) == 1:
        t0, A = (params, 1.0)
    elif len(params) == 2:
        t0, A = params
    else:
        print("ERROR: El impulso sólo acepta 2 parámetros: instante y amplitud. Se tomarán los primeros 2 valores respectivamente")
        t0, A = params[0:2]
    idx = t.index(t0)
    x = A * ss.unit_impulse(len(t), idx)
    return x
# ----------------------------------------------------------------------------------------------------------------------
# ramp: Devuelve una rampa en el intervalo dado en el instante t0 y con una pendiente m
def ramp(t, params):
    if len(params) == 0:
        t0, m = (0.0, 1.0)
    elif len(params) == 1:
        t0, m = (params, 1.0)
    elif len(params) == 2:
        t0, m = params
    else:
        print("ERROR: El impulso sólo acepta 2 parámetros: instante y pendiente. Se tomarán los primeros 2 valores respectivamente")
        t0, m = params[0:2]

    x = []
    for sample in t:
        if sample < t0:
            x.append(0)
        else:
            x.append(m * sample)
    return x
# ----------------------------------------------------------------------------------------------------------------------
# exp: Devuelve una señal exponencial en el intervalo dado y con la amplitud y el exponente dado
def exp(t, params):
    if len(params) == 0:
        A, a = (1.0, 1.0)
    elif len(params) == 1:
        A, a = (params, 1.0)
    elif len(params) == 2:
        A, a = params
    else:
        print("ERROR: La exponencial sólo acepta 2 parámetros: amplitud y exponente. Se tomarán los primeros 2 valores respectivamente")
        A, a = params[0:2]

    x =[]
    for sample in t:
        x.append(np.exp(a * sample))
    x = A * x
    return x
# ----------------------------------------------------------------------------------------------------------------------
# SWITCH
switch_rta_types = {
    1: sine,
    2: heaviside,
    3: pulse_train,
    4: impulse,
    6: ramp,
    7: exp
}
########################################################################################################################
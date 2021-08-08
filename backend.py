import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as ss
import os

########################################################################################################################
# Clase Curvespace: Contiene la lista de curvas y métodos para modificarla
# ----------------------------------------------------------------------------------------------------------------------
class Curvespace:
    def __init__(self):
        self.curves = []        # Arreglo de curvas

    # addCurve: Método para agregar una curva. Para más detalles mirar clase Curva
    def addCurve(self, c_type, data, name="", color='orange'):
        if name == "" or not self.checkName(name):
            for i in range(len(self.curves) + 1):
                name = "Curve " + str(len(self.curves) - i)
                if self.checkName(name): break

        if not self.switch_ctypes.get(c_type, self.c_type_error)(self, data, name, color):
            print("Error creando la curva")

    # delCurve: Saca la curva del Curvespace y la destruye
    # Recibe la curva (elemento) (Lo puedo cambiar al índice o nombre, lo que resulte más cómodo)
    def delCurve(self, c):
        self.curves.remove(c)
        del c
        return

    # checkName: Revisa si el nombre que se quiere asignar ya existe
    # Devuelve False si ya existe, True si está disponible
    def checkName(self, name):
        r = True
        for i in range(len(self.curves)):
            if name == self.curves[i]:
                r = False
                print("El nombre que quiere asignar ya existe")
                break
        return r

    # changeCurveName: Setter para el nombre de una curva. Recibe:
    #   - index: índice de la curva en el arreglo (lo puedo cambiar a nombre o a la curva en sí lo que les resulte más cómodo)
    #   - name: nombre nuevo para la curva
    # Devuelve False en caso de error (el nuevo nombre ya está asignado)
    def changeCurveName(self, index, name):
        r = self.checkName(name)
        if r: self.curves[index].name = name
        return r

    # changeCurveColor: Setter para el color de una curva. Recibe:
    #   - index: índice de la curva en el arreglo (lo puedo cambiar a nombre o a la curva en sí lo que les resulte más cómodo)
    #   - color: color nuevo para la curva
    # Devuelve False en caso de error
    def changeCurveColor(self, index, color):
        r = True
        self.curves[index].color = color
        return r

    def teorica(self, data, name, color):
        print("teórica")
        r = True
        t = Teo(1, data, name, color)
        if t.H is not None:
            self.curves.append(t)
        else:
            print("Los datos ingresados no son válidos")
            r = False
        return r

    def simulada(self, data, name, color):
        print("simulada")
        r = True
        s = Sim(2, data, name, color)
        if s.w != [] and s.mod != [] and s.ph != []:
            self.curves.append(s)
        else:
            print("Los datos ingresados no son válidos")
            r = False
        return r

    def medida(self, data, name, color):
        print("medida")
        r = True
        m = Med(3, data, name, color)
        if m.w != [] and m.mod != [] and m.ph != []:
            self.curves.append(m)
        else:
            print("Los datos ingresados no son válidos")
            r = False
        return r

    def c_type_error(self):
        print("Si llegó hasta acá es porque se rompió algo")
        return False

    # SWITCH
    switch_ctypes = {
        1: teorica,
        2: simulada,
        3: medida
    }

########################################################################################################################

########################################################################################################################
# Clase Curve: Contiene toda la información para graficar la curva. Necesita:
#    - Tipo de curva: - 1 si es teórica (función transferencia)
#                     - 2 si es simulada (LTSpice)
#                     - 3 si es medida (Digilent)
#                     - 0 si es otra cosa (error)
#    - Raw Data: Dependerán del tipo de curva, en cada caso se especifica mejor (mirar funciones)
#    - Nombre: Si no se especifica, se le asignará uno según el orden
#    - Color: Se permitirá elegir el color de la curva, si no se especifica se tomará naranja todo ver como hace esto la gui
#    - Visibilidad: True si la cura está visible, False si está oculta
#    - w: Intervalo de frecuencias (Arreglo vacío si hubo error)
#    - mod: Módulo de la transferencia (Arreglo vacío si hubo error)
#    - ph: Fase de la trasferencia (Arreglo vacío si hubo error)
#    - w_unit: Unidad de la frecuencia, por defecto es Hz (En LaTex)
#    - mod_unit: Unidad del módulo, por defecto es dB (En LaTex)
#    - ph_unit: Unidad de la fase, por defecto es ° (En LaTex)
# Para cada tipo se accede una clase particular, mirarlas para más detalles
# ----------------------------------------------------------------------------------------------------------------------
class Curve:
    def __init__(self, c_type, data, name, color):
        self.type = c_type          # Tipo de curva
        self.rawdata = data         # Datos como se cargan
        self.name = name            # Nombre de la curva
        self.color = color          # Color de la curva
        self.visibility = True      # Está visible? Por defecto se inicializa en True
        self.w = []
        self.mod = []
        self.ph = []
        self.w_unit = "Hz"          # Unidad de la frecuencia, se asume Hz
        self.mod_unit = "dB"        # Unidad del módulo, se asume dB
        self.ph_unit = "°"          # Unidad de la fase, se asume °

    # change_visibility: Setter para la visibilidad. Recibe un boolean
    def change_visibility(self, b):
        self.visibility = b
        return

    # change_w_unit: Cambia la unidad de la frecuencia de Hz a rad/s o viceversa
    # OJO: Cada vez que la llaman hace el cambio, SI NO HAY QUE CAMBIAR NO LA LLAMEN
    def change_w_unit(self):
        if self.w_unit != "Hz":
            self.w_unit = "\\frac{rad}{s}"
            self.w = 2*np.pi*self.w
        else:
            self.w_unit = "Hz"
            self.w = self.w/(2*np.pi)
        return

    # change_ph_unit: Cambia la unidad de la fase de ° a rad o viceversa
    # OJO: Cada vez que la llaman hace el cambio, SI NO HAY QUE CAMBIAR NO LA LLAMEN
    def change_ph_unit(self):
        if self.ph_unit != "°":
            self.ph_unit = "rad"
            self.ph = np.pi*self.w/180
        else:
            self.ph_unit = "°"
            self.ph = 180*self.ph/np.pi
        return

    # check_data: Método para la verificación de datos (método virtual)
    def check_data(self, data):
        return

    # change_data: Setter para la modificación de datos (método virtual)
    def change_data(self, data):
        return
########################################################################################################################

########################################################################################################################
# Clase Teo: Curva teórica, hija de la clase Curve
# Tiene algunos parámetros extra:
#       - H: Función Transferencia (scipy)
# ----------------------------------------------------------------------------------------------------------------------
class Teo(Curve):
    def __init__(self, c_type, data, name, color):
        super().__init__(1, data, name, color)
        num, den = self.check_data(self.rawdata)
        self.H = None
        if num is not None and den is not None:         # Si están en orden, hace la modificación
            self.H = ss.TransferFunction(num, den)
            self.w, self.mod, self.ph = ss.bode(self.H)

    # change_data: Revisa la validez de los datos nuevos. Devuelve False si hubo error.
    def change_data(self, data):
        r = True
        num, den = self.check_data(self.rawdata)        # Revisa los datos nuevos
        if num is not None and den is not None:         # Si están en orden, hace la modificación
            self.H = ss.TransferFunction(num, den)
            self.w, self.mod, self.ph = ss.bode(self.H)
        else:
            print("Los datos ingresados no son válidos")
            r = False
        return r

    # check_data: Procesa los datos de la función transferencia, asume que se recibe un arreglo con el numerador y denominador como strings
    # Ej data = ["1, 2,1, ,5", "3, 4, 1,3"]
    # Los espacios de más se eliminan y los números racionales se ingresan con punto (1.5)
    # Devuelve num = None y den = None si hubo error
    def check_data(self, data):
        num = fix_coefs(data[0])
        den = fix_coefs(data[1])
        '''
        num = data[0]
        den = data[1]
        num = num.replace(" ", "")      # Elimina espacios
        den = den.replace(" ", "")
        if num == "" or den == "":
            r = False
            print("Por favor ingrese los coeficientes")
        num = num.replace(",,", ",0,")      # Pone ceros donde falta el coeficiente
        den = den.replace(",,", ",0,")
        if num[-1] == ",": num = num + "0"  # Considera coeficientes cero al final
        if den[-1] == ",": den = den + "0"
        num = num.split(",")
        den = den.split(",")
        try:
            num = [float(s) for s in num]
            den = [float(s) for s in den]
        except ValueError:
            print("Uno de los valores ingresados no es numérico")
            r = False
        if not r:
            num = None
            den = None
        '''
        return num, den
########################################################################################################################

########################################################################################################################
# Clase Sim: Curva simulada, hija de la clase Curve
# Tiene unos parámetros extra: - Mentira por ahora no tiene
# w, mod y ph serán [] si hubo error
# ----------------------------------------------------------------------------------------------------------------------
class Sim(Curve):
    def __init__(self, c_type, data, name, color):
        super().__init__(2, data, name, color)
        if self.check_file(data):
            self.w, self.mod, self.ph = self.check_data(self.rawdata)

    # change_data: Setter para los datos
    def change_data(self, path):
        if self.check_file(path):
            self.rawdata = path
            self.w, self.mod, self.ph = self.check_data(self.rawdata)

    # check_data: Parsea el txt de la simulación de LTSpice, asume que tiene el formato de los ejemplos
    # Devuelve w, mod, ph
    def check_data(self, path):
        file = open(path, "r")
        count = 0
        file.readline()
        aux = file.readline().split("\t")
        aux_mod, aux_ph = aux[1][1:-2].split(",")

        self.mod_unit = get_unit(aux_mod)
        self.ph_unit = get_unit(aux_ph)
        for line in file:
            if line != "\n":
                count += 1
        file.close()

        w = np.zeros(count - 1)
        mod = np.zeros(count - 1)
        ph = np.zeros(count - 1)

        l = open(path, "r")

        l.readline()
        for i in range(count - 1):
            aux = l.readline().split("\t")
            w[i] = aux[0]
            aux_mod, aux_ph = aux[1][1:-2].split(",")
            mod[i] = aux_mod.replace(self.mod_unit, "")
            ph[i] = aux_ph.replace(self.ph_unit, "")
        l.close()

        if self.ph_unit == 'Â°': self.ph_unit = '°'

        return w, mod, ph

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
                if len(file.readline().split("\t")) != 2:
                    print("El archivo no cumple con el formato adecuado")
                    r = False
        return r
########################################################################################################################

########################################################################################################################
# Clase Med: Curva medida, hija de la clase Curve
#   Tiene unos parámetros extra: - Mentira por ahora no tiene
# ----------------------------------------------------------------------------------------------------------------------
class Med(Curve):
    def __init__(self, c_type, data, name, color):
        super().__init__(3, data, name, color)
        if self.check_file(data):
            self.w, self.mod, self.ph = self.check_data(self.rawdata)

    # change_data: Setter para los datos
    def change_data(self, path):
        if self.check_file(path):
            self.rawdata = path
            self.w, self.mod, self.ph = self.check_data(self.rawdata)

    # check_data: Parsea el csv de la medición de la Digilent, asume que tiene el formato de los ejemplos
    # Devuelve w, mod, ph
    def check_data(self, path):
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
        self.w_unit = units[0]
        self.mod_unit = units[1]
        if units[2] == "deg":
            self.ph_unit = "°"

        for i in range(count - 1):
            aux = l.readline().split(",")
            w[i] = aux[0]
            mod[i] = aux[1]
            ph[i] = aux[2]
        l.close()

        return w, mod, ph

    # check_file: Revisa que el archivo exista, sea .csv y que tenga el formato adecuado
    # Devuelve False en caso de error
    def check_file(self, path):
        r = True
        ext = os.path.splitext(path)[1]
        if self.type == 3 and ext != ".csv":
            print("El archivo de la medición no está en .csv")
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
                if len(file.readline().split(",")) != 3:
                    print("El archivo no cumple con el formato adecuado")
                    r = False
        return r
########################################################################################################################

########################################################################################################################
# fix_coefs: Acomoda los coeficientes del numerador o denominador y revisa si están bien ingresados
#            Devuelve None en caso de error
# ----------------------------------------------------------------------------------------------------------------------
def fix_coefs(coefs):
    r = True
    coefs = coefs.replace(" ", "")  # Elimina espacios
    if coefs == "":
        r = False
        print("Por favor ingrese los coeficientes")
    coefs = coefs.replace(",,", ",0,")
    if coefs[0] == ",":
        coefs = coefs[1:]
    if coefs[-1] == ",":
        coefs = coefs + "0"
    coefs = coefs.split(",")
    try:
        coefs = [float(s) for s in coefs]
    except ValueError:
        print("Uno de los valores ingresados no es numérico")
        r = False
    if not r:
        coefs = None
    return coefs
########################################################################################################################

########################################################################################################################
#   get_unit: Obtiene la unidad de los datos simulados de la curva
# ----------------------------------------------------------------------------------------------------------------------
def get_unit(s):
    unit = ""
    for i in range(len(s) - 1, 0, -1):
        if not s[i].isdigit():
            unit = s[i] + unit
            # s = s[:i]
        else:
            break
    return unit
########################################################################################################################




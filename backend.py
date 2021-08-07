import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as ss

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
        return 0

    def medida(self, data, name, color):
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

########################################################################################################################
# Clase Curve: Contiene toda la información para graficar la curva. Necesita:
#    - Tipo de curva: - 1 si es teórica (función transferencia)
#                     - 2 si es simulada (LTSpice)
#                     - 3 si es medida (Digilent)
#                     - 0 si es otra cosa (error)
#    - Datos: Dependerán del tipo de curva, en cada caso se especifica mejor (mirar funciones)
#    - Nombre: Si no se especifica, se le asignará uno según el orden
#    - Color: Se permitirá elegir el color de la curva, si no se especifica se tomará naranja todo ver como hace esto la gui
# Para cada tipo se accede una clase particular, mirarlas para más detalles
# ----------------------------------------------------------------------------------------------------------------------
class Curve:
    def __init__(self, c_type, data, name, color):
        self.type = c_type          # Tipo de curva
        self.rawdata = data         # Datos como se cargan
        self.name = name            # Nombre de la curva
        self.color = color          # Color de la curva
        self.visibility = True      # Está visible? Por defecto se inicializa en True

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

    # change_data: Revisa la validez de los datos nuevos. Devuelve False si hubo error.
    def change_data(self, data):
        r = True
        num, den = self.check_data(self.rawdata)        # Revisa los datos nuevos
        if num is not None and den is not None:         # Si están en orden, hace la modificación
            self.H = ss.TransferFunction(num, den)
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



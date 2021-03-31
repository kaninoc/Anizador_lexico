# validez de letras ingresadas
import re
letraValida = re.compile('\w')
simboloValido = re.compile('\W')
# Contiene los tokens y simbolos necesarios para el analizador lexico

comentarios = ["//", "/*", "*/"]

simbolos = ['+', '-', '*', '/', '%', '=', '<', '>', '<=', '>=',
            '==', '&&', '||', '!=', '!', ':', ';', ',', '.', '(', ')']
tokens = [

    "tk_mas",
    "tk_menos",
    "tk_mult",
    "tk_div",
    "tk_mod",
    "tk_asig",
    "tk_menor",
    "tk_mayor",
    "tk_menor_igual",
    "tk_mayor_igual",
    "tk_igual",
    "tk_y",
    "tk_o",
    "tk_dif",
    "tk_neg",
    "tk_dosp",
    "tk_pyc",
    "tk_coma",
    "tk_punto",
    "tk_par_izq",
    "tk_par_der"

]

reservadas = [
    "funcion_principal",
    "fin_principal",
    "booleano",
    "caracter",
    "entero",
    "real",
    "cadena",
    "entero",
    "falso",
    "verdadero"
]

funcion_defecto = ["leer", "imprimir"]

condicionales = ["si", "si_no", "fin_si"]

ciclos = ["mientras", "hacer", "para", "fin_mientras", "fin_para"]

case = ["seleccionar", "entre", "caso", "romper", "defecto", "fin_seleccionar"]

estructuras = ["estructura", "fin_estructura"]

funcion = ["funcion", "retornar", "fin_funcion"]

# print(simbolos[20]+"  "+tokens[20])


class Token:
    fila = ''
    columna = ''
    lexema = ''
    tipo = ''

    def print_information(self, fila, columna, lexema, tipo):
        print(self.fila)
        print(self.columna)
        print(self.lexema)
        print(self.tipo)


t = Token()
t.columna = 0
t.fila = 1
t.lexema = '+'
# t.tipo = "entero"
# t.print_information(t.fila, t.columna, t.lexema, t.tipo)


# variables de fila y columna del analizador Globales

linea = 1
posicion = 1
coment = False


# funcion que analiza los comentarios
def idcomentarios(cadena):
    global coment
    sp = cadena.find("//")
    if sp != -1:
        return True
    sp = cadena.find("/*")
    if sp != -1:
        coment = True
        return True
    sp = cadena.find("*/")
    if sp != -1:
        if coment == False:
            return False
        else:
            coment = False
            return True
    if coment == True:
        return True

    else:
        return False

# detecta las posiciones de los tocken e identificadores


def separarLinea(cadena):
    resultados = []
    palabraVar = ['', -1]
    simbolo = ['', -1]

    for i, letra in enumerate(cadena):
        if letra == ' ':
            # print("hola")
            if palabraVar[0] != '':
                if palabraVar[0].isnumeric():
                    resultados.append([int(palabraVar[0]), palabraVar[1]])
                else:
                    resultados.append([palabraVar[0], palabraVar[1]])
                palabraVar = ['', -1]
            if simbolo[0] != '':
                resultados.append([simbolo[0], simbolo[1]])
                simbolo = ['', -1]
        if letra != ' ':

            verificar_letra = letraValida.match(letra)  # Letra o numero valido
            # print(bool(verificar_letra))
            if bool(verificar_letra):
                # print(bool(verificar_letra))
                palabraVar[0] = palabraVar[0] + letra
                if palabraVar[1] == -1:
                    palabraVar[1] = i+1
                if simbolo[0] != '':
                    resultados.append([simbolo[0], simbolo[1]])
                    simbolo = ['', -1]
                if i+1 == len(cadena):
                    if palabraVar[0].isnumeric():
                        print(palabraVar[0].isnumeric())
                        resultados.append([int(palabraVar[0]), palabraVar[1]])
                    else:
                        resultados.append([palabraVar[0], palabraVar[1]])

            verificar_simbolo = simboloValido.match(letra)  # simbolo valido
            # print(bool(verificar_simbolo))
            if bool(verificar_simbolo):
                simbolo[0] = simbolo[0] + letra
                if simbolo[1] == -1:
                    simbolo[1] = i+1
                if palabraVar[0] != '':
                    # print("hola")
                    if palabraVar[0].isnumeric():
                        resultados.append([int(palabraVar[0]), palabraVar[1]])
                    else:
                        resultados.append([palabraVar[0], palabraVar[1]])
                    palabraVar = ['', -1]
                if i+1 == len(cadena):
                    resultados.append([simbolo[0], simbolo[1]])

    return resultados


# imprime y aniza coincidencias
def analizador(lista, linea):
    for elemento in lista:
        if validar_reservada(elemento[0]):
            print('<'+elemento[0]+','+str(linea)+','+str(elemento[1])+'>')

def validar_reservada(elemento):
    try:
        n = reservadas.index(elemento)
        return True
    except ValueError:
        return False

# procedimiento principal

while True:

    try:
        cadena = input()

        if idcomentarios(cadena) == False:
            lineas_analizadas = separarLinea(cadena)
            # print(lineas_analizadas)
            analizador(lineas_analizadas, linea)
        linea += 1
    except EOFError:
        break

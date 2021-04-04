# validez de letras ingresadas
import re
letraValida = re.compile('\w')
simboloValido = re.compile('\W')
# Contiene los tokens y simbolos necesarios para el analizador lexico

comentarios = ["//", "/*", "*/"]

nopermitidos = ['ñ', 'Ñ', 'á', 'Á', 'é', 'É', 'í',
                'Í', 'ó', 'Ó', 'ú', 'Ú', '@', '{', '}', '[', ']']

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
    "verdadero",
    "leer",
    "imprimir",
    "funcion",
    "retornar",
    "fin_funcion",
    "mientras",
    "hacer",
    "para",
    "fin_mientras",
    "fin_para",
    "seleccionar",
    "entre",
    "caso",
    "romper",
    "defecto",
    "fin_seleccionar",
    "si",
    "si_no",
    "fin_si",
    "entonces",
    "estructura",
    "fin_estructura"
]

'''
condicionales = ["si", "si_no", "fin_si"]

ciclos = ["mientras", "hacer", "para", "fin_mientras", "fin_para"]

case = ["seleccionar", "entre", "caso", "romper", "defecto", "fin_seleccionar"]

estructuras = ["estructura", "fin_estructura"]'''


class Token:
    simbolo = ''
    id = ''
    columna = ''
    fila = ''

    def print_reservada(self):
        print('<'+self.simbolo+','+str(self.fila)+','+str(self.columna)+'>')

    def print_numero(self):
        print('<'+self.simbolo+','+self.id+',' +
              str(self.fila)+','+str(self.columna)+'>')

    def print_error(self):
        print('>>> Error lexico (linea: '+str(self.fila) +
              ', posicion: '+str(self.columna)+')')


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
    # print(cadena)
    resultados = []
    palabraVar = ['', -1]
    simbolo = ['', -1]
    punto = False
    strings = ['', -1, False]
    char = ['', -1, False]

    for i, letra in enumerate(cadena):

        if ord(letra) == 39:
            if char[2] == False:
                if palabraVar[0] != '':
                    resultados.append([palabraVar[0], palabraVar[1]])
                    palabraVar = ['', -1]
                if simbolo[0] != '':
                    resultados.append([palabraVar[0], palabraVar[1]])
                    simbolo = ['', -1]
                char = [letra, i+1, True]
                continue
            if char[2] == True:
                resultados.append([char[0]+letra, char[1]])
                char = ['', -1, False]
                continue

        if validar_especiales(letra):
            if palabraVar[0] != '':
                resultados.append([palabraVar[0], palabraVar[1]])
                palabraVar = ['', -1]
            if simbolo[0] != '':
                resultados.append([palabraVar[0], palabraVar[1]])
                simbolo = ['', -1]
            resultados.append([letra, i+1])

            continue

        if letra == ' ':
            # print("hola")
            if strings[2] == True:
                strings = [strings[0] + letra, strings[1], True]
                continue
            if char[2] == True:
                char = [char[0] + letra, char[1], True]
                continue
            if palabraVar[0] != '':
                resultados.append([palabraVar[0], palabraVar[1]])
                palabraVar = ['', -1]
                punto = False
            if simbolo[0] != '':
                resultados.append([simbolo[0], simbolo[1]])
                simbolo = ['', -1]
        if letra != ' ':

            verificar_letra = letraValida.match(letra)  # Letra o numero valido
            # print(bool(verificar_letra))
            if bool(verificar_letra):
                if strings[2] == True:
                    strings = [strings[0] + letra, strings[1], True]
                    continue
                if char[2] == True:
                    char = [char[0] + letra, char[1], True]
                    continue
                # print(bool(verificar_letra))
                palabraVar[0] = palabraVar[0] + letra
                if palabraVar[1] == -1:
                    palabraVar[1] = i+1
                if simbolo[0] != '':
                    resultados.append([simbolo[0], simbolo[1]])
                    simbolo = ['', -1]
                if i+1 == len(cadena):
                    resultados.append([palabraVar[0], palabraVar[1]])

            verificar_simbolo = simboloValido.match(letra)  # simbolo valido
            # print(bool(verificar_simbolo))

            if bool(verificar_simbolo):
                if char[2] == True:
                    char = [char[0] + letra, char[1], True]
                    continue
                if letra == '.':
                    if id_numero(palabraVar[0]) == "tk_entero" and punto == False:
                        punto = True
                        palabraVar[0] = palabraVar[0] + letra
                        continue
                    else:
                        punto = False
                if letra == '"':
                    if strings[2] == False:
                        strings = [strings[0] + letra, i+1, True]
                        continue
                    else:
                        resultados.append([strings[0]+'"', strings[1]])
                        strings = ['', -1, False]
                        continue

                if letra == '(' or letra == ')' or letra == '+' or letra == '-' or letra == '*' or letra == '/' or letra == '%' or letra == ':' or letra == ';' or letra == ',' or letra == '.':
                    if palabraVar[0] != '':
                        resultados.append([palabraVar[0], palabraVar[1]])
                        resultados.append([letra, i+1])
                        palabraVar = ['', -1]
                        continue
                    if simbolo[0] != '':
                        resultados.append([simbolo[0], simbolo[1]])
                        resultados.append([letra, i+1])
                        simbolo = ['', -1]
                        continue
                    else:
                        resultados.append([letra, i+1])
                        continue

                if strings[2] == True:
                    strings = [strings[0] + letra, strings[1], True]
                    continue

                simbolo[0] = simbolo[0] + letra
                if simbolo[1] == -1:
                    simbolo[1] = i+1
                if palabraVar[0] != '':

                    resultados.append([palabraVar[0], palabraVar[1]])
                    palabraVar = ['', -1]
                if i+1 == len(cadena):
                    resultados.append([simbolo[0], simbolo[1]])
                    simbolo = ['', -1]

    return resultados

# elimina los saltos de linea


def eliminar(lista):
    aux = []
    for i, elemento in enumerate(lista):
        if elemento[0].find('\r') != -1:
            s = elemento[0]
            s = s[:len(s)-1]
            aux.append([s, elemento[1]])
        else:
            aux.append(elemento)
    return aux


# imprime y aniza coincidencias
def analizador(lista, linea):
    ##print(lista)
    for i, elemento in enumerate(lista):
        if elemento[0] == '\r' or elemento[0] == '':
            break
        if validar_tabulacion(elemento[0]):
            lista[i+1][1] = lista[i+1][1]+3
            continue
        if validar_especiales(elemento[0]) == True:
            t = Token()
            t.fila = str(linea)
            t.columna = str(elemento[1])
            t.print_error()
            return False
            break
        if validar_variable(elemento[0]):
            t = Token()
            t.simbolo = "id"
            t.id = elemento[0]
            t.fila = str(linea)
            t.columna = str(elemento[1])
            t.print_numero()
        if validar_cadena_var(elemento[0]) != "no":
            t = Token()
            t.simbolo = validar_cadena_var(elemento[0])
            t.id = elemento[0]
            t.fila = str(linea)
            t.columna = str(elemento[1])
            t.print_numero()
            continue
        if validar_caracter(elemento[0]) != "error":
            t = Token()
            t.simbolo = validar_caracter(elemento[0])
            t.id = elemento[0]
            t.fila = str(linea)
            t.columna = str(elemento[1])
            t.print_numero()
            continue
        if validar_reservada(elemento[0]):
            t = Token()
            t.simbolo = elemento[0]
            t.fila = str(linea)
            t.columna = str(elemento[1])
            t.print_reservada()
        if validar_simbolo(elemento[0]) != -1:
            n = validar_simbolo(elemento[0])
            t = Token()
            t.simbolo = tokens[n]
            t.fila = str(linea)
            t.columna = str(elemento[1])
            t.print_reservada()
        if id_numero(elemento[0]) != "no":
            t = Token()
            t.simbolo = id_numero(elemento[0])
            t.id = elemento[0]
            t.fila = str(linea)
            t.columna = str(elemento[1])
            t.print_numero()

    return True


def validar_variable(elemento):

    if elemento[0] == '"' or ord(elemento[0]) == 39:
        return False

    if validar_reservada(elemento) == False and validar_simbolo(elemento) == -1 and id_numero(elemento) == "no":
        return True


def validar_tabulacion(elemento):
    if elemento == '\t':
        return True


def validar_reservada(elemento):
    try:
        n = reservadas.index(elemento)
        return True
    except ValueError:
        return False


def validar_especiales(elemento):
    try:
        n = nopermitidos.index(elemento)
        return True
    except ValueError:
        return False


def validar_simbolo(elemento):
    try:
        n = simbolos.index(elemento)
        return n
    except ValueError:
        return -1


def id_numero(elemento):
    if elemento.isnumeric():
        return "tk_entero"
    if elemento.find(".") != -1 and elemento != '.':
        return "tk_real"
    return "no"


def validar_caracter(elemento):
    if ord(elemento[0]) == 39 and ord(elemento[len(elemento[0])-2]) == 39:
        return "tk_caracter"
    else:
        return "error"


def validar_cadena_var(elemento):
    if elemento[0] == '"' and elemento[len(elemento[0])-2] == '"':
        return "tk_cadena"
    else:
        return "no"

# procedimiento principal


while True:

    try:
        cadena = input()
        '''if cadena.find('\r')!=-1:
            # print(cadena)
            cadena = cadena.replace('\\r', '')'''
        if idcomentarios(cadena) == False and cadena != "":
            lineas_analizadas = separarLinea(cadena)
            lineas_finales = eliminar(lineas_analizadas)
            b = analizador(lineas_finales, linea)
            ##print (b)
            if b == False:
                break
        linea += 1
    except EOFError:
        break

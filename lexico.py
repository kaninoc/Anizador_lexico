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
    ##print(cadena)
    resultados = []
    palabraVar = ['', -1]
    simbolo = ['', -1]

    for i, letra in enumerate(cadena):
        if letra == ' ':
            # print("hola")
            if palabraVar[0] != '':
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
                    resultados.append([palabraVar[0], palabraVar[1]])

            verificar_simbolo = simboloValido.match(letra)  # simbolo valido
            # print(bool(verificar_simbolo))

            if bool(verificar_simbolo):
                simbolo[0] = simbolo[0] + letra
                if simbolo[1] == -1:
                    simbolo[1] = i+1
                if palabraVar[0] != '':
                    resultados.append([palabraVar[0], palabraVar[1]])
                    palabraVar = ['', -1]
                if i+1 == len(cadena):
                    resultados.append([simbolo[0], simbolo[1]])

    return resultados

def eliminar(lista):
    aux = []
    for i, elemento in enumerate(lista):
        if elemento[0].find('\r')!=-1:
            s = elemento[0]
            s = s[:len(s)-1]
            aux.append([s,elemento[1]])
        else:
            aux.append(elemento)
    return aux

# imprime y aniza coincidencias
def analizador(lista, linea):
    ##print(lista)
    for i, elemento in enumerate(lista):
        if elemento[0] == '\r' or elemento[0] == '':
            ##print("fiesta")
            break
        if elemento[0].find('\r')!=-1:
            e = elemento[0].replace('\\r', '')
            print(e)
        if validar_tabulacion(elemento[0]):
            lista[i+1][1] = lista[i+1][1]+3
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
        if validar_variable(elemento[0]):
            t = Token()
            t.simbolo = "id"
            t.id = elemento[0]
            t.fila = str(linea)
            t.columna = str(elemento[1])
            t.print_numero()
        if validar_variable(elemento[0]) == False:
            t = Token()
            t.fila = str(linea)
            t.columna = str(elemento[1])
            t.print_error()
            return False
            break

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


def validar_simbolo(elemento):
    try:
        n = simbolos.index(elemento)
        return n
    except ValueError:
        return -1


def id_numero(elemento):
    if elemento.isnumeric():
        return "tk_entero"
    if elemento.isdecimal():
        return "tk_real"
    return "no"


def validar_variable(elemento):
    # print(validar_reservada(elemento),validar_simbolo(elemento),id_numero(elemento))
    if elemento.find("ñ") != -1 or elemento.find("Ñ") != -1:
        return False
    if validar_reservada(elemento) == False and validar_simbolo(elemento) == -1 and id_numero(elemento) == "no":
        return True


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
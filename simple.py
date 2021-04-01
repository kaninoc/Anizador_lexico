import re

s = input()
regex = re.compile('[a-z]')
verificar = regex.match(s)
print (bool(verificar))

import re
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
        coment = False
        return True
    if coment == True:
        return True

    else:
        return False

# detecta las posiciones de los tocken e identificadores


def separarLinea(cadena):
    separado = cadena.split()
    pos = []
    for i in range(len(cadena)):
        if i == 0 and cadena[0] != ' ':
            pos.append(0)
        if cadena[i] != ' ' and cadena[i-1] == ' ':
            pos.append(i)
    return [separado, pos]


# determina la existencia de palabras reservadas
def analizador(lista, posiciones,linea):
    print(lista)
    for i, elemento in enumerate(lista):
        try:
            aux = reservadas.index(elemento)
            if aux != -1:
                print("<"+elemento+","+str(linea)+","+str(posiciones[i]+1)+">")
                ##print("<"+elemento+","+linea+","+posiciones[i]+1,">")
        
        except ValueError:
                print("<id,"+elemento+","+str(linea)+","+str(posiciones[i]+1)+">")


# procedimiento principal


while True:

    try:
        cadena = input()

        if idcomentarios(cadena) == False and cadena !="":
            listpalabra, pospalabras = separarLinea(cadena)
            analizador(listpalabra, pospalabras,linea)
        linea += 1
    except EOFError:
        break

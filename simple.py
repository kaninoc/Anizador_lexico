import re
digitoValido = re.compile('\d')


def separador(lista):
    aux = []
    for i, elemento in enumerate(lista):
        number = ['', -1]
        palabra = ['', -1]
        for j, letra in enumerate(elemento[0]):
            if bool(digitoValido.match(letra)) == False and j == 0:
                aux.append(elemento)
                break
            if bool(digitoValido.match(letra)):
                if palabra[0] != '':
                    aux.append([palabra[0], palabra[1]])
                    palabra = ['', -1]
                if number[1] == -1:
                    number[1] = elemento[1]+j
                number[0] = number[0] + letra
            if bool(digitoValido.match(letra)) == False:
                if number[0] != '':
                    aux.append([number[0], number[1]])
                    number = ['', -1]
                if palabra[1] == -1:
                    palabra[1] = elemento[1]+j
                palabra[0] = palabra[0] + letra
            if len(elemento[0]) == j+1:
                if number[0] != '':
                    aux.append(number)
                else:
                    aux.append(palabra)
    return aux

print(separador([["123abc",1],["1a2b4c",14]]))
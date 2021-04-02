def eliminar():
    aux = []
    lista = [['entero', 5], ['num1', 12], [',', 16], ['num2', 17], [',', 21], ['may', 22], [';\r', 25]]
    for i, elemento in enumerate(lista):
        if elemento[0].find('\r')!=-1:
            s = elemento[0]
            s = s[:len(s)-1]
            aux.append([s,elemento[1]])
        else:
            aux.append(elemento)
    return aux

print(eliminar())

a = "r\r"

print(a[:len(a)-1]+"hola")
print(a+"hola")

my_str='python string'
final_str=my_str[:-1]
print(final_str)
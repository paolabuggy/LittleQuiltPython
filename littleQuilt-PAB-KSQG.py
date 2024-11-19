# EXAMEN PRIMER PARCIAL ISC 9 C
# COMPILADORES II
# M.I.A. Eduardo Serna Pérez
# Fecha: Sept 8, 2023

# Integrantes:
# Paola Alba Bugarin ID: 226962
# Karla Susana Quezada Guerrero ID: 275101

#####  LITTLE QUILT  #####

def crearQuilt (ancho, alto):
    matrizQuilt = []
    for _ in range(alto):
        fila = [0] * ancho #Crea una fila de ancho elementos
        matrizQuilt.append(fila) #Agrega la fila a la matriz
    return matrizQuilt

# A
def quiltA():
    matrizA = crearQuilt(2,2)
    matrizA[0][0] = "/"
    matrizA[0][1] = "/"
    matrizA[1][0] = "/"
    matrizA[1][1] = "+"
    return matrizA

# B
def quiltB():
    matrizB = crearQuilt(2,2)
    matrizB[0][0] = "-"
    matrizB[0][1] = "-"
    matrizB[1][0] = "-"
    matrizB[1][1] = "-"
    return matrizB

def tamano_matriz(matriz):
    # El número de filas es igual a la longitud de la matriz
    numero_de_filas = len(matriz)
    # El número de columnas es igual a la longitud de una fila cualquiera (si todas tienen la misma longitud)
    numero_de_columnas = len(matriz[0]) if numero_de_filas > 0 else 0
    return numero_de_columnas, numero_de_filas 

def girar_matriz_90_grados(matriz):
    if not matriz:
        return []

    filas_originales = len(matriz)
    columnas_originales = len(matriz[0])

    # Crear una nueva matriz con las dimensiones giradas
    matriz_girada = [[0] * filas_originales for _ in range(columnas_originales)]

    for i in range(filas_originales):
        for j in range(columnas_originales):
            matriz_girada[j][filas_originales - 1 - i] = matriz[i][j]

    return matriz_girada

# turn(<QUILT>)
def turn(mOriginal):
    if not mOriginal:
        return []

    matriz_girada = girar_matriz_90_grados(mOriginal)
    
    for i in range(len(matriz_girada)):
        for j in range(len(matriz_girada[0])):
            if matriz_girada[i][j] == "-":
                matriz_girada[i][j] = "|"
            elif matriz_girada[i][j] == "|":
                matriz_girada[i][j] = "-"
            elif matriz_girada[i][j] == "/":
                matriz_girada[i][j] = "\\"
            elif matriz_girada[i][j] == "\\":
                matriz_girada[i][j] = "/"
    return matriz_girada

# sew(<QUILT>,<QUILT>)
def sew(quilt1, quilt2):
    # Verificar si las alturas de x y y son las mismas
    if len(quilt1) != len(quilt2):
        #raise ValueError("Las alturas del quilt y quilt 2 deben ser las mismas")
        return "error"
    # Coser quilt1 a la izquierda de quilt2
    nuevoQuilt = []
    for i in range(len(quilt1)):
        fila_sew = quilt1[i] + quilt2[i]
        nuevoQuilt.append(fila_sew)
    return nuevoQuilt

# Función para leer el archivo de entrada y unir líneas divididas
def leer_archivo_de_entrada(archivo_entrada):
    with open(archivo_entrada, 'r') as archivo:
        contenido = archivo.read()
    # Dividir el contenido por punto y coma para obtener las expresiones
    expresiones = contenido.split(';')
    return expresiones

# Función principal que interpreta las expresiones Little Quilt
def interpretar_expresion(expresion):
    expresion = expresion.strip()
    # Verificar si es una expresión compuesta
    if expresion.startswith("sew("):
        expresion = expresion[4:-1]
        sub_expresiones = []
        nivel_parentesis = 0
        inicio = 0

        # Dividir la expresión en sub-expresiones dentro de los paréntesis
        for i, caracter in enumerate(expresion):
            if caracter == '(':
                nivel_parentesis += 1
            elif caracter == ')':
                nivel_parentesis -= 1
            elif caracter == ',' and nivel_parentesis == 0:
                sub_expresiones.append(expresion[inicio:i].strip())
                inicio = i + 1
        
        sub_expresiones.append(expresion[inicio:].strip())
        
        # Interpretar las sub-expresiones y realizar la operación sew
        quilt1 = interpretar_expresion(sub_expresiones[0])
        quilt2 = interpretar_expresion(sub_expresiones[1])
        resultado = sew(quilt1, quilt2)
        
        if resultado == "error":
            return "error"
        else:
            return resultado
    elif expresion.startswith("turn("):
        expresion = expresion[5:-1].strip()
        quilt = interpretar_expresion(expresion)
        quilt = turn(quilt)
        return quilt
    else:
        return interpretar_quilt(expresion)


# Función para interpretar un quilt A o B
def interpretar_quilt(expresion):
    if expresion == "A":
        return quiltA()
    elif expresion == "B":
        return quiltB()
    else:
        return []

# Función para escribir los resultados en el archivo de salida
def escribir_resultados(quilts, archivo_salida):
    with open(archivo_salida, 'w') as archivo:
        for i, quilt in enumerate(quilts):
            archivo.write(f"Quilt {i + 1}:\n")
            if quilt == "error":
                archivo.write("error\n")
            else:
                for row in quilt:
                    archivo.write("".join(row) + "\n")


# Lectura del archivo de entrada y unión de líneas divididas
archivo_entrada = "entrada.txt"  # Nombre del archivo de entrada
expresiones = leer_archivo_de_entrada(archivo_entrada)

# Limpieza de expresiones: eliminación de espacios en blanco y líneas vacías
expresiones = [expresion.strip() for expresion in expresiones if expresion.strip() != '']

# Interpretación de las expresiones
quilts = []
for expresion in expresiones:
    quilt = interpretar_expresion(expresion)
    quilts.append(quilt)

# Escritura de los resultados en el archivo de salida
archivo_salida = "salida.txt"  # Nombre del archivo de salida
escribir_resultados(quilts, archivo_salida)

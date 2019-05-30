from manejo_de_archivos import *

# ***********************************************************************
# *------- FUNCIONES QUE HACEN EL MERGE ENTRE EL CSV Y EL BIN-----------*
# ***********************************************************************

# Esta funcion imprime mi listado de usuarios de forma ordenada.
def mostrar_usuarios_ordenados(usuarios_precargados, usuarios_nuevos):
    user_1 = usuarios_precargados.readline().strip("ï»¿")
    user_2 = leer_archivo_bin(usuarios_nuevos)
    # Ingreso al ciclo que ordenara mis usuarios
    while user_1 or user_2:
        # Tengo usuarios en los dos archivos
        if user_1 and user_2:
            pseudo_1 = user_1.strip("\n").split(";")[2]
            pseudo_2 = user_2.strip("\n").split(";")[2]
            if pseudo_1 < pseudo_2:
                user = user_1.strip("\n").split(";")
                user_1 = usuarios_precargados.readline()
            else:
                user = user_2.strip("\n").split(";")
                user_2 = leer_archivo_bin(usuarios_nuevos)
        # Solo me quedan usuarios en el archivo 1
        elif user_1:
            user = user_1.strip("\n").split(";")
            user_1 = usuarios_precargados.readline()
        # Solo me quedan usuarios en el archivo 2
        else:
            user = user_2.strip("\n").split(";")
            user_2 = leer_archivo_bin(usuarios_nuevos)
        print("Nombre: {}, Apellido: {}, Edad: {}, Pseudonimo: {}".format(user[0], user[1], user[5], user[2]))

# Funcion que lista por pantalla mis usuarios.
def listar_usuarios():
    # Abro mis archivos
    usuarios_nuevos = open("usuarios_nuevos.dat", "br")
    usuarios_precargados = open("usuarios_precargados.csv", "r")

    # Ordeno e imprimo mi base de datos
    print()
    mostrar_usuarios_ordenados(usuarios_precargados, usuarios_nuevos)
    print()

    # Cierro mis archivos
    usuarios_nuevos.close()
    usuarios_precargados.close()

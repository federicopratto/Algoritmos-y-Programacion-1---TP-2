import pickle
import os
import shutil

# ***********************************************************************
# * ------------- FUNCIONES PARA LEER Y ESCRIBIR ARCHIVOS ------------- *
# ***********************************************************************

# Esta funcion lee una entrada en mi archivo binario.
def leer_archivo_bin(archivo):
    try:
        usuario = pickle.load(archivo)
    except (EOFError, pickle.UnpicklingError):
        usuario = ""
    return usuario


# Esta funcion guarda nuevos datos en el archivo binario.
def escribir_archivo_bin(dato, archivo):
    pkl = pickle.Pickler(archivo)
    pkl.dump(dato)


# ***********************************************************************
# *-------------- FUNCIONES PARA ORDENAR ARCHIVO BIN -------------------*
# ***********************************************************************

# Esta funcion guarda en un archivo bin una lista de usuarios ordenados.
def guardar_usuarios_ordenados(archivo_ordenado):
    usuarios_nuevos = open("usuarios_nuevos.dat", "bw")

    for dato in archivo_ordenado:
        escribir_archivo_bin(dato, usuarios_nuevos)
    usuarios_nuevos.close()


# Esta funcion ordena los usuarios del archivo bin donde guardo mis usuarios nuevos.
def ordenar_archivo_bin(usuarios_nuevos):
    # Genero una lista vacia y guardo mi primer usuario.
    archivo_ordenado = []
    archivo_ordenado.append(leer_archivo_bin(usuarios_nuevos))

    # Leo el segundo usuario de mi archivo (Si es que existe)
    usuario = leer_archivo_bin(usuarios_nuevos)

    # Ingreso al ciclo que ordenara mis usuarios
    while usuario:
        pseudo = usuario.strip("\n").split(";")[2]
        i = 0
        seguir = True
        while usuario and seguir:
            aux = archivo_ordenado[i].strip("\n").split(";")[2]
            if aux > pseudo:
                aux = archivo_ordenado[i]
                archivo_ordenado[i] = usuario
                archivo_ordenado.insert(i + 1, aux)
                seguir = False
            elif i < len(archivo_ordenado)-1:
                i += 1
            else:
                archivo_ordenado.append(usuario)
                seguir = False
        # Finalizado el ciclo leo un nuevo usuario.
        usuario = leer_archivo_bin(usuarios_nuevos)
    usuarios_nuevos.close()
    guardar_usuarios_ordenados(archivo_ordenado)

# ***************************************************************************************
# *-------------- FUNCIONES PARA ORDENAR ARCHIVO DE LIKES Y MENSAJES -------------------*
# ***************************************************************************************

def cargar_novedades(novedades):
    # Guardo los datos actualizados en aux.dat
    archivo = open("likes_y_mensajes.dat", "br")
    archivo_aux = open("auxiliar.dat", "bw")
    registro = leer_archivo_bin(archivo)
    # Copio los likes de los usuarios que ya existian pero actualizados
    while registro:
        if registro[0] in novedades:
            registro = novedades[registro[0]]
            del novedades[registro[0]]
        escribir_archivo_bin(registro, archivo_aux)
        registro = leer_archivo_bin(archivo)
    # Copio los likes nuevos.
    for registro in novedades:
        escribir_archivo_bin(novedades[registro], archivo_aux)
    archivo.close()
    archivo_aux.close()
    # reinicializo la variable novedades, ya que ahora no hay novedades.
    novedades = {}



def actualizar_likes_y_mensajes(novedades):
    # Cargo mis novedades en un archivo auxiliar
    cargar_novedades(novedades)

    #Elimino el archivo de likes original
    os.remove("likes_y_mensajes.dat")

    # Convierto mi archivo aux en mi archivo likes y mensajes
    shutil.copy2("auxiliar.dat", "likes_y_mensajes.dat")

    # Borro mi archivo aux.
    os.remove("auxiliar.dat")

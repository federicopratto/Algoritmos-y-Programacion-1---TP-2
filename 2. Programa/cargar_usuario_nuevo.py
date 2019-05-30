# Importo las funciones necesarias para manejar mis archivos.
from manejo_de_archivos import *


# ***********************************************************************************
# *-------------------- FUNCIONES DE CARGA DE DATOS USUARIO NUEVO ------------------*
# ***********************************************************************************

# --------------------FUNCIONES DE CARGA Y VALIDACION DE PSEUDONIMO------------------

# Esta funcion verifica si el pseudonimo ingresado para un nuevo usuario es tiene un formato valido.
def validar_formato_pseudonimo(pseudo):
        prueba = pseudo.replace("_", "")
        if prueba.islower() and prueba.isalnum():
            return False
        print("\n* ¡Hay caracteres invalidos en el pseudonimo. Vuelva a intentarlo! *\n")
        return True


# Esta función recupera los pseudonimos de los usuarios ingresados en la base de
# datos y los compara con el nuevo pseudonimo ingresado.
def comparar_pseudonimos(usuario, pseudo):
    if pseudo == usuario.strip("\n").split(";")[2]:
        print("\n** Usuario ya existe **\n")
        return True


# Esta funcion valida el pseudonimo de un nuevo usuario.
def validar_pseudonimo(pseudo):
    # Valido si el formato del pseudonimo es correcto
    usuario_invalido = validar_formato_pseudonimo(pseudo)

    # Abro los archivos donde guardo mis usuarios.
    usuarios_precargados = open("usuarios_precargados.csv", "r")
    usuarios_nuevos = open("usuarios_nuevos.dat", "br")

    # Verifico si el pseudonimo esta en los usuarios precargados
    usuario = usuarios_precargados.readline()
    while not usuario_invalido and usuario:
        usuario_invalido = comparar_pseudonimos(usuario, pseudo)
        usuario = usuarios_precargados.readline()

    # Verifico si el pseudonimo esta en los usuarios nuevos.
    usuario = leer_archivo_bin(usuarios_nuevos)
    while not usuario_invalido and usuario:
        usuario_invalido = comparar_pseudonimos(usuario, pseudo)
        usuario = leer_archivo_bin(usuarios_nuevos)
    # Cierro mis archivos.
    usuarios_precargados.close()
    usuarios_nuevos.close()
    return usuario_invalido


#Esta función se encarga de cargar un nuevo pseudonimo de usuario.
def cargar_pseudonimo():
    seguir = True
    while(seguir):
        pseudo = input("Ingrese un pseudonimo (Solo minúsculas, números y guiones bajos): ")
        seguir = validar_pseudonimo(pseudo)
    return pseudo

# --------------------FUNCIONES DE CARGA Y VALIDACION DE CONTRASEÑA------------------

#Esta función verifica cuantas mayusculas, minusculas y numeros tiene la contraseña
def contar_caracteres_contraseña(contraseña):
    mayusculas, minusculas, digitos = 0, 0, 0
    for caracter in contraseña:
        if caracter.isdigit():
            digitos += 1
        elif caracter.isalpha():
            if caracter.islower():
                minusculas += 1
            elif caracter.isupper():
                mayusculas += 1
    return mayusculas, minusculas, digitos


#Esta función verifica si la contraseña ingresada es valida
def validar_contraseña(contraseña):
    if len(contraseña) >= 5:
        caracteres = contar_caracteres_contraseña(contraseña)
        if (0 not in caracteres):
            return False
    print("\n* ¡La contraseña ingresada no cumple los requisitos! *")
    return True


#Esta funcion se encarga de solicitar al usuario una contraseña
def cargar_contraseña():
    seguir = True
    while(seguir):
        print("\nIngrese una contraseña. La misma debera tener como minimo:\n")
        print("- Una mayúscula\n- Una minúscula\n- Un dígito decimal\n- Un largo de 5 o mas caracteres\n")
        contraseña = input("Contraseña: ")
        seguir = validar_contraseña(contraseña)
    return contraseña

# --------------------FUNCIONES DE CARGA Y VALIDACION DE SEXO, EDAD, ETC.------------------

#Esta funcion se encarga de pedir al usuario su sexo
#Esta funcion no se valida, se supone que aca el usuario no se va a equivocar.
def ingresar_sexo():
    print("\n¿Cual es su sexo?\n- Femenino (F)\n- Masculino (M)\n- Otro (O)\n")
    sexo = input("Opcion elegida: ").upper()
    if sexo == "F":
        sexo = "Mujer"
    elif sexo == "M":
        sexo = "Hombre"
    else:
        sexo = "Indefinido"
    return sexo


#Esta función carga y verifica la edad del usuario.
def ingresar_edad():
    seguir = True
    while(seguir):
        edad = int(input("\nIngrese su edad (18 a 99): "))
        if 18 <= edad <= 99:
            seguir = False
        else:
            print("\n* ¡Edad incorrecta. Intente de nuevo! *")
    return str(edad)


#Esta funcion carga la ubicacion del usuario
def cargar_ubicacion():
    print("\n¿Como quiere ingresar su ubicación?")
    print("1- Manual (Ingresar su latitud y longitud)")
    print("2- Automatica (Ingresar su direccion actual)")
    eleccion = input("\nOpción elegida: ")
    if eleccion == 1:
        latitud = input('\nIngrese su latitud: ')
        longitud = input('Ingrese su longitud: ')
        ubicacion = "{};{}".format(latitud, longitud)
    else:
        try:
            import geopy
            from geopy.geocoders import Nominatim
            geolocator = geopy.geocoders.Nominatim(user_agent="specify_your_app_name_here")
            print("\nIngrese su dirección actual")
            print("Ej: Avenida Corrientes 600, Buenos Aires\n")
            direccion = geolocator.geocode(input("Direccion: "))
            latitud = direccion.latitude
            longitud = direccion.longitude
            ubicacion = "{};{}".format(latitud, longitud)
        except:
            print("\n╔════════════════════════════════════════════════╗")
            print("║ -------- ERROR AL CARGAR LA UBICACIÓN -------- ║")
            print("║ ------------   INTENTE DE NUEVO -------------- ║")
            print("╚════════════════════════════════════════════════╝\n")
            return cargar_ubicacion()
    return ubicacion


#Esta funcion permite cargar los intereses del usuario.
def cargar_intereses():
    print("\nIngrese sus intereses separados por coma y espacio.")
    print("Ej: futbol, cafe con leche, bailar, queso cheddar")
    intereses = input("\nIntereses: ").replace(" ", "-").replace(",-", ",")
    return intereses

# ***********************************************************************************
# *------------- FUNCION GENERAL PARA CARGA DE USUARIOS NUEVOS ---------------------*
# ***********************************************************************************

#Esta funcion llama a las funciones necesarias para crear un nuevo usuario. (**)
def cargar_nuevo_usuario():
    nuevo_usuario = ""
    nuevo_usuario += input("\nIngrese su nombre: ").capitalize() + ";"
    nuevo_usuario += input("Ingrese su apellido: ").capitalize() + ";"
    pseudo = cargar_pseudonimo()
    nuevo_usuario += pseudo + ";"
    nuevo_usuario += cargar_contraseña() + ";"
    nuevo_usuario += ingresar_sexo() + ";"
    nuevo_usuario += ingresar_edad() + ";"
    nuevo_usuario += cargar_ubicacion() + ";"
    nuevo_usuario += cargar_intereses() + "\n"

    #Cargo usuario nuevo en base de datos ordenados.
    nuevos_usuarios = open("usuarios_nuevos.dat", "ba")
    escribir_archivo_bin(nuevo_usuario, nuevos_usuarios)
    nuevos_usuarios.close()
    ordenar_archivo_bin(open("usuarios_nuevos.dat", "br"))
    # Genero una nueva entrada en el archivo de likes y mensajes
    likes_y_mensajes = open("likes_y_mensajes.dat", "br+")
    escribir_archivo_bin([pseudo, {}, {}, 0], likes_y_mensajes)
    likes_y_mensajes.close()

    print("\n╔════════════════════════════════════════════════╗")
    print("║ * Ya estas registrado. ¡Bienvenido a Tender! * ║")
    print("╚════════════════════════════════════════════════╝\n")

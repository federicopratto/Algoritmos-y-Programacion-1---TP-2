from manejo_de_archivos import *

# ********************************************************************
# *-------- FUNCIONES PARA CARGAR Y VALIDAR DATOS DE INGRESO --------*
# ********************************************************************

# Esta funcion convalida si los datos de ingreso son correctos.
def validar_datos_de_ingreso(usuario, clave):
    # Veo si mi usuario esta en los precargados
    usuario_encontrado = False
    contraseña_invalida = False
    usuarios = open("usuarios_precargados.csv", "r")
    registro = usuarios.readline()
    while registro and not usuario_encontrado:
        if usuario == registro.strip("\n").split(";")[2]:
            usuario_encontrado = True
            if clave != registro.strip("\n").split(";")[3]:
                print(registro.strip("\n").split(";")[2])
                contraseña_invalida = True
        else:
            registro = usuarios.readline()
    usuarios.close()
    if not usuario_encontrado:
        # Veo si mi usuario esta en los nuevos.
        usuarios = open("usuarios_nuevos.dat", "br")
        registro = leer_archivo_bin(usuarios)
        while registro and not usuario_encontrado:
            if usuario == registro.strip("\n").split(";")[2]:
                usuario_encontrado = True
                if clave != registro.strip("\n").split(";")[3]:
                    contraseña_invalida = True
            else:
                registro = leer_archivo_bin(usuarios)
        usuarios.close()

    if not usuario_encontrado:
        print("\n* Usuario invalido, vuelva a ingresar los datos *")
        return True, usuario
    elif contraseña_invalida:
        print("\n* Clave invalida, vuelva a ingresar los datos *")
        return True, usuario
    registro = registro.strip("\n").split(";")
    usuario = [registro[2], (registro[6], registro[7]), registro[8].split(",")]
    return False, usuario


# Esta funcion solicita los datos para ingresar al sistema.
def ingresar_a_sistema():
    seguir = True
    while(seguir):
        usuario = input("\nIngrese su nombre de usuario: ").lower()
        clave = input("Ingrese su clave: ")
        seguir, usuario = validar_datos_de_ingreso(usuario, clave)
    return usuario


# *******************************************************************
# *---------- FUNCIONES PARA CARGAR CRITERIOS DE BUSQUEDA ----------*
# *******************************************************************

# Esta funcion carga y verifica que el radio de busqueda sea valido.
def cargar_radio_busqueda():
    seguir = True
    while(seguir):
        distancia = float(input("\nIngrese el radio maximo de busqueda (km): "))
        if(0 > distancia or distancia > 20000):
            print("\n* Distancia invalida, vuelva a intentarlo. *")
        else:
            seguir = False
    return distancia


# Esta funcion carga y verifica que el sexo a buscar sea valido.
def cargar_sexo_busqueda():
    seguir = True
    while(seguir):
        print("\nIngrese el sexo de interes:\n\n1- Hombres\n2- Mujeres\n3- Ambos\n")
        sexo = int(input("Opcion elegida: "))
        if sexo not in [1, 2, 3]:
            print("\n* Opcion invalida, vuelva a intentarlo. *")
        else:
            if sexo == 1: sexo = "Hombre"
            elif sexo == 2: sexo = "Mujer"
            seguir = False
    return sexo


#Esta funcion carga y verifica los rangos de edad a buscar
def rango_edad_busqueda():
    seguir = True
    i = 0
    rango_edad = [0, 0]
    mensaje = ["minima", "maxima"]
    print("\nIngrese rango de edades:\n")
    while seguir:
        if i == 2:
            seguir = False
        else:
            rango_edad[i] = int(input("-Edad {}: ".format(mensaje[i])))
            if rango_edad[i] < 18 or rango_edad[i] > 99:
                print("\n* Edad invalida, minimo 18 años y maximo 99 años *\n")
            else:
                i += 1
    return rango_edad


#Esta funcion llama a las funciones encargadas de cargar los datos para la busqueda.
def datos_para_busqueda(usuario_actual):
    print("\n¡Hola @{}! Hagamos una busqueda".format(usuario_actual[0]))
    distancia = cargar_radio_busqueda()
    sexo = cargar_sexo_busqueda()
    rango_edad = rango_edad_busqueda()
    return distancia, sexo, rango_edad


# ******************************************************************
# *--------------- FUNCIONES PARA REALIZAR BUSQUEDA ---------------*
# ******************************************************************

#Esta funcion calcula la distancia entre dos usuarios.
def calcular_distancia(coordenadas_1, coordenadas_2):
    import geopy.distance
    distancia = round(geopy.distance.geodesic(coordenadas_1, coordenadas_2).kilometers, 2)
    return distancia


#Esta funcion compara las distancias entre dos usuarios con el rango buscado por el usuario actual
def comparar_distancias(usuario_actual, usuario_2, criterios_de_busqueda):
    coordenadas_1 = usuario_actual[1]
    coordenadas_2 = usuario_2[1]
    distancia = calcular_distancia(coordenadas_1, coordenadas_2)
    if distancia > criterios_de_busqueda[0]:
        return False, distancia
    return True, distancia


#Esta funcion compara el sexo de un usuario con el sexo buscado por el usuario actual
def comparar_sexos(usuario_2, criterios_de_busqueda):
    sexo = usuario_2[2]
    if criterios_de_busqueda[1] == 3 or criterios_de_busqueda[1] == sexo or sexo == "Indefinido":
        return True
    return False


#Esta funcion compara la edad de un usario con el rango de edades buscado por el usuario actual.
def comparar_edades(usuario_2, criterios_de_busqueda):
    edad = int(usuario_2[3])
    edad_min = criterios_de_busqueda[2][0]
    edad_max = criterios_de_busqueda[2][1]
    if edad_min <= edad <= edad_max:
        return True
    return False


#Esta funcion compara los intereses entre usuarios y calcula el porcentaje de interes.
def comparar_intereses(usuario_actual, usuario_2):
    intereses_en_comun = []
    for interes in usuario_actual[2]:
        if interes in usuario_2[4]:
            intereses_en_comun.append(interes)
    cant_intereses_1 = len(usuario_actual[2])
    cant_intereses_2 = len(usuario_2[4])
    porcentaje_de_interes = round(100*(len(intereses_en_comun)/(cant_intereses_1+cant_intereses_2)))
    return porcentaje_de_interes


# Esta funcion compara si el usuario contra el que se compara es el actual, y si no lo es, devuelve los datos
# que se necesitan en una lista.
def limpiar_usuarios(usuario_actual, user_2):
    user_2 = user_2.strip("\n").split(";")
    if usuario_actual[0] != user_2[2]:
        user_2 = [user_2[2], (user_2[6], user_2[7]), user_2[4], user_2[5], user_2[8].split(",")]
        return user_2
    return ""


# Esta funcion verifica si hay usuarios para seguir leyendo.
def seguir_leyendo_usuarios(usuario_actual, user_2):
    if user_2:
        user_2 = limpiar_usuarios(usuario_actual, user_2)
        return user_2, True
    return user_2, False


#Esta funcion busca entre los usuarios del sistema los que coinciden con los criterios del actual
# y devuelve un listado de coincidencias
def realizar_busqueda(usuario_actual):
    criterios_de_busqueda = datos_para_busqueda(usuario_actual)
    usuarios_precargados = open("usuarios_precargados.csv", "r")
    usuarios_nuevos = open("usuarios_nuevos.dat", "br")
    leer_precargados = leer_nuevos = True
    coincidencias = []
    while leer_precargados or leer_nuevos:
        if leer_precargados:
            user_2 = usuarios_precargados.readline()
            user_2, leer_precargados = seguir_leyendo_usuarios(usuario_actual, user_2)
        elif leer_nuevos:
            user_2 = leer_archivo_bin(usuarios_nuevos)
            user_2, leer_nuevos = seguir_leyendo_usuarios(usuario_actual, user_2)
        if user_2:
            seguir, distancia = comparar_distancias(usuario_actual, user_2, criterios_de_busqueda)
            if seguir:
                if comparar_sexos(user_2, criterios_de_busqueda):
                    if comparar_edades(user_2, criterios_de_busqueda):
                        intereses = comparar_intereses(usuario_actual, user_2)
                        coincidencias.append([user_2, distancia, intereses])
    if coincidencias:
        coincidencias.sort(key=lambda x: x[1])
    usuarios_precargados.close()
    usuarios_nuevos.close()
    return coincidencias


# Esta funcion busca si existe el usuario en el archivo de likes y mensajes
def recuperar_likes_y_mensajes(usuario):
    archivo = open("likes_y_mensajes.dat", "br")
    registro = leer_archivo_bin(archivo)
    # Antes decia: while registro or registro[0] == usuario:
    while registro and registro[0] != usuario:
        registro = leer_archivo_bin(archivo)
    archivo.close()
    return registro


# Esta funcion carga los likes y mensajes (si es que habia) del registro a novedades
def cargar_likes_y_mensajes(usuario, novedades):
    if usuario not in novedades:
        registro = recuperar_likes_y_mensajes(usuario)
        if registro:
            novedades[usuario] = registro
        else:
            novedades[usuario] = [usuario, {}, {}, 0]


#Esta funcion verifica si ha habido match entre usuarios, y solicita al actual que mande un mensaje
#a modo de saludo.
def mandar_primer_mensaje(usuario_actual, user_2, novedades):
    if user_2 not in novedades[usuario_actual][2]:
        print("\nFelicidades, @{} tambien te dio like, enviale un mensaje".format(user_2))
        mensaje = input("Mensaje: ")
        mensaje = "@"+usuario_actual+": "+mensaje+"\n"
        novedades[usuario_actual][2][user_2] = [False, mensaje]
        novedades[user_2][2][usuario_actual] = [True, mensaje]


# Esta funcion se fija si user_2 le habia dado like al usuario actual
def ver_si_hay_match(usuario_actual, user_2, novedades):
    if usuario_actual in novedades[user_2][1]:
        if novedades[usuario_actual][1][user_2] and novedades[user_2][1][usuario_actual]:
            mandar_primer_mensaje(usuario_actual, user_2, novedades)


#Esta funcion consulta al usuario si esta interesado o no en un usuario y lo agregar a sus Likes
def tomar_like_user(usuario_actual, user_2, novedades):
    interes = input("¿Estas interesado en este perfil?(S/N): ").upper()
    cargar_likes_y_mensajes(usuario_actual, novedades)
    if interes == "S":
        cargar_likes_y_mensajes(user_2, novedades)
        if user_2 not in novedades[usuario_actual][1]:
            novedades[user_2][3] += 1
        novedades[usuario_actual][1][user_2] = True
        ver_si_hay_match(usuario_actual, user_2, novedades)
    else:
        novedades[usuario_actual][1][user_2] = False


#Esta funcion pregunta al usuario si desea ver mas coincidencias o salir al menu principal.
def seguir_viendo_coincidencias(i, coincidencias):
    seguir = False
    if i < len(coincidencias) - 1:
        eleccion = int(input("\n¿Que desea hacer?\n1- Ver mas coincidencias\n2- Salir\n\nOpcion elegida: "))
        if eleccion == 1:
            seguir = True
            i += 1
    return i, seguir


#Esta funcion muestra las coincidencias que hubo al realizar una busqueda.
def mostrar_coincidencias(usuario_actual, coincidencias, novedades):
    seguir = True
    i = 0
    print("\nResultados de la busqueda:")
    if coincidencias != []:
        while(seguir):
            print("\nUsuario: @{}".format(coincidencias[i][0][0]))
            print("Edad: {} años".format(coincidencias[i][0][3]))
            print("Distancia: {} km".format(coincidencias[i][1]))
            print("Porcentaje de coincidencia: {}%\n".format(coincidencias[i][2]))
            tomar_like_user(usuario_actual, coincidencias[i][0][0], novedades)
            i, seguir = seguir_viendo_coincidencias(i, coincidencias)
    else:
        print("\nNingun usuario encontrado. Intente mas tarde.\n")

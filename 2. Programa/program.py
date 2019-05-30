from listar_usuarios import listar_usuarios
from cargar_usuario_nuevo import cargar_nuevo_usuario
from ingreso_y_busqueda import ingresar_a_sistema, realizar_busqueda, mostrar_coincidencias
from funciones_ver_mensajes import mostrar_mensajes
from top_5 import mostrar_top_5
from manejo_de_archivos import actualizar_likes_y_mensajes


# **************************************************************
# *------- Funciones correspondientes al Menu Principal ------ *
# **************************************************************

# Esta funcion muestra el menu principal cada vez que el usuario finalice una accion
def presentacion_menu_principal():
    print("╔═══════════════════════════════════════════════╗")
    print("║ »»»»»»»»»»»» Bienvenido a Tender «««««««««««« ║")
    print("╠═══════════════════════════════════════════════╣")
    print("║ ¿Que desea hacer?                             ║")
    print("║¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯║")
    print("║ 1- Imprimir usuarios registrados              ║")
    print("║ 2- Registrar nuevo usuario                    ║")
    print("║ 3- Ingresar al sistema                        ║")
    print("║ 4- Imprimir Top 5 usuarios                    ║")
    print("║ 5- Finalizar aplicación                       ║")
    print("║                                               ║")
    print("╚═══════════════════════════════════════════════╝")
    eleccion = int(input("»» Opcion elegida: "))
    return eleccion


# Esta funcion validara si la eleccion hecha por el usuario en el menu principal es correcta
def validar_menu_principal(eleccion):
    if(eleccion not in [1, 2, 3, 4, 5]):
        print("╔═══════════════════════════════════════════════╗")
        print("║*****Opcion invalida. Vuelva a intentarlo******║")
        print("╚═══════════════════════════════════════════════╝")
        return True
    return False


# Esta funcion llama a las funciones necesarias para ejecutar el menu principal
def menu_principal():
    seguir = True
    while(seguir):
        eleccion = presentacion_menu_principal()
        seguir = validar_menu_principal(eleccion)
    return eleccion


# ********************************************************************************
# * -----------------------Cuerpo principal del programa ----------------------- *
# ********************************************************************************

# Defino una biblioteca donde ire guardando las modificaciones que se hagan a los likes y mensajes
novedades = {}

eleccion = menu_principal()
while(eleccion != 5):
    # Listar usuarios de base de datos
    if eleccion == 1:
        listar_usuarios()
    # Carga de nuevo usuario.
    elif eleccion == 2:
        cargar_nuevo_usuario()
    # Busqueda entre usuarios.
    elif eleccion == 3:
            usuario_actual = ingresar_a_sistema()
            coincidencias = realizar_busqueda(usuario_actual)
            mostrar_mensajes(usuario_actual[0], novedades)
            mostrar_coincidencias(usuario_actual[0], coincidencias, novedades)
    # Mostrar top 5
    else:
        if novedades != {}:
            actualizar_likes_y_mensajes(novedades)
        mostrar_top_5()
    eleccion = menu_principal()
if novedades != {}:
    actualizar_likes_y_mensajes(novedades)
print("\nFin del programa")

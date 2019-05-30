from ingreso_y_busqueda import recuperar_likes_y_mensajes

# Esta funcion se encarga de verificar si el usuario desea contestar un mensaje recibido o no (**)
def contestar_mensajes(usuario_actual, user_2, novedades):
    contestar = input("¿Deseas contestar? (S/N): ").upper()
    if contestar == "S":
        mensajes_anteriores = novedades[usuario_actual][2][user_2][1]
        nuevo_mensaje = input("Mensaje: ")
        nuevo_mensaje = mensajes_anteriores + "@"+usuario_actual+": "+nuevo_mensaje+"\n"
        novedades[usuario_actual][2][user_2] = [False, nuevo_mensaje]
        if user_2 not in novedades:
            registro = recuperar_likes_y_mensajes(user_2)
            novedades[user_2] = registro
        novedades[user_2][2][usuario_actual] = [True, nuevo_mensaje]


# Esta funcion muestra los mensajes que los usuarios se enviaron entre si cuando hay mensajes nuevos. (**)
def mostrar_mensajes(usuario_actual, novedades):
    if usuario_actual not in novedades:
        registro = recuperar_likes_y_mensajes(usuario_actual)
        if registro:
            novedades[usuario_actual] = registro
    if usuario_actual in novedades:
        for user_2 in novedades[usuario_actual][2]:
            if novedades[usuario_actual][2][user_2][0]:
                print("\nTienes mensajes sin leer de @{}\n".format(user_2))
                print(novedades[usuario_actual][2][user_2][1])
                novedades[usuario_actual][2][user_2][0] = False
                contestar_mensajes(usuario_actual, user_2, novedades)

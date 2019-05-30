from manejo_de_archivos import *


def limpiar_top_5(top_5):
    if top_5 == [("", 0), ("", 0), ("", 0), ("", 0), ("", 0)]:
        return []
    else:
        nuevo_top = []
        for tupla in top_5:
            if tupla[1] != 0:
                nuevo_top.append(tupla)
        return nuevo_top


def buscar_top_5():
    top_5 = [("", 0), ("", 0), ("", 0), ("", 0), ("", 0)]
    # Obtengo mi top 5
    archivo = open("likes_y_mensajes.dat", "br")
    registro = leer_archivo_bin(archivo)
    while registro:
        i = 0
        while registro[3] != 0 and i < 5 and registro[3] > top_5[i][1]:
            if i != 0:
                top_5[i - 1] = top_5[i]
            top_5[i] = (registro[0], registro[3])
            i += 1
        registro = leer_archivo_bin(archivo)
    archivo.close()
    return limpiar_top_5(top_5)


# Mostrar TOP 5
def mostrar_top_5():
    top_5 = buscar_top_5()
    print("\n╔═══════════════════════════════════════════════╗")
    print("║ »»»»»»»»»»»»»»»»» TOP  FIVE ««««««««««««««««« ║")
    if not top_5:
        print("╠═══════════════════════════════════════════════╣")
        print("║ »»»»»»»»»»» Aún nadie recibio likes ««««««««« ║")
        print("╚═══════════════════════════════════════════════╝\n")
    else:
        print("╚═══════════════════════════════════════════════╝\n")
        for i in range(1, len(top_5)+1):
            print("{}- @{} recibio {} likes".format(i, top_5[-i][0], top_5[-i][1]))
        print()

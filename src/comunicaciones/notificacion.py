# Clase de notificación

class Notificacion:
    def __init__(self, id_notificacion, mensaje):
        self.__id_notificacion = id_notificacion
        self.__mensaje = mensaje
        self.__leida = False

    def enviar(self):
        print("Notificacion enviada")

    def marcar_como_leida(self):
        self.__leida = True
        print("Notificacion marcada como leida")

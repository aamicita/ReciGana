# Clase de notificación

class Notificacion:
    def __init__(self, id_notificacion, mensaje):
        self.__id_notificacion = id_notificacion
        self.__mensaje = mensaje
        self.__leida = False

    @property
    def id_notificacion(self):
        return self.__id_notificacion

    @property
    def mensaje(self):
        return self.__mensaje

    @property
    def leida(self):
        return self.__leida

    def enviar(self):
        print("Notificacion enviada")

    def marcar_como_leida(self):
        self.__leida = True
        print("Notificacion marcada como leida")

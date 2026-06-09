# Clase de calificación

class Calificacion:
    def __init__(self, id_calificacion, puntaje, comentario):
        self.__id_calificacion = id_calificacion
        self.__puntaje = puntaje
        self.__comentario = comentario

    @property
    def id_calificacion(self):
        return self.__id_calificacion

    @property
    def puntaje(self):
        return self.__puntaje

    @property
    def comentario(self):
        return self.__comentario

    def registrar_calificacion(self):
        print("Calificacion registrada")

    def consultar_calificaciones(self):
        print("Consultando calificaciones")
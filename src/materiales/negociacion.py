# Clase de negociación

class Negociacion:
    def __init__(self, id_negociacion, precio_final, estado, fecha_inicio, fecha_cierre=None):
        self.__id_negociacion = id_negociacion
        self.__precio_final = precio_final
        self.__estado = estado
        self.__fecha_inicio = fecha_inicio
        self.__fecha_cierre = fecha_cierre

    def iniciar_negociacion(self):
        self.__estado = "iniciada"
        print("Negociacion iniciada")

    # Sobrecarga simulada con parametro por defecto
    def proponer_contra_oferta(self, nuevo_precio=None):
        if nuevo_precio is None:
            print("Contra oferta propuesta")
        else:
            self.__precio_final = nuevo_precio
            print("Contra oferta propuesta con nuevo precio")

    def finalizar_negociacion(self):
        self.__estado = "finalizada"
        print("Negociacion finalizada")

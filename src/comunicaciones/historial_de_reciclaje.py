# Clase de historial de reciclaje

class HistorialDeReciclaje:
    # Inyectar la dependencia 'registros' en el constructor

    def __init__(self, id_historial, registros=None):
        self.__id_historial = id_historial
        # Si no pasan nada, entonces empieza con una lista vacia
        self.__registros = registros if registros is not None else []

    def consultar_historial(self):
        print(f"Consultando historial {self.__id_historial}")
        if not self.__registros:
            print("No hay registros en el historial")
            return
        # Ahora el metodo
        for registro in self.__registros:
            print(registro)

    def filtrar_por_fecha(self, fecha):
        print(f"Filtrando historial por fecha {fecha}")

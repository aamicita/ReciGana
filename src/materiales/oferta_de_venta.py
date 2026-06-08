# Clase de oferta de venta

class OfertaDeVenta:
    def __init__(self, id_oferta, precio_propuesto, estado):
        self.__id_oferta = id_oferta
        self.__precio_propuesto = precio_propuesto
        self.__estado = estado

    @property
    def id_oferta(self):
        return self.__id_oferta

    @property
    def precio_propuesto(self):
        return self.__precio_propuesto

    @precio_propuesto.setter
    def precio_propuesto(self, valor):
        if valor >= 0:
            self.__precio_propuesto = valor

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, valor):
        if valor:
            self.__estado = valor

    # Sobrecarga simulada con parametro por defecto
    def crear_oferta(self, descripcion=None):
        if descripcion:
            print(f"Oferta creada: {descripcion}")
        else:
            print("Oferta creada")

    def cerrar_oferta(self):
        self.__estado = "cerrada"
        print("Oferta cerrada")

    def modificar_oferta(self, nuevo_precio):
        self.__precio_propuesto = nuevo_precio
        print("Oferta modificada")

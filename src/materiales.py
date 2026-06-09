# Clases operativas de materiales y ofertas

class MaterialReciclable:
    def __init__(self, id_material, tipo_material, cantidad, peso, estado):
        # Encapsulamiento: atributos privados
        self.__id_material = id_material
        self.__tipo_material = tipo_material
        self.__cantidad = cantidad
        self.__peso = peso
        self.__estado = estado

    @property
    def id_material(self):
        return self.__id_material

    @property
    def tipo_material(self):
        return self.__tipo_material

    @property
    def cantidad(self):
        return self.__cantidad

    @property
    def peso(self):
        return self.__peso

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, valor):
        if valor:
            self.__estado = valor

    def clasificar(self):
        print("Material clasificado")

    # Sobrecarga simulada con parametro por defecto
    def calcular_valor(self, precio_por_kg=None):
        if precio_por_kg is None:
            return 0
        return self.__peso * precio_por_kg


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


class Negociacion:
    def __init__(self, id_negociacion, precio_final, estado, fecha_inicio, fecha_cierre=None):
        self.__id_negociacion = id_negociacion
        self.__precio_final = precio_final
        self.__estado = estado
        self.__fecha_inicio = fecha_inicio
        self.__fecha_cierre = fecha_cierre

    @property
    def id_negociacion(self):
        return self.__id_negociacion

    @property
    def precio_final(self):
        return self.__precio_final

    @property
    def estado(self):
        return self.__estado

    @property
    def fecha_inicio(self):
        return self.__fecha_inicio

    @property
    def fecha_cierre(self):
        return self.__fecha_cierre

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
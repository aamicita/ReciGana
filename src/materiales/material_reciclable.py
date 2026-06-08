# Clase de material reciclable

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

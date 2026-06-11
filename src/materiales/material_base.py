from abc import ABC, abstractmethod


class MaterialBase(ABC):

    ESTADOS_VALIDOS = {"disponible", "en_negociacion", "vendido"}

    def __init__(self, id_material, cantidad, peso, estado="disponible"):
        self.__id_material = id_material

        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("La cantidad debe ser un entero mayor a cero.")
        self.__cantidad = cantidad

        if not isinstance(peso, (int, float)) or peso <= 0:
            raise ValueError("El peso debe ser un numero mayor a cero.")
        self.__peso = float(peso)

        if estado not in self.ESTADOS_VALIDOS:
            raise ValueError("Estado invalido.")
        self.__estado = estado

    @property
    def id_material(self):
        return self.__id_material

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
        if valor not in self.ESTADOS_VALIDOS:
            raise ValueError("Estado invalido.")
        self.__estado = valor

    @abstractmethod
    def get_tipo(self) -> str:
        pass

    @abstractmethod
    def clasificar(self) -> str:
        pass

    @abstractmethod
    def calcular_valor(self, precio_por_kg: float = None) -> float:
        pass

    def __str__(self) -> str:
        return (
            f"Material #{self.id_material} | "
            f"Tipo: {self.get_tipo()} | "
            f"Peso: {self.peso} kg | "
            f"Estado: {self.estado}"
        )

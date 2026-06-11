from abc import ABC, abstractmethod


class MaterialBase(ABC):

    # ======================================================
    # CONSTANTE DE CLASE
    # ======================================================
    # Conjunto de estados permitidos para un material.
    #
    # Se declara como constante porque todos los materiales
    # comparten exactamente los mismos estados.
    #
    # Usar un conjunto (set) permite búsquedas rápidas.
    # ======================================================
    ESTADOS_VALIDOS = {"disponible", "en_negociacion", "vendido"}

    # ======================================================
    # CONSTRUCTOR
    # ======================================================
    # Inicializa los atributos comunes a todos los materiales.
    #
    # Se aplican validaciones para garantizar la integridad
    # de los datos desde el momento de la creación.
    # ======================================================
    def __init__(self, id_material, cantidad, peso, estado="disponible"):

        # Identificador único del material.
        self.__id_material = id_material

        # Validación de cantidad
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError(
                "La cantidad debe ser un entero mayor a cero."
            )

        self.__cantidad = cantidad

        # Validación de peso
        if not isinstance(peso, (int, float)) or peso <= 0:
            raise ValueError(
                "El peso debe ser un número mayor a cero."
            )

        self.__peso = float(peso)

        # Validación de estado
        if estado not in self.ESTADOS_VALIDOS:
            raise ValueError(
                f"Estado inválido. Use: {self.ESTADOS_VALIDOS}"
            )

        self.__estado = estado

    # ======================================================
    # PROPIEDADES (GETTERS)
    # ======================================================

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

    # ======================================================
    # SETTER DE ESTADO
    # ======================================================

    @estado.setter
    def estado(self, valor):

        if valor not in self.ESTADOS_VALIDOS:
            raise ValueError(
                f"Estado inválido. Use: {self.ESTADOS_VALIDOS}"
            )

        self.__estado = valor

    # ======================================================
    # MÉTODOS ABSTRACTOS
    # ======================================================

    @abstractmethod
    def clasificar(self) -> str:
        pass

    @abstractmethod
    def calcular_valor(self, precio_por_kg: float) -> float:
        pass

    @abstractmethod
    def get_tipo(self) -> str:
        pass

    # ======================================================
    # REPRESENTACIÓN EN TEXTO
    # ======================================================

    def __str__(self) -> str:

        return (
            f"Material #{self.id_material} | "
            f"Tipo: {self.get_tipo()} | "
            f"Peso: {self.peso} kg | "
            f"Estado: {self.estado}"
        )
    
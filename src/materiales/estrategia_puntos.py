from abc import ABC, abstractmethod


class EstrategiaPuntos(ABC):
    """
    PATRON STRATEGY — clase base abstracta.
    Define el contrato que todas las estrategias deben cumplir.
    Cada estrategia calcula puntos de forma diferente.
    """

    @abstractmethod
    def calcular_puntos(self, peso: float) -> int:
        """Recibe el peso en kg y retorna los puntos ganados."""
        pass


class PuntosEstandar(EstrategiaPuntos):
    """
    Estrategia estandar: 10 puntos por kg.
    Se aplica a plastico, papel y carton.
    """
    PUNTOS_POR_KG = 10

    def calcular_puntos(self, peso: float) -> int:
        puntos = int(peso * self.PUNTOS_POR_KG)
        print(f"Estrategia estandar: {peso} kg x {self.PUNTOS_POR_KG} = {puntos} puntos")
        return puntos


class PuntosEspecial(EstrategiaPuntos):
    """
    Estrategia especial: 20 puntos por kg.
    Se aplica a metal y vidrio por su mayor valor de reciclaje.
    """
    PUNTOS_POR_KG = 20

    def calcular_puntos(self, peso: float) -> int:
        puntos = int(peso * self.PUNTOS_POR_KG)
        print(f"Estrategia especial: {peso} kg x {self.PUNTOS_POR_KG} = {puntos} puntos")
        return puntos


class PuntosOrganico(EstrategiaPuntos):
    """
    Estrategia organico: 5 puntos por kg.
    Se aplica a material organico y biodegradable.
    """
    PUNTOS_POR_KG = 5

    def calcular_puntos(self, peso: float) -> int:
        puntos = int(peso * self.PUNTOS_POR_KG)
        print(f"Estrategia organico: {peso} kg x {self.PUNTOS_POR_KG} = {puntos} puntos")
        return puntos


class CalculadorPuntos:
    """
    Contexto del patron Strategy.
    El ciudadano usa esta clase para calcular sus puntos.
    La estrategia se puede cambiar en cualquier momento
    sin modificar el codigo del ciudadano.

    Uso:
        calc = CalculadorPuntos(PuntosEspecial())
        calc.calcular(5.0)   ->  100 puntos

        calc.cambiar_estrategia(PuntosEstandar())
        calc.calcular(5.0)   ->  50 puntos
    """

    def __init__(self, estrategia: EstrategiaPuntos):
        self.__estrategia = estrategia

    def cambiar_estrategia(self, estrategia: EstrategiaPuntos):
        """Permite cambiar la estrategia en tiempo de ejecucion."""
        self.__estrategia = estrategia
        print(f"Estrategia cambiada a: {estrategia.__class__.__name__}")

    def calcular(self, peso: float) -> int:
        """Delega el calculo a la estrategia activa."""
        return self.__estrategia.calcular_puntos(peso)

    @staticmethod
    def para_material(tipo: str):
        """
        Fabrica rapida: recibe el tipo de material
        y devuelve el CalculadorPuntos con la estrategia correcta.

        Uso:
            calc = CalculadorPuntos.para_material("metal")
            calc.calcular(3.0)  ->  60 puntos
        """
        tipo = tipo.lower()
        if tipo in {"metal", "vidrio"}:
            return CalculadorPuntos(PuntosEspecial())
        elif tipo in {"organico"}:
            return CalculadorPuntos(PuntosOrganico())
        else:
            return CalculadorPuntos(PuntosEstandar())

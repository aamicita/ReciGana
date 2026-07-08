# materiales/plastico.py
from .material_base import MaterialBase


class Plastico(MaterialBase):
    """
    Material reciclable: plástico.
    Categoría: Reciclable seco.
    """

    PRECIO_BASE = 0.50

    @classmethod
    def cambiar_precio_base(cls, nuevo_precio: float):
        if not isinstance(nuevo_precio, (int, float)) or nuevo_precio <= 0:
            raise ValueError("El precio debe ser mayor a cero.")
        cls.PRECIO_BASE = nuevo_precio

    def get_tipo(self) -> str:
        return "plastico"

    def clasificar(self) -> str:
        categoria = "Reciclable seco"
        print(f"Material 'plastico' clasificado como: {categoria}")
        return categoria

    def calcular_valor(self, precio_por_kg: float = None) -> float:
        """
        SOBRECARGA SIMULADA 
        Python no permite dos métodos con el mismo nombre y distinta
        firma como en Java. Para lograr un efecto parecido, usamos un
        parámetro con valor por defecto:
            material.calcular_valor()      -> usa el precio base
            material.calcular_valor(0.50)  -> usa el precio que le pases
        Las demás clases de material (Vidrio, Metal, Papel, Cartón,
        Orgánico) siguen exactamente este mismo patrón.
        """
        precio = precio_por_kg if precio_por_kg else self.PRECIO_BASE

        if not isinstance(precio, (int, float)) or precio <= 0:
            raise ValueError("El precio por kg debe ser mayor a cero.")

        valor_total = self.peso * precio
        print(f"Plástico: {self.peso} kg × ${precio} = ${valor_total:.2f}")
        return valor_total
# materiales/papel.py
from .material_base import MaterialBase


class Papel(MaterialBase):
    """
    Material reciclable: papel.
    Categoría: Reciclable seco.
    El papel tiene el precio base más bajo entre los secos.
    """

    PRECIO_BASE = 0.15

    @classmethod
    def cambiar_precio_base(cls, nuevo_precio: float):
        if not isinstance(nuevo_precio, (int, float)) or nuevo_precio <= 0:
            raise ValueError("El precio debe ser mayor a cero.")
        cls.PRECIO_BASE = nuevo_precio
        
    def get_tipo(self) -> str:
        return "papel"

    def clasificar(self) -> str:
        categoria = "Reciclable seco"
        print(f"Material 'papel' clasificado como: {categoria}")
        return categoria

    def calcular_valor(self, precio_por_kg: float = None) -> float:
        precio = precio_por_kg if precio_por_kg else self.PRECIO_BASE

        if not isinstance(precio, (int, float)) or precio <= 0:
            raise ValueError("El precio por kg debe ser mayor a cero.")

        valor_total = self.peso * precio
        print(f"Papel: {self.peso} kg × ${precio} = ${valor_total:.2f}")
        return valor_total
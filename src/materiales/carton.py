# materiales/carton.py
from .material_base import MaterialBase


class Carton(MaterialBase):
    """
    Material reciclable: cartón.
    Categoría: Reciclable seco.
    Similar al papel pero con precio levemente mayor.
    """

    PRECIO_BASE = 0.25

    def get_tipo(self) -> str:
        return "carton"

    def clasificar(self) -> str:
        categoria = "Reciclable seco"
        print(f"Material 'carton' clasificado como: {categoria}")
        return categoria

    def calcular_valor(self, precio_por_kg: float = None) -> float:
        precio = precio_por_kg if precio_por_kg else self.PRECIO_BASE

        if not isinstance(precio, (int, float)) or precio <= 0:
            raise ValueError("El precio por kg debe ser mayor a cero.")

        valor_total = self.peso * precio
        print(f"Cartón: {self.peso} kg × ${precio} = ${valor_total:.2f}")
        return valor_total
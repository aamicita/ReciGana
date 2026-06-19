# materiales/organico.py
# OJO: este es diferente — su categoría es "Biodegradable"
from .material_base import MaterialBase


class Organico(MaterialBase):
    """
    Material reciclable: orgánico.
    Categoría: Biodegradable  ← DIFERENTE a los demás.
    """

    PRECIO_BASE = 0.10  

    @classmethod
    def cambiar_precio_base(cls, nuevo_precio: float):
        if not isinstance(nuevo_precio, (int, float)) or nuevo_precio <= 0:
            raise ValueError("El precio debe ser mayor a cero.")
        cls.PRECIO_BASE = nuevo_precio
        
    def get_tipo(self) -> str:
        return "organico"

    def clasificar(self) -> str:
        # ← ÚNICO que retorna "Biodegradable"
        categoria = "Biodegradable"
        print(f"Material 'organico' clasificado como: {categoria}")
        return categoria

    def calcular_valor(self, precio_por_kg: float = None) -> float:
        precio = precio_por_kg if precio_por_kg else self.PRECIO_BASE

        if not isinstance(precio, (int, float)) or precio <= 0:
            raise ValueError("El precio por kg debe ser mayor a cero.")

        valor_total = self.peso * precio
        print(f"Orgánico: {self.peso} kg × ${precio} = ${valor_total:.2f}")
        return valor_total
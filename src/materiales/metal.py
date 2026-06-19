from .material_base import MaterialBase

class Metal(MaterialBase):
    """
    Material reciclable: metal.
    Categoría: Reciclable seco.
    El metal tiene el precio base más alto por kg.
    """

    PRECIO_BASE = 1.20  # El metal vale más que otros materiales

    @classmethod
    def cambiar_precio_base(cls, nuevo_precio: float):
        if not isinstance(nuevo_precio, (int, float)) or nuevo_precio <= 0:
            raise ValueError("El precio debe ser mayor a cero.")
        cls.PRECIO_BASE = nuevo_precio

        
    def get_tipo(self) -> str:
        return "metal"

    def clasificar(self) -> str:
        categoria = "Reciclable seco"
        print(f"Material 'metal' clasificado como: {categoria}")
        return categoria

    def calcular_valor(self, precio_por_kg: float = None) -> float:
        precio = precio_por_kg if precio_por_kg else self.PRECIO_BASE

        if not isinstance(precio, (int, float)) or precio <= 0:
            raise ValueError("El precio por kg debe ser mayor a cero.")

        valor_total = self.peso * precio
        print(f"Metal: {self.peso} kg × ${precio} = ${valor_total:.2f}")
        return valor_total
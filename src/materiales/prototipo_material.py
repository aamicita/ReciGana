# Patrón Prototype — Clonación de materiales
# Archivo: modelos/materiales/prototipo_material.py

import copy


class PrototipoMaterial:
    """
    Patrón Prototype aplicado a materiales reciclables.

    Problema que resuelve:
    Si un ciudadano siempre publica el mismo material
    (por ejemplo, siempre vende 10 kg de cartón cada semana),
    en vez de crear ese objeto desde cero con todos sus datos,
    puede CLONAR el material anterior y solo cambiar lo que
    sea diferente (por ejemplo, el peso o el estado).

    Ejemplo de uso:
        original = PrototipoMaterial("cartón", 10, "disponible")
        clon = original.clonar()
        clon.peso_kg = 15   # Solo cambiamos el peso
    """

    def __init__(self, tipo, peso_kg, estado="disponible", foto=None, descripcion=""):
        self.tipo        = tipo
        self.peso_kg     = peso_kg
        self.estado      = estado
        self.foto        = foto
        self.descripcion = descripcion

    def clonar(self):
        """
        Crea y retorna una copia INDEPENDIENTE de este material.
        Usamos copy.deepcopy para que el clon no comparta
        referencias con el original.
        """
        clon = copy.deepcopy(self)
        # El clon siempre empieza como disponible
        clon.estado = "disponible"
        print(f"[Prototype] Material clonado: {self.tipo}, {self.peso_kg} kg")
        return clon

    def __str__(self):
        return (
            f"Material [{self.estado}] → "
            f"{self.tipo} | {self.peso_kg} kg | "
            f"Foto: {self.foto or 'sin foto'}"
        )
# src/materiales/__init__.py
from .material_base       import MaterialBase
from .plastico            import Plastico
from .vidrio              import Vidrio
from .metal               import Metal
from .papel               import Papel
from .carton              import Carton
from .organico            import Organico
from .fabrica_materiales  import FabricaMateriales

__all__ = [
    "MaterialBase",
    "Plastico",
    "Vidrio",
    "Metal",
    "Papel",
    "Carton",
    "Organico",
    "FabricaMateriales",
]
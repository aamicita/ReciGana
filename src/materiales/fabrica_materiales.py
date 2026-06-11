from .material_base  import MaterialBase
from .plastico       import Plastico
from .vidrio         import Vidrio
from .metal          import Metal
from .papel          import Papel
from .carton         import Carton
from .organico       import Organico

class FabricaMateriales:
    """
    FACTORY METHOD — decide qué clase crear según el tipo.
    En vez de hacer: m = Plastico(...)  o  m = Vidrio(...)
    Siempre haces:   m = FabricaMateriales.crear("plastico", ...)
    """

    _REGISTRO = {
        "plastico": Plastico,
        "vidrio":   Vidrio,
        "metal":    Metal,
        "papel":    Papel,
        "carton":   Carton,
        "organico": Organico,
    }

    @staticmethod
    def crear(tipo: str, id_material, cantidad: int,
              peso: float, estado: str = "disponible") -> MaterialBase:
        """
        Crea y devuelve el material correcto según el tipo.
        Ejemplo: FabricaMateriales.crear("metal", 1, 2, 5.0)
        """
        tipo_lower = tipo.lower()
        clase = FabricaMateriales._REGISTRO.get(tipo_lower)

        if clase is None:
            tipos_validos = list(FabricaMateriales._REGISTRO.keys())
            raise ValueError(
                f"Tipo '{tipo}' no reconocido. "
                f"Tipos válidos: {tipos_validos}"
            )

        return clase(id_material, cantidad, peso, estado)

    @staticmethod
    def tipos_disponibles() -> list:
        """Devuelve la lista de tipos registrados."""
        return list(FabricaMateriales._REGISTRO.keys())
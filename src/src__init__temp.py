# __init__ principal del sistema ReciGana
# Aqui se exportan todas las clases disponibles del sistema
 
from .usuarios import Administrador, Ciudadano, Reciclador, Usuarios
from .usuarios import GestorSistema
from .usuarios import FabricaUsuariosBase, FabricaUsuariosManta
from .materiales import FabricaMateriales, MaterialBase
from .materiales.negociacion import Negociacion
from .materiales.oferta_de_venta import OfertaDeVenta
from .materiales.prototipo_material import PrototipoMaterial
from .materiales.constructor_oferta import OfertaVentaBuilder
from .comunicaciones import (
    Notificacion,
    Reporte,
    HistorialDeReciclaje,
    Calificacion,
    ReporteBuilder,
)
 
# NUEVO: importamos la Facade para que sea accesible desde el paquete raiz.
# Ahora cualquier archivo se puede hacer simplemente:

# en lugar de importar cada clase por separado.
from .facade_recigana import ReciGanaFacade
 
__all__ = [
    "Usuarios", "Administrador", "Ciudadano", "Reciclador",
    "GestorSistema",
    "FabricaUsuariosBase", "FabricaUsuariosManta",
    "MaterialBase", "FabricaMateriales",
    "OfertaDeVenta", "Negociacion",
    "PrototipoMaterial", "OfertaVentaBuilder",
    "Notificacion", "Reporte", "HistorialDeReciclaje",
    "Calificacion", "ReporteBuilder",
    # NUEVO: la Facade queda disponible como parte del paquete
    "ReciGanaFacade",
]
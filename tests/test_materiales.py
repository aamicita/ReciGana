import sys
import os
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.materiales.fabrica_materiales import FabricaMateriales
from src.materiales.plastico           import Plastico
from src.materiales.vidrio             import Vidrio
from src.materiales.metal              import Metal
from src.materiales.papel              import Papel
from src.materiales.carton             import Carton
from src.materiales.organico           import Organico
from src.materiales.negociacion        import Negociacion
from src.materiales.oferta_de_venta    import OfertaDeVenta


# ─────────────────────────────────────────
# Tests de Negociacion (sin cambios)
# ─────────────────────────────────────────

def test_negociacion_atributos():
    n = Negociacion("N1", 100.0, "pendiente", "2024-01-01")
    assert n.id_negociacion == "N1"
    assert n.precio_final == 100.0
    assert n.estado == "pendiente"
    assert n.fecha_inicio == "2024-01-01"
    assert n.fecha_cierre is None

def test_negociacion_iniciar():
    n = Negociacion("N2", 200.0, "pendiente", "2024-01-01")
    n.iniciar_negociacion()
    assert n.estado == "iniciada"

def test_negociacion_finalizar():
    n = Negociacion("N3", 300.0, "iniciada", "2024-01-01")
    n.finalizar_negociacion()
    assert n.estado == "finalizada"

def test_negociacion_contra_oferta():
    n = Negociacion("N4", 100.0, "iniciada", "2024-01-01")
    n.proponer_contra_oferta(150.0)
    assert n.precio_final == 150.0


# ─────────────────────────────────────────
# Tests de OfertaDeVenta (sin cambios)
# ─────────────────────────────────────────

def test_oferta_atributos():
    o = OfertaDeVenta("O1", 50.0, "pendiente")
    assert o.id_oferta == "O1"
    assert o.precio_propuesto == 50.0
    assert o.estado == "pendiente"

def test_oferta_cerrar():
    o = OfertaDeVenta("O2", 75.0, "pendiente")
    o.cerrar_oferta()
    assert o.estado == "cerrada"


# ─────────────────────────────────────────
# Tests de clases concretas de materiales
# ─────────────────────────────────────────

def test_plastico_atributos():
    m = Plastico("M1", 10, 5.0)
    assert m.id_material == "M1"
    assert m.get_tipo() == "plastico"
    assert m.cantidad == 10
    assert m.peso == 5.0
    assert m.estado == "disponible"

def test_plastico_clasificar():
    m = Plastico("M2", 3, 2.0)
    assert m.clasificar() == "Reciclable seco"

def test_plastico_calcular_valor_precio_base():
    m = Plastico("M3", 1, 4.0)
    assert m.calcular_valor() == 4.0 * Plastico.PRECIO_BASE

def test_plastico_calcular_valor_precio_custom():
    m = Plastico("M4", 1, 4.0)
    assert m.calcular_valor(1.0) == 4.0

def test_vidrio_tipo_y_categoria():
    m = Vidrio("M5", 2, 3.0)
    assert m.get_tipo() == "vidrio"
    assert m.clasificar() == "Reciclable seco"

def test_metal_precio_base_alto():
    m = Metal("M6", 1, 2.0)
    assert m.get_tipo() == "metal"
    assert m.calcular_valor() == 2.0 * Metal.PRECIO_BASE

def test_papel_tipo_y_categoria():
    m = Papel("M7", 5, 1.5)
    assert m.get_tipo() == "papel"
    assert m.clasificar() == "Reciclable seco"

def test_carton_calcular_valor():
    m = Carton("M8", 2, 3.0)
    assert m.calcular_valor() == 3.0 * Carton.PRECIO_BASE

def test_organico_categoria_diferente():
    m = Organico("M9", 4, 2.5)
    assert m.get_tipo() == "organico"
    assert m.clasificar() == "Biodegradable"

def test_organico_calcular_valor():
    m = Organico("M10", 1, 5.0)
    assert m.calcular_valor() == 5.0 * Organico.PRECIO_BASE


# ─────────────────────────────────────────
# Tests de FabricaMateriales
# ─────────────────────────────────────────

def test_fabrica_crea_plastico():
    m = FabricaMateriales.crear("plastico", 1, 3, 2.5)
    assert isinstance(m, Plastico)
    assert m.get_tipo() == "plastico"

def test_fabrica_crea_vidrio():
    m = FabricaMateriales.crear("vidrio", 2, 1, 1.0)
    assert isinstance(m, Vidrio)

def test_fabrica_crea_metal():
    m = FabricaMateriales.crear("metal", 3, 2, 5.0)
    assert isinstance(m, Metal)

def test_fabrica_crea_papel():
    m = FabricaMateriales.crear("papel", 4, 4, 3.0)
    assert isinstance(m, Papel)

def test_fabrica_crea_carton():
    m = FabricaMateriales.crear("carton", 5, 2, 2.0)
    assert isinstance(m, Carton)

def test_fabrica_crea_organico():
    m = FabricaMateriales.crear("organico", 6, 5, 4.5)
    assert isinstance(m, Organico)

def test_fabrica_tipo_mayusculas():
    m = FabricaMateriales.crear("PLASTICO", 7, 1, 1.0)
    assert isinstance(m, Plastico)

def test_fabrica_tipo_invalido():
    with pytest.raises(ValueError):
        FabricaMateriales.crear("madera", 99, 1, 1.0)

def test_fabrica_tipos_disponibles():
    tipos = FabricaMateriales.tipos_disponibles()
    assert "plastico" in tipos
    assert "vidrio"   in tipos
    assert "metal"    in tipos
    assert "papel"    in tipos
    assert "carton"   in tipos
    assert "organico" in tipos

def test_fabrica_estado_personalizado():
    m = FabricaMateriales.crear("metal", 8, 1, 3.0, "vendido")
    assert m.estado == "vendido"

def test_material_str():
    m = FabricaMateriales.crear("plastico", 1, 2, 3.0)
    resultado = str(m)
    assert "plastico" in resultado
    assert "3.0"      in resultado
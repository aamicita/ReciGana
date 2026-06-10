import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from materiales.negociacion import Negociacion
from materiales.material_reciclable import MaterialReciclable
from materiales.oferta_de_venta import OfertaDeVenta

# Tests de Negociacion
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

# Tests de MaterialReciclable
def test_material_atributos():
    m = MaterialReciclable("M1", "plastico", 10, 5.0, "disponible")
    assert m.id_material == "M1"
    assert m.tipo_material == "plastico"
    assert m.cantidad == 10
    assert m.peso == 5.0
    assert m.estado == "disponible"

def test_material_calcular_valor():
    m = MaterialReciclable("M2", "metal", 5, 10.0, "disponible")
    assert m.calcular_valor() == 0
    assert m.calcular_valor(2.5) == 25.0

# Tests de OfertaDeVenta — usamos "pendiente" que es el estado válido
def test_oferta_atributos():
    o = OfertaDeVenta("O1", 50.0, "pendiente")
    assert o.id_oferta == "O1"
    assert o.precio_propuesto == 50.0
    assert o.estado == "pendiente"

def test_oferta_cerrar():
    o = OfertaDeVenta("O2", 75.0, "pendiente")
    o.cerrar_oferta()
    assert o.estado == "cerrada"
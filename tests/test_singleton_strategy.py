import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.usuarios.gestor_sistema import GestorSistema
from src.materiales.estrategia_puntos import (
    CalculadorPuntos, PuntosEstandar, PuntosEspecial, PuntosOrganico
)
from src.usuarios.ciudadano import Ciudadano
from src.materiales.fabrica_materiales import FabricaMateriales


# ─────────────────────────────────────────
# Tests de Singleton
# ─────────────────────────────────────────

def setup_function():
    GestorSistema.resetear()

def test_singleton_misma_instancia():
    g1 = GestorSistema.obtener_instancia()
    g2 = GestorSistema.obtener_instancia()
    assert g1 is g2

def test_singleton_tres_llamadas_misma_instancia():
    g1 = GestorSistema.obtener_instancia()
    g2 = GestorSistema.obtener_instancia()
    g3 = GestorSistema.obtener_instancia()
    assert g1 is g2 is g3

def test_singleton_datos_compartidos():
    g1 = GestorSistema.obtener_instancia()
    c = Ciudadano(1, "Ana", "0991234567", "ana@mail.com", "pass123", "Av. 10")
    g1.registrar_usuario(c)
    g2 = GestorSistema.obtener_instancia()
    assert len(g2.obtener_usuarios()) == 1

def test_singleton_registrar_usuario():
    g = GestorSistema.obtener_instancia()
    c = Ciudadano(1, "Ana", "0991234567", "ana@mail.com", "pass123", "Av. 10")
    g.registrar_usuario(c)
    assert len(g.obtener_usuarios()) == 1

def test_singleton_registrar_material():
    g = GestorSistema.obtener_instancia()
    m = FabricaMateriales.crear("metal", 1, 2, 5.0)
    g.registrar_material(m)
    assert len(g.obtener_materiales()) == 1

def test_singleton_buscar_usuario_existente():
    g = GestorSistema.obtener_instancia()
    c = Ciudadano(42, "Luis", "0997654321", "luis@mail.com", "pass456", "Calle 5")
    g.registrar_usuario(c)
    encontrado = g.buscar_usuario(42)
    assert encontrado is c

def test_singleton_buscar_usuario_no_existente():
    g = GestorSistema.obtener_instancia()
    assert g.buscar_usuario(999) is None

def test_singleton_id_usuarios_autoincremental():
    g = GestorSistema.obtener_instancia()
    id1 = g.siguiente_id_usuario()
    id2 = g.siguiente_id_usuario()
    id3 = g.siguiente_id_usuario()
    assert id1 == 1
    assert id2 == 2
    assert id3 == 3

def test_singleton_resetear():
    g1 = GestorSistema.obtener_instancia()
    GestorSistema.resetear()
    g2 = GestorSistema.obtener_instancia()
    assert g1 is not g2


# ─────────────────────────────────────────
# Tests de Strategy
# ─────────────────────────────────────────

def test_strategy_estandar_calcula_correctamente():
    calc = CalculadorPuntos(PuntosEstandar())
    assert calc.calcular(5.0) == 50

def test_strategy_especial_calcula_correctamente():
    calc = CalculadorPuntos(PuntosEspecial())
    assert calc.calcular(5.0) == 100

def test_strategy_organico_calcula_correctamente():
    calc = CalculadorPuntos(PuntosOrganico())
    assert calc.calcular(5.0) == 25

def test_strategy_especial_doble_que_estandar():
    peso = 4.0
    estandar = CalculadorPuntos(PuntosEstandar()).calcular(peso)
    especial  = CalculadorPuntos(PuntosEspecial()).calcular(peso)
    assert especial == estandar * 2

def test_strategy_cambiar_en_ejecucion():
    calc = CalculadorPuntos(PuntosEstandar())
    puntos_antes = calc.calcular(4.0)   # 40
    calc.cambiar_estrategia(PuntosEspecial())
    puntos_despues = calc.calcular(4.0) # 80
    assert puntos_antes == 40
    assert puntos_despues == 80

def test_strategy_para_material_plastico():
    calc = CalculadorPuntos.para_material("plastico")
    assert calc.calcular(1.0) == 10

def test_strategy_para_material_metal():
    calc = CalculadorPuntos.para_material("metal")
    assert calc.calcular(1.0) == 20

def test_strategy_para_material_vidrio():
    calc = CalculadorPuntos.para_material("vidrio")
    assert calc.calcular(1.0) == 20

def test_strategy_para_material_organico():
    calc = CalculadorPuntos.para_material("organico")
    assert calc.calcular(1.0) == 5

def test_strategy_para_material_papel():
    calc = CalculadorPuntos.para_material("papel")
    assert calc.calcular(1.0) == 10

def test_strategy_para_material_carton():
    calc = CalculadorPuntos.para_material("carton")
    assert calc.calcular(1.0) == 10

def test_strategy_peso_cero_da_cero_puntos():
    calc = CalculadorPuntos(PuntosEspecial())
    assert calc.calcular(0.0) == 0

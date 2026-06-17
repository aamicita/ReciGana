import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.usuarios.gestor_sistema import GestorSistema
from src.materiales.estrategia_puntos import (
    CalculadorPuntos, PuntosEstandar, PuntosEspecial, PuntosOrganico
)
from src.materiales.fabrica_materiales import FabricaMateriales
from src.usuarios.ciudadano import Ciudadano

print("=" * 45)
print("  PRUEBA — Singleton + Strategy")
print("=" * 45)

# ── SINGLETON ──────────────────────────────
print("\n--- Singleton ---")
g1 = GestorSistema.obtener_instancia()
g2 = GestorSistema.obtener_instancia()
g3 = GestorSistema.obtener_instancia()

print(f"g1 is g2: {g1 is g2}")   # True
print(f"g1 is g3: {g1 is g3}")   # True

# Registrar usuarios en el gestor
c1 = Ciudadano(1, "Ana Torres", "0991234567", "ana@mail.com", "pass123", "Av. 10")
c2 = Ciudadano(2, "Luis Vera",  "0997654321", "luis@mail.com","pass456", "Calle 5")
g1.registrar_usuario(c1)
g1.registrar_usuario(c2)

# Registrar materiales
m1 = FabricaMateriales.crear("metal",    1, 2, 5.0)
m2 = FabricaMateriales.crear("plastico", 2, 3, 2.5)
g1.registrar_material(m1)
g1.registrar_material(m2)

g1.resumen()

# ── STRATEGY ──────────────────────────────
print("\n--- Strategy ---")

# Forma directa: elegir estrategia manualmente
calc_estandar = CalculadorPuntos(PuntosEstandar())
calc_especial = CalculadorPuntos(PuntosEspecial())
calc_organico = CalculadorPuntos(PuntosOrganico())

print("\nMismo peso (5 kg), distintas estrategias:")
calc_estandar.calcular(5.0)   # 50  puntos
calc_especial.calcular(5.0)   # 100 puntos
calc_organico.calcular(5.0)   # 25  puntos

# Forma automatica: la estrategia se asigna segun el tipo
print("\nAsignacion automatica segun tipo de material:")
for tipo in ["plastico", "vidrio", "metal", "papel", "carton", "organico"]:
    calc = CalculadorPuntos.para_material(tipo)
    puntos = calc.calcular(3.0)
    print(f"  {tipo:10} -> {puntos} puntos")

# Cambiar estrategia en tiempo de ejecucion
print("\nCambio de estrategia en tiempo de ejecucion:")
calc = CalculadorPuntos(PuntosEstandar())
calc.calcular(4.0)                          # 40 puntos
calc.cambiar_estrategia(PuntosEspecial())
calc.calcular(4.0)                          # 80 puntos

print("\n✅ Singleton y Strategy funcionando correctamente.")

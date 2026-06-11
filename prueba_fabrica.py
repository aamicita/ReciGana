from src.materiales import FabricaMateriales

print("=" * 45)
print("  PRUEBA — Factory Method ReciGana")
print("=" * 45)

tipos = [
    ("plastico", 1, 3, 2.5),
    ("vidrio",   2, 1, 1.0),
    ("metal",    3, 2, 5.0),
    ("papel",    4, 4, 3.0),
    ("carton",   5, 2, 2.0),
    ("organico", 6, 5, 4.5),
]

for tipo, id_m, cantidad, peso in tipos:
    m = FabricaMateriales.crear(tipo, id_m, cantidad, peso)
    print(f"\n{m}")
    m.clasificar()
    m.calcular_valor()

print("\n--- Prueba tipo inválido ---")
try:
    FabricaMateriales.crear("madera", 99, 1, 1.0)
except ValueError as e:
    print(f"Error capturado: {e}")

print("\n✅ Todo funcionando correctamente.")
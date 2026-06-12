# Pruebas del módulo comunicaciones
# Aquí verificamos que Prototype y Builder funcionan correctamente

from src.comunicaciones import (
    Notificacion,
    Calificacion,
    HistorialDeReciclaje,
    ReporteBuilder,
)

print("=" * 55)
print("  PRUEBAS — Comunicaciones (Prototype + Builder)")
print("=" * 55)



# ===== PRUEBA 1: Prototype en Notificacion =====
# Explicación: Creamos UNA notificación base y la clonamos
# para enviarla a otro usuario sin crear todo desde cero
print("\n--- PRUEBA 1: Prototype - Notificacion ---")

# Creamos la notificación original
notif_original = Notificacion(1, "Tu oferta fue aceptada", "María")

# La marcamos como leída (para demostrar que el clon nace sin leer)
notif_original.marcar_como_leida()
print(f"Original : {notif_original}")

# Clonamos y cambiamos solo el destinatario
notif_clon = notif_original.clonar(nuevo_destinatario="Carlos")
print(f"Clon     : {notif_clon}")

# Verificamos que el clon nació como NO leído
assert notif_clon.leida == False, "El clon debe nacer como no leído"
assert notif_clon.destinatario == "Carlos", "El destinatario debe ser Carlos"
print("✅ Prototype Notificacion: OK")



# ====== PRUEBA 2: Prototype en Calificacion =======
# Explicación: Clonamos una calificación base cambiando
# solo el comentario, el puntaje se mantiene igual
print("\n--- PRUEBA 2: Prototype - Calificacion ---")

# Creamos la calificación original
calif_original = Calificacion(1, 5, "Excelente servicio")
calif_original.registrar_calificacion()
print(f"Original : {calif_original}")

# Clonamos y cambiamos solo el comentario
calif_clon = calif_original.clonar(nuevo_comentario="Muy puntual")
print(f"Clon     : {calif_clon}")

# Verificamos que el clon nació como NO registrado
assert calif_clon.registrada == False, "El clon debe nacer sin registrar"
assert calif_clon.puntaje == 5, "El puntaje debe mantenerse en 5"
assert calif_clon.comentario == "Muy puntual", "El comentario debe cambiar"
print("✅ Prototype Calificacion: OK")



# ===== PRUEBA 3: Prototype en HistorialDeReciclaje ======
# Explicación: Clonamos un historial completo con todos
# sus registros a un nuevo historial con diferente ID
print("\n--- PRUEBA 3: Prototype - HistorialDeReciclaje ---")

# Creamos el historial original y le agregamos registros
historial_original = HistorialDeReciclaje(1)
historial_original.agregar_registro("plástico", 5.0, "venta")
historial_original.agregar_registro("cartón", 3.0, "venta")
print(f"Original : {historial_original}")

# Clonamos con un nuevo ID
historial_clon = historial_original.clonar(nuevo_id=2)
print(f"Clon     : {historial_clon}")

# Verificamos que el clon tiene el nuevo ID pero los mismos registros
assert historial_clon.id_historial == 2, "El ID del clon debe ser 2"
assert historial_clon.total_registros == 2, "El clon debe tener 2 registros"
print("✅ Prototype HistorialDeReciclaje: OK")



# ====== PRUEBA 4: Builder en Reporte — construcción correcta =====

# Explicación: Construimos un reporte paso a paso
# usando el Builder. Cada método agrega un campo.
print("\n--- PRUEBA 4: Builder - Reporte correcto ---")

reporte = (ReporteBuilder()
            .con_id(1)
            .con_fecha("2025-06-01")
            .con_tipo("ventas")
            .con_contenido({
                "total_ventas": 15,
                "ingresos_USD": 300.0,
                "material_top": "cartón"
            })
            .construir())

# Generamos y exportamos el reporte
reporte.generar_reporte()
archivo = reporte.exportar_pdf()
print(f"Archivo exportado: {archivo}")
assert reporte.generado == True, "El reporte debe estar marcado como generado"
print("✅ Builder Reporte: OK")



# ==== PRUEBA 5: Builder — error cuando falta un campo =====
# Explicación: Si intentamos construir sin todos los campos
# el Builder debe lanzar un error claro diciéndonos qué falta
print("\n--- PRUEBA 5: Builder - campo faltante ---")

try:
    # Intentamos construir sin fecha ni contenido
    reporte_malo = (ReporteBuilder()
                    .con_id(2)
                    .con_tipo("usuarios")
                    .construir())  # Falta .con_fecha() y .con_contenido()
except ValueError as e:
    print(f"Error capturado correctamente: {e}")
    print("✅ Builder error campo faltante: OK")



# ===== PRUEBA 6: Builder — tipo de reporte inválido ======

print("\n--- PRUEBA 6: Builder - tipo inválido ---")

try:
    reporte_tipo_malo = (ReporteBuilder()
                          .con_id(3)
                          .con_fecha("2025-06-01")
                          .con_tipo("inventado")  # Este tipo no existe
                          .con_contenido({})
                          .construir())
except ValueError as e:
    print(f"Error capturado correctamente: {e}")
    print("✅ Builder tipo inválido: OK")


print("\n" + "=" * 55)
print("  ✅ TODAS LAS PRUEBAS DE COMUNICACIONES PASARON")
print("=" * 55)
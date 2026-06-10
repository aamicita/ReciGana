"""
Módulo principal de ReciGana - Sistema de gestión de reciclaje
Demuestra el flujo completo: registro, publicación, oferta y negociación.
"""

# Importamos las clases de usuarios desde la carpeta src/usuarios
from src.usuarios import Administrador, Ciudadano, Reciclador

# Importamos las clases de materiales desde la carpeta src/materiales
from src.materiales import MaterialReciclable, OfertaDeVenta, Negociacion

# Importamos las clases de comunicaciones desde la carpeta src/comunicaciones
from src.comunicaciones import Notificacion, Reporte, HistorialDeReciclaje, Calificacion


def main():
    """
    Función principal que demuestra el flujo completo del sistema ReciGana.
    Simula un escenario real: un ciudadano publica material, un reciclador
    hace una oferta, negocian el precio y se completa la transacción.
    """

    try:
        # Mostramos el encabezado del sistema en la consola
        print("=" * 50)
        print("   BIENVENIDO A RECIGANA - RECICLAJE EN MANTA")
        print("=" * 50)

        # ===== PASO 1: CREAR USUARIOS =====
        print("\n--- Creando usuarios ---")

        # Creamos un administrador con sus datos básicos
        # Parámetros: id, nombre, teléfono, correo, contraseña
        admin = Administrador(
            "A1", "Ana", "0991234567", "ana@recigana.com", "clave1234"
        )

        # Creamos un ciudadano que será quien publique materiales para vender
        # Tiene un parámetro extra: dirección física en Manta
        ciudadano = Ciudadano(
            "C1", "Luis", "0992345678", "luis@recigana.com", "clave1234", "Av. Central Manta"
        )

        # Creamos un reciclador que buscará materiales para comprar
        # Tiene un parámetro extra: zona de cobertura donde opera
        reciclador = Reciclador(
            "R1", "Marta", "0993456789", "marta@recigana.com", "clave1234", "Zona Norte"
        )

        # ===== PASO 2: INICIAR SESIONES =====
        print("\n--- Iniciando sesiones ---")

        # Iniciamos sesión del administrador verificando su contraseña
        # Si la contraseña es correcta retorna True y activa la sesión
        admin.iniciar_sesion("clave1234")

        # Iniciamos sesión del ciudadano con su contraseña
        ciudadano.iniciar_sesion("clave1234")

        # Iniciamos sesión del reciclador con su contraseña
        reciclador.iniciar_sesion("clave1234")

        # ===== PASO 3: ADMINISTRADOR GESTIONA USUARIOS =====
        print("\n--- Administrador gestiona usuarios ---")

        # El administrador registra al ciudadano en la plataforma
        # Verifica que no exista otro usuario con el mismo id antes de agregar
        admin.agregar_usuario(ciudadano)

        # El administrador registra al reciclador en la plataforma
        admin.agregar_usuario(reciclador)

        # El administrador consulta todos los usuarios registrados
        # Muestra el total y los datos de cada usuario
        admin.gestionar_usuarios()

        # ===== PASO 4: CIUDADANO PUBLICA MATERIALES =====
        print("\n--- Ciudadano publica materiales ---")

        # El ciudadano publica un material de plástico de 5kg sin foto
        # El material queda en estado "disponible" automáticamente
        ciudadano.publicar_material("plastico", 5.0)

        # El ciudadano publica un material de cartón de 3kg con foto adjunta
        # La foto es opcional — se pasa como tercer parámetro
        ciudadano.publicar_material("carton", 3.0, "foto.jpg")

        # ===== PASO 5: CREAR MATERIAL RECICLABLE =====
        print("\n--- Creando material reciclable ---")

        # Creamos un objeto MaterialReciclable con sus características
        # Parámetros: id, tipo, cantidad, peso en kg, estado inicial
        material = MaterialReciclable("M1", "plastico", 2, 5.0, "disponible")

        # Clasificamos el material para saber si es reciclable seco o biodegradable
        material.clasificar()

        # Calculamos el valor del material a $0.80 por kg
        # Retorna el valor total: 5kg x $0.80 = $4.00
        material.calcular_valor(0.80)

        # ===== PASO 6: RECICLADOR CONSULTA Y HACE OFERTA =====
        print("\n--- Reciclador consulta materiales y hace oferta ---")

        # Obtenemos la lista de materiales publicados por el ciudadano
        # materiales_publicados es una propiedad que retorna la lista interna
        materiales_disponibles = ciudadano.materiales_publicados

        # El reciclador consulta los materiales disponibles en la plataforma
        # Filtra automáticamente solo los que tienen estado "disponible"
        reciclador.consultar_ofertas(materiales_disponibles)

        # ===== PASO 7: CREAR Y PROCESAR OFERTA =====
        print("\n--- Procesando oferta de venta ---")

        # Creamos una oferta de venta con precio inicial de $10
        # El estado debe ser "pendiente" al crear una oferta nueva
        oferta = OfertaDeVenta("O1", 10.0, "pendiente")

        # Confirmamos la creación de la oferta con una descripción
        oferta.crear_oferta("Oferta por plastico 5kg")

        # El reciclador modifica su oferta subiendo el precio a $12
        # Solo se puede modificar si la oferta está en estado "pendiente"
        oferta.modificar_oferta(12.0)

        # ===== PASO 8: NEGOCIACIÓN =====
        print("\n--- Procesando negociación ---")

        # Creamos una negociación entre ciudadano y reciclador
        # Parámetros: id, precio inicial, estado, fecha de inicio
        negociacion = Negociacion("N1", 12.0, "pendiente", "2026-05-15")

        # Iniciamos formalmente la negociación
        # Solo se puede iniciar si está en estado "pendiente"
        negociacion.iniciar_negociacion()

        # El ciudadano propone una contra oferta subiendo el precio a $14
        # El nuevo precio queda registrado en el historial de contra ofertas
        negociacion.proponer_contra_oferta(14.0)

        # Ambas partes llegan a un acuerdo y finalizan la negociación
        # Se registra automáticamente la fecha y hora de cierre
        negociacion.finalizar_negociacion()

        # ===== PASO 9: NOTIFICACIONES =====
        print("\n--- Enviando notificaciones ---")

        # Creamos una notificación dirigida al usuario "Luis"
        # Parámetros: id, mensaje, destinatario (opcional)
        notificacion = Notificacion("NOT1", "Tienes una nueva oferta", "Luis")

        # Enviamos la notificación al destinatario
        notificacion.enviar()

        # Marcamos la notificación como leída cuando el usuario la ve
        # Solo se puede marcar como leída una vez
        notificacion.marcar_como_leida()

        # ===== PASO 10: HISTORIAL DE RECICLAJE =====
        print("\n--- Registrando historial ---")

        # Creamos el historial de reciclaje para este usuario
        historial = HistorialDeReciclaje("H1")

        # Registramos la venta de plástico en el historial
        # Parámetros: tipo de material, peso en kg, tipo de transacción
        historial.agregar_registro("plastico", 5.0, "venta")

        # Registramos la venta de cartón en el historial
        historial.agregar_registro("carton", 3.0, "venta")

        # Consultamos todo el historial con sus registros
        historial.consultar_historial()

        # ===== PASO 11: CALIFICACIÓN =====
        print("\n--- Registrando calificación ---")

        # Creamos una calificación de 5 estrellas con comentario
        # El puntaje debe estar entre 1 y 5
        calificacion = Calificacion("CAL1", 5, "Excelente servicio")

        # Registramos oficialmente la calificación en el sistema
        # Solo se puede registrar una vez
        calificacion.registrar_calificacion()

        # ===== PASO 12: REPORTE FINAL =====
        print("\n--- Generando reporte ---")

        # Creamos un reporte de ventas con datos reales como diccionario
        # El tipo debe ser uno válido: ventas, usuarios, materiales, ofertas
        reporte = Reporte("REP1", "2026-05-15", "ventas", {
            "total_ventas": 2,        # Número de ventas realizadas
            "kg_reciclados": 8.0,     # Total de kg reciclados
            "ingresos": 14.0          # Total de ingresos en dólares
        })

        # Generamos e imprimimos el reporte con todos sus datos
        reporte.generar_reporte()

        # ===== PASO 13: REPORTE DEL ADMINISTRADOR =====
        print("\n--- Reporte del administrador ---")

        # El administrador genera su propio reporte del estado de la plataforma
        # Muestra total de usuarios, ofertas aceptadas, rechazadas y pendientes
        admin.generar_reporte()

        # Mostramos el mensaje de cierre del sistema
        print("\n" + "=" * 50)
        print("   SISTEMA RECIGANA EJECUTADO EXITOSAMENTE")
        print("=" * 50)

    except Exception as e:
        # Si ocurre cualquier error inesperado lo mostramos y relanzamos
        print(f"\nError en la ejecución principal: {e}")
        raise


# Este bloque asegura que main() solo se ejecute cuando
# corremos este archivo directamente (no cuando se importa)
if __name__ == "__main__":
    main()
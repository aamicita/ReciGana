"""
Módulo principal de ReciGana - Sistema de gestión de reciclaje
Demuestra el flujo completo: registro, publicación, oferta y negociación.
"""

# Importamos las clases de usuarios
from src.usuarios import Administrador, Ciudadano, Reciclador
from src.usuarios import GestorSistema
from src.usuarios import FabricaUsuariosManta

#importamos clase de adaptador
from src.adaptadores.adaptador_usuario import AdaptadorUsuarioBackend


# Importamos las clases de materiales
from src.materiales import MaterialBase
from src.materiales.fabrica_materiales import FabricaMateriales
from src.materiales.oferta_de_venta import OfertaDeVenta
from src.materiales.negociacion import Negociacion

# Importamos las clases de comunicaciones
from src.comunicaciones import Notificacion, Reporte, HistorialDeReciclaje, Calificacion
from src.comunicaciones import ReporteBuilder
from src.comunicaciones.canal_envio import CanalEmailSimulado     #inyecccion de dependencias

class UsuarioDBFalso:
    def __init__(self, id, nombre, email, ciudad):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.ciudad = ciudad

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

        # Creamos un objeto FabricaMateriales con sus características
        # Parámetros: id, tipo, cantidad, peso en kg, estado inicial
        material = FabricaMateriales.crear("plastico", "M1", 2, 5.0)

        # Clasificamos el material para saber si es reciclable seco o biodegradable
        material.clasificar()

        # Calculamos el valor del material a $0.80 por kg
        # Retorna el valor total: 5kg x $0.80 = $4.00
        material.calcular_valor(0.80)

        #Precio base de materiales reciclables
        print("\n ---Precio base de materiales reciclables---")

        #Importamos cada clase de material para accedes a su atributo PRECIO_BASE definido en su propio archivo
        from src.materiales.metal import Metal
        from src.materiales.carton import Carton
        from src.materiales.vidrio import Vidrio
        from src.materiales.plastico import Plastico
        from src.materiales.papel import Papel
        from src.materiales.organico import Organico

        # Mostramos el precio base de cada material reciclable   
        # Estos valore vienen directamente de cada clase 
        print(f"Precio base de Metal: ${Metal.PRECIO_BASE}")
        print(f"Precio base de Cartón: ${Carton.PRECIO_BASE}")
        print(f"Precio base de Vidrio: ${Vidrio.PRECIO_BASE}")
        print(f"Precio base de Plástico: ${Plastico.PRECIO_BASE}")
        print(f"Precio base de Papel: ${Papel.PRECIO_BASE}")
        print(f"Precio base de Orgánico: ${Organico.PRECIO_BASE}")

        #Preguntamos al usuario si desea modificar algun precio base
        #El usuario decide si quier hacer cambios o no
        modificar_precio = input("\n¿Desea modificar algún precio base? (s/n): ").strip().lower()
        if modificar_precio == 's':
            #Solicitamos al usuario el material y el nuevo precio
            material_a_modificar = input("Ingrese el material a modificar (metal, carton, vidrio, plastico, papel, organico): ").strip().lower()
            nuevo_precio = float(input("Ingrese el nuevo precio base: "))

            #Modificamos el precio base del material seleccionadotry:
            try:
                if material_a_modificar == "metal":
                    Metal.cambiar_precio_base(nuevo_precio)
                    print(f"Precio base de Metal modificado a: ${Metal.PRECIO_BASE}")
                elif material_a_modificar == "carton":
                    Carton.cambiar_precio_base(nuevo_precio)
                    print(f"Precio base de Cartón modificado a: ${Carton.PRECIO_BASE}")
                elif material_a_modificar == "vidrio":
                    Vidrio.cambiar_precio_base(nuevo_precio)
                    print(f"Precio base de Vidrio modificado a: ${Vidrio.PRECIO_BASE}")
                elif material_a_modificar == "plastico":
                    Plastico.cambiar_precio_base(nuevo_precio)
                    print(f"Precio base de Plástico modificado a: ${Plastico.PRECIO_BASE}")
                elif material_a_modificar == "papel":
                    Papel.cambiar_precio_base(nuevo_precio)
                    print(f"Precio base de Papel modificado a: ${Papel.PRECIO_BASE}")
                elif material_a_modificar == "organico":
                    Organico.cambiar_precio_base(nuevo_precio)
                    print(f"Precio base de Orgánico modificado a: ${Organico.PRECIO_BASE}")
                else:
                    print("Material no reconocido. No se realizaron cambios.")
            except ValueError as ve:
                # Si el precio es 0 o negativo, capturamos el error
                print(f"Error: {ve}")


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

        #DEMO: INYECCION DE DEPENDENCIAS
        print("\n--- Demostrando inyección de dependencias (canal de envío) ---")
        notif_email = Notificacion("NOT1-B", "Tienes una nueva oferta", "Luis",
                                    canal_envio=CanalEmailSimulado())
        notif_email.enviar()   # Se "envía" simulando un correo, no un print plano

        #DEMO: ADAPTER
        print("\n--- Adaptando un usuario del backend al dominio POO ---")
        usuario_backend = UsuarioDBFalso(99, "Sofía", "sofia@correo.com", "Manta")
        ciudadano_adaptado = AdaptadorUsuarioBackend.a_ciudadano(usuario_backend)
        print(ciudadano_adaptado)
        
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
        
        # ==== AGG ULTIMAMENTE CLASE PATRONES DE DISEÑO ===
        
        
        # ===== PASO 14: SINGLETON — GestorSistema =====
        print("\n--- Patrón Singleton: GestorSistema ---")

        # Importamos el GestorSistema aquí para no mezclar con los imports de arriba
        from src.usuarios import GestorSistema

        # El Singleton garantiza que solo exista UNA instancia del gestor.
        # Aunque llamemos obtener_instancia() dos veces, siempre
        # nos devuelve el MISMO objeto con la MISMA lista de datos.
        # Esto es importante en ReciGana porque si hubiera dos gestores
        # separados, cada uno tendría su propia lista de usuarios
        # y los datos estarían desincronizados.
        gestor1 = GestorSistema.obtener_instancia()
        gestor2 = GestorSistema.obtener_instancia()

        # Con "is" verificamos que ambas variables apuntan
        # exactamente al mismo objeto en memoria
        print(f"¿gestor1 y gestor2 son el mismo objeto? {gestor1 is gestor2}")
        # Esto debe imprimir: True

        # Registramos a nuestros usuarios en el gestor central
        gestor1.registrar_usuario(ciudadano)
        gestor1.registrar_usuario(reciclador)

        # Mostramos el resumen del sistema
        gestor1.resumen()


        # ===== PASO 15: ABSTRACT FACTORY — FabricaUsuariosManta =====
        print("\n--- Patrón Abstract Factory: FabricaUsuariosManta ---")

        from src.usuarios import FabricaUsuariosManta

        # En vez de crear usuarios directamente escribiendo Ciudadano(...)
        # usamos la fábrica para que ella se encargue de crearlos.
        # Ventaja: si ReciGana se expande a Guayaquil, solo creamos
        # FabricaUsuariosGuayaquil sin tocar el resto del código.
        fabrica = FabricaUsuariosManta()

        # La fábrica crea cada tipo de usuario correctamente
        ciudadano2 = fabrica.crear_ciudadano(
            "C2", "Pedro Mora", "0994567890",
            "pedro@email.com", "clave789",
            "Calle Flavio Alfaro"     # Dirección en Manta
        )

        reciclador2 = fabrica.crear_reciclador(
            "R2", "Carmen Vera", "0995678901",
            "carmen@email.com", "clave321",
            "Los Esteros"             # Zona de cobertura
        )

        # Mostramos los usuarios creados por la fábrica
        print(f"Ciudadano creado  : {ciudadano2}")
        print(f"Reciclador creado : {reciclador2}")


        # ===== PASO 16: PROTOTYPE — Notificacion =====
        print("\n--- Patrón Prototype: Notificacion ---")

        # El Prototype nos permite clonar un objeto ya existente
        # y cambiarle solo lo que necesitamos.
        # En ReciGana el mismo mensaje "Tu oferta fue aceptada"
        # se envía a muchos usuarios. En vez de crear ese objeto
        # desde cero cada vez, creamos UNO base y lo clonamos
        # cambiando solo el destinatario.

        # Creamos la notificación base (la "plantilla")
        notif_base = Notificacion("NOT2", "Tu material fue vendido", "Pedro")

        # Clonamos y solo cambiamos el destinatario
        # El mensaje sigue siendo el mismo
        notif_clon = notif_base.clonar(nuevo_destinatario="Carmen")

        # Enviamos ambas notificaciones
        notif_base.enviar()   # Va dirigida a Pedro
        notif_clon.enviar()   # Va dirigida a Carmen, mismo mensaje


        # ===== PASO 17: BUILDER — ReporteBuilder =====
        print("\n--- Patrón Builder: ReporteBuilder ---")

        from src.comunicaciones import ReporteBuilder

        # El Builder nos permite construir objetos complejos paso a paso.
        # En ReciGana un Reporte tiene varios campos: ID, fecha, tipo
        # y contenido. Con Builder cada paso es claro y si olvidamos
        # un campo, el Builder nos avisa exactamente cuál falta.
        # Es como llenar un formulario campo por campo.

        reporte_builder = (ReporteBuilder()
            # Paso 1: asignamos el ID del reporte
            .con_id("REP2")
            # Paso 2: asignamos la fecha del período reportado
            .con_fecha("2026-05-15")
            # Paso 3: indicamos el tipo de reporte
            .con_tipo("usuarios")
            # Paso 4: agregamos el contenido con datos reales
            .con_contenido({
                "total_usuarios" : 2,   # Usuarios registrados
                "ciudadanos"     : 1,   # Cantidad de ciudadanos
                "recicladores"   : 1    # Cantidad de recicladores
            })
            # Paso final: construimos el objeto Reporte completo
            .construir())

        # Generamos el reporte para que se muestre en pantalla
        reporte_builder.generar_reporte()

    except Exception as e:
        # Si ocurre cualquier error inesperado lo mostramos y relanzamos
        print(f"\nError en la ejecución principal: {e}")
        raise


# Este bloque asegura que main() solo se ejecute cuando
# corremos este archivo directamente (no cuando se importa)
if __name__ == "__main__":
    main()
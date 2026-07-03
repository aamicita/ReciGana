
# PATRÓN FACADE — ReciGanaFacade

# ¿Qué patrón es este?

# FACADE (Fachada): proporciona una interfaz SIMPLE y unificada
# a un conjunto de clases complejas.

# En ReciGana:
# Sin Facade, para registrar un intercambio necesitas llamar a:
#   - FabricaMateriales.crear(...)
#   - Ciudadano.publicar_material(...)
#   - HistorialDeReciclaje.agregar_registro(...)
#   - Notificacion(...).enviar()
# Con Facade, solo llamas a:
#   - facade.registrar_intercambio(...)

# Importamos los módulos del sistema que la Facade va a simplificar
from src.usuarios.ciudadano import Ciudadano
from src.usuarios.reciclador import Reciclador
from src.usuarios.gestor_sistema import GestorSistema
from src.materiales.fabrica_materiales import FabricaMateriales
from src.materiales.negociacion import Negociacion, ObservadorCiudadano, ObservadorReciclador
from src.materiales.oferta_de_venta import OfertaDeVenta
from src.comunicaciones.notificacion import Notificacion
from src.comunicaciones.historial_de_reciclaje import HistorialDeReciclaje
from src.comunicaciones.reporte import Reporte
from datetime import datetime
 
 
class ReciGanaFacade:
    """
    PATRÓN FACADE — Fachada principal del sistema ReciGana.
 
    Esta clase es la "puerta de entrada" simplificada al sistema.
    En vez de que los tests o el código cliente tenga que conocer
    y coordinar múltiples clases de distintos módulos, esta
    Facade ofrece métodos sencillos que hacen todo el trabajo.
 
    Ejemplo sin Facade (lo que habría que hacer antes):
        gestor = GestorSistema.obtener_instancia()
        ciudadano = Ciudadano(1, "María", "099...", "m@m.com", "clave", "Av. 10")
        gestor.registrar_usuario(ciudadano)
        material = FabricaMateriales.crear("plastico", 1, 5, 10.0)
        gestor.registrar_material(material)
        historial = HistorialDeReciclaje(1)
        historial.agregar_registro("plastico", 10.0, "venta")
        notif = Notificacion(1, "Material publicado", "María")
        notif.enviar()
 
    Ejemplo CON Facade (lo que se hace ahora):
        facade = ReciGanaFacade()
        facade.registrar_ciudadano(1, "María", "099...", "m@m.com", "clave", "Av. 10")
        facade.publicar_material(ciudadano, "plastico", 10.0)
    """
 
    def __init__(self):
        # La Facade usa el GestorSistema (Singleton) internamente.
        # El cliente no necesita saber que existe GestorSistema.
        self.__gestor = GestorSistema.obtener_instancia()
 
        # Contador interno para generar IDs de notificaciones
        self.__contador_notificaciones = 1
 
        print("[Facade] ReciGanaFacade inicializada y lista para usar.")
 
    # ==========================================================
    # SECCIÓN 1: OPERACIONES DE USUARIOS
    # Simplifica la creación y registro de usuarios
    # ==========================================================
 
    def registrar_ciudadano(self, id_u, nombre, telefono, correo,
                             contrasenia, direccion):
        """
        FACADE — registra un ciudadano en el sistema en un solo paso.
 
        Sin Facade, necesitarías:
            ciudadano = Ciudadano(id_u, nombre, ...)
            gestor = GestorSistema.obtener_instancia()
            gestor.registrar_usuario(ciudadano)
            ciudadano.registrar()
 
        Con Facade, solo llamas a este método y listo.
 
        Retorna el objeto Ciudadano ya registrado.
        """
        # Paso 1: crear el ciudadano
        ciudadano = Ciudadano(
            id_u, nombre, telefono, correo, contrasenia, direccion
        )
 
        # Paso 2: registrarlo en el gestor del sistema
        self.__gestor.registrar_usuario(ciudadano)
 
        # Paso 3: confirmar el registro
        ciudadano.registrar()
 
        print(
            f"[Facade] Ciudadano '{nombre}' registrado "
            f"exitosamente (ID: {id_u})."
        )
        return ciudadano
 
    def registrar_reciclador(self, id_u, nombre, telefono, correo,
                              contrasenia, zona_cobertura):
        """
        FACADE — registra un reciclador en el sistema en un solo paso.
 
        Retorna el objeto Reciclador ya registrado.
        """
        # Paso 1: crear el reciclador
        reciclador = Reciclador(
            id_u, nombre, telefono, correo, contrasenia, zona_cobertura
        )
 
        # Paso 2: registrarlo en el sistema
        self.__gestor.registrar_usuario(reciclador)
 
        # Paso 3: confirmar el registro
        reciclador.registrarse()
 
        print(
            f"[Facade] Reciclador '{nombre}' registrado "
            f"en zona '{zona_cobertura}' (ID: {id_u})."
        )
        return reciclador
 
    # ==========================================================
    # SECCIÓN 2: OPERACIONES DE MATERIALES
    # Simplifica publicar materiales y hacer ofertas
    # ==========================================================
 
    def publicar_material(self, ciudadano, tipo_material,
                           peso_kg, foto=None):
        """
        FACADE — un ciudadano publica un material Y lo registra
        en el sistema, todo en un solo paso.
 
        Sin Facade necesitarías:
            material_dict = ciudadano.publicar_material(tipo, peso, foto)
            obj_material = FabricaMateriales.crear(tipo, id, 1, peso)
            gestor.registrar_material(obj_material)
 
        Retorna el diccionario del material publicado.
        """
        # Paso 1: el ciudadano publica el material (crea el dict)
        material_dict = ciudadano.publicar_material(
            tipo_material, peso_kg, foto
        )
 
        # Paso 2: creamos también el objeto material en la fábrica
        # para registrarlo formalmente en el sistema
        id_mat = self.__gestor.siguiente_id_material()
        obj_material = FabricaMateriales.crear(
            tipo_material, id_mat, 1, peso_kg
        )
        self.__gestor.registrar_material(obj_material)
 
        # Paso 3: enviamos notificación automática al ciudadano
        self.__enviar_notificacion(
            destinatario=ciudadano.nombre,
            mensaje=f"Tu material '{tipo_material}' de {peso_kg} kg fue publicado."
        )
 
        print(
            f"[Facade] Material '{tipo_material}' publicado "
            f"por '{ciudadano.nombre}'."
        )
        return material_dict
 
    def hacer_oferta(self, reciclador, material_dict, precio_ofrecido):
        """
        FACADE — un reciclador hace una oferta sobre un material
        publicado. Crea la oferta y la registra en un solo paso.
 
        Retorna el diccionario de la oferta creada.
        """
        # Paso 1: el reciclador hace la oferta
        oferta_dict = reciclador.realizar_oferta(
            material_dict, precio_ofrecido
        )
 
        if oferta_dict is None:
            print("[Facade] No se pudo crear la oferta.")
            return None
 
        # Paso 2: notificamos al reciclador que su oferta fue enviada
        self.__enviar_notificacion(
            destinatario=reciclador.nombre,
            mensaje=(
                f"Tu oferta de ${precio_ofrecido} por "
                f"'{material_dict.get('tipo')}' fue enviada."
            )
        )
 
        print(
            f"[Facade] Oferta de ${precio_ofrecido} creada "
            f"por '{reciclador.nombre}'."
        )
        return oferta_dict
 
    # ==========================================================
    # SECCIÓN 3: OPERACIÓN CENTRAL — REGISTRAR UN INTERCAMBIO
    # Esta es la operación más compleja del sistema.
    # Sin Facade involucra 5+ clases de 3 módulos distintos.
    # ==========================================================
 
    def registrar_intercambio(self, ciudadano, reciclador,
                               tipo_material, peso_kg, precio):
        """
        FACADE — registra un intercambio COMPLETO entre un ciudadano
        y un reciclador. Es la operación más importante del sistema.
 
        Esta sola llamada coordina automáticamente:
            1. Crear la negociacion y finalizarla
            2. Actualizar el historial del ciudadano
            3. Actualizar el historial del reciclador
            4. Notificar al ciudadano que vendió
            5. Notificar al reciclador que compró
 
        Sin Facade, tendrias que escribir unas 20 líneas de código
        conociendo exactamente qué clases de qué módulos llamar.
 
        Retorna un resumen del intercambio como diccionario.
        """
        print(
            f"\n[Facade] Iniciando intercambio: "
            f"'{ciudadano.nombre}' vende {peso_kg}kg de "
            f"'{tipo_material}' a '{reciclador.nombre}' "
            f"por ${precio}"
        )
 
        # Paso 1: crear y finalizar la negociación (módulo materiales)
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        negociacion = Negociacion(
            id_negociacion=f"NEG-{fecha_hoy}-{ciudadano.nombre[:3].upper()}",
            precio_final=precio,
            estado="pendiente",
            fecha_inicio=fecha_hoy
        )
        negociacion.iniciar_negociacion()
        # Paso 1: crear y finalizar la negociación (módulo materiales)
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        negociacion = Negociacion(
            id_negociacion=f"NEG-{fecha_hoy}-{ciudadano.nombre[:3].upper()}",
            precio_final=precio,
            estado="pendiente",
            fecha_inicio=fecha_hoy
        )
        negociacion.iniciar_negociacion()
        
        negociacion.suscribir(ObservadorCiudadano(ciudadano.nombre, peso_kg, tipo_material))
        negociacion.suscribir(ObservadorReciclador(reciclador.nombre, peso_kg, tipo_material))

        negociacion.finalizar_negociacion()
        negociacion.finalizar_negociacion()
 
        # Paso 2: registrar en el historial del ciudadano
        # (módulo comunicaciones)
        historial_ciudadano = HistorialDeReciclaje(
            id_historial=f"HC-{ciudadano.nombre[:3].upper()}"
        )
        historial_ciudadano.agregar_registro(
            tipo_material=tipo_material,
            peso_kg=peso_kg,
            tipo_transaccion="venta"
        )
 
        # Paso 3: registrar en el historial del reciclador
        # (módulo comunicaciones)
        historial_reciclador = HistorialDeReciclaje(
            id_historial=f"HR-{reciclador.nombre[:3].upper()}"
        )
        historial_reciclador.agregar_registro(
            tipo_material=tipo_material,
            peso_kg=peso_kg,
            tipo_transaccion="compra"
        )
 
        #COMENTADO PORQUE DESPUES ENVIA NOTIFICACION A USUARIOS 2 VECES
        """# Paso 4: notificar al ciudadano (módulo comunicaciones)
        self.__enviar_notificacion(
            destinatario=ciudadano.nombre,
            mensaje=(
                f"Vendiste {peso_kg} kg de '{tipo_material}' "
                f"a {reciclador.nombre} por ${precio}."
            )
        )
 
        # Paso 5: notificar al reciclador (módulo comunicaciones)
        self.__enviar_notificacion(
            destinatario=reciclador.nombre,
            mensaje=(
                f"Compraste {peso_kg} kg de '{tipo_material}' "
                f"a {ciudadano.nombre} por ${precio}."
            )
        )
 
        # Armamos el resumen del intercambio para retornar
        resumen = {
            "tipo_material":     tipo_material,
            "peso_kg":           peso_kg,
            "precio":            precio,
            "ciudadano":         ciudadano.nombre,
            "reciclador":        reciclador.nombre,
            "estado_negociacion": negociacion.estado,
            "fecha":             fecha_hoy
        }
 
        print(
            f"[Facade] Intercambio completado exitosamente. "
            f"Negociacion estado: {negociacion.estado}"
        )
        return resumen """
 
    # ==========================================================
    # SECCIÓN 4: OPERACIONES DE CONSULTA
    # Simplifica el acceso a información del sistema
    # ==========================================================
 
    def obtener_resumen_sistema(self):
        """
        FACADE — obtiene un resumen del estado del sistema
        en un solo método.
 
        Sin Facade necesitarías llamar a GestorSistema directamente
        y saber que existe ese método.
 
        Retorna un diccionario con estadísticas básicas.
        """
        usuarios   = self.__gestor.obtener_usuarios()
        materiales = self.__gestor.obtener_materiales()
 
        resumen = {
            "total_usuarios":   len(usuarios),
            "total_materiales": len(materiales),
        }
 
        print(
            f"[Facade] Resumen del sistema: "
            f"{resumen['total_usuarios']} usuarios, "
            f"{resumen['total_materiales']} materiales."
        )
        return resumen
 
    def generar_reporte_sistema(self, id_reporte, fecha):
        """
        FACADE — genera un reporte del sistema en un solo paso.
 
        Sin Facade tendrías que importar Reporte, construirlo
        con todos sus parámetros y llamar a generar_reporte().
 
        Retorna el objeto Reporte ya generado.
        """
        usuarios   = self.__gestor.obtener_usuarios()
        materiales = self.__gestor.obtener_materiales()
 
        # Creamos el reporte con los datos del sistema
        reporte = Reporte(
            id_reporte=id_reporte,
            fecha=fecha,
            tipo_reporte="usuarios",
            contenido={
                "total_usuarios":   len(usuarios),
                "total_materiales": len(materiales),
            }
        )
 
        # Generamos el reporte automáticamente
        reporte.generar_reporte()
 
        print(f"[Facade] Reporte #{id_reporte} generado para la fecha {fecha}.")
        return reporte
 
    # ==========================================================
    # MÉTODO PRIVADO DE APOYO
    # No forma parte de la interfaz pública del Facade
    # ==========================================================
 
    def __enviar_notificacion(self, destinatario, mensaje):
        """
        Método interno que crea y envía una notificación.
        Es privado porque el cliente no necesita saber
        cómo se construyen las notificaciones internamente.
        """
        notif = Notificacion(
            id_notificacion=self.__contador_notificaciones,
            mensaje=mensaje,
            destinatario=destinatario
        )
        notif.enviar()
 
        # Incrementamos el contador para el próximo ID
        self.__contador_notificaciones += 1
        return notif
 
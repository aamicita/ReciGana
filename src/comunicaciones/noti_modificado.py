# =============================================================================
# 2) IMPLEMENTACIÓN CON EL PATRÓN DE COMPORTAMIENTO "OBSERVER"
# =============================================================================
#
# Idea del patrón: el objeto que cambia de estado (el SUJETO / OBSERVABLE)
# mantiene una lista de "observadores" suscritos. Cada vez que ocurre un
# evento relevante, el sujeto simplemente recorre su lista y les avisa a
# TODOS, sin necesitar saber qué hace cada observador con esa información.
#
# Esto invierte la dependencia: en la versión anterior, el Facade "conocía"
# a la Negociacion y decidía a quién avisar. Ahora es la propia Negociacion
# quien avisa a quien esté suscrito, y el Facade (o cualquier otra parte
# del sistema) solo se encarga de suscribir observadores al inicio.
# =============================================================================

class ObservadorNegociacion(ABC):
    """
    Interfaz que deben implementar todos los observadores interesados en
    los cambios de estado de una Negociacion.
    """

    @abstractmethod
    def actualizar(self, negociacion, evento: str):
        """
        Es llamado automáticamente por el sujeto (Negociacion) cada vez
        que ocurre un evento relevante.
            negociacion -- la instancia de Negociacion que cambió
            evento      -- texto que describe qué pasó
                            ("iniciada", "finalizada", "cancelada")
        """
        ...


class SujetoObservable:
    """
    Clase base reutilizable que implementa el mecanismo de suscripción y
    notificación del patrón Observer. Cualquier clase del sistema que
    necesite avisar a observadores puede heredar de aquí.
    """

    def __init__(self):
        self._observadores = []

    def suscribir(self, observador: ObservadorNegociacion):
        if observador not in self._observadores:
            self._observadores.append(observador)

    def desuscribir(self, observador: ObservadorNegociacion):
        if observador in self._observadores:
            self._observadores.remove(observador)

    def notificar_observadores(self, evento: str):
        for observador in self._observadores:
            observador.actualizar(self, evento)


class Negociacion(SujetoObservable):
    """
    Representa el proceso de negociación entre un ciudadano (vendedor) y
    un reciclador (comprador) sobre el precio de un material reciclable.

    SUJETO/OBSERVABLE del patrón Observer: cada vez que cambia de estado
    (se inicia, se finaliza o se cancela), notifica automáticamente a
    todos los observadores que estén suscritos, sin necesitar saber qué
    hace cada uno con esa información.
    """

    ESTADOS_VALIDOS = {"pendiente", "iniciada", "finalizada", "cancelada"}

    def __init__(self, id_negociacion, precio_final, estado, fecha_inicio):
        super().__init__()
        self.id_negociacion = id_negociacion
        self.precio_final = precio_final

        if estado not in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido. Use uno de: {self.ESTADOS_VALIDOS}")
        self.estado = estado

        self.fecha_inicio = fecha_inicio
        self.fecha_cierre = None

    def iniciar_negociacion(self):
        if self.estado != "pendiente":
            print(f"No se puede iniciar. Estado actual: '{self.estado}'.")
            return False
        self.estado = "iniciada"
        print(f"Negociación #{self.id_negociacion} iniciada. Precio: ${self.precio_final}")
        self.notificar_observadores("iniciada")
        return True

    def finalizar_negociacion(self):
        if self.estado != "iniciada":
            print(f"No se puede finalizar. Estado actual: '{self.estado}'.")
            return False
        self.estado = "finalizada"
        self.fecha_cierre = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Negociación #{self.id_negociacion} finalizada. Precio: ${self.precio_final}")
        # Aquí es donde antes el Facade tenía que avisar "a mano".
        # Ahora la propia Negociacion avisa a todos sus interesados.
        self.notificar_observadores("finalizada")
        return True

    def cancelar_negociacion(self):
        if self.estado in ("finalizada", "cancelada"):
            print(f"La negociación ya está '{self.estado}', no se puede cancelar.")
            return False
        self.estado = "cancelada"
        self.fecha_cierre = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Negociación #{self.id_negociacion} cancelada.")
        self.notificar_observadores("cancelada")
        return True

    def __str__(self):
        return (f"Negociación #{self.id_negociacion} | Estado: {self.estado} | "
                f"Precio: ${self.precio_final}")


# ---------- Observadores concretos ----------
# Reutilizan la clase Notificacion tal como existe en el proyecto real
# (src/comunicaciones/notificacion.py). Aquí usamos una versión mínima
# para que el ejemplo sea autocontenido y ejecutable.

class NotificacionSimple2:
    """Versión mínima de Notificacion, solo para esta demo."""

    def __init__(self, mensaje, destinatario):
        self.mensaje = mensaje
        self.destinatario = destinatario

    def enviar(self):
        print(f"Notificación enviada a '{self.destinatario}': {self.mensaje}")
        return True


class ObservadorCiudadano(ObservadorNegociacion):
    """
    Observador concreto que representa al ciudadano (vendedor). Reacciona
    solamente cuando la negociación se finaliza, generando una notificación
    de venta.
    """

    def __init__(self, nombre, peso_kg, tipo_material):
        self.nombre = nombre
        self.peso_kg = peso_kg
        self.tipo_material = tipo_material

    def actualizar(self, negociacion, evento):
        if evento == "finalizada":
            mensaje = (f"Vendiste {self.peso_kg}kg de '{self.tipo_material}' "
                       f"por ${negociacion.precio_final}.")
            NotificacionSimple2(mensaje, self.nombre).enviar()
        elif evento == "cancelada":
            NotificacionSimple2(
                f"Tu negociación #{negociacion.id_negociacion} fue cancelada.",
                self.nombre
            ).enviar()


class ObservadorReciclador(ObservadorNegociacion):
    """
    Observador concreto que representa al reciclador (comprador). Reacciona
    solamente cuando la negociación se finaliza, generando una notificación
    de compra.
    """

    def __init__(self, nombre, peso_kg, tipo_material):
        self.nombre = nombre
        self.peso_kg = peso_kg
        self.tipo_material = tipo_material

    def actualizar(self, negociacion, evento):
        if evento == "finalizada":
            mensaje = (f"Compraste {self.peso_kg}kg de '{self.tipo_material}' "
                       f"por ${negociacion.precio_final}.")
            NotificacionSimple2(mensaje, self.nombre).enviar()
        elif evento == "cancelada":
            NotificacionSimple2(
                f"La negociación #{negociacion.id_negociacion} fue cancelada.",
                self.nombre
            ).enviar()


class ObservadorAuditoria(ObservadorNegociacion):
    """
    Observador concreto adicional: un módulo de auditoría interno que
    registra TODOS los eventos de TODAS las negociaciones. Se agrega sin
    tocar ni una sola línea de la clase Negociacion ni de los otros
    observadores: esa es la ventaja principal del patrón Observer.
    """

    def __init__(self):
        self.registro = []

    def actualizar(self, negociacion, evento):
        entrada = f"[AUDITORÍA] Negociación #{negociacion.id_negociacion} -> evento: {evento}"
        self.registro.append(entrada)
        print(entrada)


def realizar_intercambio_con_patron(ciudadano, reciclador, tipo_material, peso_kg, precio,
                                     con_auditoria=False):
    """
    Simula el método del Facade con el patrón Observer aplicado: ya no
    tiene que acordarse de notificar a cada interesado manualmente.
    Simplemente suscribe a los observadores UNA vez y la propia
    Negociacion se encarga de avisarles cuando corresponda.
    """
    negociacion = Negociacion(
        id_negociacion="NEG-002",
        precio_final=precio,
        estado="pendiente",
        fecha_inicio=datetime.now().strftime("%Y-%m-%d"),
    )

    # Suscribimos a los interesados. El Facade ya NO decide cuándo ni con
    # qué mensaje avisarles: eso ahora lo sabe cada observador.
    negociacion.suscribir(ObservadorCiudadano(ciudadano, peso_kg, tipo_material))
    negociacion.suscribir(ObservadorReciclador(reciclador, peso_kg, tipo_material))

    if con_auditoria:
        # Agregar un nuevo interesado es tan simple como suscribirlo:
        # no se modifica Negociacion ni los demás observadores.
        negociacion.suscribir(ObservadorAuditoria())

    negociacion.iniciar_negociacion()
    negociacion.finalizar_negociacion()

    return negociacion


# =============================================================================
# 3) EJEMPLO DE USO
# =============================================================================
#
# Demuestra el mismo flujo de negocio (iniciar -> finalizar una negociación
# de compraventa) primero con la versión SIN patrón y luego con la versión
# CON el patrón Observer, incluyendo un tercer observador (auditoría) que
# se agrega sin modificar ninguna clase existente.
# =============================================================================

if __name__ == "__main__":

    print("=" * 70)
    print("DEMO 1: Negociación SIN patrón Observer (notificación manual)")
    print("=" * 70)
    realizar_intercambio_sin_patron(
        ciudadano="María", reciclador="Luis",
        tipo_material="Cartón", peso_kg=20, precio=15.0
    )

    print()
    print("=" * 70)
    print("DEMO 2: Negociación CON el patrón Observer")
    print("=" * 70)
    realizar_intercambio_con_patron(
        ciudadano="María", reciclador="Luis",
        tipo_material="Cartón", peso_kg=20, precio=15.0
    )

    print()
    print("=" * 70)
    print("DEMO 3: Agregando un tercer observador (auditoría) SIN modificar")
    print("         la clase Negociacion ni los observadores existentes")
    print("=" * 70)
    realizar_intercambio_con_patron(
        ciudadano="Ana", reciclador="Pedro",
        tipo_material="Vidrio", peso_kg=8, precio=6.0,
        con_auditoria=True
    )

    print()
    print("=" * 70)
    print("DEMO 4: Negociación cancelada -> los observadores también")
    print("         reaccionan a ese evento")
    print("=" * 70)
    negociacion_cancelada = Negociacion(
        id_negociacion="NEG-003", precio_final=10.0,
        estado="pendiente", fecha_inicio=datetime.now().strftime("%Y-%m-%d")
    )
    negociacion_cancelada.suscribir(ObservadorCiudadano("Carla", 5, "Plástico"))
    negociacion_cancelada.suscribir(ObservadorReciclador("Jorge", 5, "Plástico"))
    negociacion_cancelada.iniciar_negociacion()
    negociacion_cancelada.cancelar_negociacion()

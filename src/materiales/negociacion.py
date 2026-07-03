from abc import ABC, abstractmethod
from datetime import datetime

# =============================================================================
# 1) SIMULACIÓN DE LA VERSIÓN SIN PATRÓN (Para que la Demo 1 funcione)
# =============================================================================
def realizar_intercambio_sin_patron(ciudadano, reciclador, tipo_material, peso_kg, precio):
    """Simula la versión antigua donde el Facade hacía todo manualmente."""
    print(f"Negociación #NEG-001 iniciada (Sin Patrón). Precio: ${precio}")
    print(f"Negociación #NEG-001 finalizada (Sin Patrón). Precio: ${precio}")
    # Notificación manual hardcodeada
    print(f"Notificación enviada a '{ciudadano}': Vendiste {peso_kg}kg de '{tipo_material}' por ${precio}.")
    print(f"Notificación enviada a '{reciclador}': Compraste {peso_kg}kg de '{tipo_material}' por ${precio}.")


# =============================================================================
# 2) IMPLEMENTACIÓN CON EL PATRÓN DE COMPORTAMIENTO "OBSERVER"
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
        """
        pass


class SujetoObservable:
    """
    Clase base reutilizable que implementa el mecanismo de suscripción y
    notificación del patrón Observer.
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
    SUJETO/OBSERVABLE del patrón Observer.
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
    
    def proponer_contra_oferta(self, nuevo_precio):
        if self.estado != "iniciada":
            print(f"No se puede proponer contraoferta en estado '{self.estado}'.")
            return False
        self.precio_final = nuevo_precio
        print(f"Nueva contraoferta propuesta para #{self.id_negociacion}: ${self.precio_final}")
        return True
    
    def __str__(self):
        return (f"Negociación #{self.id_negociacion} | Estado: {self.estado} | "
                f"Precio: ${self.precio_final}")


# ---------- Observadores concretos ----------

class NotificacionSimple2:
    """Versión mínima de Notificacion, solo para esta demo."""

    def __init__(self, mensaje, destinatario):
        self.mensaje = mensaje
        self.destinatario = destinatario

    def enviar(self):
        print(f"Notificación enviada a '{self.destinatario}': {self.mensaje}")
        return True


class ObservadorCiudadano(ObservadorNegociacion):
    """Observador concreto que representa al ciudadano (vendedor)."""

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
    """Observador concreto que representa al reciclador (comprador)."""

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
    """Módulo de auditoría interno que registra todos los eventos."""

    def __init__(self):
        self.registro = []

    def actualizar(self, negociacion, evento):
        entrada = f"[AUDITORÍA] Negociación #{negociacion.id_negociacion} -> evento: {evento}"
        self.registro.append(entrada)
        print(entrada)


def realizar_intercambio_con_patron(ciudadano, reciclador, tipo_material, peso_kg, precio,
                                    con_auditoria=False):
    """Simula el método del Facade usando Observer."""
    negociacion = Negociacion(
        id_negociacion="NEG-002",
        precio_final=precio,
        estado="pendiente",
        fecha_inicio=datetime.now().strftime("%Y-%m-%d"),
    )

    negociacion.suscribir(ObservadorCiudadano(ciudadano, peso_kg, tipo_material))
    negociacion.suscribir(ObservadorReciclador(reciclador, peso_kg, tipo_material))

    if con_auditoria:
        negociacion.suscribir(ObservadorAuditoria())

    negociacion.iniciar_negociacion()
    negociacion.finalizar_negociacion()

    return negociacion


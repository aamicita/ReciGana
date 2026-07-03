# PROBLEMA de este enfoque:
#   - La clase Negociacion NO avisa a nadie por sí misma cuando cambia de
#     estado. Es una clase "ciega" respecto a quién está interesado en
#     sus cambios.
#   - Es el FACADE quien tiene que saber, paso a paso, a quién le toca
#     avisar y con qué mensaje ("Paso 4: notificar al ciudadano",
#     "Paso 5: notificar al reciclador").
#   - Si se agrega un nuevo interesado (por ejemplo, un módulo de
#     auditoría o un sistema de puntos que debe reaccionar cuando una
#     negociación se cierra), hay que volver a modificar el Facade y
#     agregar un nuevo bloque de código manual.
#   - La responsabilidad de "quién debe enterarse de qué" queda mezclada
#     con la lógica de orquestación del intercambio, en vez de estar en
#     manos de la propia Negociacion.

from datetime import datetime
from abc import ABC, abstractmethod

class NegociacionSinPatron:
    """
    Representa el proceso de negociación entre un ciudadano (vendedor) y un
    reciclador (comprador) sobre el precio de un material reciclable.

    Esta versión NO conoce a sus interesados: simplemente cambia de estado.
    Es responsabilidad de quien la use (el Facade) enterarse del cambio y
    decidir a quién avisar.
    """

    ESTADOS_VALIDOS = {"pendiente", "iniciada", "finalizada", "cancelada"}

    def __init__(self, id_negociacion, precio_final, estado, fecha_inicio):
        self.id_negociacion = id_negociacion
        self.precio_final = precio_final
        self.estado = estado
        self.fecha_inicio = fecha_inicio
        self.fecha_cierre = None

    def iniciar_negociacion(self):
        if self.estado != "pendiente":
            print(f"No se puede iniciar. Estado actual: '{self.estado}'.")
            return False
        self.estado = "iniciada"
        print(f"Negociación #{self.id_negociacion} iniciada. Precio: ${self.precio_final}")
        return True

    def finalizar_negociacion(self):
        if self.estado != "iniciada":
            print(f"No se puede finalizar. Estado actual: '{self.estado}'.")
            return False
        self.estado = "finalizada"
        self.fecha_cierre = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Negociación #{self.id_negociacion} finalizada. Precio: ${self.precio_final}")
        return True

    def cancelar_negociacion(self):
        if self.estado in ("finalizada", "cancelada"):
            print(f"La negociación ya está '{self.estado}', no se puede cancelar.")
            return False
        self.estado = "cancelada"
        self.fecha_cierre = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Negociación #{self.id_negociacion} cancelada.")
        return True


class NotificacionSimple:
    """Versión mínima de la clase Notificacion, solo para esta demo."""

    def __init__(self, mensaje, destinatario):
        self.mensaje = mensaje
        self.destinatario = destinatario

    def enviar(self):
        print(f"Notificación enviada a '{self.destinatario}': {self.mensaje}")
        return True


def enviar_notificacion_manual(destinatario, mensaje):
    """
    Función auxiliar que simula lo que hace el Facade "a mano":
    crear una Notificacion y enviarla.
    """
    NotificacionSimple(mensaje, destinatario).enviar()


def realizar_intercambio_sin_patron(ciudadano, reciclador, tipo_material, peso_kg, precio):
    """
    Simula el método del Facade tal como estaba originalmente: es ESTA
    función la que tiene que acordarse de notificar a cada interesado,
    uno por uno, después de finalizar la negociación.
    """
    negociacion = NegociacionSinPatron(
        id_negociacion="NEG-001",
        precio_final=precio,
        estado="pendiente",
        fecha_inicio=datetime.now().strftime("%Y-%m-%d"),
    )
    negociacion.iniciar_negociacion()
    negociacion.finalizar_negociacion()

    # El Facade tiene que saber manualmente a quién avisar y con qué mensaje
    enviar_notificacion_manual(
        ciudadano,
        f"Vendiste {peso_kg}kg de '{tipo_material}' a {reciclador} por ${precio}."
    )
    enviar_notificacion_manual(
        reciclador,
        f"Compraste {peso_kg}kg de '{tipo_material}' a {ciudadano} por ${precio}."
    )
    # Si mañana se agrega un tercer interesado (ej. auditoría), hay que
    # volver a tocar esta función y agregar una línea más aquí.
    return negociacion


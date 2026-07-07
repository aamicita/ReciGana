# INYECCIÓN DE DEPENDENCIAS 
# ¿Cuál es el problema que resolvemos aquí?
#
# Antes, la clase Notificacion decidía POR SÍ MISMA cómo se envía
# un mensaje: siempre con un print(). Si mañana quisiéramos enviar
# por correo, por SMS o por WhatsApp, tendríamos que ENTRAR a
# modificar el código interno de Notificacion. Eso viola el
# principio de "abierto/cerrado" (una de las reglas SOLID): una clase debería estar abierta a
# extenderse, pero cerrada a modificarse.
#
# La solución es la Inyección de Dependencias:
#   - Definimos una interfaz (CanalEnvio) que dice QUE debe saber
#     hacer cualquier canal: enviar(destinatario, mensaje).
#   - Creamos varias implementaciones concretas (Consola, Email...).
#   - En vez de que Notificacion cree su propio canal, se lo
#     "inyectamos" desde afuera, por el constructor.
#
# Así, Notificacion ya NO depende de una forma concreta de enviar,
# depende de la ABSTRACCIÓN CanalEnvio. Esto también es el
# principio de Inversión de Dependencias (la "D" de SOLID).
# ============================================================

from abc import ABC, abstractmethod

# POLIMORFISMO CON INTERFAZ 
# A diferencia de MaterialBase (que es clase abstracta con estado
# compartido: ESTADOS_VALIDOS, validaciones en __init__), CanalEnvio
# es una interfaz PURA: solo define el contrato enviar(), sin ningún
# atributo ni lógica compartida. CanalConsola, CanalEmailSimulado y
# CanalSMSSimulado implementan ese mismo contrato cada una a su manera.

class CanalEnvio(ABC):
    """
    Interfaz (contrato) que debe cumplir cualquier canal de envío.
    Cualquier clase nueva que se quiera inyectar en Notificacion
    DEBE heredar de aquí e implementar el método enviar().
    """

    @abstractmethod
    def enviar(self, destinatario, mensaje) -> bool:
        """
        Envía el mensaje al destinatario usando el medio que
        corresponda (consola, email, sms, etc.).
        Debe retornar True si el envío fue exitoso.
        """
        pass


class CanalConsola(CanalEnvio):
    """
    Canal por defecto: imprime el mensaje en consola.
    Es el mismo comportamiento que ya tenía Notificacion antes
    de aplicar el patrón, así que nada se rompe si no se inyecta
    ningún canal explícitamente.
    """

    def enviar(self, destinatario, mensaje) -> bool:
        if destinatario:
            print(f"Notificación enviada a '{destinatario}': {mensaje}")
        else:
            print(f"Notificación enviada: {mensaje}")
        return True


class CanalEmailSimulado(CanalEnvio):
    """
    Simula el envío de un correo electrónico.
    No manda un correo real, pero demuestra que Notificacion puede usar OTRO
    canal sin que tengamos que tocarle una sola línea.
    """

    def enviar(self, destinatario, mensaje) -> bool:
        correo_destino = f"{destinatario.lower().replace(' ', '.')}@recigana.com" if destinatario else "usuarios@recigana.com"
        print("─" * 50)
        print(f"[EMAIL] Para : {correo_destino}")
        print("[EMAIL] Asunto: Notificación de ReciGana")
        print(f"[EMAIL] Cuerpo: {mensaje}")
        print("─" * 50)
        return True


class CanalSMSSimulado(CanalEnvio):
    """
    Simula el envío de un SMS. Otro ejemplo de canal intercambiable.
    """

    def enviar(self, destinatario, mensaje) -> bool:
        print(f"[SMS] -> {destinatario or 'usuario'}: {mensaje[:60]}")
        return True
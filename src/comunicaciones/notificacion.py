# Clase de notificación del sistema ReciGana
# Se usa para avisar a los usuarios sobre eventos importantes
# Ejemplo: "Tu oferta fue aceptada", "Nuevo material disponible"

from datetime import datetime  # Importamos datetime para registrar cuándo se creó la notificación


class Notificacion:
    """
    Representa una notificación enviada a un usuario de la plataforma.
    Las notificaciones nacen como no leídas y se marcan como leídas cuando el usuario las ve.
    """

    def __init__(self, id_notificacion, mensaje, destinatario=None):
        # Guardamos el identificador único de esta notificación
        self.__id_notificacion = id_notificacion

        # Validamos que el mensaje no esté vacío antes de guardarlo
        if not isinstance(mensaje, str) or len(mensaje.strip()) == 0:
            raise ValueError("El mensaje de la notificación no puede estar vacío.")

        # Guardamos el mensaje limpiando espacios al inicio y al final
        self.__mensaje = mensaje.strip()

        # Guardamos a quién va dirigida la notificación (puede ser None si es general)
        self.__destinatario = destinatario

        # Toda notificación empieza como NO leída cuando se crea
        self.__leida = False

        # Registramos automáticamente la fecha y hora exacta de creación
        # Formato: "2024-01-15 10:30:00"
        self.__fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ---------- Propiedades ----------
    # Las propiedades permiten leer los atributos privados desde fuera de la clase
    # sin poder modificarlos directamente (solo lectura)

    @property
    def id_notificacion(self):
        # Retorna el id único de esta notificación
        return self.__id_notificacion

    @property
    def mensaje(self):
        # Retorna el texto del mensaje de la notificación
        return self.__mensaje

    @property
    def leida(self):
        # Retorna True si ya fue leída, False si todavía no
        return self.__leida

    @property
    def destinatario(self):
        # Retorna el nombre del usuario al que va dirigida
        return self.__destinatario

    @property
    def fecha_creacion(self):
        # Retorna la fecha y hora en que se creó la notificación
        return self.__fecha_creacion

    # ---------- Métodos ----------

    def enviar(self):
        """
        Envía la notificación al destinatario.
        Si tiene destinatario lo menciona, si no envía de forma general.
        Retorna True para confirmar que el envío fue exitoso.
        """
        # Verificamos si hay un destinatario específico para personalizar el mensaje
        if self.__destinatario:
            # Si hay destinatario, lo incluimos en el mensaje de confirmación
            print(f"Notificación enviada a '{self.__destinatario}': {self.__mensaje}")
        else:
            # Si no hay destinatario, enviamos el mensaje de forma general
            print(f"Notificación enviada: {self.__mensaje}")

        # Retornamos True para indicar que el envío fue exitoso
        return True

    def marcar_como_leida(self):
        """
        Marca la notificación como leída.
        Si ya estaba leída, informa que no es necesario marcarla de nuevo.
        Retorna True si se marcó correctamente, False si ya estaba leída.
        """
        # Si ya fue leída antes, no hacemos nada y avisamos al usuario
        if self.__leida:
            print("Esta notificación ya fue leída anteriormente.")
            return False  # Retornamos False porque no hubo cambio

        # Cambiamos el estado de no leída a leída
        self.__leida = True

        # Confirmamos al usuario que se marcó correctamente
        print(f"Notificación #{self.__id_notificacion} marcada como leída.")

        # Retornamos True para indicar que el cambio fue exitoso
        return True

    def __str__(self):
        """
        Representación legible de la notificación cuando se imprime con print().
        Ejemplo: "[🔔 No leída] 2024-01-15 10:30:00 | Tu oferta fue aceptada"
        """
        # Mostramos ✅ si fue leída o 🔔 si todavía no
        estado = "✅ Leída" if self.__leida else "🔔 No leída"

        # Retornamos una cadena con el estado, la fecha y el mensaje
        return f"[{estado}] {self.__fecha_creacion} | {self.__mensaje}"
# Se usa para avisar a los usuarios sobre eventos importantes
# Ejemplo: "Tu oferta fue aceptada", "Nuevo material disponible"

from datetime import datetime  # Para registrar cuándo se creó la notificación
import copy                    # Para poder clonar notificaciones (Patrón Prototype)

# INYECCIÓN DE DEPENDENCIAS: importamos la interfaz y el canal por
# defecto. Notificacion ya no decide "cómo" enviar, solo delega
# ese trabajo al canal que le inyecten.
from src.comunicaciones.canal_envio import CanalEnvio, CanalConsola


class Notificacion:
    """
    Representa una notificación enviada a un usuario de la plataforma.
    Las notificaciones nacen como no leídas y se marcan como leídas
    cuando el usuario las ve.
    """

    def __init__(self, id_notificacion, mensaje, destinatario=None,
                 canal_envio: CanalEnvio = None):
        """
        Parámetro nuevo:
            canal_envio -- objeto que sabe CÓMO enviar el mensaje
                           (CanalConsola, CanalEmailSimulado, etc.)

        INYECCIÓN DE DEPENDENCIAS:
        Si no nos pasan ningún canal, usamos CanalConsola() por
        defecto para que TODO el código viejo (y los tests que ya
        existen) siga funcionando exactamente igual que antes.
        Si nos inyectan otro canal, Notificacion lo usa sin
        necesitar saber nada de cómo funciona por dentro.
        """
        # Guardamos el identificador único de esta notificación
        self.__id_notificacion = id_notificacion

        # Validamos que el mensaje no esté vacío antes de guardarlo
        if not isinstance(mensaje, str) or len(mensaje.strip()) == 0:
            raise ValueError("El mensaje de la notificación no puede estar vacío.")

        # Guardamos el mensaje limpiando espacios al inicio y al final
        self.__mensaje = mensaje.strip()

        # Guardamos a quién va dirigida (puede ser None si es general)
        self.__destinatario = destinatario

        # Toda notificación empieza como NO leída cuando se crea
        self.__leida = False

        # Registramos automáticamente la fecha y hora exacta de creación
        self.__fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # DEPENDENCIA INYECTADA: si no llega ninguna, usamos consola
        # por defecto. Esto se llama "inyección con valor por defecto"
        # y es una práctica común para no romper código existente.
        self.__canal = canal_envio if canal_envio is not None else CanalConsola()

    # ---------- Propiedades ----------
    # Las propiedades permiten leer los atributos privados desde fuera
    # de la clase sin poder modificarlos directamente

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

        INYECCIÓN DE DEPENDENCIAS: ya no imprimimos directamente
        aquí. Delegamos el "cómo enviar" al canal que nos inyectaron
        en el constructor (self.__canal). Notificacion ya no sabe
        ni le importa si eso es una consola, un email o un SMS.

        Retorna True para confirmar que el envío fue exitoso.
        """
        return self.__canal.enviar(self.__destinatario, self.__mensaje)

    def cambiar_canal(self, nuevo_canal: CanalEnvio):
        """
        INYECCIÓN DE DEPENDENCIAS (setter injection):
        Permite cambiar el canal de envío DESPUÉS de creada la
        notificación, sin tener que crear un objeto nuevo.

        Ejemplo:
            notif = Notificacion(1, "Hola", "María")
            notif.cambiar_canal(CanalEmailSimulado())
            notif.enviar()  # ahora se envía simulando un email
        """
        if not isinstance(nuevo_canal, CanalEnvio):
            raise ValueError("El canal debe implementar la interfaz CanalEnvio.")
        self.__canal = nuevo_canal

    def marcar_como_leida(self):
        """
        Marca la notificación como leída.
        Retorna True si se marcó, False si ya estaba leída.
        """
        # Si ya fue leída antes no hacemos nada
        if self.__leida:
            print("Esta notificación ya fue leída anteriormente.")
            return False

        # Cambiamos el estado a leída
        self.__leida = True
        print(f"Notificación #{self.__id_notificacion} marcada como leída.")
        return True

    def clonar(self, nuevo_destinatario=None, nuevo_mensaje=None):
        """
        PATRÓN PROTOTYPE — Clona esta notificación.

        ¿Para qué sirve?
        Imagina que el sistema necesita enviar el mismo aviso
        "Tu oferta fue aceptada" a 50 usuarios diferentes.
        En vez de crear 50 objetos Notificacion desde cero,
        creamos UNO y lo clonamos 50 veces cambiando solo
        el destinatario. Así ahorramos código y esfuerzo.

        Parámetros opcionales:
            nuevo_destinatario -- a quién va la copia
            nuevo_mensaje      -- mensaje de la copia

        Ejemplo de uso:
            base = Notificacion(1, "Tu oferta fue aceptada", "María")
            copia = base.clonar(nuevo_destinatario="Carlos")
            # copia tiene el mismo mensaje pero va dirigida a Carlos
        """
        # copy.deepcopy crea una copia COMPLETAMENTE independiente
        # del objeto original. Si cambias el clon, el original
        # no se ve afectado para nada
        clon = copy.deepcopy(self)

        # El clon siempre nace como NO leído, aunque el original
        # ya haya sido leído anteriormente
        # Usamos _Notificacion__ porque el atributo es privado
        clon._Notificacion__leida = False

        # Si nos pasan un nuevo destinatario lo aplicamos al clon
        if nuevo_destinatario is not None:
            clon._Notificacion__destinatario = nuevo_destinatario

        # Si nos pasan un nuevo mensaje lo aplicamos al clon
        if nuevo_mensaje is not None:
            clon._Notificacion__mensaje = nuevo_mensaje.strip()

        print(f"[Prototype] Notificación clonada para: {clon._Notificacion__destinatario}")
        return clon

    def __str__(self):
        """
        Representación legible cuando se imprime con print().
        Ejemplo: "[🔔 No leída] 2024-01-15 10:30:00 | Tu oferta fue aceptada"
        """
        if self.__leida:
            estado = "Leída"
        else:
            estado = "No leída"
        return f"[{estado}] {self.__fecha_creacion} | {self.__mensaje}"
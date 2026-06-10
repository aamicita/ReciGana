# Clase de negociación del sistema ReciGana
# Gestiona el proceso de negociación entre un ciudadano y un reciclador
# cuando acuerdan el precio de un material reciclable

from datetime import datetime  # Para registrar fechas de inicio y cierre


class Negociacion:
    """
    Representa el proceso de negociación entre un ciudadano (vendedor)
    y un reciclador (comprador) sobre el precio de un material reciclable.
    Ciclo de vida: pendiente → iniciada → finalizada o cancelada
    """

    # Estados válidos por los que puede pasar una negociación
    ESTADOS_VALIDOS = {"pendiente", "iniciada", "finalizada", "cancelada"}

    def __init__(self, id_negociacion, precio_final, estado, fecha_inicio, fecha_cierre=None):
        # Identificador único de esta negociación
        self.__id_negociacion = id_negociacion

        # Precio acordado al final de la negociación (puede cambiar con contra ofertas)
        if not isinstance(precio_final, (int, float)) or precio_final <= 0:
            raise ValueError("El precio final debe ser un número mayor a cero.")
        self.__precio_final = precio_final

        # Validamos que el estado inicial sea uno de los permitidos
        if estado not in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido. Use uno de: {self.ESTADOS_VALIDOS}")
        self.__estado = estado

        # Fecha en que comenzó la negociación (formato: "YYYY-MM-DD")
        self.__fecha_inicio = fecha_inicio

        # Fecha en que terminó la negociación (None si todavía no ha cerrado)
        self.__fecha_cierre = fecha_cierre

        # Guardamos el historial de contra ofertas para ver cómo evolucionó el precio
        # Cada entrada tiene el precio propuesto y la fecha en que se propuso
        self.__historial_contra_ofertas = []

    # ---------- Propiedades ----------

    @property
    def id_negociacion(self):
        # Permite leer el id de la negociación desde fuera de la clase
        return self.__id_negociacion

    @property
    def precio_final(self):
        # Retorna el precio actual acordado en la negociación
        return self.__precio_final

    @property
    def estado(self):
        # Retorna el estado actual de la negociación
        return self.__estado

    @property
    def fecha_inicio(self):
        # Retorna la fecha en que inició la negociación
        return self.__fecha_inicio

    @property
    def fecha_cierre(self):
        # Retorna la fecha en que cerró la negociación (None si sigue abierta)
        return self.__fecha_cierre

    @property
    def historial_contra_ofertas(self):
        # Retorna una copia del historial para no modificar el original
        return list(self.__historial_contra_ofertas)

    # ---------- Métodos ----------

    def iniciar_negociacion(self):
        """
        Inicia formalmente la negociación entre el ciudadano y el reciclador.
        Solo se puede iniciar si está en estado 'pendiente'.
        Retorna True si se inició correctamente.
        """
        # Verificamos que la negociación esté en estado pendiente antes de iniciarla
        if self.__estado != "pendiente":
            print(f"No se puede iniciar. Estado actual: '{self.__estado}'.")
            return False

        # Cambiamos el estado a iniciada para indicar que comenzó el proceso
        self.__estado = "iniciada"
        print(f"Negociación #{self.__id_negociacion} iniciada. Precio inicial: ${self.__precio_final}")
        return True

    def proponer_contra_oferta(self, nuevo_precio=None):
        """
        Permite proponer un nuevo precio durante la negociación.
        Solo se puede hacer si la negociación está 'iniciada'.
        Parámetro:
            nuevo_precio -- nuevo precio propuesto en dólares (opcional)
        Retorna True si se registró correctamente.
        """
        # No tiene sentido proponer una contra oferta si la negociación no está activa
        if self.__estado != "iniciada":
            print("Solo se pueden proponer contra ofertas en negociaciones iniciadas.")
            return False

        if nuevo_precio is None:
            # Si no se pasa precio, solo registramos que hubo intención de contra oferta
            print("Contra oferta propuesta sin nuevo precio.")
            return True

        # Validamos que el nuevo precio sea un número positivo
        if not isinstance(nuevo_precio, (int, float)) or nuevo_precio <= 0:
            raise ValueError("El nuevo precio debe ser un número mayor a cero.")

        # Guardamos la contra oferta en el historial con fecha y hora
        self.__historial_contra_ofertas.append({
            "precio": nuevo_precio,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        # Actualizamos el precio final con el nuevo precio propuesto
        self.__precio_final = nuevo_precio
        print(f"Contra oferta propuesta: nuevo precio ${nuevo_precio}")
        return True

    def finalizar_negociacion(self):
        """
        Finaliza la negociación cuando ambas partes llegaron a un acuerdo.
        Registra automáticamente la fecha de cierre.
        Solo se puede finalizar si está 'iniciada'.
        Retorna True si se finalizó correctamente.
        """
        # Solo podemos finalizar una negociación que esté en curso
        if self.__estado != "iniciada":
            print(f"No se puede finalizar. Estado actual: '{self.__estado}'.")
            return False

        # Cambiamos el estado a finalizada
        self.__estado = "finalizada"

        # Registramos automáticamente la fecha y hora de cierre
        self.__fecha_cierre = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"Negociación #{self.__id_negociacion} finalizada. "
              f"Precio acordado: ${self.__precio_final} | Cierre: {self.__fecha_cierre}")
        return True

    def cancelar_negociacion(self):
        """
        Cancela la negociación si no se llegó a un acuerdo.
        Se puede cancelar desde cualquier estado activo.
        Retorna True si se canceló correctamente.
        """
        # No tiene sentido cancelar algo que ya terminó
        if self.__estado in ("finalizada", "cancelada"):
            print(f"La negociación ya está '{self.__estado}', no se puede cancelar.")
            return False

        # Cambiamos el estado a cancelada
        self.__estado = "cancelada"

        # Registramos la fecha de cancelación
        self.__fecha_cierre = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"Negociación #{self.__id_negociacion} cancelada.")
        return True

    def __str__(self):
        # Representación legible de la negociación cuando se imprime con print()
        return (f"Negociación #{self.__id_negociacion} | "
                f"Estado: {self.__estado} | "
                f"Precio: ${self.__precio_final} | "
                f"Inicio: {self.__fecha_inicio} | "
                f"Cierre: {self.__fecha_cierre or 'En curso'}")
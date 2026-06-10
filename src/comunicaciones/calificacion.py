# Clase de calificación del sistema ReciGana


class Calificacion:
    """
    Representa la calificación que un usuario le da a otro
    después de completar un intercambio de materiales reciclables.
    Por ejemplo: un ciudadano califica al reciclador tras venderle material.
    """

    # Rango válido de puntaje en la plataforma
    PUNTAJE_MINIMO = 1
    PUNTAJE_MAXIMO = 5

    def __init__(self, id_calificacion, puntaje, comentario):
        self.__id_calificacion = id_calificacion

        # Validamos que el puntaje esté dentro del rango permitido (1 a 5)
        if not isinstance(puntaje, (int, float)) or not (self.PUNTAJE_MINIMO <= puntaje <= self.PUNTAJE_MAXIMO):
            raise ValueError(f"El puntaje debe estar entre {self.PUNTAJE_MINIMO} y {self.PUNTAJE_MAXIMO}.")
        self.__puntaje = puntaje

        # El comentario es opcional pero si se da debe ser texto
        if comentario is not None and not isinstance(comentario, str):
            raise ValueError("El comentario debe ser texto.")
        self.__comentario = comentario.strip() if comentario else ""

        # Estado interno para saber si ya fue registrada oficialmente
        self.__registrada = False

    # ---------- Propiedades ----------

    @property
    def id_calificacion(self):
        """Retorna el identificador único de la calificación."""
        return self.__id_calificacion

    @property
    def puntaje(self):
        """Retorna el puntaje de la calificación (1 a 5)."""
        return self.__puntaje

    @property
    def comentario(self):
        """Retorna el comentario asociado a la calificación."""
        return self.__comentario

    @property
    def registrada(self):
        """Retorna True si la calificación ya fue registrada."""
        return self.__registrada

    # ---------- Métodos ----------

    def registrar_calificacion(self):
        """
        Registra oficialmente la calificación en el sistema.
        Solo se puede registrar una vez.
        Retorna True si se registró correctamente.
        """
        if self.__registrada:
            print("Esta calificación ya fue registrada anteriormente.")
            return False

        self.__registrada = True
        print(f"Calificación registrada: {self.__puntaje} estrellas. Comentario: '{self.__comentario}'")
        return True

    def consultar_calificaciones(self):
        """
        Muestra el detalle completo de la calificación.
        Retorna un diccionario con los datos de la calificación.
        """
        detalle = {
            "id": self.__id_calificacion,
            "puntaje": self.__puntaje,
            "comentario": self.__comentario,
            "registrada": self.__registrada
        }
        print(f"Calificación #{self.__id_calificacion}: {self.__puntaje}⭐ - '{self.__comentario}'")
        return detalle

    def __str__(self):
        """Representación legible de la calificación."""
        estrellas = "⭐" * int(self.__puntaje)
        return f"Calificación {self.__id_calificacion}: {estrellas} | {self.__comentario}"
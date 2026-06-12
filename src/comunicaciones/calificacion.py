# Clase de calificación del sistema ReciGana
# Representa la calificación que un usuario le da a otro
# después de completar un intercambio de materiales reciclables

import copy  # Para poder clonar calificaciones (Patrón Prototype)


class Calificacion:
    """
    Representa la calificación que un usuario le da a otro
    después de completar un intercambio de materiales reciclables.
    Por ejemplo: un ciudadano califica al reciclador tras venderle material.
    """

    # Rango válido de puntaje en la plataforma (de 1 a 5 estrellas)
    PUNTAJE_MINIMO = 1
    PUNTAJE_MAXIMO = 5

    def __init__(self, id_calificacion, puntaje, comentario):
        # Guardamos el identificador único de esta calificación
        self.__id_calificacion = id_calificacion

        # Validamos que el puntaje esté dentro del rango permitido (1 a 5)
        if not isinstance(puntaje, (int, float)) or not (
            self.PUNTAJE_MINIMO <= puntaje <= self.PUNTAJE_MAXIMO
        ):
            raise ValueError(
                f"El puntaje debe estar entre "
                f"{self.PUNTAJE_MINIMO} y {self.PUNTAJE_MAXIMO}."
            )
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
        Retorna True si se registró, False si ya estaba registrada.
        """
        # Si ya fue registrada antes no hacemos nada
        if self.__registrada:
            print("Esta calificación ya fue registrada anteriormente.")
            return False

        # Marcamos como registrada
        self.__registrada = True
        print(
            f"Calificación registrada: {self.__puntaje} estrellas. "
            f"Comentario: '{self.__comentario}'"
        )
        return True

    def consultar_calificaciones(self):
        """
        Muestra el detalle completo de la calificación.
        Retorna un diccionario con los datos.
        """
        detalle = {
            "id": self.__id_calificacion,
            "puntaje": self.__puntaje,
            "comentario": self.__comentario,
            "registrada": self.__registrada
        }
        print(
            f"Calificación #{self.__id_calificacion}: "
            f"{self.__puntaje}⭐ - '{self.__comentario}'"
        )
        return detalle

    def clonar(self, nuevo_puntaje=None, nuevo_comentario=None):
        """
        PATRÓN PROTOTYPE — Clona esta calificación.

        ¿Para qué sirve?
        Imagina que María siempre le da 5 estrellas a los recicladores
        con comentarios muy parecidos. En vez de crear una calificación
        nueva desde cero cada vez, clonamos la base y solo cambiamos
        el comentario. Así reutilizamos el objeto base.

        Parámetros opcionales:
            nuevo_puntaje    -- puntaje de la copia (1 a 5)
            nuevo_comentario -- comentario de la copia

        Ejemplo de uso:
            base = Calificacion(1, 5, "Excelente servicio")
            copia = base.clonar(nuevo_comentario="Muy puntual")
            # copia tiene puntaje 5 pero diferente comentario
        """
        # Creamos una copia completamente independiente del original
        clon = copy.deepcopy(self)

        # El clon siempre nace como NO registrado, aunque el original
        # ya haya sido registrado antes
        clon._Calificacion__registrada = False

        # Si nos pasan un nuevo puntaje lo validamos y aplicamos
        if nuevo_puntaje is not None:
            if not (self.PUNTAJE_MINIMO <= nuevo_puntaje <= self.PUNTAJE_MAXIMO):
                raise ValueError(
                    f"El puntaje debe estar entre "
                    f"{self.PUNTAJE_MINIMO} y {self.PUNTAJE_MAXIMO}."
                )
            clon._Calificacion__puntaje = nuevo_puntaje

        # Si nos pasan un nuevo comentario lo aplicamos al clon
        if nuevo_comentario is not None:
            clon._Calificacion__comentario = nuevo_comentario.strip()

        print(f"[Prototype] Calificación clonada: {clon._Calificacion__puntaje}⭐")
        return clon

    def __str__(self):
        """Representación legible de la calificación."""
        estrellas = "⭐" * int(self.__puntaje)
        return f"Calificación {self.__id_calificacion}: {estrellas} | {self.__comentario}"
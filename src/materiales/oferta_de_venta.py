# Clase de oferta de venta

# Clase de oferta de venta del sistema ReciGana
# Representa la oferta que un reciclador hace sobre un material publicado por un ciudadano

from datetime import datetime  # Para registrar cuándo se creó o modificó la oferta


class OfertaDeVenta:
    """
    Representa una oferta económica que un reciclador hace
    sobre un material reciclable publicado por un ciudadano.
    Ciclo de vida: pendiente → aceptada o rechazada → cerrada
    """

    # Estados válidos que puede tener una oferta
    ESTADOS_VALIDOS = {"pendiente", "aceptada", "rechazada", "cerrada"}

    def __init__(self, id_oferta, precio_propuesto, estado="pendiente"):
        # Identificador único de esta oferta
        self.__id_oferta = id_oferta

        # Validamos que el precio sea un número positivo
        if not isinstance(precio_propuesto, (int, float)) or precio_propuesto <= 0:
            raise ValueError("El precio propuesto debe ser un número mayor a cero.")
        self.__precio_propuesto = precio_propuesto

        # Validamos que el estado inicial sea uno de los permitidos
        if estado not in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido. Use uno de: {self.ESTADOS_VALIDOS}")
        self.__estado = estado

        # Fecha y hora exacta en que se creó la oferta
        self.__fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Guardamos el historial de cambios de precio para trazabilidad
        self.__historial_precios = [{"precio": precio_propuesto, "fecha": self.__fecha_creacion}]

    # ---------- Propiedades ----------

    @property
    def id_oferta(self):
        # Retorna el identificador único de la oferta
        return self.__id_oferta

    @property
    def precio_propuesto(self):
        # Retorna el precio actual propuesto por el reciclador
        return self.__precio_propuesto

    @precio_propuesto.setter
    def precio_propuesto(self, valor):
        # Solo permite precios positivos mayores a cero
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise ValueError("El precio debe ser un número mayor a cero.")
        self.__precio_propuesto = valor

    @property
    def estado(self):
        # Retorna el estado actual de la oferta
        return self.__estado

    @estado.setter
    def estado(self, valor):
        # Solo permite cambiar a estados definidos en ESTADOS_VALIDOS
        if valor not in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido. Use uno de: {self.ESTADOS_VALIDOS}")
        self.__estado = valor

    @property
    def fecha_creacion(self):
        # Retorna la fecha en que se creó la oferta
        return self.__fecha_creacion

    @property
    def historial_precios(self):
        # Retorna una copia del historial de precios para no modificar el original
        return list(self.__historial_precios)

    # ---------- Métodos ----------

    def crear_oferta(self, descripcion=None):
        """
        Confirma la creación de la oferta en la plataforma.
        Parámetro:
            descripcion -- texto opcional que describe la oferta
        Retorna True si se creó correctamente.
        """
        # Solo se puede crear si está en estado pendiente
        if self.__estado != "pendiente":
            print("No se puede crear una oferta que ya fue procesada.")
            return False

        if descripcion:
            # Si hay descripción la mostramos junto con el precio
            print(f"Oferta #{self.__id_oferta} creada: {descripcion} | Precio: ${self.__precio_propuesto}")
        else:
            # Si no hay descripción mostramos solo el precio
            print(f"Oferta #{self.__id_oferta} creada | Precio: ${self.__precio_propuesto}")

        return True

    def modificar_oferta(self, nuevo_precio):
        """
        Modifica el precio de la oferta mientras esté pendiente.
        Parámetro:
            nuevo_precio -- nuevo precio propuesto en dólares
        Retorna True si se modificó correctamente.
        """
        # Solo se puede modificar si la oferta todavía está pendiente
        if self.__estado != "pendiente":
            print("Solo se pueden modificar ofertas en estado 'pendiente'.")
            return False

        # Validamos que el nuevo precio sea positivo
        if not isinstance(nuevo_precio, (int, float)) or nuevo_precio <= 0:
            raise ValueError("El nuevo precio debe ser un número mayor a cero.")

        # Guardamos el cambio en el historial de precios
        self.__historial_precios.append({
            "precio": nuevo_precio,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        # Actualizamos el precio actual
        self.__precio_propuesto = nuevo_precio
        print(f"Oferta #{self.__id_oferta} modificada. Nuevo precio: ${nuevo_precio}")
        return True

    def cerrar_oferta(self):
        """
        Cierra la oferta cuando ya fue procesada (aceptada o rechazada).
        Retorna True si se cerró correctamente.
        """
        # No tiene sentido cerrar una oferta que ya está cerrada
        if self.__estado == "cerrada":
            print("Esta oferta ya está cerrada.")
            return False

        # Cambiamos el estado a cerrada
        self.__estado = "cerrada"
        print(f"Oferta #{self.__id_oferta} cerrada.")
        return True

    def __str__(self):
        # Representación legible de la oferta cuando se imprime con print()
        return (f"Oferta #{self.__id_oferta} | "
                f"Precio: ${self.__precio_propuesto} | "
                f"Estado: {self.__estado} | "
                f"Creada: {self.__fecha_creacion}")

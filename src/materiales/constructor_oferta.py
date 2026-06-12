# Patrón Builder — Construcción paso a paso de una oferta de venta
# Archivo: modelos/materiales/constructor_oferta.py


class OfertaVentaBuilder:
    """
    Patrón Builder aplicado a la construcción de una OfertaDeVenta.

    Problema que resuelve:
    Una oferta de venta tiene muchos campos:
    material, precio, ciudadano que vende, foto, descripción,
    fecha, estado... Si pasáramos todo eso junto al constructor
    sería muy confuso y propenso a errores.

    Con Builder construimos la oferta PASO A PASO,
    como llenar un formulario campo por campo,
    y al final llamamos a construir() para obtener
    el objeto completo.

    Ejemplo de uso:
        oferta = (OfertaVentaBuilder()
                    .con_material("cartón", 10)
                    .con_precio(5.00)
                    .con_ciudadano("María López")
                    .con_descripcion("Cartón limpio y seco")
                    .construir())
    """

    def __init__(self):
        # Empezamos con un diccionario vacío que iremos llenando
        self.__datos = {
            "material":    None,
            "peso_kg":     None,
            "precio":      None,
            "ciudadano":   None,
            "descripcion": "",
            "foto":        None,
            "estado":      "disponible",
        }

    def con_material(self, tipo, peso_kg):
        """Paso 1: Definir qué material se vende y cuánto pesa."""
        self.__datos["material"] = tipo
        self.__datos["peso_kg"]  = peso_kg
        return self  # Retornamos self para encadenar pasos

    def con_precio(self, precio):
        """Paso 2: Definir el precio que pide el ciudadano."""
        if not isinstance(precio, (int, float)) or precio <= 0:
            raise ValueError("El precio debe ser mayor a cero.")
        self.__datos["precio"] = precio
        return self

    def con_ciudadano(self, nombre_ciudadano):
        """Paso 3: Indicar qué ciudadano publica esta oferta."""
        self.__datos["ciudadano"] = nombre_ciudadano
        return self

    def con_descripcion(self, descripcion):
        """Paso 4 (opcional): Agregar descripción del material."""
        self.__datos["descripcion"] = descripcion
        return self

    def con_foto(self, foto):
        """Paso 5 (opcional): Agregar foto del material."""
        self.__datos["foto"] = foto
        return self

    def construir(self):
        """
        Paso final: Valida que los campos obligatorios estén
        completos y retorna el diccionario con la oferta lista.
        """
        # Verificamos que los campos obligatorios no sean None
        campos_obligatorios = ["material", "peso_kg", "precio", "ciudadano"]
        for campo in campos_obligatorios:
            if self.__datos[campo] is None:
                raise ValueError(
                    f"Falta el campo obligatorio '{campo}' para construir la oferta."
                )

        print(
            f"[Builder] Oferta construida: "
            f"{self.__datos['material']} | "
            f"{self.__datos['peso_kg']} kg | "
            f"${self.__datos['precio']} | "
            f"Ciudadano: {self.__datos['ciudadano']}"
        )
        # Retornamos una copia del diccionario para no exponer el interno
        return dict(self.__datos)
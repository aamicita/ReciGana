# Clase de material reciclable del sistema ReciGana
# Representa cualquier material que un ciudadano publica para vender


class MaterialReciclable:
    """
    Representa un material reciclable publicado en la plataforma.
    Ejemplos: plástico, cartón, metal, vidrio, papel.
    """

    # Tipos de materiales aceptados en la plataforma
    TIPOS_VALIDOS = {"plastico", "carton", "metal", "vidrio", "papel", "organico"}

    # Estados posibles de un material durante su ciclo de vida
    ESTADOS_VALIDOS = {"disponible", "en_negociacion", "vendido"}

    def __init__(self, id_material, tipo_material, cantidad, peso, estado="disponible"):
        # Identificador único del material
        self.__id_material = id_material

        # Validamos que el tipo sea uno de los aceptados por la plataforma
        if tipo_material.lower() not in self.TIPOS_VALIDOS:
            raise ValueError(f"Tipo de material inválido. Use uno de: {self.TIPOS_VALIDOS}")
        self.__tipo_material = tipo_material.lower()

        # Validamos que la cantidad sea un número entero positivo
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("La cantidad debe ser un número entero mayor a cero.")
        self.__cantidad = cantidad

        # Validamos que el peso sea un número positivo (en kg)
        if not isinstance(peso, (int, float)) or peso <= 0:
            raise ValueError("El peso debe ser un número mayor a cero.")
        self.__peso = peso

        # Validamos que el estado inicial sea uno de los permitidos
        if estado not in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido. Use uno de: {self.ESTADOS_VALIDOS}")
        self.__estado = estado

    # ---------- Propiedades ----------

    @property
    def id_material(self):
        # Retorna el identificador único del material
        return self.__id_material

    @property
    def tipo_material(self):
        # Retorna el tipo de material (plastico, carton, etc.)
        return self.__tipo_material

    @property
    def cantidad(self):
        # Retorna la cantidad de unidades del material
        return self.__cantidad

    @property
    def peso(self):
        # Retorna el peso total del material en kg
        return self.__peso

    @property
    def estado(self):
        # Retorna el estado actual del material
        return self.__estado

    @estado.setter
    def estado(self, valor):
        # Solo permite cambiar a un estado válido definido en ESTADOS_VALIDOS
        if valor not in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido. Use uno de: {self.ESTADOS_VALIDOS}")
        self.__estado = valor

    # ---------- Métodos ----------

    def clasificar(self):
        """
        Clasifica el material según su tipo.
        Retorna la categoría a la que pertenece el material.
        """
        # Definimos a qué categoría pertenece cada tipo de material
        categorias = {
            "plastico": "Reciclable seco",
            "carton": "Reciclable seco",
            "metal": "Reciclable seco",
            "vidrio": "Reciclable seco",
            "papel": "Reciclable seco",
            "organico": "Biodegradable"
        }

        # Buscamos la categoría del tipo actual
        categoria = categorias.get(self.__tipo_material, "Sin clasificar")
        print(f"Material '{self.__tipo_material}' clasificado como: {categoria}")
        return categoria

    def calcular_valor(self, precio_por_kg=None):
        """
        Calcula el valor del material según el precio por kg.
        Si no se pasa precio retorna 0 (valor desconocido).
        Parámetro:
            precio_por_kg -- precio en dólares por cada kg (opcional)
        Retorna el valor total calculado.
        """
        # Si no se pasa precio no podemos calcular el valor
        if precio_por_kg is None:
            return 0

        # Validamos que el precio sea un número positivo
        if not isinstance(precio_por_kg, (int, float)) or precio_por_kg <= 0:
            raise ValueError("El precio por kg debe ser un número mayor a cero.")

        # Calculamos el valor total: peso * precio por kg
        valor_total = self.__peso * precio_por_kg
        print(f"Valor del material: {self.__peso} kg x ${precio_por_kg} = ${valor_total:.2f}")
        return valor_total

    def __str__(self):
        # Representación legible del material cuando se imprime con print()
        return (f"Material #{self.__id_material} | "
                f"Tipo: {self.__tipo_material} | "
                f"Peso: {self.__peso} kg | "
                f"Estado: {self.__estado}")
# Clase de material reciclable del sistema ReciGana
# Representa cualquier material que un ciudadano publica para vender


class MaterialReciclable:
    """
    Representa un material reciclable publicado en la plataforma.
    Ejemplos: plástico, cartón, metal, vidrio, papel.
    """

    TIPOS_VALIDOS = {"plastico", "carton", "metal", "vidrio", "papel", "organico"}
    ESTADOS_VALIDOS = {"disponible", "en_negociacion", "vendido"}

    RECICLABLE_SECO = "Reciclable seco"
    BIODEGRADABLE = "Biodegradable"
    SIN_CLASIFICAR = "Sin clasificar"

    # Mapa de categorías definido a nivel de clase (evita recrearlo en cada llamada)
    _CATEGORIAS = {
        "plastico": "Reciclable seco",
        "carton":   "Reciclable seco",
        "metal":    "Reciclable seco",
        "vidrio":   "Reciclable seco",
        "papel":    "Reciclable seco",
        "organico": "Biodegradable",
    }

    def __init__(self, id_material, tipo_material, cantidad, peso, estado="disponible"):
        self.__id_material = id_material

        tipo = tipo_material.lower()
        if tipo not in self.TIPOS_VALIDOS:
            raise ValueError(f"Tipo inválido. Use uno de: {self.TIPOS_VALIDOS}")
        self.__tipo_material = tipo

        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("La cantidad debe ser un entero mayor a cero.")
        self.__cantidad = cantidad

        if not isinstance(peso, (int, float)) or peso <= 0:
            raise ValueError("El peso debe ser un número mayor a cero.")
        self.__peso = float(peso)  # Normalizado siempre a float

        if estado not in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido. Use uno de: {self.ESTADOS_VALIDOS}")
        self.__estado = estado

    # ---------- Propiedades ----------

    @property
    def id_material(self):
        return self.__id_material

    @property
    def tipo_material(self):
        return self.__tipo_material

    @property
    def cantidad(self):
        return self.__cantidad

    @property
    def peso(self):
        return self.__peso

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, valor):
        if valor not in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido. Use uno de: {self.ESTADOS_VALIDOS}")
        self.__estado = valor

    # ---------- Métodos ----------

    def clasificar(self) -> str:                          # ✅ Indentación corregida
        """
        Clasifica el material según su tipo.
        Retorna la categoría correspondiente.
        """
        categoria = self._CATEGORIAS.get(self.__tipo_material, self.SIN_CLASIFICAR)
        print(f"Material '{self.__tipo_material}' clasificado como: {categoria}")
        return categoria

    def calcular_valor(self, precio_por_kg: float = None) -> float:
        """
        Calcula el valor total del material (peso × precio_por_kg).
        Retorna 0 si no se proporciona precio.
        """
        if precio_por_kg is None:
            return 0.0

        if not isinstance(precio_por_kg, (int, float)) or precio_por_kg <= 0:
            raise ValueError("El precio por kg debe ser un número mayor a cero.")

        valor_total = self.__peso * precio_por_kg
        print(f"Valor: {self.__peso} kg × ${precio_por_kg} = ${valor_total:.2f}")
        return valor_total

    def __str__(self) -> str:
        return (
            f"Material #{self.__id_material} | "
            f"Tipo: {self.__tipo_material} | "
            f"Peso: {self.__peso} kg | "
            f"Estado: {self.__estado}"
        )
# Clase de reporte del sistema ReciGana
# Genera y exporta reportes sobre la actividad de la plataforma

from datetime import datetime  # Para registrar cuándo se generó el reporte


class Reporte:
    """
    Representa un reporte de actividad de la plataforma ReciGana.
    Puede ser un reporte de ventas, usuarios activos, materiales más reciclados, etc.
    """

    # Tipos de reporte válidos en la plataforma
    TIPOS_VALIDOS = {"ventas", "usuarios", "materiales", "ofertas"}

    def __init__(self, id_reporte, fecha, tipo_reporte, contenido):
        # Identificador único del reporte
        self.__id_reporte = id_reporte

        # Fecha del período que cubre el reporte (ej: "2024-01-15")
        self.__fecha = fecha

        # Validamos que el tipo de reporte sea uno de los permitidos
        if tipo_reporte not in self.TIPOS_VALIDOS:
            raise ValueError(f"Tipo de reporte inválido. Use uno de: {self.TIPOS_VALIDOS}")
        self.__tipo_reporte = tipo_reporte

        # Contenido del reporte: diccionario con los datos a reportar
        if not isinstance(contenido, dict):
            raise ValueError("El contenido debe ser un diccionario con los datos del reporte.")
        self.__contenido = contenido

        # Fecha y hora exacta en que se creó este objeto reporte
        self.__fecha_generacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Estado del reporte: False = no generado, True = ya generado
        self.__generado = False

    # ---------- Propiedades ----------

    @property
    def id_reporte(self):
        # Retorna el identificador del reporte
        return self.__id_reporte

    @property
    def fecha(self):
        # Retorna la fecha del período reportado
        return self.__fecha

    @property
    def tipo_reporte(self):
        # Retorna el tipo de reporte (ventas, usuarios, etc.)
        return self.__tipo_reporte

    @property
    def contenido(self):
        # Retorna una copia del contenido para no modificar el original
        return dict(self.__contenido)

    @property
    def generado(self):
        # Retorna True si el reporte ya fue generado
        return self.__generado

    # ---------- Métodos ----------

    def generar_reporte(self):
        """
        Genera el reporte mostrando todos los datos del contenido.
        Solo se puede generar una vez.
        Retorna el contenido del reporte como diccionario.
        """
        # Evitamos generar el mismo reporte dos veces
        if self.__generado:
            print("Este reporte ya fue generado anteriormente.")
            return self.__contenido

        # Marcamos el reporte como generado
        self.__generado = True

        # Mostramos el encabezado del reporte
        print(f"===== REPORTE DE {self.__tipo_reporte.upper()} =====")
        print(f"Fecha del período : {self.__fecha}")
        print(f"Generado el       : {self.__fecha_generacion}")
        print("Datos:")

        # Recorremos e imprimimos cada dato del contenido
        for clave, valor in self.__contenido.items():
            print(f"  - {clave}: {valor}")

        print("=" * 40)
        return self.__contenido

    def exportar_pdf(self):
        """
        Simula la exportación del reporte a PDF.
        Solo se puede exportar si el reporte fue generado primero.
        Retorna el nombre del archivo generado.
        """
        # No permitimos exportar si el reporte no ha sido generado
        if not self.__generado:
            print("Debes generar el reporte antes de exportarlo.")
            return None

        # Creamos el nombre del archivo con el tipo y la fecha
        nombre_archivo = f"reporte_{self.__tipo_reporte}_{self.__fecha}.pdf"

        print(f"Reporte exportado como: {nombre_archivo}")
        return nombre_archivo

    def __str__(self):
        # Representación legible del reporte cuando se imprime con print()
        estado = "Generado" if self.__generado else "Pendiente"
        return f"Reporte #{self.__id_reporte} | Tipo: {self.__tipo_reporte} | Fecha: {self.__fecha} | Estado: {estado}"
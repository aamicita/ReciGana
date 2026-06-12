# Patrón Builder — Construcción paso a paso de un Reporte

from .reporte import Reporte


class ReporteBuilder:
    """
    PATRÓN BUILDER aplicado a la construcción de Reportes.

    ¿Qué problema resuelve?
    La clase Reporte necesita varios datos para crearse:
    un ID, una fecha, un tipo y un contenido. Si pasamos
    todo junto al constructor puede ser confuso y propenso
    a errores, especialmente si en el futuro se agregan
    más campos opcionales.

    Con Builder construimos el reporte PASO A PASO,
    como llenar un formulario campo por campo, y al final
    llamamos a construir() para obtener el objeto completo.
    Si falta algún campo obligatorio, Builder nos avisa
    con un error claro antes de crear el objeto.

    Ejemplo de uso:
        reporte = (ReporteBuilder()
                    .con_id(1)
                    .con_fecha("2025-06-01")
                    .con_tipo("ventas")
                    .con_contenido({"total_ventas": 15})
                    .construir())
    """

    def __init__(self):
        # Iniciamos todos los campos en None
        # Iremos llenándolos paso a paso con cada método
        self.__id_reporte = None  # Identificador del reporte
        self.__fecha      = None  # Fecha del período que cubre
        self.__tipo       = None  # Tipo: ventas, usuarios, materiales, ofertas
        self.__contenido  = None  # Diccionario con los datos del reporte

    def con_id(self, id_reporte):
        """
        Paso 1: Asignar el identificador del reporte.
        Retornamos self para poder encadenar los pasos seguidos.
        Ejemplo: .con_id(1).con_fecha("2025-06-01")...
        """
        self.__id_reporte = id_reporte
        return self  # Retornamos self para encadenar pasos

    def con_fecha(self, fecha):
        """
        Paso 2: Asignar la fecha del período reportado.
        Formato esperado: 'YYYY-MM-DD'
        Ejemplo: '2025-06-01'
        """
        self.__fecha = fecha
        return self  # Retornamos self para encadenar pasos

    def con_tipo(self, tipo):
        """
        Paso 3: Asignar el tipo de reporte.
        Solo se aceptan estos tipos:
            - 'ventas'     → reporte de ventas de materiales
            - 'usuarios'   → reporte de usuarios registrados
            - 'materiales' → reporte de materiales publicados
            - 'ofertas'    → reporte de ofertas realizadas
        Si el tipo no es válido lanza un error inmediatamente.
        """
        # Lista de tipos permitidos en la plataforma
        tipos_validos = {"ventas", "usuarios", "materiales", "ofertas"}

        # Si el tipo no está en la lista lanzamos error
        if tipo not in tipos_validos:
            raise ValueError(
                f"Tipo inválido '{tipo}'. "
                f"Use uno de: {tipos_validos}"
            )
        self.__tipo = tipo
        return self  # Retornamos self para encadenar pasos

    def con_contenido(self, contenido):
        """
        Paso 4: Asignar el contenido del reporte.
        Debe ser un diccionario con los datos a mostrar.
        Ejemplo: {"total_ventas": 15, "ingresos_USD": 300.0}
        Si no es un diccionario lanza un error.
        """
        # Verificamos que sea un diccionario
        if not isinstance(contenido, dict):
            raise ValueError(
                "El contenido debe ser un diccionario. "
                "Ejemplo: {'total_ventas': 15}"
            )
        self.__contenido = contenido
        return self  # Retornamos self para encadenar pasos

    def construir(self):
        """
        Paso final: Valida que todos los campos obligatorios
        estén completos y crea el objeto Reporte.

        Si falta algún campo obligatorio lanza un ValueError
        con un mensaje claro indicando qué falta.

        Retorna una instancia de Reporte lista para usar.
        """
        # Revisamos uno por uno que ningún campo esté vacío
        # Si falta alguno avisamos exactamente cuál es
        if self.__id_reporte is None:
            raise ValueError(
                "Falta el ID del reporte. Usa .con_id()"
            )
        if self.__fecha is None:
            raise ValueError(
                "Falta la fecha del reporte. Usa .con_fecha()"
            )
        if self.__tipo is None:
            raise ValueError(
                "Falta el tipo de reporte. Usa .con_tipo()"
            )
        if self.__contenido is None:
            raise ValueError(
                "Falta el contenido del reporte. Usa .con_contenido()"
            )

        # Todo está completo, informamos que el reporte fue construido
        print(
            f"[Builder] Reporte construido exitosamente: "
            f"#{self.__id_reporte} | "
            f"Tipo: {self.__tipo} | "
            f"Fecha: {self.__fecha}"
        )

        # Creamos y retornamos el objeto Reporte con todos los datos
        # A partir de aquí ya puedes llamar a reporte.generar_reporte()
        # o reporte.exportar_pdf()
        return Reporte(
            self.__id_reporte,
            self.__fecha,
            self.__tipo,
            self.__contenido
        )
# Clase de reporte

class Reporte:
    def __init__(self, id_reporte, fecha, tipo_reporte, contenido):
        self.__id_reporte = id_reporte
        self.__fecha = fecha
        self.__tipo_reporte = tipo_reporte
        self.__contenido = contenido

    def generar_reporte(self):
        print("Reporte generado")

    def exportar_pdf(self):
        print("Exportando reporte a PDF")

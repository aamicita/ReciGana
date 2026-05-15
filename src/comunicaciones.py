# Clases de comunicacion y reportes

class Notificacion:
    def __init__(self, id_notificacion, mensaje):
        self.__id_notificacion = id_notificacion
        self.__mensaje = mensaje
        self.__leida = False

    def enviar(self):
        print("Notificacion enviada")

    def marcar_como_leida(self):
        self.__leida = True
        print("Notificacion marcada como leida")


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


class HistorialDeReciclaje:
    def __init__(self, id_historial):
        self.__id_historial = id_historial

    def consultar_historial(self):
        print("Consultando historial")

    def filtrar_por_fecha(self, fecha):
        print(f"Filtrando historial por fecha {fecha}")


class Calificacion:
    def __init__(self, id_calificacion, puntaje, comentario):
        self.__id_calificacion = id_calificacion
        self.__puntaje = puntaje
        self.__comentario = comentario

    def registrar_calificacion(self):
        print("Calificacion registrada")

    def consultar_calificaciones(self):
        print("Consultando calificaciones")

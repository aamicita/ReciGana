# Clases de comunicacion y reportes

class Notificacion:
    def __init__(self, id_notificacion, mensaje):
        self.__id_notificacion = id_notificacion
        self.__mensaje = mensaje
        self.__leida = False

    @property
    def id_notificacion(self):
        return self.__id_notificacion

    @property
    def mensaje(self):
        return self.__mensaje

    @property
    def leida(self):
        return self.__leida

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

    @property
    def id_reporte(self):
        return self.__id_reporte

    @property
    def fecha(self):
        return self.__fecha

    @property
    def tipo_reporte(self):
        return self.__tipo_reporte

    @property
    def contenido(self):
        return self.__contenido

    def generar_reporte(self):
        print("Reporte generado")

    def exportar_pdf(self):
        print("Exportando reporte a PDF")


class HistorialDeReciclaje:
    # inyectar la dependencia 'registros' en el constructor

    def __init__(self, id_historial, registros=None):
        self.__id_historial = id_historial
        # si no pasan nada, entonces empieza con una lista vacia
        self.__registros = registros if registros is not None else []

    def consultar_historial(self):
        print(f"Consultando historial {self.__id_historial}")
        if not self.__registros:
            print("No hay registros en el historial")
            return
        for _ in self.__registros:  # S1481: variable no usada → reemplazada por _
            pass

    def filtrar_por_fecha(self, fecha):  # S5603: función movida al nivel correcto de indentación
        print(f"Filtrando historial por fecha {fecha}")


class Calificacion:
    def __init__(self, id_calificacion, puntaje, comentario):
        self.__id_calificacion = id_calificacion
        self.__puntaje = puntaje
        self.__comentario = comentario

    @property
    def id_calificacion(self):
        return self.__id_calificacion

    @property
    def puntaje(self):
        return self.__puntaje

    @property
    def comentario(self):
        return self.__comentario

    def registrar_calificacion(self):
        print("Calificacion registrada")

    def consultar_calificaciones(self):
        print("Consultando calificaciones")
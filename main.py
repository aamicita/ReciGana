from src.usuarios import Administrador, Ciudadano, Reciclador
from src.materiales import MaterialReciclable, OfertaDeVenta, Negociacion
from src.comunicaciones import Notificacion, Reporte, HistorialDeReciclaje, Calificacion


def main():
    admin = Administrador(1, "Ana", "099000111", "ana@recigana.com", "1234")
    ciudadano = Ciudadano(2, "Luis", "099000222", "luis@recigana.com", "1234", "Av. Central")
    reciclador = Reciclador(3, "Marta", "099000333", "marta@recigana.com", "1234", "Zona Norte")

    admin.iniciar_sesion()
    ciudadano.publicar_material("plastico", 5)
    ciudadano.publicar_material("carton", 3, "foto.jpg")
    reciclador.consultar_ofertas()

    material = MaterialReciclable(1, "plastico", 2, 5, "disponible")
    oferta = OfertaDeVenta(1, 10, "abierta")
    negociacion = Negociacion(1, 12, "pendiente", "2026-05-15")

    material.clasificar()
    oferta.crear_oferta()
    oferta.crear_oferta("Oferta con descripcion")
    negociacion.iniciar_negociacion()

    notificacion = Notificacion(1, "Tienes una nueva oferta")
    reporte = Reporte(1, "2026-05-15", "mensual", "contenido")
    historial = HistorialDeReciclaje(1)
    calificacion = Calificacion(1, 5, "Buen servicio")

    notificacion.enviar()
    reporte.generar_reporte()
    historial.consultar_historial()
    calificacion.registrar_calificacion()


if __name__ == "__main__":
    main()

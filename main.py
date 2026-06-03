"""
Módulo principal de ReciGana - Sistema de gestión de reciclaje
"""
from src.usuarios import Administrador, Ciudadano, Reciclador
from src.materiales import MaterialReciclable, OfertaDeVenta, Negociacion
from src.comunicaciones import (
    Notificacion,
    Reporte,
    HistorialDeReciclaje,
    Calificacion,
)


def main():
    """
    Función principal que inicializa y demuestra las funcionalidades del sistema.
    """
    try:
        # Crear usuarios
        admin = Administrador(
            1, "Ana", "099000111", "ana@recigana.com", "1234"
        )
        ciudadano = Ciudadano(
            2, "Luis", "099000222", "luis@recigana.com", "1234", "Av. Central"
        )
        reciclador = Reciclador(
            3, "Marta", "099000333", "marta@recigana.com", "1234", "Zona Norte"
        )

        # Operaciones de administrador
        admin.iniciar_sesion()

        # Operaciones de ciudadano
        ciudadano.publicar_material("plastico", 5)
        ciudadano.publicar_material("carton", 3, "foto.jpg")

        # Operaciones de reciclador
        reciclador.consultar_ofertas()

        # Crear y procesar materiales
        material = MaterialReciclable(1, "plastico", 2, 5, "disponible")
        material.clasificar()

        # Crear y procesar oferta
        oferta = OfertaDeVenta(1, 10, "abierta")
        oferta.crear_oferta()
        oferta.crear_oferta("Oferta con descripcion")

        # Crear y procesar negociación
        negociacion = Negociacion(1, 12, "pendiente", "2026-05-15")
        negociacion.iniciar_negociacion()

        # Comunicaciones
        notificacion = Notificacion(1, "Tienes una nueva oferta")
        notificacion.enviar()

        reporte = Reporte(1, "2026-05-15", "mensual", "contenido")
        reporte.generar_reporte()

        historial = HistorialDeReciclaje(1)
        historial.consultar_historial()

        calificacion = Calificacion(1, 5, "Buen servicio")
        calificacion.registrar_calificacion()

    except Exception as e:
        print(f"Error en la ejecución principal: {e}")
        raise


if __name__ == "__main__":
    main()

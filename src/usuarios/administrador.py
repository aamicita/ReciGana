# Herencia: Administrador hereda de Usuarios
from .usuario import Usuarios


class Administrador(Usuarios):
    def __init__(self, id_usuario, nombre, telefono, correo, contrasenia):
        # Uso de super() para inicializar atributos heredados
        super().__init__(id_usuario, nombre, telefono, correo, contrasenia)

    def gestionar_usuarios(self):
        print("Gestionando usuarios...")

    def gestionar_recicladores(self):
        print("Gestionando recicladores...")

    def gestionar_ofertas(self):
        print("Gestionando ofertas...")

    def generar_reporte(self):
        print("Generando reporte...")

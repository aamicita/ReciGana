# Herencia: Reciclador hereda de Usuarios
from .usuario import Usuarios


class Reciclador(Usuarios):
    def __init__(self, id_usuario, nombre, telefono, correo, contrasenia, zona_cobertura):
        super().__init__(id_usuario, nombre, telefono, correo, contrasenia)
        self.__zona_cobertura = zona_cobertura  # Encapsulamiento

    @property
    def zona_cobertura(self):
        return self.__zona_cobertura

    @zona_cobertura.setter
    def zona_cobertura(self, valor):
        if valor:
            self.__zona_cobertura = valor

    def registrarse(self):
        print("Reciclador registrado")

    def consultar_ofertas(self):
        print("Consultando ofertas...")

    def aceptar_oferta(self):
        print("Oferta aceptada por reciclador")

    def realizar_oferta(self):
        print("Oferta realizada")

    def rechazar_oferta(self):
        print("Oferta rechazada por reciclador")

# Herencia: Ciudadano hereda de Usuarios
from .usuario import Usuarios


class Ciudadano(Usuarios):
    def __init__(self, id_usuario, nombre, telefono, correo, contrasenia, direccion):
        super().__init__(id_usuario, nombre, telefono, correo, contrasenia)
        self.__direccion = direccion  # Encapsulamiento

    @property
    def direccion(self):
        return self.__direccion

    @direccion.setter
    def direccion(self, valor):
        if valor:
            self.__direccion = valor

    def registrar(self):
        print("Ciudadano registrado")

    # Sobrecarga simulada con parametro por defecto
    def publicar_material(self, tipo, peso, foto=None):
        if foto:
            print(f"Publicando material con foto: {tipo}, {peso} kg")
        else:
            print(f"Publicando material: {tipo}, {peso} kg")

    def aceptar_oferta(self):
        print("Oferta aceptada")

    def rechazar_oferta(self):
        print("Oferta rechazada")

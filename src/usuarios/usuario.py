# Clase base de usuarios (herencia y encapsulamiento)

class Usuarios:
    # Encapsulamiento: atributos privados con __
    def __init__(self, id_usuario, nombre, telefono, correo, contrasenia):
        self.__id = id_usuario
        self.__nombre = nombre
        self.__telefono = telefono
        self.__correo = correo
        self.__contrasenia = contrasenia
        self._sesion_activa = False  # protegido

    # Propiedades con @property y @setter
    @property
    def id(self):
        return self.__id

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if valor:
            self.__nombre = valor

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        if valor:
            self.__telefono = valor

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if valor and "@" in valor:
            self.__correo = valor

    @property
    def contrasenia(self):
        return self.__contrasenia

    @contrasenia.setter
    def contrasenia(self, valor):
        if valor and len(valor) >= 4:
            self.__contrasenia = valor

    def iniciar_sesion(self):
        self._sesion_activa = True
        print(f"Sesion iniciada para {self.__nombre}")

    def cerrar_sesion(self):
        self._sesion_activa = False
        print(f"Sesion cerrada para {self.__nombre}")

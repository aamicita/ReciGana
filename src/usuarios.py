# Clases de usuarios (herencia y encapsulamiento)

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


# Herencia: Administrador hereda de Usuarios
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


# Herencia: Ciudadano hereda de Usuarios
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


# Herencia: Reciclador hereda de Usuarios
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

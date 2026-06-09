# Clase base de usuarios (herencia y encapsulamiento)

import hashlib
import re


class Usuarios:
    """
    Clase base para todos los usuarios del sistema ReciGana.
    Representa a cualquier persona registrada en la plataforma.
    """

    ROLES_VALIDOS = {"ciudadano", "administrador"}

    def __init__(self, id_usuario, nombre, telefono, correo, contrasenia, rol="ciudadano"):
        self.__id = id_usuario
        self.__nombre = nombre
        self.__telefono = telefono
        self.__correo = correo
        self.__contrasenia = self.__encriptar(contrasenia)
        self.__rol = rol if rol in self.ROLES_VALIDOS else "ciudadano"
        self._sesion_activa = False

    # ---------- Encriptación ----------

    @staticmethod
    def __encriptar(contrasenia):
        """Convierte la contraseña en un hash SHA-256 para no guardarla en texto plano."""
        return hashlib.sha256(contrasenia.encode()).hexdigest()

    def verificar_contrasenia(self, contrasenia):
        """Verifica si la contraseña ingresada es correcta."""
        return self.__contrasenia == self.__encriptar(contrasenia)

    # ---------- Propiedades ----------

    @property
    def id(self):
        return self.__id

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if isinstance(valor, str) and len(valor.strip()) >= 2:
            self.__nombre = valor.strip()
        else:
            raise ValueError("El nombre debe tener al menos 2 caracteres.")

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        if isinstance(valor, str) and valor.strip().isdigit() and len(valor.strip()) >= 7:
            self.__telefono = valor.strip()
        else:
            raise ValueError("El teléfono debe contener solo dígitos y tener al menos 7 caracteres.")

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        patron = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
        if isinstance(valor, str) and re.match(patron, valor):
            self.__correo = valor.lower()
        else:
            raise ValueError("El correo no tiene un formato válido.")

    @property
    def rol(self):
        return self.__rol

    @property
    def sesion_activa(self):
        return self._sesion_activa

    # ---------- Métodos ----------

    def iniciar_sesion(self, contrasenia):
        """Inicia sesión verificando la contraseña."""
        if self.verificar_contrasenia(contrasenia):
            self._sesion_activa = True
            return True
        return False

    def cerrar_sesion(self):
        """Cierra la sesión activa del usuario."""
        self._sesion_activa = False

    def es_administrador(self):
        """Retorna True si el usuario tiene rol de administrador."""
        return self.__rol == "administrador"

    def __str__(self):
        return f"[{self.__rol.upper()}] {self.__nombre} ({self.__correo})"

    def __repr__(self):
        return f"Usuarios(id={self.__id}, nombre={self.__nombre}, rol={self.__rol})"
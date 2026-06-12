# Patrón Abstract Factory — Fábrica de usuarios
# Archivo: modelos/usuarios/fabrica_usuarios.py

from abc import ABC, abstractmethod
from src.usuarios.ciudadano import Ciudadano
from src.usuarios.reciclador import Reciclador
from src.usuarios.administrador import Administrador


# ---------- Fábrica abstracta ----------
# Esta es la "plantilla" que dice qué métodos debe tener
# cualquier fábrica de usuarios.

class FabricaUsuariosBase(ABC):
    """
    Clase abstracta que define QUÉ debe poder crear
    cualquier fábrica de usuarios.
    No se puede instanciar directamente, solo sirve de plantilla.
    """

    @abstractmethod
    def crear_ciudadano(self, id_u, nombre, telefono, correo, contrasenia, direccion):
        """Crea y retorna un objeto Ciudadano."""
        pass

    @abstractmethod
    def crear_reciclador(self, id_u, nombre, telefono, correo, contrasenia, zona):
        """Crea y retorna un objeto Reciclador."""
        pass

    @abstractmethod
    def crear_administrador(self, id_u, nombre, telefono, correo, contrasenia):
        """Crea y retorna un objeto Administrador."""
        pass


# ---------- Fábrica concreta ----------
# Esta es la fábrica real que SÍ crea los objetos.
# Si mañana ReciGana tiene versión Guayaquil, crearías
# otra clase FabricaUsuariosGuayaquil que herede de FabricaUsuariosBase.

class FabricaUsuariosManta(FabricaUsuariosBase):
    """
    Fábrica concreta para crear usuarios de la ciudad de Manta.
    Implementa todos los métodos abstractos de FabricaUsuariosBase.
    """

    def crear_ciudadano(self, id_u, nombre, telefono, correo, contrasenia, direccion):
        """
        Crea un ciudadano de Manta.
        Retorna una instancia de Ciudadano.
        """
        print(f"[FabricaManta] Creando ciudadano: {nombre}")
        return Ciudadano(id_u, nombre, telefono, correo, contrasenia, direccion)

    def crear_reciclador(self, id_u, nombre, telefono, correo, contrasenia, zona):
        """
        Crea un reciclador que opera en Manta.
        Retorna una instancia de Reciclador.
        """
        print(f"[FabricaManta] Creando reciclador: {nombre} | Zona: {zona}")
        return Reciclador(id_u, nombre, telefono, correo, contrasenia, zona)

    def crear_administrador(self, id_u, nombre, telefono, correo, contrasenia):
        """
        Crea el administrador del sistema.
        Retorna una instancia de Administrador.
        """
        print(f"[FabricaManta] Creando administrador: {nombre}")
        return Administrador(id_u, nombre, telefono, correo, contrasenia)
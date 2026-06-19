# Herencia: Administrador hereda de Usuarios
from .usuario import Usuarios


class Administrador(Usuarios):
    """
    Representa al administrador del sistema ReciGana.
    Es el único usuario con permisos para gestionar otros usuarios,
    revisar ofertas y generar reportes de la plataforma.
    Hereda autenticación y datos básicos de la clase Usuarios.
    """

    def __init__(self, id_usuario, nombre, telefono, correo, contrasenia):
        # Llamamos al constructor padre asignando rol "administrador"
        # Esto le da permisos especiales dentro del sistema
        super().__init__(id_usuario, nombre, telefono, correo, contrasenia, rol="administrador")

        # Lista interna de usuarios registrados en la plataforma
        self._usuarios = []

        # Lista interna de ofertas activas en la plataforma
        self._ofertas = []

    # ---------- Propiedades ----------

    @property
    def usuarios(self):
        """Retorna una copia de la lista de usuarios registrados."""
        return list(self._usuarios)

    @property
    def ofertas(self):
        """Retorna una copia de la lista de ofertas activas."""
        return list(self._ofertas)

    # ---------- Gestión de usuarios ----------

    def gestionar_usuarios(self):
        """
        Muestra un resumen de todos los usuarios registrados en la plataforma.
        Retorna la lista de usuarios.
        """
        total = len(self._usuarios)
        print(f"Total de usuarios registrados: {total}")
        for usuario in self._usuarios:
            print(f"  - {usuario}")
        return self._usuarios

    def agregar_usuario(self, usuario):
        """
        Registra un nuevo usuario en la plataforma.
        Parámetro:
            usuario -- instancia de Usuarios (Ciudadano o Reciclador)
        Retorna True si se agregó correctamente.
        """
        # Verificamos que no exista ya un usuario con el mismo id
        ids_existentes = [u.id for u in self._usuarios]
        if usuario.id in ids_existentes:
            print(f"Ya existe un usuario con el id '{usuario.id}'.")
            return False

        self._usuarios.append(usuario)
        print(f"Usuario '{usuario.nombre}' agregado exitosamente.")
        return True

    def eliminar_usuario(self, id_usuario):
        """
        Elimina un usuario de la plataforma por su id.
        Parámetro:
            id_usuario -- identificador del usuario a eliminar
        Retorna True si se eliminó, False si no se encontró.
        """
        for usuario in self._usuarios:
            if usuario.id == id_usuario:
                self._usuarios.remove(usuario)
                print(f"Usuario '{usuario.nombre}' eliminado.")
                return True
        print(f"No se encontró un usuario con id '{id_usuario}'.")
        return False

    def buscar_usuario(self, id_usuario):
        """
        Busca un usuario por su id.
        Retorna el usuario si existe, None si no se encuentra.
        """
        for usuario in self._usuarios:
            if usuario.id == id_usuario:
                return usuario
        return None

    # ---------- Gestión de ofertas ----------

    def gestionar_ofertas(self):
        """
        Muestra un resumen de todas las ofertas activas en la plataforma.
        Retorna la lista de ofertas.
        """
        total = len(self._ofertas)
        print(f"Total de ofertas activas: {total}")
        for oferta in self._ofertas:
            print(f"  - {oferta}")
        return self._ofertas

    def agregar_oferta(self, oferta):
        """
        Registra una nueva oferta en la plataforma.
        Parámetro:
            oferta -- diccionario con los datos de la oferta
        """
        self._ofertas.append(oferta)
        print(f"Oferta registrada: {oferta}")

    # ---------- Reportes ----------

    def generar_reporte(self):
        """
        Genera un reporte general del estado de la plataforma.
        Retorna un diccionario con las estadísticas principales.
        """
        # Contamos ofertas según su estado
        aceptadas = sum(1 for o in self._ofertas if o.get("estado") == "aceptada")
        rechazadas = sum(1 for o in self._ofertas if o.get("estado") == "rechazada")
        pendientes = sum(1 for o in self._ofertas if o.get("estado") == "pendiente")

        reporte = {
            "total_usuarios": len(self._usuarios),
            "total_ofertas": len(self._ofertas),
            "ofertas_aceptadas": aceptadas,
            "ofertas_rechazadas": rechazadas,
            "ofertas_pendientes": pendientes,
        }

        print("===== REPORTE RECIGANA =====")
        for clave, valor in reporte.items():
            print(f"  {clave}: {valor}")
        print("============================")

        return reporte

    def __str__(self):
        """Representación legible del administrador."""
        return f"Administrador: {self.nombre} | Usuarios: {len(self._usuarios)} | Ofertas: {len(self._ofertas)}"
# PATRÓN ESTRUCTURAL: ADAPTER
# ============================================================
#
# ¿Cuál es el problema real que resolvemos aquí?
#
# En este proyecto conviven DOS representaciones distintas de
# "un usuario":
#
#   1) UsuarioDB (carpeta backend/models.py) -> viene de la base
#      de datos (SQLAlchemy). Tiene: id, nombre, email, ciudad,
#      puntos_totales.
#
#   2) Ciudadano (carpeta src/usuarios/ciudadano.py) -> es la
#      clase POO del dominio que usa el Facade y el resto del
#      sistema. Necesita: id_usuario, nombre, telefono, correo,
#      contrasenia, direccion.
#
# Estas dos clases NO se pueden usar la una en lugar de la otra:
# tienen atributos con nombres distintos y algunos datos que una
# tiene y la otra no. Si quisiéramos, por ejemplo, tomar un
# usuario que viene de la base de datos y usarlo dentro de la
# lógica de negocio (Facade, ofertas, negociación...), tendríamos
# un problema de compatibilidad.
#
# El patrón ADAPTER resuelve esto: creamos una clase "traductora"
# en el medio, que sabe convertir de un formato al otro. Así:
#   - El backend sigue funcionando exactamente igual.
#   - Las clases POO (Ciudadano, Facade, etc.) siguen funcionando
#     exactamente igual.
#   - Nadie tiene que modificarse para "entender" al otro.
#
# Nota de diseño: el adaptador NO importa directamente el modelo
# UsuarioDB de SQLAlchemy (para no acoplar la carpeta src/ a la
# carpeta backend/, que ni siquiera es un paquete de Python
# instalable). En su lugar, el adaptador acepta CUALQUIER objeto
# que tenga los atributos necesarios (id, nombre, email, ciudad).
# Esto también es una práctica real de Adapter: adaptar una
# "interfaz" (un conjunto de atributos/métodos esperados), no
# necesariamente una clase concreta.
# ============================================================


# RELACIÓN DE DEPENDENCIA 
# AdaptadorUsuarioBackend necesita a Ciudadano solo para construirlo
# dentro de sus métodos, no lo guarda como atributo permanente.
from src.usuarios.ciudadano import Ciudadano


class AdaptadorUsuarioBackend:
    """
    Traduce entre el objeto de la base de datos (UsuarioDB) y la
    clase de dominio Ciudadano, y viceversa.
    """

    # Contraseña temporal que se asigna cuando adaptamos un usuario
    # que viene del backend, ya que UsuarioDB no guarda contraseña
    # en el mismo formato que exige la clase Usuarios del dominio.
    # En un sistema real, aquí se forzaría un cambio de clave en el
    # primer inicio de sesión.
    CONTRASENIA_TEMPORAL = "ReciGana2026*"

    @staticmethod
    def a_ciudadano(usuario_backend) -> Ciudadano:
        """
        Convierte un usuario del backend (o cualquier objeto con
        los atributos id, nombre, email, ciudad) en un objeto
        Ciudadano del dominio POO.

        Parámetro:
            usuario_backend -- objeto con atributos .id, .nombre,
                                .email y .ciudad (por ejemplo, una
                                fila UsuarioDB de SQLAlchemy).

        Retorna:
            Un objeto Ciudadano listo para usarse con el Facade.
        """
        atributos_necesarios = ("id", "nombre", "email", "ciudad")
        faltantes = [
            atributo for atributo in atributos_necesarios
            if not hasattr(usuario_backend, atributo)
        ]
        if faltantes:
            raise ValueError(
                "El objeto recibido no es compatible con el adaptador. "
                f"Le faltan los atributos: {faltantes}."
            )

        direccion = usuario_backend.ciudad or "Dirección no especificada"
        # La clase Ciudadano exige al menos 5 caracteres de dirección
        if len(direccion.strip()) < 5:
            direccion = f"{direccion} (dirección pendiente por completar)"

        print(
            f"[Adapter] Convirtiendo UsuarioDB #{usuario_backend.id} "
            f"({usuario_backend.nombre}) en un objeto Ciudadano del dominio."
        )

        return Ciudadano(
            id_usuario=usuario_backend.id,
            nombre=usuario_backend.nombre,
            telefono="No registrado",
            correo=usuario_backend.email,
            contrasenia=AdaptadorUsuarioBackend.CONTRASENIA_TEMPORAL,
            direccion=direccion
        )

    @staticmethod
    def de_ciudadano_a_diccionario(ciudadano: Ciudadano) -> dict:
        """
        Convierte un objeto Ciudadano del dominio POO en un
        diccionario con el formato que espera el backend para
        crear un UsuarioDB (ver backend/schemas.py -> UsuarioCreate).

        Esto sirve para el camino inverso: si el sistema de
        consola/POO crea un ciudadano nuevo y luego se quiere
        guardar en la base de datos del backend.

        Retorna:
            Un diccionario listo para pasarle a UsuarioDB(**dict)
            o a UsuarioCreate(**dict) en el backend.
        """
        return {
            "nombre": ciudadano.nombre,
            "email": ciudadano.correo,
            # El backend solo maneja "ciudad", así que usamos la
            # dirección del ciudadano como valor aproximado.
            "ciudad": ciudadano.direccion,
        }
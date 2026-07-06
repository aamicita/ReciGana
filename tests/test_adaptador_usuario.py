import unittest

from src.adaptadores.adaptador_usuario import AdaptadorUsuarioBackend
from src.usuarios.ciudadano import Ciudadano


class UsuarioDBFalso:
    """
    Simula un objeto UsuarioDB del backend (sin necesitar una base
    de datos real ni SQLAlchemy instalado), solo para probar que
    el Adapter funciona igual con el objeto real.
    """

    def __init__(self, id, nombre, email, ciudad):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.ciudad = ciudad


class TestAdaptadorUsuario(unittest.TestCase):

    def test_convierte_usuario_backend_a_ciudadano(self):
        usuario_backend = UsuarioDBFalso(
            id=10, nombre="María", email="maria@correo.com", ciudad="Manta"
        )

        ciudadano = AdaptadorUsuarioBackend.a_ciudadano(usuario_backend)

        self.assertIsInstance(ciudadano, Ciudadano)
        self.assertEqual(ciudadano.id, 10)
        self.assertEqual(ciudadano.nombre, "María")
        self.assertEqual(ciudadano.correo, "maria@correo.com")
        self.assertIn("Manta", ciudadano.direccion)

    def test_falla_si_faltan_atributos(self):
        class ObjetoIncompleto:
            def __init__(self):
                self.id = 1
                self.nombre = "Sin datos"

        with self.assertRaises(ValueError):
            AdaptadorUsuarioBackend.a_ciudadano(ObjetoIncompleto())

    def test_convierte_ciudadano_a_diccionario_backend(self):
        ciudadano = Ciudadano(
            id_usuario=1,
            nombre="Luis",
            telefono="0999999999",
            correo="luis@correo.com",
            contrasenia="clave123",
            direccion="Av. Flavio Reyes"
        )

        datos = AdaptadorUsuarioBackend.de_ciudadano_a_diccionario(ciudadano)

        self.assertEqual(datos["nombre"], "Luis")
        self.assertEqual(datos["email"], "luis@correo.com")
        self.assertEqual(datos["ciudad"], "Av. Flavio Reyes")


if __name__ == "__main__":
    unittest.main()
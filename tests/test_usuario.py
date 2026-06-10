import unittest
from src.usuarios.usuario import Usuarios


class TestUsuarios(unittest.TestCase):

    def setUp(self):
        self.usuario = Usuarios(
            1,
            "Juan",
            "0987654321",
            "juan@gmail.com",
            "123456"
        )

    def test_creacion_usuario(self):
        self.assertEqual(self.usuario.id, 1)
        self.assertEqual(self.usuario.nombre, "Juan")
        self.assertEqual(self.usuario.telefono, "0987654321")
        self.assertEqual(self.usuario.correo, "juan@gmail.com")
        self.assertEqual(self.usuario.rol, "ciudadano")

    def test_verificar_contrasenia_correcta(self):
        self.assertTrue(
            self.usuario.verificar_contrasenia("123456")
        )

    def test_verificar_contrasenia_incorrecta(self):
        self.assertFalse(
            self.usuario.verificar_contrasenia("abcdef")
        )

    def test_iniciar_sesion_correcta(self):
        resultado = self.usuario.iniciar_sesion("123456")
        self.assertTrue(resultado)
        self.assertTrue(self.usuario.sesion_activa)

    def test_iniciar_sesion_incorrecta(self):
        resultado = self.usuario.iniciar_sesion("xxxx")
        self.assertFalse(resultado)

    def test_cerrar_sesion(self):
        self.usuario.iniciar_sesion("123456")
        self.usuario.cerrar_sesion()

        self.assertFalse(
            self.usuario.sesion_activa
        )

    def test_es_administrador_false(self):
        self.assertFalse(
            self.usuario.es_administrador()
        )

    def test_es_administrador_true(self):
        admin = Usuarios(
            2,
            "Admin",
            "0999999999",
            "admin@gmail.com",
            "123456",
            "administrador"
        )

        self.assertTrue(
            admin.es_administrador()
        )

    def test_set_nombre_valido(self):
        self.usuario.nombre = "Pedro"
        self.assertEqual(
            self.usuario.nombre,
            "Pedro"
        )

    def test_set_nombre_invalido(self):
        with self.assertRaises(ValueError):
            self.usuario.nombre = ""

    def test_set_telefono_valido(self):
        self.usuario.telefono = "1111111"
        self.assertEqual(
            self.usuario.telefono,
            "1111111"
        )

    def test_set_telefono_invalido(self):
        with self.assertRaises(ValueError):
            self.usuario.telefono = "abc"

    def test_set_correo_valido(self):
        self.usuario.correo = "nuevo@gmail.com"

        self.assertEqual(
            self.usuario.correo,
            "nuevo@gmail.com"
        )

    def test_set_correo_invalido(self):
        with self.assertRaises(ValueError):
            self.usuario.correo = "correo_mal"

    def test_str(self):
        texto = str(self.usuario)

        self.assertIn(
            "Juan",
            texto
        )

    def test_repr(self):
        texto = repr(self.usuario)

        self.assertIn(
            "Usuarios",
            texto
        )


if __name__ == "__main__":
    unittest.main()
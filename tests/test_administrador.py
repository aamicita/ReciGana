import unittest

from src.usuarios.administrador import Administrador
from src.usuarios.ciudadano import Ciudadano


class TestAdministrador(unittest.TestCase):

    def setUp(self):
        self.admin = Administrador(
            1,
            "Admin",
            "0999999999",
            "admin@gmail.com",
            "123456"
        )

        self.usuario = Ciudadano(
            2,
            "Juan",
            "0987654321",
            "juan@gmail.com",
            "123456",
            "Manta Centro"
        )

    def test_agregar_usuario(self):
        resultado = self.admin.agregar_usuario(
            self.usuario
        )

        self.assertTrue(resultado)
        self.assertEqual(
            len(self.admin.usuarios),
            1
        )

    def test_agregar_usuario_duplicado(self):
        self.admin.agregar_usuario(
            self.usuario
        )

        resultado = self.admin.agregar_usuario(
            self.usuario
        )

        self.assertFalse(resultado)

    def test_buscar_usuario_existente(self):
        self.admin.agregar_usuario(
            self.usuario
        )

        encontrado = self.admin.buscar_usuario(2)

        self.assertEqual(
            encontrado,
            self.usuario
        )

    def test_buscar_usuario_inexistente(self):
        encontrado = self.admin.buscar_usuario(999)

        self.assertIsNone(encontrado)

    def test_eliminar_usuario_existente(self):
        self.admin.agregar_usuario(
            self.usuario
        )

        resultado = self.admin.eliminar_usuario(2)

        self.assertTrue(resultado)

    def test_eliminar_usuario_inexistente(self):
        resultado = self.admin.eliminar_usuario(
            999
        )

        self.assertFalse(resultado)

    def test_gestionar_usuarios(self):
        self.admin.agregar_usuario(
            self.usuario
        )

        usuarios = self.admin.gestionar_usuarios()

        self.assertEqual(
            len(usuarios),
            1
        )

    def test_agregar_oferta(self):
        oferta = {
            "estado": "pendiente"
        }

        self.admin.agregar_oferta(
            oferta
        )

        self.assertEqual(
            len(self.admin.ofertas),
            1
        )

    def test_gestionar_ofertas(self):
        oferta = {
            "estado": "pendiente"
        }

        self.admin.agregar_oferta(
            oferta
        )

        ofertas = self.admin.gestionar_ofertas()

        self.assertEqual(
            len(ofertas),
            1
        )

    def test_generar_reporte(self):
        self.admin.agregar_usuario(
            self.usuario
        )

        self.admin.agregar_oferta(
            {"estado": "aceptada"}
        )

        self.admin.agregar_oferta(
            {"estado": "rechazada"}
        )

        self.admin.agregar_oferta(
            {"estado": "pendiente"}
        )

        reporte = self.admin.generar_reporte()

        self.assertEqual(
            reporte["total_usuarios"],
            1
        )

        self.assertEqual(
            reporte["total_ofertas"],
            3
        )

        self.assertEqual(
            reporte["ofertas_aceptadas"],
            1
        )

        self.assertEqual(
            reporte["ofertas_rechazadas"],
            1
        )

        self.assertEqual(
            reporte["ofertas_pendientes"],
            1
        )

    def test_str(self):
        texto = str(self.admin)

        self.assertIn(
            "Administrador",
            texto
        )


if __name__ == "__main__":
    unittest.main()
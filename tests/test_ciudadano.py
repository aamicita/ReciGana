import unittest
from src.usuarios.ciudadano import Ciudadano


class TestCiudadano(unittest.TestCase):

    def setUp(self):
        self.ciudadano = Ciudadano(
            1,
            "Juan",
            "0987654321",
            "juan@gmail.com",
            "123456",
            "Manta Centro"
        )

    def test_registrar(self):
        self.assertTrue(self.ciudadano.registrar())

    def test_publicar_material(self):
        material = self.ciudadano.publicar_material(
            "plastico",
            5
        )

        self.assertEqual(material["tipo"], "plastico")
        self.assertEqual(material["peso_kg"], 5)
        self.assertEqual(material["estado"], "disponible")

    def test_publicar_material_con_foto(self):
        material = self.ciudadano.publicar_material(
            "carton",
            10,
            "foto.jpg"
        )

        self.assertEqual(material["foto"], "foto.jpg")

    def test_publicar_material_tipo_invalido(self):
        with self.assertRaises(ValueError):
            self.ciudadano.publicar_material("", 5)

    def test_publicar_material_peso_invalido(self):
        with self.assertRaises(ValueError):
            self.ciudadano.publicar_material("plastico", -1)

    def test_recibir_oferta(self):
        oferta = {"precio": 10}

        self.ciudadano.recibir_oferta(oferta)

        self.assertIn(
            oferta,
            self.ciudadano.ofertas_recibidas
        )

    def test_aceptar_oferta(self):
        oferta = {"precio": 10}

        self.ciudadano.recibir_oferta(oferta)

        resultado = self.ciudadano.aceptar_oferta(oferta)

        self.assertTrue(resultado)
        self.assertEqual(
            oferta["estado"],
            "aceptada"
        )

    def test_rechazar_oferta(self):
        oferta = {"precio": 10}

        self.ciudadano.recibir_oferta(oferta)

        resultado = self.ciudadano.rechazar_oferta(oferta)

        self.assertTrue(resultado)
        self.assertEqual(
            oferta["estado"],
            "rechazada"
        )

    def test_aceptar_oferta_inexistente(self):
        oferta = {"precio": 10}

        self.assertFalse(
            self.ciudadano.aceptar_oferta(oferta)
        )

    def test_rechazar_oferta_inexistente(self):
        oferta = {"precio": 10}

        self.assertFalse(
            self.ciudadano.rechazar_oferta(oferta)
        )

    def test_direccion_valida(self):
        self.ciudadano.direccion = "Nueva direccion"

        self.assertEqual(
            self.ciudadano.direccion,
            "Nueva direccion"
        )

    def test_direccion_invalida(self):
        with self.assertRaises(ValueError):
            self.ciudadano.direccion = "abc"

    def test_str(self):
        texto = str(self.ciudadano)

        self.assertIn(
            "Ciudadano",
            texto
        )


if __name__ == "__main__":
    unittest.main()
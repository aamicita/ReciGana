import unittest

from src.usuarios.reciclador import Reciclador


class TestReciclador(unittest.TestCase):

    def setUp(self):
        self.reciclador = Reciclador(
            1,
            "Carlos",
            "0987654321",
            "carlos@gmail.com",
            "123456",
            "Manta Centro"
        )

        self.material = {
            "tipo": "plastico",
            "peso_kg": 10,
            "estado": "disponible"
        }

    def test_registrarse(self):
        self.assertTrue(
            self.reciclador.registrarse()
        )

    def test_zona_cobertura_valida(self):
        self.reciclador.zona_cobertura = "Tarqui"

        self.assertEqual(
            self.reciclador.zona_cobertura,
            "Tarqui"
        )

    def test_zona_cobertura_invalida(self):
        with self.assertRaises(ValueError):
            self.reciclador.zona_cobertura = "ab"

    def test_consultar_ofertas_con_materiales(self):
        materiales = [
            self.material,
            {
                "tipo": "carton",
                "peso_kg": 5,
                "estado": "vendido"
            }
        ]

        resultado = self.reciclador.consultar_ofertas(
            materiales
        )

        self.assertEqual(
            len(resultado),
            1
        )

    def test_consultar_ofertas_sin_materiales(self):
        resultado = self.reciclador.consultar_ofertas([])

        self.assertEqual(
            resultado,
            []
        )

    def test_realizar_oferta(self):
        oferta = self.reciclador.realizar_oferta(
            self.material,
            20
        )

        self.assertEqual(
            oferta["precio_ofrecido"],
            20
        )

        self.assertEqual(
            oferta["estado"],
            "pendiente"
        )

    def test_realizar_oferta_precio_invalido(self):
        with self.assertRaises(ValueError):
            self.reciclador.realizar_oferta(
                self.material,
                -5
            )

    def test_realizar_oferta_material_no_disponible(self):
        material = {
            "tipo": "plastico",
            "peso_kg": 10,
            "estado": "vendido"
        }

        resultado = self.reciclador.realizar_oferta(
            material,
            20
        )

        self.assertIsNone(resultado)

    def test_aceptar_oferta(self):
        oferta = self.reciclador.realizar_oferta(
            self.material,
            20
        )

        self.reciclador.aceptar_oferta(
            oferta
        )

        self.assertEqual(
            oferta["estado"],
            "aceptada"
        )

        self.assertEqual(
            len(self.reciclador.materiales_comprados),
            1
        )

    def test_rechazar_oferta(self):
        oferta = self.reciclador.realizar_oferta(
            self.material,
            20
        )

        self.reciclador.rechazar_oferta(
            oferta
        )

        self.assertEqual(
            oferta["estado"],
            "rechazada"
        )

    def test_str(self):
        texto = str(self.reciclador)

        self.assertIn(
            "Reciclador",
            texto
        )


if __name__ == "__main__":
    unittest.main()
import unittest

from src.comunicaciones.calificacion import Calificacion


class TestCalificacion(unittest.TestCase):

    def setUp(self):
        self.calificacion = Calificacion(
            1,
            5,
            "Excelente servicio"
        )

    def test_creacion_calificacion(self):
        self.assertEqual(
            self.calificacion.id_calificacion,
            1
        )

        self.assertEqual(
            self.calificacion.puntaje,
            5
        )

        self.assertEqual(
            self.calificacion.comentario,
            "Excelente servicio"
        )

        self.assertFalse(
            self.calificacion.registrada
        )

    def test_puntaje_invalido_menor(self):
        with self.assertRaises(ValueError):
            Calificacion(
                1,
                0,
                "Comentario"
            )

    def test_puntaje_invalido_mayor(self):
        with self.assertRaises(ValueError):
            Calificacion(
                1,
                6,
                "Comentario"
            )

    def test_comentario_invalido(self):
        with self.assertRaises(ValueError):
            Calificacion(
                1,
                5,
                123
            )

    def test_registrar_calificacion(self):
        resultado = self.calificacion.registrar_calificacion()

        self.assertTrue(resultado)
        self.assertTrue(
            self.calificacion.registrada
        )

    def test_registrar_calificacion_dos_veces(self):
        self.calificacion.registrar_calificacion()

        resultado = self.calificacion.registrar_calificacion()

        self.assertFalse(resultado)

    def test_consultar_calificaciones(self):
        detalle = self.calificacion.consultar_calificaciones()

        self.assertEqual(
            detalle["id"],
            1
        )

        self.assertEqual(
            detalle["puntaje"],
            5
        )

        self.assertEqual(
            detalle["comentario"],
            "Excelente servicio"
        )

    def test_str(self):
        texto = str(self.calificacion)

        self.assertIn(
            "Calificación",
            texto
        )

        self.assertIn(
            "Excelente servicio",
            texto
        )


if __name__ == "__main__":
    unittest.main()
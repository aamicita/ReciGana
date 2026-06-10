import unittest
from datetime import datetime

from src.comunicaciones.historial_de_reciclaje import HistorialDeReciclaje


class TestHistorialDeReciclaje(unittest.TestCase):

    def setUp(self):
        self.historial = HistorialDeReciclaje(1)

    def test_creacion_historial(self):
        self.assertEqual(
            self.historial.id_historial,
            1
        )

        self.assertEqual(
            self.historial.total_registros,
            0
        )

    def test_agregar_registro_venta(self):
        registro = self.historial.agregar_registro(
            "plastico",
            5,
            "venta"
        )

        self.assertEqual(
            registro["tipo_material"],
            "plastico"
        )

        self.assertEqual(
            registro["peso_kg"],
            5
        )

        self.assertEqual(
            registro["tipo_transaccion"],
            "venta"
        )

    def test_agregar_registro_compra(self):
        registro = self.historial.agregar_registro(
            "carton",
            10,
            "compra"
        )

        self.assertEqual(
            registro["tipo_transaccion"],
            "compra"
        )

    def test_agregar_registro_peso_invalido(self):
        with self.assertRaises(ValueError):
            self.historial.agregar_registro(
                "plastico",
                -1,
                "venta"
            )

    def test_agregar_registro_tipo_invalido(self):
        with self.assertRaises(ValueError):
            self.historial.agregar_registro(
                "plastico",
                5,
                "intercambio"
            )

    def test_consultar_historial_vacio(self):
        resultado = self.historial.consultar_historial()

        self.assertEqual(
            resultado,
            []
        )

    def test_consultar_historial_con_datos(self):
        self.historial.agregar_registro(
            "plastico",
            5,
            "venta"
        )

        resultado = self.historial.consultar_historial()

        self.assertEqual(
            len(resultado),
            1
        )

    def test_filtrar_por_fecha_existente(self):
        registro = self.historial.agregar_registro(
            "plastico",
            5,
            "venta"
        )

        fecha = registro["fecha"][:10]

        resultado = self.historial.filtrar_por_fecha(
            fecha
        )

        self.assertEqual(
            len(resultado),
            1
        )

    def test_filtrar_por_fecha_inexistente(self):
        resultado = self.historial.filtrar_por_fecha(
            "2000-01-01"
        )

        self.assertEqual(
            resultado,
            []
        )

    def test_filtrar_por_tipo_existente(self):
        self.historial.agregar_registro(
            "plastico",
            5,
            "venta"
        )

        resultado = self.historial.filtrar_por_tipo(
            "plastico"
        )

        self.assertEqual(
            len(resultado),
            1
        )

    def test_filtrar_por_tipo_mayusculas(self):
        self.historial.agregar_registro(
            "plastico",
            5,
            "venta"
        )

        resultado = self.historial.filtrar_por_tipo(
            "PLASTICO"
        )

        self.assertEqual(
            len(resultado),
            1
        )

    def test_filtrar_por_tipo_inexistente(self):
        resultado = self.historial.filtrar_por_tipo(
            "vidrio"
        )

        self.assertEqual(
            resultado,
            []
        )

    def test_str(self):
        texto = str(self.historial)

        self.assertIn(
            "Historial",
            texto
        )


if __name__ == "__main__":
    unittest.main()
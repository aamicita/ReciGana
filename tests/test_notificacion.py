# ==========================================================
# TESTS DE LA CLASE Notificacion
# Sistema: ReciGana
#
# Objetivo:
# Verificar que la clase Notificacion funcione correctamente,
# validando creación, envío, lectura y representación textual.
# ==========================================================

import unittest

from src.comunicaciones.notificacion import Notificacion


class TestNotificacion(unittest.TestCase):

    def setUp(self):
        """
        Este método se ejecuta antes de cada test.

        Creamos una notificación válida que reutilizaremos
        en la mayoría de las pruebas.
        """
        self.notificacion = Notificacion(
            1,
            "Tu oferta fue aceptada",
            "Juan"
        )

    # ======================================================
    # PRUEBAS DEL CONSTRUCTOR
    # ======================================================

    def test_creacion_notificacion(self):
        """
        Verifica que todos los atributos se guarden correctamente
        cuando se crea una notificación válida.
        """

        self.assertEqual(
            self.notificacion.id_notificacion,
            1
        )

        self.assertEqual(
            self.notificacion.mensaje,
            "Tu oferta fue aceptada"
        )

        self.assertEqual(
            self.notificacion.destinatario,
            "Juan"
        )

        # Toda notificación inicia como NO leída
        self.assertFalse(
            self.notificacion.leida
        )

    def test_mensaje_vacio(self):
        """
        No debe permitirse crear una notificación
        con un mensaje vacío.
        """

        with self.assertRaises(ValueError):
            Notificacion(
                1,
                ""
            )

    def test_mensaje_solo_espacios(self):
        """
        Tampoco debe permitirse un mensaje compuesto
        únicamente por espacios.
        """

        with self.assertRaises(ValueError):
            Notificacion(
                1,
                "     "
            )

    def test_mensaje_no_string(self):
        """
        El mensaje debe ser texto (str).
        Si llega otro tipo de dato debe lanzar excepción.
        """

        with self.assertRaises(ValueError):
            Notificacion(
                1,
                12345
            )

    # ======================================================
    # PRUEBAS DEL MÉTODO enviar()
    # ======================================================

    def test_enviar_con_destinatario(self):
        """
        Verifica que el método enviar()
        retorne True cuando existe destinatario.
        """

        resultado = self.notificacion.enviar()

        self.assertTrue(resultado)

    def test_enviar_sin_destinatario(self):
        """
        Verifica que también funcione cuando la
        notificación es general.
        """

        notificacion = Notificacion(
            2,
            "Nuevo material disponible"
        )

        resultado = notificacion.enviar()

        self.assertTrue(resultado)

    # ======================================================
    # PRUEBAS DEL MÉTODO marcar_como_leida()
    # ======================================================

    def test_marcar_como_leida(self):
        """
        La primera vez que se marca como leída
        debe retornar True.
        """

        resultado = self.notificacion.marcar_como_leida()

        self.assertTrue(resultado)

        self.assertTrue(
            self.notificacion.leida
        )

    def test_marcar_como_leida_dos_veces(self):
        """
        Si ya fue leída anteriormente,
        debe retornar False.
        """

        self.notificacion.marcar_como_leida()

        resultado = self.notificacion.marcar_como_leida()

        self.assertFalse(resultado)

    # ======================================================
    # PRUEBAS DE PROPIEDADES
    # ======================================================

    def test_fecha_creacion_existe(self):
        """
        Verifica que la fecha de creación
        se genere automáticamente.
        """

        self.assertIsNotNone(
            self.notificacion.fecha_creacion
        )

        self.assertIsInstance(
            self.notificacion.fecha_creacion,
            str
        )

    # ======================================================
    # PRUEBAS DEL MÉTODO __str__
    # ======================================================

    def test_str_no_leida(self):
        """
        Verifica la representación textual
        cuando la notificación todavía no ha sido leída.
        """

        texto = str(self.notificacion)

        self.assertIn(
            "No leída",
            texto
        )

        self.assertIn(
            "Tu oferta fue aceptada",
            texto
        )

    def test_str_leida(self):
        """
        Verifica la representación textual
        después de marcarla como leída.
        """

        self.notificacion.marcar_como_leida()

        texto = str(self.notificacion)

        self.assertIn(
            "Leída",
            texto
        )

        self.assertIn(
            "Tu oferta fue aceptada",
            texto
        )


if __name__ == "__main__":
    unittest.main()
    
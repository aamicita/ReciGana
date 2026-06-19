
# TESTS DEL PATRÓN FACADE — ReciGanaFacade

# Estos tests verifican que la Facade simplifica correctamente
# las operaciones del sistema.
 
import sys
import os
import unittest
 
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
 
from src.facade_recigana import ReciGanaFacade
from src.usuarios.gestor_sistema import GestorSistema
 
 
class TestFacade(unittest.TestCase):
    """
    Pruebas del patrón Facade (ReciGanaFacade).
 
    Cada test demuestra que la Facade simplifica operaciones
    que sin ella requerirían múltiples llamadas a clases distintas.
    """
 
    def setUp(self):
        """
        Se ejecuta antes de cada test.
        Reseteamos el sistema para tener un estado limpio.
        """
        # Reseteamos el Singleton para que cada test comience limpio
        GestorSistema.resetear()
 
        # Creamos la Facade — esta es la única clase que necesitamos
        self.facade = ReciGanaFacade()
 
    # ----------------------------------------------------------
    # TEST 1: La Facade puede registrar un ciudadano
    # ----------------------------------------------------------
    def test_registrar_ciudadano(self):
        """
        Verifica que la Facade registra un ciudadano correctamente.
        Sin Facade esto requeriría crear Ciudadano + GestorSistema.
        """
        ciudadano = self.facade.registrar_ciudadano(
            1, "María López", "0991234567",
            "maria@email.com", "clave123", "Av. 4 de Noviembre"
        )
 
        # El ciudadano debe existir y tener el nombre correcto
        self.assertIsNotNone(ciudadano)
        self.assertEqual(ciudadano.nombre, "María López")
 
        # Debe estar registrado en el sistema
        gestor = GestorSistema.obtener_instancia()
        self.assertEqual(len(gestor.obtener_usuarios()), 1)
 
    # ----------------------------------------------------------
    # TEST 2: La Facade puede registrar un reciclador
    # ----------------------------------------------------------
    def test_registrar_reciclador(self):
        """
        Verifica que la Facade registra un reciclador correctamente.
        """
        reciclador = self.facade.registrar_reciclador(
            2, "Juan Pérez", "0997654321",
            "juan@email.com", "clave456", "Manta Centro"
        )
 
        self.assertIsNotNone(reciclador)
        self.assertEqual(reciclador.nombre, "Juan Pérez")
        self.assertEqual(reciclador.zona_cobertura, "Manta Centro")
 
    # ----------------------------------------------------------
    # TEST 3: La Facade puede publicar un material
    # ----------------------------------------------------------
    def test_publicar_material(self):
        """
        Verifica que publicar un material a través de la Facade
        registra tanto el dict del ciudadano como el objeto en el gestor.
        Sin Facade necesitarías coordinar Ciudadano + FabricaMateriales
        + GestorSistema manualmente.
        """
        ciudadano = self.facade.registrar_ciudadano(
            1, "María", "0991234567",
            "maria@email.com", "clave123", "Av. 10"
        )
 
        material = self.facade.publicar_material(
            ciudadano, "plastico", 10.0
        )
 
        # El material debe estar en la lista del ciudadano
        self.assertIsNotNone(material)
        self.assertEqual(material["tipo"], "plastico")
        self.assertEqual(material["peso_kg"], 10.0)
        self.assertEqual(len(ciudadano.materiales_publicados), 1)
 
        # También debe estar registrado en el gestor del sistema
        gestor = GestorSistema.obtener_instancia()
        self.assertEqual(len(gestor.obtener_materiales()), 1)
 
    # ----------------------------------------------------------
    # TEST 4: La Facade puede registrar un intercambio completo
    # ----------------------------------------------------------
    def test_registrar_intercambio_completo(self):
        """
        Verifica la operación más importante de la Facade:
        registrar un intercambio completo entre ciudadano y reciclador.
 
        Sin Facade esto requiere coordinar:
            Negociacion + HistorialDeReciclaje (x2) + Notificacion (x2)
        Con Facade: una sola llamada.
        """
        ciudadano = self.facade.registrar_ciudadano(
            1, "María", "0991234567",
            "maria@email.com", "clave123", "Av. 10"
        )
        reciclador = self.facade.registrar_reciclador(
            2, "Juan", "0997654321",
            "juan@email.com", "clave456", "Manta Centro"
        )
 
        # Registramos el intercambio completo con una sola llamada
        resumen = self.facade.registrar_intercambio(
            ciudadano=ciudadano,
            reciclador=reciclador,
            tipo_material="carton",
            peso_kg=5.0,
            precio=2.50
        )
 
        # El resumen debe tener todos los datos del intercambio
        self.assertIsNotNone(resumen)
        self.assertEqual(resumen["tipo_material"], "carton")
        self.assertEqual(resumen["peso_kg"], 5.0)
        self.assertEqual(resumen["precio"], 2.50)
        self.assertEqual(resumen["ciudadano"], "María")
        self.assertEqual(resumen["reciclador"], "Juan")
        # La negociacion debe haber quedado en estado finalizada
        self.assertEqual(resumen["estado_negociacion"], "finalizada")
 
    # ----------------------------------------------------------
    # TEST 5: La Facade puede hacer una oferta
    # ----------------------------------------------------------
    def test_hacer_oferta(self):
        """
        Verifica que hacer una oferta a través de la Facade funciona.
        """
        ciudadano = self.facade.registrar_ciudadano(
            1, "María", "0991234567",
            "maria@email.com", "clave123", "Av. 10"
        )
        reciclador = self.facade.registrar_reciclador(
            2, "Juan", "0997654321",
            "juan@email.com", "clave456", "Manta Centro"
        )
 
        material = self.facade.publicar_material(
            ciudadano, "metal", 3.0
        )
 
        oferta = self.facade.hacer_oferta(reciclador, material, 15.0)
 
        self.assertIsNotNone(oferta)
        self.assertEqual(oferta["precio_ofrecido"], 15.0)
        self.assertEqual(oferta["estado"], "pendiente")
 
    # ----------------------------------------------------------
    # TEST 6: La Facade da resumen del sistema
    # ----------------------------------------------------------
    def test_obtener_resumen_sistema(self):
        """
        Verifica que la Facade puede dar el resumen del sistema.
        """
        self.facade.registrar_ciudadano(
            1, "María", "0991234567",
            "maria@email.com", "clave123", "Av. 10"
        )
        self.facade.registrar_reciclador(
            2, "Juan", "0997654321",
            "juan@email.com", "clave456", "Manta Centro"
        )
 
        resumen = self.facade.obtener_resumen_sistema()
 
        self.assertEqual(resumen["total_usuarios"], 2)
 
    # ----------------------------------------------------------
    # TEST 7: La Facade puede generar un reporte
    # ----------------------------------------------------------
    def test_generar_reporte_sistema(self):
        """
        Verifica que la Facade genera un reporte en un solo paso.
        Sin Facade: importar Reporte, construirlo, llamar generar_reporte().
        Con Facade: una sola llamada.
        """
        self.facade.registrar_ciudadano(
            1, "María", "0991234567",
            "maria@email.com", "clave123", "Av. 10"
        )
 
        reporte = self.facade.generar_reporte_sistema(
            id_reporte=1,
            fecha="2025-06-01"
        )
 
        self.assertIsNotNone(reporte)
        self.assertTrue(reporte.generado)
        self.assertEqual(reporte.tipo_reporte, "usuarios")
 
    # ----------------------------------------------------------
    # TEST 8: La Facade es reutilizable en múltiples operaciones
    # ----------------------------------------------------------
    def test_multiples_operaciones_misma_facade(self):
        """
        Verifica que la misma instancia de Facade puede manejar
        múltiples usuarios y materiales sin conflictos.
        """
        # Registramos dos ciudadanos y un reciclador
        c1 = self.facade.registrar_ciudadano(
            1, "Ana", "0991111111", "ana@mail.com", "pass1", "Calle A"
        )
        c2 = self.facade.registrar_ciudadano(
            2, "Luis", "0992222222", "luis@mail.com", "pass2", "Calle B"
        )
        r1 = self.facade.registrar_reciclador(
            3, "Pedro", "0993333333", "pedro@mail.com", "pass3", "Tarqui"
        )
 
        # Publicamos materiales de ambos ciudadanos
        self.facade.publicar_material(c1, "plastico", 5.0)
        self.facade.publicar_material(c2, "carton", 8.0)
 
        # Verificamos que el sistema tiene todos los registros
        resumen = self.facade.obtener_resumen_sistema()
 
        self.assertEqual(resumen["total_usuarios"], 3)
        self.assertEqual(resumen["total_materiales"], 2)
 
 
if __name__ == "__main__":
    unittest.main()
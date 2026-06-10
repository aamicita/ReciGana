import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from comunicaciones.calificacion import Calificacion

# Tests de Notificacion
def test_notificacion_atributos():
    n = Notificacion("N1", "Hola")
    assert n.id_notificacion == "N1"
    assert n.mensaje == "Hola"
    assert n.leida == False

def test_notificacion_marcar_leida():
    n = Notificacion("N2", "Test")
    n.marcar_como_leida()
    assert n.leida == True

# Tests de Calificacion
def test_calificacion_atributos():
    c = Calificacion("C1", 5, "Excelente")
    assert c.id_calificacion == "C1"
    assert c.puntaje == 5
    assert c.comentario == "Excelente"
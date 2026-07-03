from src.materiales.negociacion import Negociacion, ObservadorCiudadano, ObservadorReciclador, ObservadorAuditoria

def test_patron_observer_notificaciones_exitosas():
    # 1. Crear la negociación en estado pendiente
    negociacion = Negociacion("TEST-OBS-01", 50.0, "pendiente", "2026-07-03")
    
    # 2. Instanciar y suscribir los observadores
    obs_ciudadano = ObservadorCiudadano("María", 10.0, "Plástico")
    obs_reciclador = ObservadorReciclador("Juan", 10.0, "Plástico")
    obs_auditoria = ObservadorAuditoria()
    
    negociacion.suscribir(obs_ciudadano)
    negociacion.suscribir(obs_reciclador)
    negociacion.suscribir(obs_auditoria)
    
    # 3. Probar los cambios de estado para ejecutar el código nuevo
    assert negociacion.iniciar_negociacion() is True
    assert negociacion.proponer_contra_oferta(60.0) is True
    assert negociacion.finalizar_negociacion() is True
    
    # Verificar que cambió el estado correctamente
    assert negociacion.estado == "finalizada"

def test_patron_observer_cancelacion():
    negociacion = Negociacion("TEST-OBS-02", 20.0, "pendiente", "2026-07-03")
    obs_ciudadano = ObservadorCiudadano("María", 5.0, "Cartón")
    
    negociacion.suscribir(obs_ciudadano)
    negociacion.iniciar_negociacion()
    assert negociacion.cancelar_negociacion() is True
    assert negociacion.estado == "cancelada"
"""
====================================================
EJEMPLOS DE PRINCIPIOS SOLID - PROYECTO RECIGANA
==================================================
Proyecto: ReciGana
Materia: Arquitectura de Software

Este archivo contiene ejemplos de violaciones y
correcciones de los principios SOLID encontradas
en el proyecto ReciGana.

Cada sección incluye:

1. Código original
2. Problema identificado
3. Código corregido
4. Explicación de la solución
"""

from abc import ABC, abstractmethod


# ==================================================
# S - SINGLE RESPONSIBILITY PRINCIPLE (SRP)
# ==================================================

"""
PRINCIPIO:

Una clase debe tener UNA sola responsabilidad.
Una clase debe tener UNA sola razón para cambiar.
"""


# --------------------------------------------------
# CÓDIGO ORIGINAL
# --------------------------------------------------

class AdministradorOriginal:

    def gestionar_usuarios(self):
        print("Gestionando usuarios")

    def gestionar_recicladores(self):
        print("Gestionando recicladores")

    def gestionar_ofertas(self):
        print("Gestionando ofertas")

    def generar_reporte(self):
        print("Generando reporte")


"""
PROBLEMA:

La clase Administrador realiza demasiadas tareas.

Responsabilidad 1:
- Gestión de usuarios

Responsabilidad 2:
- Gestión de recicladores

Responsabilidad 3:
- Gestión de ofertas

Responsabilidad 4:
- Generación de reportes

Si cambia cualquiera de esas áreas,
debemos modificar la misma clase.

Esto viola SRP.
"""


# --------------------------------------------------
# CÓDIGO CORREGIDO
# --------------------------------------------------

class GestorUsuarios:
    def gestionar_usuarios(self):
        print("Gestionando usuarios")


class GestorRecicladores:
    def gestionar_recicladores(self):
        print("Gestionando recicladores")


class GestorOfertas:
    def gestionar_ofertas(self):
        print("Gestionando ofertas")


class GeneradorReportes:
    def generar_reporte(self):
        print("Generando reporte")


class Administrador:

    def __init__(self):

        # El administrador delega las tareas.

        self.gestor_usuarios = GestorUsuarios()
        self.gestor_recicladores = GestorRecicladores()
        self.gestor_ofertas = GestorOfertas()
        self.generador_reportes = GeneradorReportes()


"""
¿POR QUÉ FUNCIONA?

Cada clase tiene una única responsabilidad.

Si cambia la lógica de reportes,
solo cambia GeneradorReportes.

Si cambia la gestión de usuarios,
solo cambia GestorUsuarios.

Ahora se cumple SRP.
"""


# ==================================================
# O - OPEN CLOSED PRINCIPLE (OCP)
# ==================================================

"""
PRINCIPIO:

Las clases deben estar abiertas para extensión
pero cerradas para modificación.
"""


# --------------------------------------------------
# CÓDIGO ORIGINAL
# --------------------------------------------------

class ReporteOriginal:

    def generar_reporte(self):
        print("Reporte generado")

    def exportar_pdf(self):
        print("Exportando PDF")


"""
PROBLEMA:

Si mañana queremos:

- Excel
- CSV
- JSON

Debemos modificar la clase Reporte.

Eso viola OCP.
"""


# --------------------------------------------------
# CÓDIGO CORREGIDO
# --------------------------------------------------

class ExportadorReporte(ABC):

    @abstractmethod
    def exportar(self):
        pass


class ExportadorPDF(ExportadorReporte):

    def exportar(self):
        print("Exportando PDF")


class ExportadorExcel(ExportadorReporte):

    def exportar(self):
        print("Exportando Excel")


class Reporte:

    def __init__(self, exportador):
        self.exportador = exportador

    def exportar(self):
        self.exportador.exportar()


"""
¿POR QUÉ FUNCIONA?

Reporte ya no conoce formatos específicos.

Para agregar CSV:

class ExportadorCSV(ExportadorReporte)

No se modifica Reporte.

Se cumple OCP.
"""


# ==================================================
# L - LISKOV SUBSTITUTION PRINCIPLE (LSP)
# ==================================================

"""
PRINCIPIO:

Una clase hija debe poder sustituir
a la clase padre sin romper el sistema.
"""


# --------------------------------------------------
# CÓDIGO CORREGIDO PROPUESTO
# --------------------------------------------------

class Usuario(ABC):

    @abstractmethod
    def procesar_oferta(self):
        pass


class Ciudadano(Usuario):

    def procesar_oferta(self):
        print("Oferta aceptada")


class Reciclador(Usuario):

    def procesar_oferta(self):
        print("Oferta aceptada por reciclador")


class AdministradorSistema(Usuario):

    def procesar_oferta(self):
        print("Gestionando ofertas")


"""
¿POR QUÉ FUNCIONA?

Todas las clases tienen el mismo contrato:

procesar_oferta()

Por lo tanto:

usuarios = [
    Ciudadano(),
    Reciclador(),
    AdministradorSistema()
]

Todos pueden utilizarse de la misma manera.

Se cumple LSP.
"""


# ==================================================
# I - INTERFACE SEGREGATION PRINCIPLE (ISP)
# ==================================================

"""
PRINCIPIO:

Los clientes no deben depender
de métodos que no utilizan.
"""


# --------------------------------------------------
# CÓDIGO CORREGIDO
# --------------------------------------------------

class IAutenticacion(ABC):

    @abstractmethod
    def iniciar_sesion(self):
        pass

    @abstractmethod
    def cerrar_sesion(self):
        pass


class IDatosUsuario(ABC):

    @property
    @abstractmethod
    def correo(self):
        pass


"""
¿POR QUÉ FUNCIONA?

Antes todo estaba mezclado.

Ahora:

IAutenticacion
→ solo autenticación

IDatosUsuario
→ solo datos

Cada cliente usa únicamente
la interfaz que necesita.

Se cumple ISP.
"""


# ==================================================
# D - DEPENDENCY INVERSION PRINCIPLE (DIP)
# ==================================================

"""
PRINCIPIO:

Los módulos de alto nivel no deben depender
de módulos de bajo nivel.

Ambos deben depender de abstracciones.
"""


# --------------------------------------------------
# CÓDIGO ORIGINAL
# --------------------------------------------------

class NotificacionOriginal:

    def enviar(self):
        print("Notificación enviada")


"""
PROBLEMA:

La clase depende directamente de print().

Si queremos:

- Email
- SMS
- WhatsApp
- Slack

debemos modificar la clase.
"""


# --------------------------------------------------
# CÓDIGO CORREGIDO
# --------------------------------------------------

class CanalNotificacion(ABC):

    @abstractmethod
    def enviar(self, mensaje):
        pass


class NotificacionConsola(CanalNotificacion):

    def enviar(self, mensaje):
        print(mensaje)


class NotificacionEmail(CanalNotificacion):

    def enviar(self, mensaje):
        print(f"Enviando email: {mensaje}")


class Notificacion:

    def __init__(self, canal):
        self.canal = canal

    def enviar(self, mensaje):
        self.canal.enviar(mensaje)


"""
¿POR QUÉ FUNCIONA?

La clase Notificacion ya no depende
de print().

Depende de la abstracción:

CanalNotificacion

Podemos cambiar:

- Consola
- Email
- SMS
- WhatsApp

sin modificar Notificacion.

Se cumple DIP.
"""
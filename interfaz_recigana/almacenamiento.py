# -*- coding: utf-8 -*-
"""
almacenamiento.py
Se encarga de guardar y leer los datos de la aplicación.

- Los USUARIOS (ciudadanos y recicladores) se guardan en formato CSV,
  para que se puedan abrir directamente con doble clic en Excel.
  Cada rol tiene SU PROPIO archivo, para que nunca se mezclen:

    data/ciudadanos.csv      -> tabla de ciudadanos registrados
    data/recicladores.csv    -> tabla de recicladores registrados

- Las publicaciones de materiales y los mensajes del chat se guardan
  en JSON porque tienen listas dentro de listas (ofertas, mensajes)
  y eso no se representa bien en una tabla plana como CSV:

    data/publicaciones.json  -> materiales publicados + sus ofertas
    data/mensajes.json       -> chats entre ciudadano y reciclador

No se necesita ninguna base de datos ni librería externa,
todo funciona con los módulos "csv" y "json" que ya vienen
incluidos en Python.
"""

import csv
import json
import os
import hashlib
from datetime import datetime

CARPETA_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

ARCHIVO_CIUDADANOS = os.path.join(CARPETA_DATA, "ciudadanos.csv")
ARCHIVO_RECICLADORES = os.path.join(CARPETA_DATA, "recicladores.csv")
ARCHIVO_PUBLICACIONES = os.path.join(CARPETA_DATA, "publicaciones.json")
ARCHIVO_MENSAJES = os.path.join(CARPETA_DATA, "mensajes.json")

# Columnas de cada tabla CSV, en el orden en que aparecerán en Excel
CAMPOS_CIUDADANO = ["id", "nombres", "apellidos", "ciudad", "correo",
                     "password_hash", "fecha_registro"]
CAMPOS_RECICLADOR = ["id", "nombres", "apellidos", "ciudad", "zona_cobertura",
                      "correo", "password_hash", "fecha_registro"]


def _asegurar_archivos():
    """Crea la carpeta 'data' y los archivos si todavía no existen."""
    os.makedirs(CARPETA_DATA, exist_ok=True)

    # Archivos CSV de usuarios (con su fila de encabezados)
    for archivo, campos in [
        (ARCHIVO_CIUDADANOS, CAMPOS_CIUDADANO),
        (ARCHIVO_RECICLADORES, CAMPOS_RECICLADOR),
    ]:
        if not os.path.exists(archivo):
            # encoding "utf-8-sig" hace que Excel muestre bien tildes y ñ
            with open(archivo, "w", newline="", encoding="utf-8-sig") as f:
                escritor = csv.DictWriter(f, fieldnames=campos)
                escritor.writeheader()

    # Archivos JSON de publicaciones y mensajes
    for archivo, valor_inicial in [
        (ARCHIVO_PUBLICACIONES, []),
        (ARCHIVO_MENSAJES, {}),
    ]:
        if not os.path.exists(archivo):
            with open(archivo, "w", encoding="utf-8") as f:
                json.dump(valor_inicial, f, ensure_ascii=False, indent=2)


def _leer_csv(archivo, campos):
    """Lee un archivo CSV y retorna una lista de diccionarios."""
    _asegurar_archivos()
    filas = []
    with open(archivo, "r", newline="", encoding="utf-8-sig") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            if fila.get("id"):
                fila["id"] = int(fila["id"])
                filas.append(fila)
    return filas


def _escribir_csv(archivo, campos, filas):
    """Sobreescribe el archivo CSV completo con la lista de diccionarios dada."""
    with open(archivo, "w", newline="", encoding="utf-8-sig") as f:
        escritor = csv.DictWriter(f, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(filas)


def _leer(archivo, valor_por_defecto):
    _asegurar_archivos()
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return valor_por_defecto


def _escribir(archivo, datos):
    _asegurar_archivos()
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)


def encriptar_contrasenia(texto: str) -> str:
    """Igual que en la clase Usuarios del backend: hash SHA-256."""
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def _siguiente_id(lista):
    if not lista:
        return 1
    return max(item["id"] for item in lista) + 1


# ================= CIUDADANOS =================

def obtener_ciudadanos():
    return _leer_csv(ARCHIVO_CIUDADANOS, CAMPOS_CIUDADANO)


def guardar_ciudadano(nombres, apellidos, ciudad, correo, contrasenia):
    ciudadanos = obtener_ciudadanos()
    nuevo = {
        "id": _siguiente_id(ciudadanos),
        "nombres": nombres,
        "apellidos": apellidos,
        "ciudad": ciudad,
        "correo": correo.lower(),
        "password_hash": encriptar_contrasenia(contrasenia),
        "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    ciudadanos.append(nuevo)
    _escribir_csv(ARCHIVO_CIUDADANOS, CAMPOS_CIUDADANO, ciudadanos)
    return nuevo


def actualizar_contrasenia_ciudadano(correo, nueva_contrasenia):
    ciudadanos = obtener_ciudadanos()
    for c in ciudadanos:
        if c["correo"] == correo.lower():
            c["password_hash"] = encriptar_contrasenia(nueva_contrasenia)
            _escribir_csv(ARCHIVO_CIUDADANOS, CAMPOS_CIUDADANO, ciudadanos)
            return True
    return False


def buscar_ciudadano_por_correo(correo):
    for c in obtener_ciudadanos():
        if c["correo"] == correo.lower():
            return c
    return None


# ================= RECICLADORES =================

def obtener_recicladores():
    return _leer_csv(ARCHIVO_RECICLADORES, CAMPOS_RECICLADOR)


def guardar_reciclador(nombres, apellidos, ciudad, zona_cobertura, correo, contrasenia):
    recicladores = obtener_recicladores()
    nuevo = {
        "id": _siguiente_id(recicladores),
        "nombres": nombres,
        "apellidos": apellidos,
        "ciudad": ciudad,
        "zona_cobertura": zona_cobertura,
        "correo": correo.lower(),
        "password_hash": encriptar_contrasenia(contrasenia),
        "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    recicladores.append(nuevo)
    _escribir_csv(ARCHIVO_RECICLADORES, CAMPOS_RECICLADOR, recicladores)
    return nuevo


def actualizar_contrasenia_reciclador(correo, nueva_contrasenia):
    recicladores = obtener_recicladores()
    for r in recicladores:
        if r["correo"] == correo.lower():
            r["password_hash"] = encriptar_contrasenia(nueva_contrasenia)
            _escribir_csv(ARCHIVO_RECICLADORES, CAMPOS_RECICLADOR, recicladores)
            return True
    return False


def buscar_reciclador_por_correo(correo):
    for r in obtener_recicladores():
        if r["correo"] == correo.lower():
            return r
    return None


# ================= PUBLICACIONES DE MATERIALES =================

def obtener_publicaciones():
    return _leer(ARCHIVO_PUBLICACIONES, [])


def guardar_publicacion(ciudadano_correo, ciudadano_nombre, tipo_material,
                         peso_kg, foto, descripcion):
    publicaciones = obtener_publicaciones()
    nueva = {
        "id": _siguiente_id(publicaciones),
        "ciudadano_correo": ciudadano_correo.lower(),
        "ciudadano_nombre": ciudadano_nombre,
        "tipo_material": tipo_material,
        "peso_kg": peso_kg,
        "foto": foto,
        "descripcion": descripcion,
        "estado": "disponible",   # disponible -> negociacion -> vendido
        "fecha_publicacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ofertas": [],
    }
    publicaciones.append(nueva)
    _escribir(ARCHIVO_PUBLICACIONES, publicaciones)
    return nueva


def _guardar_todas_publicaciones(publicaciones):
    _escribir(ARCHIVO_PUBLICACIONES, publicaciones)


def agregar_oferta(publicacion_id, reciclador_correo, reciclador_nombre, precio):
    publicaciones = obtener_publicaciones()
    for pub in publicaciones:
        if pub["id"] == publicacion_id:
            id_oferta = 1
            if pub["ofertas"]:
                id_oferta = max(o["id"] for o in pub["ofertas"]) + 1
            oferta = {
                "id": id_oferta,
                "reciclador_correo": reciclador_correo.lower(),
                "reciclador_nombre": reciclador_nombre,
                "precio": precio,
                "estado": "pendiente",  # pendiente -> aceptada -> rechazada
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            pub["ofertas"].append(oferta)
            pub["estado"] = "negociacion"
            _guardar_todas_publicaciones(publicaciones)
            return oferta
    return None


def responder_oferta(publicacion_id, oferta_id, aceptar: bool):
    """El ciudadano acepta o rechaza una oferta puntual."""
    publicaciones = obtener_publicaciones()
    for pub in publicaciones:
        if pub["id"] == publicacion_id:
            for oferta in pub["ofertas"]:
                if oferta["id"] == oferta_id:
                    oferta["estado"] = "aceptada" if aceptar else "rechazada"
            # Si se aceptó una oferta, las demás quedan rechazadas automáticamente
            if aceptar:
                for oferta in pub["ofertas"]:
                    if oferta["id"] != oferta_id and oferta["estado"] == "pendiente":
                        oferta["estado"] = "rechazada"
            _guardar_todas_publicaciones(publicaciones)
            return True
    return False


def marcar_como_vendido(publicacion_id):
    publicaciones = obtener_publicaciones()
    for pub in publicaciones:
        if pub["id"] == publicacion_id:
            pub["estado"] = "vendido"
            _guardar_todas_publicaciones(publicaciones)
            return True
    return False


# ================= MENSAJES / CHAT =================

def obtener_mensajes(publicacion_id):
    todos = _leer(ARCHIVO_MENSAJES, {})
    return todos.get(str(publicacion_id), [])


def agregar_mensaje(publicacion_id, autor_nombre, autor_rol, texto):
    todos = _leer(ARCHIVO_MENSAJES, {})
    clave = str(publicacion_id)
    if clave not in todos:
        todos[clave] = []
    todos[clave].append({
        "autor": autor_nombre,
        "rol": autor_rol,
        "texto": texto,
        "hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })
    _escribir(ARCHIVO_MENSAJES, todos)

# -*- coding: utf-8 -*-
"""
almacenamiento.py
Se encarga de guardar y leer los datos de la aplicación.

- Los USUARIOS (ciudadanos y recicladores) se guardan en formato CSV,
  para que se puedan abrir directamente con doble clic en Excel.
  Cada rol tiene SU PROPIO archivo, para que nunca se mezclen:

    data/ciudadanos.csv      -> tabla de ciudadanos registrados
    data/recicladores.csv    -> tabla de recicladores registrados

- Las publicaciones de materiales, los mensajes del chat y las
  calificaciones se guardan en JSON porque tienen listas dentro de
  listas (ofertas, mensajes, comentarios) y eso no se representa
  bien en una tabla plana como CSV:

    data/publicaciones.json   -> materiales publicados + sus ofertas
    data/mensajes.json        -> chats entre ciudadano y reciclador
    data/calificaciones.json  -> calificaciones que los ciudadanos
                                  dejan a los recicladores

No se necesita ninguna base de datos ni librería externa,
todo funciona con los módulos "csv" y "json" que ya vienen
incluidos en Python.

NOVEDADES en esta versión (v4):
  - obtener_publicaciones() ahora se "auto-corrige" cada vez que se
    llama: si una publicación quedó guardada como "negociacion" pero
    ya no tiene ninguna oferta ACEPTADA (por ejemplo, porque la única
    oferta que tenía fue rechazada), se vuelve a poner "disponible"
    automáticamente. Esto es lo que hace posible que un reciclador
    rechazado pueda volver a ver el material y ofertar de nuevo, sin
    importar si los datos ya existentes habían quedado "atascados"
    de una versión anterior.
  - Los mensajes del chat ahora tienen:
      "id"           -> identificador único dentro de esa conversación
      "autor_correo" -> correo de quien escribió el mensaje
      "leido"        -> True/False, para mostrar el "visto" tipo WhatsApp
    Esto permite:
      * Marcar mensajes como leídos cuando el otro usuario abre el chat.
      * Contar cuántos mensajes no leídos tiene un usuario (para
        mostrar el avisito 🔴 en la interfaz).
      * Borrar un mensaje puntual, pero SOLO si quien borra es el
        mismo que lo escribió.

(Se mantienen todas las funciones de versiones anteriores: dirección
detallada del ciudadano, fotos de perfil, calificaciones, y el
comprobante de recolección.)
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
ARCHIVO_CALIFICACIONES = os.path.join(CARPETA_DATA, "calificaciones.json")

# Columnas de cada tabla CSV, en el orden en que aparecerán en Excel.
CAMPOS_CIUDADANO = ["id", "nombres", "apellidos", "ciudad", "parroquia",
                     "barrio", "referencia", "correo", "password_hash",
                     "foto_perfil", "fecha_registro"]
CAMPOS_RECICLADOR = ["id", "nombres", "apellidos", "ciudad", "zona_cobertura",
                      "correo", "password_hash", "foto_perfil", "fecha_registro"]


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

    # Archivos JSON de publicaciones, mensajes y calificaciones
    for archivo, valor_inicial in [
        (ARCHIVO_PUBLICACIONES, []),
        (ARCHIVO_MENSAJES, {}),
        (ARCHIVO_CALIFICACIONES, []),
    ]:
        if not os.path.exists(archivo):
            with open(archivo, "w", encoding="utf-8") as f:
                json.dump(valor_inicial, f, ensure_ascii=False, indent=2)


def _leer_csv(archivo, campos):
    """
    Lee un archivo CSV y retorna una lista de diccionarios.

    IMPORTANTE (compatibilidad hacia atrás): si el archivo fue creado
    con una versión anterior de esta app y le faltan columnas nuevas
    (por ejemplo 'parroquia' o 'foto_perfil'), esta función las
    completa con "" en vez de fallar. Así no se pierde la información
    que ya tenías guardada.
    """
    _asegurar_archivos()
    filas = []
    with open(archivo, "r", newline="", encoding="utf-8-sig") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            if fila.get("id"):
                fila["id"] = int(fila["id"])
                # Rellenamos cualquier columna nueva que no exista en filas viejas
                for campo in campos:
                    if campo not in fila or fila[campo] is None:
                        fila[campo] = ""
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


def guardar_ciudadano(nombres, apellidos, ciudad, correo, contrasenia,
                       parroquia="", barrio="", referencia=""):
    ciudadanos = obtener_ciudadanos()
    nuevo = {
        "id": _siguiente_id(ciudadanos),
        "nombres": nombres,
        "apellidos": apellidos,
        "ciudad": ciudad,
        "parroquia": parroquia,
        "barrio": barrio,
        "referencia": referencia,
        "correo": correo.lower(),
        "password_hash": encriptar_contrasenia(contrasenia),
        "foto_perfil": "",
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


def actualizar_perfil_ciudadano(correo, ciudad=None, parroquia=None,
                                 barrio=None, referencia=None, foto_perfil=None):
    """
    Actualiza los datos de perfil del ciudadano (dirección y/o foto).
    Solo se cambian los campos que se pasen (los que sean None se dejan igual).
    """
    ciudadanos = obtener_ciudadanos()
    for c in ciudadanos:
        if c["correo"] == correo.lower():
            if ciudad is not None:
                c["ciudad"] = ciudad
            if parroquia is not None:
                c["parroquia"] = parroquia
            if barrio is not None:
                c["barrio"] = barrio
            if referencia is not None:
                c["referencia"] = referencia
            if foto_perfil is not None:
                c["foto_perfil"] = foto_perfil
            _escribir_csv(ARCHIVO_CIUDADANOS, CAMPOS_CIUDADANO, ciudadanos)
            return c
    return None


def direccion_completa_ciudadano(ciudadano: dict) -> str:
    """
    Arma un texto legible de la dirección completa a partir de los
    campos separados. Si algún campo está vacío, simplemente se omite.
    Ejemplo: "Manta, Tarqui, Nuevo Manta (Ref: frente a la ferretería)"
    """
    partes = [ciudadano.get("ciudad", ""), ciudadano.get("parroquia", ""),
              ciudadano.get("barrio", "")]
    partes = [p for p in partes if p]
    texto = ", ".join(partes) if partes else "Sin dirección registrada"
    if ciudadano.get("referencia"):
        texto += f' (Ref: {ciudadano["referencia"]})'
    return texto


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
        "foto_perfil": "",
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


def actualizar_perfil_reciclador(correo, zona_cobertura=None, foto_perfil=None):
    """Actualiza la zona de cobertura y/o la foto de perfil del reciclador."""
    recicladores = obtener_recicladores()
    for r in recicladores:
        if r["correo"] == correo.lower():
            if zona_cobertura is not None:
                r["zona_cobertura"] = zona_cobertura
            if foto_perfil is not None:
                r["foto_perfil"] = foto_perfil
            _escribir_csv(ARCHIVO_RECICLADORES, CAMPOS_RECICLADOR, recicladores)
            return r
    return None


# ================= PUBLICACIONES DE MATERIALES =================

def _recalcular_estado_publicacion(pub):
    """
    Recalcula el estado de la publicación en función de sus ofertas
    actuales, para que nunca quede "atascada" en negociación.

        - Si ya fue marcada como vendida ("vendido"), no se toca.
        - Si tiene alguna oferta ACEPTADA, pasa (o se mantiene) en
          "negociacion" (así se oculta de "Materiales disponibles"
          mientras se concreta la venta con ese reciclador).
        - Si no tiene ninguna oferta aceptada (por ejemplo, porque la
          única que tenía fue rechazada), vuelve a "disponible" para
          que cualquier reciclador pueda seguir ofertando.
    """
    if pub.get("estado") == "vendido":
        return
    if any(o["estado"] == "aceptada" for o in pub["ofertas"]):
        pub["estado"] = "negociacion"
    else:
        pub["estado"] = "disponible"


def obtener_publicaciones():
    """
    Lee todas las publicaciones y, de paso, se "auto-corrige":
    si alguna quedó guardada como "negociacion" sin tener ya
    ninguna oferta aceptada (por ejemplo porque venía de una
    versión anterior de la app, o porque se rechazó la única
    oferta que tenía), se recalcula su estado real y -si cambió-
    se guarda ya corregido en el archivo, para que no vuelva a
    pasar lo mismo la próxima vez.
    """
    publicaciones = _leer(ARCHIVO_PUBLICACIONES, [])
    cambiado = False
    for pub in publicaciones:
        estado_anterior = pub.get("estado")
        _recalcular_estado_publicacion(pub)
        if pub.get("estado") != estado_anterior:
            cambiado = True
    if cambiado:
        _escribir(ARCHIVO_PUBLICACIONES, publicaciones)
    return publicaciones


def guardar_publicacion(ciudadano_correo, ciudadano_nombre, tipo_material,
                         peso_kg, foto, descripcion, precio_esperado=None):
    """
    precio_esperado es OPCIONAL: el ciudadano puede sugerir un precio
    de referencia (como en Mercado Libre), pero el reciclador sigue
    pudiendo ofertar un valor distinto. Si no se especifica, queda
    en None y simplemente no se muestra ese dato en las tarjetas.
    """
    publicaciones = obtener_publicaciones()
    nueva = {
        "id": _siguiente_id(publicaciones),
        "ciudadano_correo": ciudadano_correo.lower(),
        "ciudadano_nombre": ciudadano_nombre,
        "tipo_material": tipo_material,
        "peso_kg": peso_kg,
        "foto": foto,
        "descripcion": descripcion,
        "precio_esperado": precio_esperado,
        "estado": "disponible",   # disponible <-> negociacion -> vendido
        "fecha_publicacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ofertas": [],
    }
    publicaciones.append(nueva)
    _escribir(ARCHIVO_PUBLICACIONES, publicaciones)
    return nueva


def _guardar_todas_publicaciones(publicaciones):
    _escribir(ARCHIVO_PUBLICACIONES, publicaciones)


def agregar_oferta(publicacion_id, reciclador_correo, reciclador_nombre, precio):
    """
    Hacer una oferta pendiente NO cambia el estado de la publicación a
    "negociacion". Así, mientras no haya una oferta aceptada, la
    publicación se sigue viendo en "Materiales disponibles" para
    todos los recicladores (incluido el mismo que ya ofertó, quien
    simplemente verá su oferta como "pendiente" en vez del formulario).
    """
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
                "estado": "pendiente",  # pendiente -> aceptada / rechazada
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            pub["ofertas"].append(oferta)
            _recalcular_estado_publicacion(pub)
            _guardar_todas_publicaciones(publicaciones)
            return oferta
    return None


def responder_oferta(publicacion_id, oferta_id, aceptar: bool):
    """
    El ciudadano acepta o rechaza una oferta puntual.

    Si se rechaza y ya no queda ninguna oferta aceptada, la
    publicación vuelve automáticamente a "disponible" (ver
    _recalcular_estado_publicacion), en vez de quedarse en
    "negociacion" para siempre. Esto es lo que le permite al
    reciclador rechazado (o a cualquier otro) volver a ofertar.
    """
    publicaciones = obtener_publicaciones()
    for pub in publicaciones:
        if pub["id"] == publicacion_id:
            for oferta in pub["ofertas"]:
                if oferta["id"] == oferta_id:
                    oferta["estado"] = "aceptada" if aceptar else "rechazada"
            # Si se aceptó una oferta, las demás pendientes quedan rechazadas automáticamente
            if aceptar:
                for oferta in pub["ofertas"]:
                    if oferta["id"] != oferta_id and oferta["estado"] == "pendiente":
                        oferta["estado"] = "rechazada"
            _recalcular_estado_publicacion(pub)
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


def obtener_publicacion_por_id(publicacion_id):
    for pub in obtener_publicaciones():
        if pub["id"] == publicacion_id:
            return pub
    return None


def armar_comprobante_recoleccion(publicacion_id):
    """
    "Confirmación de Recolección" (tal como se propuso en el
    documento del proyecto).

    No se guarda como un archivo aparte: se arma "al vuelo" combinando
    datos que YA existen (la publicación + la oferta aceptada + el
    perfil del ciudadano), para no duplicar información en dos lugares
    distintos. Retorna None si la publicación no existe o si todavía
    no tiene una oferta aceptada.
    """
    pub = obtener_publicacion_por_id(publicacion_id)
    if pub is None:
        return None

    oferta_aceptada = next((o for o in pub["ofertas"] if o["estado"] == "aceptada"), None)
    if oferta_aceptada is None:
        return None

    ciudadano = buscar_ciudadano_por_correo(pub["ciudadano_correo"])
    direccion = direccion_completa_ciudadano(ciudadano) if ciudadano else "No disponible"

    return {
        "tipo_material": pub["tipo_material"],
        "peso_kg": pub["peso_kg"],
        "foto": pub["foto"],
        "descripcion": pub["descripcion"],
        "precio_acordado": oferta_aceptada["precio"],
        "ciudadano_nombre": pub["ciudadano_nombre"],
        "reciclador_nombre": oferta_aceptada["reciclador_nombre"],
        "direccion": direccion,
        "fecha_acuerdo": oferta_aceptada["fecha"],
        "estado_publicacion": pub["estado"],
    }


# ================= MENSAJES / CHAT =================
# Cada conversación se identifica por la pareja
# (publicacion_id, reciclador_correo), y no solo por publicacion_id.
# Esto evita que se mezclen los mensajes de distintos recicladores
# que interactúan con la misma publicación.
#
# Cada mensaje tiene:
#   id            -> identificador único DENTRO de esa conversación
#   autor         -> nombre para mostrar
#   autor_correo  -> correo de quien lo escribió (sirve para saber si
#                    es "mío" y para poder borrarlo)
#   rol           -> "ciudadano" o "reciclador"
#   texto         -> contenido del mensaje
#   hora          -> fecha y hora en que se envió
#   leido         -> True/False, si el otro usuario ya lo vio

def _clave_chat(publicacion_id, reciclador_correo):
    return f'{publicacion_id}_{reciclador_correo.lower()}'


def obtener_mensajes(publicacion_id, reciclador_correo):
    todos = _leer(ARCHIVO_MENSAJES, {})
    return todos.get(_clave_chat(publicacion_id, reciclador_correo), [])


def agregar_mensaje(publicacion_id, reciclador_correo, autor_nombre, autor_correo, autor_rol, texto):
    todos = _leer(ARCHIVO_MENSAJES, {})
    clave = _clave_chat(publicacion_id, reciclador_correo)
    if clave not in todos:
        todos[clave] = []

    siguiente_id = 1
    if todos[clave]:
        siguiente_id = max(m.get("id", 0) for m in todos[clave]) + 1

    todos[clave].append({
        "id": siguiente_id,
        "autor": autor_nombre,
        "autor_correo": autor_correo.lower(),
        "rol": autor_rol,
        "texto": texto,
        "hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "leido": False,
    })
    _escribir(ARCHIVO_MENSAJES, todos)


def marcar_mensajes_leidos(publicacion_id, reciclador_correo, rol_lector):
    """
    Marca como leídos todos los mensajes de esa conversación que NO
    fueron escritos por 'rol_lector' (es decir, los del otro
    participante). Se llama cada vez que alguien abre un chat.
    """
    todos = _leer(ARCHIVO_MENSAJES, {})
    clave = _clave_chat(publicacion_id, reciclador_correo)
    cambiado = False
    for m in todos.get(clave, []):
        if m.get("rol") != rol_lector and not m.get("leido", False):
            m["leido"] = True
            cambiado = True
    if cambiado:
        _escribir(ARCHIVO_MENSAJES, todos)


def contar_mensajes_no_leidos(publicacion_id, reciclador_correo, rol_lector):
    """Cuenta cuántos mensajes de ESA conversación todavía no ha visto 'rol_lector'."""
    mensajes = obtener_mensajes(publicacion_id, reciclador_correo)
    return sum(1 for m in mensajes if m.get("rol") != rol_lector and not m.get("leido", False))


def eliminar_mensaje(publicacion_id, reciclador_correo, mensaje_id, correo_autor):
    """
    Elimina un mensaje puntual, pero SOLO si quien lo pide ('correo_autor')
    es el mismo que lo escribió. Retorna True si se borró algo.
    """
    todos = _leer(ARCHIVO_MENSAJES, {})
    clave = _clave_chat(publicacion_id, reciclador_correo)
    lista = todos.get(clave, [])
    nueva_lista = [
        m for m in lista
        if not (m.get("id") == mensaje_id and m.get("autor_correo") == correo_autor.lower())
    ]
    if len(nueva_lista) != len(lista):
        todos[clave] = nueva_lista
        _escribir(ARCHIVO_MENSAJES, todos)
        return True
    return False


def total_no_leidos_ciudadano(ciudadano_correo):
    """
    Suma los mensajes no leídos de TODAS las conversaciones (con
    todos los recicladores) de las publicaciones de este ciudadano.
    Sirve para mostrar un avisito global en el menú / inicio.
    """
    total = 0
    for pub in obtener_publicaciones():
        if pub["ciudadano_correo"] != ciudadano_correo.lower():
            continue
        recicladores_involucrados = {o["reciclador_correo"] for o in pub["ofertas"]}
        for reciclador_correo in recicladores_involucrados:
            total += contar_mensajes_no_leidos(pub["id"], reciclador_correo, "ciudadano")
    return total


def total_no_leidos_reciclador(reciclador_correo):
    """Igual que la anterior, pero desde el lado del reciclador."""
    total = 0
    for pub in obtener_publicaciones():
        participa = any(o["reciclador_correo"] == reciclador_correo.lower() for o in pub["ofertas"])
        if not participa:
            continue
        total += contar_mensajes_no_leidos(pub["id"], reciclador_correo, "reciclador")
    return total


# ================= CALIFICACIONES =================
# El ciudadano califica al reciclador después de una venta (1 a 5
# estrellas + comentario opcional). No es obligatorio: se puede omitir.

def obtener_calificaciones():
    return _leer(ARCHIVO_CALIFICACIONES, [])


def ya_existe_calificacion(publicacion_id):
    """Evita que se pueda calificar dos veces la misma transacción."""
    return any(c["publicacion_id"] == publicacion_id for c in obtener_calificaciones())


def guardar_calificacion(publicacion_id, reciclador_correo, reciclador_nombre,
                          ciudadano_correo, ciudadano_nombre, puntaje, comentario=""):
    if not isinstance(puntaje, int) or not (1 <= puntaje <= 5):
        raise ValueError("El puntaje debe ser un entero entre 1 y 5.")

    calificaciones = obtener_calificaciones()
    nueva = {
        "id": _siguiente_id(calificaciones) if calificaciones else 1,
        "publicacion_id": publicacion_id,
        "reciclador_correo": reciclador_correo.lower(),
        "reciclador_nombre": reciclador_nombre,
        "ciudadano_correo": ciudadano_correo.lower(),
        "ciudadano_nombre": ciudadano_nombre,
        "puntaje": puntaje,
        "comentario": comentario.strip() if comentario else "",
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    calificaciones.append(nueva)
    _escribir(ARCHIVO_CALIFICACIONES, calificaciones)
    return nueva


def obtener_calificaciones_de_reciclador(reciclador_correo):
    return [c for c in obtener_calificaciones()
            if c["reciclador_correo"] == reciclador_correo.lower()]


def promedio_calificacion_reciclador(reciclador_correo):
    """
    Retorna una tupla (promedio, cantidad).
    Si el reciclador todavía no tiene calificaciones, retorna (0, 0).
    """
    califs = obtener_calificaciones_de_reciclador(reciclador_correo)
    if not califs:
        return 0, 0
    promedio = sum(c["puntaje"] for c in califs) / len(califs)
    return round(promedio, 1), len(califs)
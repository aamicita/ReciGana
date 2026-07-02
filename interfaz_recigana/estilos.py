# -*- coding: utf-8 -*-
"""
estilos.py
Paleta de colores de la interfaz de ReciGana.
Aquí se definen los colores del tema CLARO y del tema OSCURO.
Cambiar colores desde un solo lugar hace que sea fácil
mantener la app con un estilo consistente en todas las pantallas.
"""

# ---------- TEMA CLARO (verde reciclaje, fresco y limpio) ----------
TEMA_CLARO = {
    "bg_principal":   "#EAF7EC",   # Fondo general, verde muy clarito
    "bg_panel":       "#FFFFFF",   # Fondo de tarjetas/paneles
    "bg_menu":        "#DDF0DF",   # Fondo del menú lateral
    "primario":       "#2E7D32",   # Verde fuerte (botones principales)
    "primario_hover": "#1B5E20",   # Verde más oscuro (hover)
    "secundario":     "#66BB6A",   # Verde medio (acentos)
    "texto":          "#1B3B1E",   # Texto principal oscuro
    "texto_claro":    "#5C6B5D",   # Texto secundario / placeholders
    "borde":          "#B7DDB9",   # Bordes suaves
    "entrada_bg":     "#FFFFFF",   # Fondo de campos de texto
    "error":          "#C62828",   # Rojo para errores
    "exito":          "#2E7D32",   # Verde para mensajes de éxito
    "advertencia":    "#EF6C00",   # Naranja para advertencias/estados pendientes
    "blanco":         "#FFFFFF",
}

# ---------- TEMA OSCURO ----------
TEMA_OSCURO = {
    "bg_principal":   "#121612",
    "bg_panel":       "#1E241F",
    "bg_menu":        "#182019",
    "primario":       "#4CAF50",
    "primario_hover": "#66BB6A",
    "secundario":     "#81C784",
    "texto":          "#E8F5E9",
    "texto_claro":    "#A5B6A6",
    "borde":          "#33402F",
    "entrada_bg":     "#26302A",
    "error":          "#EF5350",
    "exito":          "#81C784",
    "advertencia":    "#FFB74D",
    "blanco":         "#FFFFFF",
}

FUENTE_TITULO   = ("Segoe UI", 26, "bold")
FUENTE_SUBTITULO = ("Segoe UI", 12, "italic")
FUENTE_SECCION  = ("Segoe UI", 16, "bold")
FUENTE_NORMAL   = ("Segoe UI", 11)
FUENTE_ETIQUETA = ("Segoe UI", 10, "bold")
FUENTE_BOTON    = ("Segoe UI", 11, "bold")


def obtener_tema(modo_oscuro: bool) -> dict:
    """Retorna el diccionario de colores según el modo activo."""
    return TEMA_OSCURO if modo_oscuro else TEMA_CLARO

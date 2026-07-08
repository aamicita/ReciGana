# -*- coding: utf-8 -*-
"""
app_recigana.py
================
Interfaz gráfica de ReciGana hecha con Tkinter (viene incluido con Python,
no requiere instalar nada más, EXCEPTO Pillow para poder mostrar las fotos
de los materiales -> pip install Pillow

Cómo ejecutar:
    python app_recigana.py

Estructura de pantallas (ACTUALIZADA):
    Login unificado (pantalla de inicio, elige rol con radiobuttons)
      ├── Recuperar contraseña
      ├── Registrarse
      │     ├── Registro Ciudadano  -> al terminar, va a Login unificado
      │     └── Registro Reciclador -> al terminar, va a Login unificado
      ├── Dashboard Ciudadano   (una vez logueado)
      │     └── Chat (con un reciclador, sobre una publicación con oferta aceptada)
      └── Dashboard Reciclador  (una vez logueado)
            └── Chat (con un ciudadano, sobre una publicación con oferta aceptada)

CAMBIO: ya no existe la pantalla "principal" (con REGISTRARSE / INICIAR
SESIÓN / SALIR). La aplicación abre directo en el login unificado, y al
cerrar sesión también se vuelve a esa misma pantalla.

CAMBIO: el chat ya NO se abre en una ventana aparte (Toplevel), porque en
Windows a veces esas ventanas no reciben el foco del teclado correctamente.
Ahora el chat es una pantalla más DENTRO de la misma ventana principal,
igual que "Publicar material" o "Mis publicaciones". Solo es visible una
vez que el usuario ya inició sesión.

Todos los datos se guardan en la carpeta 'data/' en archivos CSV/JSON
separados por rol (ver almacenamiento.py).
"""

import re
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

from PIL import Image, ImageTk

import almacenamiento as datos
from estilos import obtener_tema, FUENTE_TITULO, FUENTE_SUBTITULO, FUENTE_SECCION, \
    FUENTE_NORMAL, FUENTE_ETIQUETA, FUENTE_BOTON

PATRON_CORREO = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'


class ReciGanaApp(tk.Tk):
    """Ventana principal que controla el cambio entre pantallas."""

    def __init__(self):
        super().__init__()
        self.title("ReciGana")
        self.geometry("980x640")
        self.minsize(860, 580)

        # ----- Estado global de la aplicación -----
        self.modo_oscuro = False
        self.usuario_actual = None   # dict con los datos del usuario logueado
        self.rol_actual = None       # "ciudadano" o "reciclador"

        # Contenedor donde se dibuja la pantalla activa
        self.contenedor = tk.Frame(self)
        self.contenedor.pack(fill="both", expand=True)

        # La app abre directo en el login unificado (ya no hay pantalla "principal")
        self.mostrar_login_unificado()

    # ------------------------------------------------------------
    # Utilidad: limpia el contenedor antes de dibujar una pantalla nueva
    # ------------------------------------------------------------
    def _limpiar(self):
        for widget in self.contenedor.winfo_children():
            widget.destroy()

    def tema(self):
        return obtener_tema(self.modo_oscuro)

    # ------------------------------------------------------------
    # Widgets reutilizables
    # ------------------------------------------------------------
    def _boton(self, padre, texto, comando, color=None, ancho=22, hover=None):
        t = self.tema()
        color = color or t["primario"]
        hover = hover or t["primario_hover"]
        btn = tk.Button(
            padre, text=texto, command=comando, width=ancho,
            bg=color, fg=t["blanco"], activebackground=hover,
            activeforeground=t["blanco"], font=FUENTE_BOTON,
            relief="flat", cursor="hand2", bd=0, pady=8,
        )
        btn.bind("<Enter>", lambda e: btn.config(bg=hover))
        btn.bind("<Leave>", lambda e: btn.config(bg=color))
        return btn

    def _campo_texto(self, padre, etiqueta, mostrar=None, ancho=32):
        """Crea Label + Entry y retorna el Entry. mostrar='*' para contraseñas."""
        t = self.tema()
        tk.Label(padre, text=etiqueta, font=FUENTE_ETIQUETA,
                  bg=t["bg_panel"], fg=t["texto"]).pack(anchor="w", pady=(10, 2))
        entrada = tk.Entry(padre, width=ancho, font=FUENTE_NORMAL, show=mostrar,
                            bg=t["entrada_bg"], fg=t["texto"], relief="solid",
                            bd=1, highlightthickness=1,
                            highlightbackground=t["borde"], highlightcolor=t["primario"])
        entrada.pack(anchor="w", ipady=5, fill="x")
        return entrada

    def _campo_contrasenia(self, padre, etiqueta, ancho=32):
        """Campo de contraseña con botón de ojito para mostrar/ocultar."""
        t = self.tema()
        tk.Label(padre, text=etiqueta, font=FUENTE_ETIQUETA,
                  bg=t["bg_panel"], fg=t["texto"]).pack(anchor="w", pady=(10, 2))

        cont = tk.Frame(padre, bg=t["entrada_bg"], highlightthickness=1,
                         highlightbackground=t["borde"], highlightcolor=t["primario"])
        cont.pack(anchor="w", fill="x")

        entrada = tk.Entry(cont, width=ancho, font=FUENTE_NORMAL, show="*",
                            bg=t["entrada_bg"], fg=t["texto"], relief="flat", bd=0)
        entrada.pack(side="left", ipady=5, fill="x", expand=True, padx=(4, 0))

        estado = {"visible": False}

        def alternar():
            if estado["visible"]:
                entrada.config(show="*")
                boton_ojo.config(text="Mostrar")
            else:
                entrada.config(show="")
                boton_ojo.config(text="Ocultar")
            estado["visible"] = not estado["visible"]

        boton_ojo = tk.Button(cont, text="Mostrar", command=alternar, relief="flat",
                               bg=t["entrada_bg"], fg=t["primario"], cursor="hand2",
                               font=("Segoe UI", 9, "bold"), bd=0)
        boton_ojo.pack(side="right", padx=4)
        return entrada

    def _encabezado_pantalla(self, padre, titulo, subtitulo=None):
        t = self.tema()
        tk.Label(padre, text=titulo, font=FUENTE_SECCION,
                  bg=padre["bg"], fg=t["primario"]).pack(pady=(25, 4))
        if subtitulo:
            tk.Label(padre, text=subtitulo, font=FUENTE_NORMAL,
                      bg=padre["bg"], fg=t["texto_claro"]).pack(pady=(0, 10))

    # ==============================================================
    # SELECCIÓN DE TIPO DE USUARIO PARA REGISTRO
    # ==============================================================
    def mostrar_seleccion_registro(self):
        self._limpiar()
        t = self.tema()
        fondo = tk.Frame(self.contenedor, bg=t["bg_principal"])
        fondo.pack(fill="both", expand=True)

        centro = tk.Frame(fondo, bg=t["bg_principal"])
        centro.pack(expand=True)

        tk.Label(centro, text="¿Qué tipo de usuario eres?", font=FUENTE_SECCION,
                  bg=t["bg_principal"], fg=t["primario"]).pack(pady=(0, 30))

        self._boton(centro, "🙋 Soy Ciudadano", self.mostrar_registro_ciudadano, ancho=28).pack(pady=10)
        self._boton(centro, "♻ Soy Reciclador", self.mostrar_registro_reciclador,
                    color=t["secundario"], hover=t["primario"], ancho=28).pack(pady=10)
        self._boton(centro, "← Volver", self.mostrar_login_unificado, color=t["texto_claro"],
                    hover=t["texto"], ancho=28).pack(pady=(30, 10))

    # ==============================================================
    # REGISTRO — CIUDADANO
    # ==============================================================
    def mostrar_registro_ciudadano(self):
        self._limpiar()
        t = self.tema()
        fondo = tk.Frame(self.contenedor, bg=t["bg_principal"])
        fondo.pack(fill="both", expand=True)

        panel = tk.Frame(fondo, bg=t["bg_panel"], padx=40, pady=10,
                          highlightbackground=t["borde"], highlightthickness=1)
        panel.place(relx=0.5, rely=0.5, anchor="center")

        self._encabezado_pantalla(panel, "📋 Registro de Ciudadano",
                                    "Publica tus materiales reciclables y gana dinero")

        e_nombres = self._campo_texto(panel, "Nombres *")
        e_apellidos = self._campo_texto(panel, "Apellidos *")
        e_ciudad = self._campo_texto(panel, "Ciudad *")
        e_correo = self._campo_texto(panel, "Correo electrónico *")
        e_pass = self._campo_contrasenia(panel, "Contraseña * (mínimo 6 caracteres)")
        e_pass2 = self._campo_contrasenia(panel, "Confirmar contraseña *")

        def registrar():
            nombres = e_nombres.get().strip()
            apellidos = e_apellidos.get().strip()
            ciudad = e_ciudad.get().strip()
            correo = e_correo.get().strip()
            clave = e_pass.get()
            clave2 = e_pass2.get()

            if not all([nombres, apellidos, ciudad, correo, clave, clave2]):
                messagebox.showerror("Campos incompletos", "Todos los campos son obligatorios.")
                return
            if not re.match(PATRON_CORREO, correo):
                messagebox.showerror("Correo inválido", "Ingresa un correo electrónico válido.")
                return
            if datos.buscar_ciudadano_por_correo(correo) or datos.buscar_reciclador_por_correo(correo):
                messagebox.showerror("Correo en uso", "Ya existe una cuenta registrada con ese correo.")
                return
            if len(clave) < 6:
                messagebox.showerror("Contraseña débil", "La contraseña debe tener al menos 6 caracteres.")
                return
            if clave != clave2:
                messagebox.showerror("No coincide", "Las contraseñas no coinciden.")
                return

            datos.guardar_ciudadano(nombres, apellidos, ciudad, correo, clave)
            messagebox.showinfo("¡Listo!", f"Ciudadano '{nombres}' registrado exitosamente.\nYa puedes iniciar sesión.")
            self.mostrar_login_unificado()

        botones = tk.Frame(panel, bg=t["bg_panel"])
        botones.pack(pady=25)
        self._boton(botones, "REGISTRAR CIUDADANO", registrar, ancho=24).pack(pady=6)
        self._boton(botones, "← Volver", self.mostrar_seleccion_registro,
                    color=t["texto_claro"], hover=t["texto"], ancho=24).pack(pady=6)

    # ==============================================================
    # REGISTRO — RECICLADOR
    # ==============================================================
    def mostrar_registro_reciclador(self):
        self._limpiar()
        t = self.tema()
        fondo = tk.Frame(self.contenedor, bg=t["bg_principal"])
        fondo.pack(fill="both", expand=True)

        panel = tk.Frame(fondo, bg=t["bg_panel"], padx=40, pady=10,
                          highlightbackground=t["borde"], highlightthickness=1)
        panel.place(relx=0.5, rely=0.5, anchor="center")

        self._encabezado_pantalla(panel, "♻ Registro de Reciclador",
                                    "Encuentra materiales cerca de ti y haz tus ofertas")

        e_nombres = self._campo_texto(panel, "Nombres *")
        e_apellidos = self._campo_texto(panel, "Apellidos *")
        e_ciudad = self._campo_texto(panel, "Ciudad *")
        e_zona = self._campo_texto(panel, "Zona de cobertura * (ej: Manta Centro, Tarqui)")
        e_correo = self._campo_texto(panel, "Correo electrónico *")
        e_pass = self._campo_contrasenia(panel, "Contraseña * (mínimo 6 caracteres)")
        e_pass2 = self._campo_contrasenia(panel, "Confirmar contraseña *")

        def registrar():
            nombres = e_nombres.get().strip()
            apellidos = e_apellidos.get().strip()
            ciudad = e_ciudad.get().strip()
            zona = e_zona.get().strip()
            correo = e_correo.get().strip()
            clave = e_pass.get()
            clave2 = e_pass2.get()

            if not all([nombres, apellidos, ciudad, zona, correo, clave, clave2]):
                messagebox.showerror("Campos incompletos", "Todos los campos son obligatorios.")
                return
            if not re.match(PATRON_CORREO, correo):
                messagebox.showerror("Correo inválido", "Ingresa un correo electrónico válido.")
                return
            if datos.buscar_ciudadano_por_correo(correo) or datos.buscar_reciclador_por_correo(correo):
                messagebox.showerror("Correo en uso", "Ya existe una cuenta registrada con ese correo.")
                return
            if len(clave) < 6:
                messagebox.showerror("Contraseña débil", "La contraseña debe tener al menos 6 caracteres.")
                return
            if clave != clave2:
                messagebox.showerror("No coincide", "Las contraseñas no coinciden.")
                return

            datos.guardar_reciclador(nombres, apellidos, ciudad, zona, correo, clave)
            messagebox.showinfo("¡Listo!", f"Reciclador '{nombres}' registrado exitosamente.\nYa puedes iniciar sesión.")
            self.mostrar_login_unificado()

        botones = tk.Frame(panel, bg=t["bg_panel"])
        botones.pack(pady=25)
        self._boton(botones, "REGISTRAR RECICLADOR", registrar, ancho=24).pack(pady=6)
        self._boton(botones, "← Volver", self.mostrar_seleccion_registro,
                    color=t["texto_claro"], hover=t["texto"], ancho=24).pack(pady=6)

    # ==============================================================
    # LOGIN UNIFICADO
    # Es la PANTALLA DE INICIO de toda la aplicación, y también
    # a donde se regresa al cerrar sesión.
    # ==============================================================
    def mostrar_login_unificado(self):
        self._limpiar()
        t = self.tema()
        self.usuario_actual = None
        self.rol_actual = None

        fondo = tk.Frame(self.contenedor, bg=t["bg_principal"])
        fondo.pack(fill="both", expand=True)

        # Botón pequeño de modo oscuro arriba a la derecha
        barra_top = tk.Frame(fondo, bg=t["bg_principal"])
        barra_top.pack(fill="x")
        icono = "☀ Modo claro" if self.modo_oscuro else "🌙 Modo oscuro"
        tk.Button(barra_top, text=icono, command=self._alternar_modo_oscuro,
                  relief="flat", bg=t["bg_principal"], fg=t["primario"],
                  font=("Segoe UI", 10, "bold"), cursor="hand2"
                  ).pack(anchor="ne", padx=20, pady=15)

        tk.Label(fondo, text="♻ ReciGana", font=FUENTE_TITULO,
                  bg=t["bg_principal"], fg=t["primario"]).pack(pady=(10, 4))
        tk.Label(fondo, text="¡Recicla, gana y ayuda al planeta!",
                  font=FUENTE_SUBTITULO, bg=t["bg_principal"],
                  fg=t["texto_claro"]).pack(pady=(0, 20))

        panel = tk.Frame(fondo, bg=t["bg_panel"], padx=40, pady=20,
                          highlightbackground=t["borde"], highlightthickness=1)
        panel.pack()

        self._encabezado_pantalla(panel, "Iniciar sesión")

        tk.Label(panel, text="Soy:", font=FUENTE_ETIQUETA,
                  bg=t["bg_panel"], fg=t["texto"]).pack(anchor="w", pady=(5, 2))
        rol_var = tk.StringVar(value="ciudadano")
        fila_rol = tk.Frame(panel, bg=t["bg_panel"])
        fila_rol.pack(anchor="w", pady=(0, 5))
        tk.Radiobutton(fila_rol, text="🙋 Ciudadano", variable=rol_var, value="ciudadano",
                        bg=t["bg_panel"], fg=t["texto"], selectcolor=t["bg_panel"],
                        font=FUENTE_NORMAL, activebackground=t["bg_panel"]).pack(side="left", padx=(0, 15))
        tk.Radiobutton(fila_rol, text="♻ Reciclador", variable=rol_var, value="reciclador",
                        bg=t["bg_panel"], fg=t["texto"], selectcolor=t["bg_panel"],
                        font=FUENTE_NORMAL, activebackground=t["bg_panel"]).pack(side="left")

        e_correo = self._campo_texto(panel, "Correo electrónico")
        e_pass = self._campo_contrasenia(panel, "Contraseña")

        etiqueta_error = tk.Label(panel, text="", font=("Segoe UI", 9, "bold"),
                                    bg=t["bg_panel"], fg=t["error"])
        etiqueta_error.pack(pady=(8, 0))

        enlace_olvido = tk.Label(panel, text="¿Olvidaste tu contraseña?",
                                   font=("Segoe UI", 9, "underline"),
                                   bg=t["bg_panel"], fg=t["primario"], cursor="hand2")
        enlace_olvido.pack(pady=(6, 0))
        enlace_olvido.bind("<Button-1>", lambda e: self.mostrar_recuperar_contrasenia(rol_var.get()))

        def iniciar_sesion():
            correo = e_correo.get().strip()
            clave = e_pass.get()
            rol = rol_var.get()

            if not correo or not clave:
                etiqueta_error.config(text="Debes ingresar correo y contraseña.")
                return

            if rol == "ciudadano":
                usuario = datos.buscar_ciudadano_por_correo(correo)
            else:
                usuario = datos.buscar_reciclador_por_correo(correo)

            if not usuario or usuario["password_hash"] != datos.encriptar_contrasenia(clave):
                etiqueta_error.config(text="Correo o contraseña incorrectos.")
                return

            self.usuario_actual = usuario
            self.rol_actual = rol
            if rol == "ciudadano":
                self.mostrar_dashboard_ciudadano()
            else:
                self.mostrar_dashboard_reciclador()

        botones = tk.Frame(panel, bg=t["bg_panel"])
        botones.pack(pady=20)
        self._boton(botones, "INICIAR SESIÓN", iniciar_sesion, ancho=24).pack(pady=6)

        enlace_registro = tk.Label(panel, text="¿No tienes cuenta? Regístrate aquí",
                                     font=("Segoe UI", 9, "underline"),
                                     bg=t["bg_panel"], fg=t["secundario"], cursor="hand2")
        enlace_registro.pack(pady=(10, 0))
        enlace_registro.bind("<Button-1>", lambda e: self.mostrar_seleccion_registro())

        e_correo.focus_set()
        e_correo.bind("<Return>", lambda e: iniciar_sesion())
        e_pass.bind("<Return>", lambda e: iniciar_sesion())

    def _alternar_modo_oscuro(self):
        self.modo_oscuro = not self.modo_oscuro
        self.mostrar_login_unificado()

    # ==============================================================
    # RECUPERAR / RESTABLECER CONTRASEÑA
    # ==============================================================
    def mostrar_recuperar_contrasenia(self, rol):
        self._limpiar()
        t = self.tema()
        fondo = tk.Frame(self.contenedor, bg=t["bg_principal"])
        fondo.pack(fill="both", expand=True)

        panel = tk.Frame(fondo, bg=t["bg_panel"], padx=40, pady=10,
                          highlightbackground=t["borde"], highlightthickness=1)
        panel.place(relx=0.5, rely=0.5, anchor="center")

        self._encabezado_pantalla(panel, "🔑 Recuperar contraseña",
                                    f"Rol: {rol.capitalize()}")

        e_correo = self._campo_texto(panel, "Correo electrónico registrado")
        e_nueva = self._campo_contrasenia(panel, "Nueva contraseña (mínimo 6 caracteres)")
        e_nueva2 = self._campo_contrasenia(panel, "Confirmar nueva contraseña")

        def restablecer():
            correo = e_correo.get().strip()
            nueva = e_nueva.get()
            nueva2 = e_nueva2.get()

            if not correo or not nueva or not nueva2:
                messagebox.showerror("Campos incompletos", "Todos los campos son obligatorios.")
                return

            if rol == "ciudadano":
                existe = datos.buscar_ciudadano_por_correo(correo)
            else:
                existe = datos.buscar_reciclador_por_correo(correo)

            if not existe:
                messagebox.showerror("No encontrado", "No existe una cuenta con ese correo en este rol.")
                return
            if len(nueva) < 6:
                messagebox.showerror("Contraseña débil", "La contraseña debe tener al menos 6 caracteres.")
                return
            if nueva != nueva2:
                messagebox.showerror("No coincide", "Las contraseñas no coinciden.")
                return

            if rol == "ciudadano":
                datos.actualizar_contrasenia_ciudadano(correo, nueva)
            else:
                datos.actualizar_contrasenia_reciclador(correo, nueva)

            messagebox.showinfo("¡Listo!", "Tu contraseña fue actualizada. Ya puedes iniciar sesión.")
            self.mostrar_login_unificado()

        botones = tk.Frame(panel, bg=t["bg_panel"])
        botones.pack(pady=20)
        self._boton(botones, "RESTABLECER CONTRASEÑA", restablecer, ancho=26).pack(pady=6)
        self._boton(botones, "← Volver", self.mostrar_login_unificado,
                    color=t["texto_claro"], hover=t["texto"], ancho=26).pack(pady=6)

    # ==============================================================
    # ESTRUCTURA COMÚN DE DASHBOARD (menú lateral + área de contenido)
    # ==============================================================
    def _crear_estructura_dashboard(self, titulo_menu, opciones):
        """
        opciones: lista de tuplas (texto_boton, comando)
        Retorna el frame 'area_contenido' donde cada sección dibuja lo suyo.
        """
        t = self.tema()
        fondo = tk.Frame(self.contenedor, bg=t["bg_principal"])
        fondo.pack(fill="both", expand=True)

        # ---- Menú lateral ----
        menu = tk.Frame(fondo, bg=t["bg_menu"], width=230)
        menu.pack(side="left", fill="y")
        menu.pack_propagate(False)

        nombre = f'{self.usuario_actual["nombres"]} {self.usuario_actual["apellidos"]}'
        tk.Label(menu, text="♻ ReciGana", font=("Segoe UI", 16, "bold"),
                  bg=t["bg_menu"], fg=t["primario"]).pack(pady=(20, 2))
        tk.Label(menu, text=titulo_menu, font=("Segoe UI", 10, "bold"),
                  bg=t["bg_menu"], fg=t["texto_claro"]).pack(pady=(0, 5))
        tk.Label(menu, text=nombre, font=("Segoe UI", 10),
                  bg=t["bg_menu"], fg=t["texto"], wraplength=200,
                  justify="center").pack(pady=(0, 20))

        for texto, comando in opciones:
            b = tk.Button(menu, text=texto, command=comando, anchor="w",
                          bg=t["bg_menu"], fg=t["texto"], relief="flat",
                          font=FUENTE_NORMAL, cursor="hand2", padx=15, pady=10)
            b.pack(fill="x")
            b.bind("<Enter>", lambda e, btn=b: btn.config(bg=t["borde"]))
            b.bind("<Leave>", lambda e, btn=b: btn.config(bg=t["bg_menu"]))

        icono_tema = "☀ Modo claro" if self.modo_oscuro else "🌙 Modo oscuro"
        tk.Button(menu, text=icono_tema, command=self._alternar_modo_oscuro_dashboard,
                  bg=t["bg_menu"], fg=t["primario"], relief="flat",
                  font=("Segoe UI", 9, "bold"), cursor="hand2").pack(side="bottom", pady=10)
        tk.Button(menu, text="🚪 Cerrar sesión", command=self.mostrar_login_unificado,
                  bg=t["error"], fg=t["blanco"], relief="flat",
                  font=FUENTE_BOTON, cursor="hand2", pady=8).pack(side="bottom", fill="x")

        # ---- Área de contenido ----
        area = tk.Frame(fondo, bg=t["bg_principal"])
        area.pack(side="left", fill="both", expand=True)
        return area

    def _alternar_modo_oscuro_dashboard(self):
        self.modo_oscuro = not self.modo_oscuro
        if self.rol_actual == "ciudadano":
            self.mostrar_dashboard_ciudadano()
        else:
            self.mostrar_dashboard_reciclador()

    # ==============================================================
    # DASHBOARD — CIUDADANO
    # ==============================================================
    def mostrar_dashboard_ciudadano(self, seccion="inicio"):
        self._limpiar()
        opciones = [
            ("🏠 Inicio", lambda: self.mostrar_dashboard_ciudadano("inicio")),
            ("📦 Publicar material", lambda: self.mostrar_dashboard_ciudadano("publicar")),
            ("📋 Mis publicaciones", lambda: self.mostrar_dashboard_ciudadano("publicaciones")),
        ]
        area = self._crear_estructura_dashboard("Panel del Ciudadano", opciones)

        if seccion == "inicio":
            self._seccion_bienvenida_ciudadano(area)
        elif seccion == "publicar":
            self._seccion_publicar_material(area)
        elif seccion == "publicaciones":
            self._seccion_mis_publicaciones(area)

    def _seccion_bienvenida_ciudadano(self, area):
        t = self.tema()
        mis_pubs = [p for p in datos.obtener_publicaciones()
                    if p["ciudadano_correo"] == self.usuario_actual["correo"]]
        disponibles = sum(1 for p in mis_pubs if p["estado"] != "vendido")
        vendidos = sum(1 for p in mis_pubs if p["estado"] == "vendido")
        total_ofertas = sum(len(p["ofertas"]) for p in mis_pubs)

        tk.Label(area, text=f'¡Bienvenido, {self.usuario_actual["nombres"]}! 🌿',
                  font=FUENTE_SECCION, bg=t["bg_principal"], fg=t["primario"]
                  ).pack(anchor="w", padx=30, pady=(30, 5))
        tk.Label(area, text="Publica tus materiales reciclables y conecta con recicladores de tu zona.",
                  font=FUENTE_NORMAL, bg=t["bg_principal"], fg=t["texto_claro"]
                  ).pack(anchor="w", padx=30, pady=(0, 20))

        tarjetas = tk.Frame(area, bg=t["bg_principal"])
        tarjetas.pack(anchor="w", padx=30)
        for titulo, valor in [("Publicaciones activas", disponibles),
                               ("Materiales vendidos", vendidos),
                               ("Ofertas recibidas", total_ofertas)]:
            tarjeta = tk.Frame(tarjetas, bg=t["bg_panel"], padx=25, pady=20,
                                highlightbackground=t["borde"], highlightthickness=1)
            tarjeta.pack(side="left", padx=10)
            tk.Label(tarjeta, text=str(valor), font=("Segoe UI", 22, "bold"),
                      bg=t["bg_panel"], fg=t["primario"]).pack()
            tk.Label(tarjeta, text=titulo, font=FUENTE_NORMAL,
                      bg=t["bg_panel"], fg=t["texto_claro"]).pack()

    def _seccion_publicar_material(self, area):
        t = self.tema()
        panel = tk.Frame(area, bg=t["bg_panel"], padx=35, pady=20,
                          highlightbackground=t["borde"], highlightthickness=1)
        panel.pack(anchor="w", padx=30, pady=25, fill="x")

        tk.Label(panel, text="📦 Publicar nuevo material", font=FUENTE_SECCION,
                  bg=t["bg_panel"], fg=t["primario"]).pack(anchor="w", pady=(0, 15))

        tk.Label(panel, text="Tipo de material *", font=FUENTE_ETIQUETA,
                  bg=t["bg_panel"], fg=t["texto"]).pack(anchor="w", pady=(5, 2))
        combo_tipo = ttk.Combobox(panel, state="readonly", width=30, values=[
            "Plástico", "Vidrio", "Metal", "Papel", "Cartón", "Orgánico"
        ])
        combo_tipo.pack(anchor="w", ipady=3)

        e_peso = self._campo_texto(panel, "Peso en kg *", ancho=32)
        e_desc = self._campo_texto(panel, "Descripción (opcional)", ancho=32)

        ruta_foto = tk.StringVar(value="")
        tk.Label(panel, text="Foto del material (opcional)", font=FUENTE_ETIQUETA,
                  bg=t["bg_panel"], fg=t["texto"]).pack(anchor="w", pady=(10, 2))
        fila_foto = tk.Frame(panel, bg=t["bg_panel"])
        fila_foto.pack(anchor="w")
        etiqueta_foto = tk.Label(fila_foto, text="Ningún archivo seleccionado",
                                   font=("Segoe UI", 9), bg=t["bg_panel"], fg=t["texto_claro"])
        etiqueta_foto.pack(side="left", padx=(0, 10))

        def elegir_foto():
            archivo = filedialog.askopenfilename(
                title="Selecciona una foto del material",
                filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.gif *.bmp")]
            )
            if archivo:
                ruta_foto.set(archivo)
                nombre_corto = archivo.split("/")[-1].split("\\")[-1]
                etiqueta_foto.config(text=nombre_corto, fg=t["exito"])

        tk.Button(fila_foto, text="📷 Elegir foto", command=elegir_foto,
                  bg=t["secundario"], fg=t["blanco"], relief="flat",
                  cursor="hand2", font=("Segoe UI", 9, "bold"), padx=10, pady=4).pack(side="left")

        def publicar():
            tipo = combo_tipo.get()
            peso_texto = e_peso.get().strip()
            descripcion = e_desc.get().strip()

            if not tipo:
                messagebox.showerror("Falta información", "Selecciona el tipo de material.")
                return
            if not peso_texto:
                messagebox.showerror("Falta información", "Ingresa el peso del material.")
                return
            try:
                peso = float(peso_texto)
                if peso <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Peso inválido", "El peso debe ser un número mayor a cero.")
                return

            nombre_completo = f'{self.usuario_actual["nombres"]} {self.usuario_actual["apellidos"]}'
            datos.guardar_publicacion(
                self.usuario_actual["correo"], nombre_completo, tipo,
                peso, ruta_foto.get(), descripcion
            )
            messagebox.showinfo("¡Publicado!", f"Tu material de {tipo.lower()} ({peso} kg) fue publicado.")
            self.mostrar_dashboard_ciudadano("publicaciones")

        self._boton(panel, "PUBLICAR MATERIAL", publicar, ancho=26).pack(pady=(20, 0))

    def _seccion_mis_publicaciones(self, area):
        t = self.tema()
        tk.Label(area, text="📋 Mis publicaciones", font=FUENTE_SECCION,
                  bg=t["bg_principal"], fg=t["primario"]).pack(anchor="w", padx=30, pady=(25, 10))

        mis_pubs = [p for p in datos.obtener_publicaciones()
                    if p["ciudadano_correo"] == self.usuario_actual["correo"]]

        contenedor_scroll = self._crear_area_scroll(area)

        if not mis_pubs:
            tk.Label(contenedor_scroll, text="Todavía no has publicado ningún material.",
                      font=FUENTE_NORMAL, bg=t["bg_principal"], fg=t["texto_claro"]
                      ).pack(anchor="w", padx=10, pady=20)
            return

        for pub in reversed(mis_pubs):
            self._tarjeta_publicacion_ciudadano(contenedor_scroll, pub)

    def _tarjeta_publicacion_ciudadano(self, padre, pub):
        t = self.tema()
        colores_estado = {
            "disponible": t["exito"], "negociacion": t["advertencia"], "vendido": t["texto_claro"]
        }
        tarjeta = tk.Frame(padre, bg=t["bg_panel"], padx=20, pady=15,
                            highlightbackground=t["borde"], highlightthickness=1)
        tarjeta.pack(fill="x", padx=10, pady=8)

        fila = tk.Frame(tarjeta, bg=t["bg_panel"])
        fila.pack(fill="x")
        tk.Label(fila, text=f'{pub["tipo_material"]} — {pub["peso_kg"]} kg',
                  font=("Segoe UI", 13, "bold"), bg=t["bg_panel"], fg=t["texto"]
                  ).pack(side="left")
        tk.Label(fila, text=pub["estado"].upper(), font=("Segoe UI", 9, "bold"),
                  bg=t["bg_panel"], fg=colores_estado.get(pub["estado"], t["texto"])
                  ).pack(side="right")

        if pub.get("descripcion"):
            tk.Label(tarjeta, text=pub["descripcion"], font=FUENTE_NORMAL,
                      bg=t["bg_panel"], fg=t["texto_claro"], wraplength=600, justify="left"
                      ).pack(anchor="w", pady=(5, 0))

        tk.Label(tarjeta, text=f'Publicado: {pub["fecha_publicacion"]}',
                  font=("Segoe UI", 8), bg=t["bg_panel"], fg=t["texto_claro"]
                  ).pack(anchor="w", pady=(4, 8))

        ofertas_pendientes = [o for o in pub["ofertas"] if o["estado"] == "pendiente"]
        if ofertas_pendientes:
            tk.Label(tarjeta, text=f"💰 {len(ofertas_pendientes)} oferta(s) pendiente(s):",
                      font=FUENTE_ETIQUETA, bg=t["bg_panel"], fg=t["primario"]).pack(anchor="w")
            for oferta in ofertas_pendientes:
                fila_oferta = tk.Frame(tarjeta, bg=t["bg_panel"])
                fila_oferta.pack(fill="x", pady=3)
                tk.Label(fila_oferta,
                          text=f'{oferta["reciclador_nombre"]} ofrece ${oferta["precio"]}',
                          font=FUENTE_NORMAL, bg=t["bg_panel"], fg=t["texto"]).pack(side="left")
                tk.Button(fila_oferta, text="✔ Aceptar", bg=t["primario"], fg=t["blanco"],
                          relief="flat", cursor="hand2", font=("Segoe UI", 9, "bold"),
                          command=lambda p=pub, o=oferta: self._responder_oferta_ui(p, o, True)
                          ).pack(side="right", padx=3)
                tk.Button(fila_oferta, text="✘ Rechazar", bg=t["error"], fg=t["blanco"],
                          relief="flat", cursor="hand2", font=("Segoe UI", 9, "bold"),
                          command=lambda p=pub, o=oferta: self._responder_oferta_ui(p, o, False)
                          ).pack(side="right", padx=3)

        oferta_aceptada = next((o for o in pub["ofertas"] if o["estado"] == "aceptada"), None)
        botonera = tk.Frame(tarjeta, bg=t["bg_panel"])
        botonera.pack(anchor="w", pady=(8, 0))
        if oferta_aceptada:
            tk.Button(botonera, text=f'💬 Chatear con {oferta_aceptada["reciclador_nombre"]}',
                      bg=t["secundario"], fg=t["blanco"], relief="flat", cursor="hand2",
                      font=("Segoe UI", 9, "bold"), padx=10, pady=4,
                      command=lambda p=pub, o=oferta_aceptada: self.mostrar_chat(p, o["reciclador_nombre"])
                      ).pack(side="left", padx=(0, 8))
        if pub["estado"] != "vendido":
            tk.Button(botonera, text="📦 Marcar como vendido", bg=t["texto_claro"], fg=t["blanco"],
                      relief="flat", cursor="hand2", font=("Segoe UI", 9, "bold"), padx=10, pady=4,
                      command=lambda p=pub: self._marcar_vendido_ui(p)
                      ).pack(side="left")

    def _responder_oferta_ui(self, publicacion, oferta, aceptar):
        datos.responder_oferta(publicacion["id"], oferta["id"], aceptar)
        accion = "aceptada" if aceptar else "rechazada"
        messagebox.showinfo("Listo", f'Oferta de {oferta["reciclador_nombre"]} {accion}.')
        self.mostrar_dashboard_ciudadano("publicaciones")

    def _marcar_vendido_ui(self, publicacion):
        if messagebox.askyesno("Confirmar", "¿Marcar este material como vendido?\n"
                                              "Ya no aparecerá para otros recicladores."):
            datos.marcar_como_vendido(publicacion["id"])
            self.mostrar_dashboard_ciudadano("publicaciones")

    # ==============================================================
    # DASHBOARD — RECICLADOR
    # ==============================================================
    def mostrar_dashboard_reciclador(self, seccion="inicio"):
        self._limpiar()
        opciones = [
            ("🏠 Inicio", lambda: self.mostrar_dashboard_reciclador("inicio")),
            ("🔍 Materiales disponibles", lambda: self.mostrar_dashboard_reciclador("disponibles")),
            ("📑 Mis ofertas", lambda: self.mostrar_dashboard_reciclador("mis_ofertas")),
        ]
        area = self._crear_estructura_dashboard("Panel del Reciclador", opciones)

        if seccion == "inicio":
            self._seccion_bienvenida_reciclador(area)
        elif seccion == "disponibles":
            self._seccion_materiales_disponibles(area)
        elif seccion == "mis_ofertas":
            self._seccion_mis_ofertas(area)

    def _seccion_bienvenida_reciclador(self, area):
        t = self.tema()
        todas = datos.obtener_publicaciones()
        disponibles = sum(1 for p in todas if p["estado"] == "disponible")
        mis_ofertas = [o for p in todas for o in p["ofertas"]
                       if o["reciclador_correo"] == self.usuario_actual["correo"]]
        aceptadas = sum(1 for o in mis_ofertas if o["estado"] == "aceptada")

        tk.Label(area, text=f'¡Bienvenido, {self.usuario_actual["nombres"]}! ♻',
                  font=FUENTE_SECCION, bg=t["bg_principal"], fg=t["primario"]
                  ).pack(anchor="w", padx=30, pady=(30, 5))
        tk.Label(area, text=f'Zona de cobertura: {self.usuario_actual.get("zona_cobertura", "-")}',
                  font=FUENTE_NORMAL, bg=t["bg_principal"], fg=t["texto_claro"]
                  ).pack(anchor="w", padx=30, pady=(0, 20))

        tarjetas = tk.Frame(area, bg=t["bg_principal"])
        tarjetas.pack(anchor="w", padx=30)
        for titulo, valor in [("Materiales disponibles", disponibles),
                               ("Ofertas realizadas", len(mis_ofertas)),
                               ("Ofertas aceptadas", aceptadas)]:
            tarjeta = tk.Frame(tarjetas, bg=t["bg_panel"], padx=25, pady=20,
                                highlightbackground=t["borde"], highlightthickness=1)
            tarjeta.pack(side="left", padx=10)
            tk.Label(tarjeta, text=str(valor), font=("Segoe UI", 22, "bold"),
                      bg=t["bg_panel"], fg=t["primario"]).pack()
            tk.Label(tarjeta, text=titulo, font=FUENTE_NORMAL,
                      bg=t["bg_panel"], fg=t["texto_claro"]).pack()

    def _seccion_materiales_disponibles(self, area):
        t = self.tema()
        tk.Label(area, text="🔍 Materiales disponibles", font=FUENTE_SECCION,
                  bg=t["bg_principal"], fg=t["primario"]).pack(anchor="w", padx=30, pady=(25, 10))

        disponibles = [p for p in datos.obtener_publicaciones() if p["estado"] == "disponible"]
        contenedor_scroll = self._crear_area_scroll(area)

        if not disponibles:
            tk.Label(contenedor_scroll, text="No hay materiales disponibles por el momento.",
                      font=FUENTE_NORMAL, bg=t["bg_principal"], fg=t["texto_claro"]
                      ).pack(anchor="w", padx=10, pady=20)
            return

        for pub in reversed(disponibles):
            self._tarjeta_publicacion_reciclador(contenedor_scroll, pub)

    def _tarjeta_publicacion_reciclador(self, padre, pub):
        t = self.tema()
        tarjeta = tk.Frame(padre, bg=t["bg_panel"], padx=20, pady=15,
                            highlightbackground=t["borde"], highlightthickness=1)
        tarjeta.pack(fill="x", padx=10, pady=8)

        tk.Label(tarjeta, text=f'{pub["tipo_material"]} — {pub["peso_kg"]} kg',
                  font=("Segoe UI", 13, "bold"), bg=t["bg_panel"], fg=t["texto"]
                  ).pack(anchor="w")
        tk.Label(tarjeta, text=f'Publicado por: {pub["ciudadano_nombre"]}',
                  font=FUENTE_NORMAL, bg=t["bg_panel"], fg=t["texto_claro"]).pack(anchor="w")
        if pub.get("descripcion"):
            tk.Label(tarjeta, text=pub["descripcion"], font=FUENTE_NORMAL,
                      bg=t["bg_panel"], fg=t["texto_claro"], wraplength=600, justify="left"
                      ).pack(anchor="w", pady=(5, 0))

        if pub.get("foto"):
            try:
                imagen = Image.open(pub["foto"])
                imagen.thumbnail((220, 220))
                foto_tk = ImageTk.PhotoImage(imagen)
                etiqueta_foto = tk.Label(tarjeta, image=foto_tk, bg=t["bg_panel"])
                etiqueta_foto.image = foto_tk  # se guarda la referencia, si no, la imagen desaparece
                etiqueta_foto.pack(anchor="w", pady=(8, 4))
            except Exception:
                tk.Label(tarjeta, text="📷 Tiene foto adjunta (no se pudo cargar)",
                          font=("Segoe UI", 9, "italic"), bg=t["bg_panel"], fg=t["secundario"]
                          ).pack(anchor="w", pady=(3, 0))

        ya_ofertado = any(o["reciclador_correo"] == self.usuario_actual["correo"]
                           for o in pub["ofertas"])

        fila = tk.Frame(tarjeta, bg=t["bg_panel"])
        fila.pack(anchor="w", pady=(10, 0))

        if ya_ofertado:
            tk.Label(fila, text="✔ Ya enviaste una oferta por este material",
                      font=("Segoe UI", 9, "bold"), bg=t["bg_panel"], fg=t["primario"]).pack(side="left")
        else:
            e_precio = tk.Entry(fila, width=10, font=FUENTE_NORMAL, bg=t["entrada_bg"],
                                 fg=t["texto"], relief="solid", bd=1)
            e_precio.pack(side="left", padx=(0, 8), ipady=4)
            tk.Label(fila, text="USD", font=FUENTE_NORMAL, bg=t["bg_panel"],
                      fg=t["texto_claro"]).pack(side="left", padx=(0, 8))

            def enviar_oferta(p=pub, entrada=e_precio):
                texto = entrada.get().strip()
                if not texto:
                    messagebox.showerror("Falta el precio", "Ingresa el precio que ofreces.")
                    return
                try:
                    precio = float(texto)
                    if precio <= 0:
                        raise ValueError
                except ValueError:
                    messagebox.showerror("Precio inválido", "Ingresa un número mayor a cero.")
                    return
                nombre_completo = f'{self.usuario_actual["nombres"]} {self.usuario_actual["apellidos"]}'
                datos.agregar_oferta(p["id"], self.usuario_actual["correo"], nombre_completo, precio)
                messagebox.showinfo("Oferta enviada", f'Tu oferta de ${precio} fue enviada a {p["ciudadano_nombre"]}.')
                self.mostrar_dashboard_reciclador("disponibles")

            tk.Button(fila, text="💰 Hacer oferta", command=enviar_oferta,
                      bg=t["primario"], fg=t["blanco"], relief="flat", cursor="hand2",
                      font=("Segoe UI", 9, "bold"), padx=10, pady=4).pack(side="left")

    def _seccion_mis_ofertas(self, area):
        t = self.tema()
        tk.Label(area, text="📑 Mis ofertas realizadas", font=FUENTE_SECCION,
                  bg=t["bg_principal"], fg=t["primario"]).pack(anchor="w", padx=30, pady=(25, 10))

        contenedor_scroll = self._crear_area_scroll(area)
        colores_estado = {
            "pendiente": t["advertencia"], "aceptada": t["exito"], "rechazada": t["error"]
        }

        encontro_alguna = False
        for pub in reversed(datos.obtener_publicaciones()):
            for oferta in pub["ofertas"]:
                if oferta["reciclador_correo"] != self.usuario_actual["correo"]:
                    continue
                encontro_alguna = True
                tarjeta = tk.Frame(contenedor_scroll, bg=t["bg_panel"], padx=20, pady=15,
                                    highlightbackground=t["borde"], highlightthickness=1)
                tarjeta.pack(fill="x", padx=10, pady=8)

                fila = tk.Frame(tarjeta, bg=t["bg_panel"])
                fila.pack(fill="x")
                tk.Label(fila, text=f'{pub["tipo_material"]} — {pub["peso_kg"]} kg | Tu oferta: ${oferta["precio"]}',
                          font=("Segoe UI", 12, "bold"), bg=t["bg_panel"], fg=t["texto"]).pack(side="left")
                tk.Label(fila, text=oferta["estado"].upper(), font=("Segoe UI", 9, "bold"),
                          bg=t["bg_panel"], fg=colores_estado.get(oferta["estado"], t["texto"])
                          ).pack(side="right")

                tk.Label(tarjeta, text=f'Ciudadano: {pub["ciudadano_nombre"]}', font=FUENTE_NORMAL,
                          bg=t["bg_panel"], fg=t["texto_claro"]).pack(anchor="w", pady=(4, 0))

                if pub.get("foto"):
                    try:
                        imagen = Image.open(pub["foto"])
                        imagen.thumbnail((180, 180))
                        foto_tk = ImageTk.PhotoImage(imagen)
                        etiqueta_foto = tk.Label(tarjeta, image=foto_tk, bg=t["bg_panel"])
                        etiqueta_foto.image = foto_tk
                        etiqueta_foto.pack(anchor="w", pady=(6, 0))
                    except Exception:
                        pass

                if oferta["estado"] == "aceptada":
                    tk.Button(tarjeta, text=f'💬 Chatear con {pub["ciudadano_nombre"]}',
                              bg=t["secundario"], fg=t["blanco"], relief="flat", cursor="hand2",
                              font=("Segoe UI", 9, "bold"), padx=10, pady=4,
                              command=lambda p=pub: self.mostrar_chat(p, p["ciudadano_nombre"])
                              ).pack(anchor="w", pady=(8, 0))

        if not encontro_alguna:
            tk.Label(contenedor_scroll, text="Todavía no has hecho ninguna oferta.",
                      font=FUENTE_NORMAL, bg=t["bg_principal"], fg=t["texto_claro"]
                      ).pack(anchor="w", padx=10, pady=20)

    # ==============================================================
    # ÁREA CON SCROLL (para listas largas de publicaciones)
    # ==============================================================
    def _crear_area_scroll(self, padre):
        t = self.tema()
        contenedor = tk.Frame(padre, bg=t["bg_principal"])
        contenedor.pack(fill="both", expand=True, padx=20)

        canvas = tk.Canvas(contenedor, bg=t["bg_principal"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(contenedor, orient="vertical", command=canvas.yview)
        interior = tk.Frame(canvas, bg=t["bg_principal"])

        interior.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=interior, anchor="nw", width=680)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def _rueda(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _rueda)

        return interior

    # ==============================================================
    # CHAT entre ciudadano y reciclador de una publicación
    # CAMBIO: ya no es una ventana aparte (Toplevel). Ahora es una
    # pantalla más dentro de la ventana principal, exactamente igual
    # que "Publicar material" o "Mis publicaciones". Esto elimina los
    # problemas de foco/teclado que daban las ventanas emergentes en
    # Windows. Solo es accesible si ya iniciaste sesión, dando clic
    # en el botón "💬 Chatear con..." de una publicación con oferta
    # aceptada.
    # ==============================================================
    def mostrar_chat(self, publicacion, nombre_otro):
        self._limpiar()
        t = self.tema()
        fondo = tk.Frame(self.contenedor, bg=t["bg_principal"])
        fondo.pack(fill="both", expand=True)

        # A dónde regresa el botón "Volver", según el rol de quien está chateando
        if self.rol_actual == "ciudadano":
            volver = lambda: self.mostrar_dashboard_ciudadano("publicaciones")
        else:
            volver = lambda: self.mostrar_dashboard_reciclador("mis_ofertas")

        barra_top = tk.Frame(fondo, bg=t["bg_principal"])
        barra_top.pack(fill="x", padx=20, pady=(15, 0))
        self._boton(barra_top, "← Volver", volver, color=t["texto_claro"],
                    hover=t["texto"], ancho=14).pack(anchor="w")

        tk.Label(fondo, text=f'💬 Chat con {nombre_otro}', font=FUENTE_SECCION,
                  bg=t["bg_principal"], fg=t["primario"]).pack(pady=(10, 2))
        tk.Label(fondo, text=f'Sobre: {publicacion["tipo_material"]} — {publicacion["peso_kg"]} kg',
                  font=("Segoe UI", 9), bg=t["bg_principal"], fg=t["texto_claro"]).pack(pady=(0, 10))

        # CAMBIO CLAVE: el cuadro de escribir se empaca PRIMERO y anclado
        # con side="bottom", para RESERVAR su espacio abajo del todo antes
        # que la caja de mensajes. Así nunca se queda fuera de la ventana.
        # Además se le da más padding y tamaño para que se vea grande y
        # bien visible, no aplastado contra el borde inferior.
        contenedor_envio = tk.Frame(fondo, bg=t["bg_principal"])
        contenedor_envio.pack(side="bottom", fill="x", padx=30, pady=(10, 25))

        fila_envio = tk.Frame(contenedor_envio, bg=t["entrada_bg"], highlightthickness=1,
                               highlightbackground=t["borde"])
        fila_envio.pack(fill="x")

        entrada_mensaje = tk.Entry(fila_envio, font=("Segoe UI", 13), bg=t["entrada_bg"],
                                     fg=t["texto"], relief="flat", bd=0)
        entrada_mensaje.pack(side="left", fill="x", expand=True, ipady=12, padx=(12, 8))

        nombre_propio = f'{self.usuario_actual["nombres"]} {self.usuario_actual["apellidos"]}'

        def enviar(event=None):
            texto = entrada_mensaje.get().strip()
            if not texto:
                return
            datos.agregar_mensaje(publicacion["id"], nombre_propio, self.rol_actual, texto)
            entrada_mensaje.delete(0, "end")
            recargar_mensajes()

        entrada_mensaje.bind("<Return>", enviar)
        tk.Button(fila_envio, text="Enviar ➤", command=enviar, bg=t["primario"], fg=t["blanco"],
                  relief="flat", cursor="hand2", font=("Segoe UI", 12, "bold"),
                  padx=20, pady=10).pack(side="right", padx=6, pady=6)

        # La caja de mensajes se empaca DESPUÉS: ocupa lo que sobra
        # (ya con el cuadro de escribir asegurado abajo)
        panel = tk.Frame(fondo, bg=t["bg_panel"], highlightbackground=t["borde"], highlightthickness=1)
        panel.pack(fill="both", expand=True, padx=30, pady=(0, 10))

        area_mensajes = tk.Text(panel, bg=t["bg_panel"], fg=t["texto"], font=FUENTE_NORMAL,
                                  wrap="word", relief="flat", state="disabled", padx=10, pady=10)
        area_mensajes.pack(fill="both", expand=True, padx=5, pady=5)

        def recargar_mensajes():
            area_mensajes.config(state="normal")
            area_mensajes.delete("1.0", "end")
            mensajes = datos.obtener_mensajes(publicacion["id"])
            if not mensajes:
                area_mensajes.insert("end", "Todavía no hay mensajes. ¡Escribe el primero!\n")
            for m in mensajes:
                hora = m["hora"].split(" ")[1][:5]
                area_mensajes.insert("end", f'[{hora}] {m["autor"]}: {m["texto"]}\n\n')
            area_mensajes.config(state="disabled")
            area_mensajes.see("end")

        recargar_mensajes()
        entrada_mensaje.focus_set()


# ======================================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# ======================================================================
if __name__ == "__main__":
    app = ReciGanaApp()
    app.mainloop()
# -*- coding: utf-8 -*-
"""
app_recigana.py
================
Interfaz gráfica de ReciGana hecha con Tkinter (viene incluido con Python,
no requiere instalar nada más, EXCEPTO Pillow para poder mostrar las fotos
de los materiales y de perfil -> pip install Pillow

Cómo ejecutar:
    python app_recigana.py

Estructura de pantallas:
    Login unificado (pantalla de inicio, elige rol con radiobuttons)
      ├── Recuperar contraseña
      ├── Registrarse
      │     ├── Registro Ciudadano  -> al terminar, va a Login unificado
      │     └── Registro Reciclador -> al terminar, va a Login unificado
      ├── Dashboard Ciudadano   (una vez logueado)
      │     ├── Publicar material
      │     ├── Mis publicaciones
      │     │     ├── Comprobante de recolección (cuando hay oferta aceptada)
      │     │     └── Calificar al reciclador (cuando el material fue vendido)
      │     ├── Mi perfil (foto + dirección detallada)
      │     └── Chat (con un reciclador, sobre una publicación)
      └── Dashboard Reciclador  (una vez logueado)
            ├── Materiales disponibles
            ├── Mis ofertas
            │     └── Comprobante de recolección (cuando hay oferta aceptada)
            ├── Mi perfil (foto + zona + calificación promedio)
            └── Chat (con un ciudadano, sobre una publicación)

NOVEDADES DE ESTA VERSIÓN (v4):
  1) El estado de las publicaciones se auto-corrige solo (ver
     almacenamiento.py): si un reciclador fue rechazado, el material
     vuelve a "disponible" automáticamente y él (o cualquier otro)
     puede volver a ofertar por el mismo material.
  2) Aviso de mensajes nuevos 🔴, tipo WhatsApp:
       - En el menú lateral, junto a "Mis publicaciones" / "Mis ofertas".
       - En cada botón de Chat de cada tarjeta.
       - En la tarjeta de estadísticas "Mensajes sin leer" del inicio.
  3) El chat ahora se ve como una conversación real: cada mensaje es
     una "burbuja" (los tuyos a la derecha, los del otro a la
     izquierda), con hora y un check de "visto":
       ✓   = enviado, todavía no lo han leído
       ✓✓  = ya lo leyeron
  4) Cada quien puede borrar sus propios mensajes (aparece un botoncito
     🗑 solo en las burbujas que tú escribiste).
  5) En "Mis ofertas" del reciclador ahora también se ve la foto de
     perfil del ciudadano (antes solo se veía el nombre), igual que ya
     pasaba del lado del ciudadano con la foto del reciclador.

  (Se mantienen todas las novedades de versiones anteriores: reciclador
  rechazado puede volver a ofertar, publicaciones visibles para todos
  mientras no tengan oferta aceptada, foto de perfil del ciudadano
  visible para el reciclador, tarjetas de estadísticas clickeables,
  foto del material, sección "Mi perfil", calificaciones con estrellas,
  comprobante de recolección y chats separados por publicación+reciclador.)

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

    def _campo_texto(self, padre, etiqueta, mostrar=None, ancho=32, valor_inicial=""):
        """Crea Label + Entry y retorna el Entry. mostrar='*' para contraseñas."""
        t = self.tema()
        tk.Label(padre, text=etiqueta, font=FUENTE_ETIQUETA,
                  bg=t["bg_panel"], fg=t["texto"]).pack(anchor="w", pady=(10, 2))
        entrada = tk.Entry(padre, width=ancho, font=FUENTE_NORMAL, show=mostrar,
                            bg=t["entrada_bg"], fg=t["texto"], relief="solid",
                            bd=1, highlightthickness=1,
                            highlightbackground=t["borde"], highlightcolor=t["primario"])
        if valor_inicial:
            entrada.insert(0, valor_inicial)
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

    def _hacer_clicable(self, widget, comando):
        """
        Hace que un Frame (y todo lo que tenga dentro) reaccione a un
        clic como si fuera un botón. Se usa para las tarjetas de
        estadísticas del Inicio.
        """
        t = self.tema()

        def _entrar(e):
            widget.config(highlightbackground=t["primario"])

        def _salir(e):
            widget.config(highlightbackground=t["borde"])

        def aplicar(w):
            w.bind("<Button-1>", lambda e: comando())
            w.config(cursor="hand2")
            for hijo in w.winfo_children():
                aplicar(hijo)

        widget.bind("<Enter>", _entrar)
        widget.bind("<Leave>", _salir)
        aplicar(widget)

    def _tarjeta_estadistica(self, padre, titulo, valor, comando=None):
        """
        Tarjeta de estadística del Inicio. Si se pasa 'comando', la
        tarjeta se vuelve clickeable y navega a esa sección.
        """
        t = self.tema()
        tarjeta = tk.Frame(padre, bg=t["bg_panel"], padx=25, pady=20,
                            highlightbackground=t["borde"], highlightthickness=1)
        tarjeta.pack(side="left", padx=10)
        tk.Label(tarjeta, text=str(valor), font=("Segoe UI", 22, "bold"),
                  bg=t["bg_panel"], fg=t["primario"]).pack()
        tk.Label(tarjeta, text=titulo, font=FUENTE_NORMAL,
                  bg=t["bg_panel"], fg=t["texto_claro"]).pack()
        if comando:
            tk.Label(tarjeta, text="Ver más →", font=("Segoe UI", 8, "bold"),
                      bg=t["bg_panel"], fg=t["secundario"]).pack(pady=(4, 0))
            self._hacer_clicable(tarjeta, comando)
        return tarjeta

    # ------------------------------------------------------------
    # Avatar / foto de perfil (reutilizable para ciudadano y reciclador)
    # ------------------------------------------------------------
    def _avatar(self, padre, ruta_foto, tamanio=90):
        """
        Muestra la foto de perfil si existe; si no, muestra un ícono
        genérico de usuario. Retorna el Label creado (por si se quiere
        reemplazar la imagen después).
        """
        t = self.tema()
        contenedor = tk.Frame(padre, bg=t["avatar_bg"], width=tamanio, height=tamanio,
                               highlightbackground=t["borde"], highlightthickness=1)
        contenedor.pack_propagate(False)

        if ruta_foto:
            try:
                imagen = Image.open(ruta_foto)
                imagen.thumbnail((tamanio, tamanio))
                foto_tk = ImageTk.PhotoImage(imagen)
                etiqueta = tk.Label(contenedor, image=foto_tk, bg=t["avatar_bg"])
                etiqueta.image = foto_tk  # evita que el garbage collector la borre
                etiqueta.pack(expand=True)
                return contenedor
            except Exception:
                pass

        # Sin foto (o no se pudo cargar): ícono placeholder
        tk.Label(contenedor, text="👤", font=("Segoe UI", int(tamanio * 0.4)),
                  bg=t["avatar_bg"], fg=t["texto_claro"]).pack(expand=True)
        return contenedor

    def _texto_estrellas(self, promedio, cantidad):
        """Convierte un promedio numérico en texto con estrellitas."""
        if cantidad == 0:
            return "Sin calificaciones todavía"
        llenas = round(promedio)
        return f'{"⭐" * llenas}{"☆" * (5 - llenas)}  {promedio}/5 ({cantidad} reseña{"s" if cantidad != 1 else ""})'

    def _texto_badge_no_leidos(self, cantidad):
        """Texto cortito tipo '🔴3' para pegar al final de un botón/menú."""
        return f" 🔴{cantidad}" if cantidad else ""

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

        canvas_scroll = tk.Canvas(fondo, bg=t["bg_principal"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(fondo, orient="vertical", command=canvas_scroll.yview)
        canvas_scroll.configure(yscrollcommand=scrollbar.set)

        canvas_scroll.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        panel = tk.Frame(canvas_scroll, bg=t["bg_panel"], padx=40, pady=20,
                          highlightbackground=t["borde"], highlightthickness=1)

        ventana_id = canvas_scroll.create_window((0, 0), window=panel, anchor="n")

        def _actualizar_scrollregion(event=None):
            canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all"))

        def _centrar_panel(event):
            # Mantiene el panel centrado horizontalmente al redimensionar
            canvas_scroll.coords(ventana_id, event.width / 2, 20)

        panel.bind("<Configure>", _actualizar_scrollregion)
        canvas_scroll.bind("<Configure>", _centrar_panel)

        def _rueda(event):
            canvas_scroll.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas_scroll.bind_all("<MouseWheel>", _rueda)

        self._encabezado_pantalla(panel, "📋 Registro de Ciudadano",
                                    "Publica tus materiales reciclables y gana dinero")

        e_nombres = self._campo_texto(panel, "Nombres *")
        e_apellidos = self._campo_texto(panel, "Apellidos *")

        tk.Label(panel, text="Dirección", font=("Segoe UI", 11, "bold"),
                  bg=t["bg_panel"], fg=t["secundario"]).pack(anchor="w", pady=(18, 0))
        e_ciudad = self._campo_texto(panel, "Ciudad * (ej: Manta)")
        e_parroquia = self._campo_texto(panel, "Parroquia * (ej: Tarqui)")
        e_barrio = self._campo_texto(panel, "Barrio * (ej: Nuevo Manta)")
        e_referencia = self._campo_texto(panel, "Referencia (opcional, ej: frente a la ferretería)")

        e_correo = self._campo_texto(panel, "Correo electrónico *")
        e_pass = self._campo_contrasenia(panel, "Contraseña * (mínimo 6 caracteres)")
        e_pass2 = self._campo_contrasenia(panel, "Confirmar contraseña *")

        def registrar():
            nombres = e_nombres.get().strip()
            apellidos = e_apellidos.get().strip()
            ciudad = e_ciudad.get().strip()
            parroquia = e_parroquia.get().strip()
            barrio = e_barrio.get().strip()
            referencia = e_referencia.get().strip()
            correo = e_correo.get().strip()
            clave = e_pass.get()
            clave2 = e_pass2.get()

            if not all([nombres, apellidos, ciudad, parroquia, barrio, correo, clave, clave2]):
                messagebox.showerror("Campos incompletos",
                                      "Todos los campos son obligatorios, excepto la referencia.")
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

            datos.guardar_ciudadano(nombres, apellidos, ciudad, correo, clave,
                                     parroquia=parroquia, barrio=barrio, referencia=referencia)
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
    # ==============================================================
    def mostrar_login_unificado(self):
        self._limpiar()
        t = self.tema()
        self.usuario_actual = None
        self.rol_actual = None

        fondo = tk.Frame(self.contenedor, bg=t["bg_principal"])
        fondo.pack(fill="both", expand=True)

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

        # Mini avatar en el menú lateral, junto al nombre
        self._avatar(menu, self.usuario_actual.get("foto_perfil", ""), tamanio=54).pack(pady=(0, 6))
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

    def _recargar_usuario_actual(self):
        """
        Vuelve a leer los datos del usuario actual desde almacenamiento
        (por si se acaban de editar en 'Mi perfil'), para que el resto
        de la app siempre use la información más reciente.
        """
        correo = self.usuario_actual["correo"]
        if self.rol_actual == "ciudadano":
            self.usuario_actual = datos.buscar_ciudadano_por_correo(correo)
        else:
            self.usuario_actual = datos.buscar_reciclador_por_correo(correo)

    # ==============================================================
    # DASHBOARD — CIUDADANO
    # ==============================================================
    def mostrar_dashboard_ciudadano(self, seccion="inicio"):
        self._limpiar()
        badge_mensajes = datos.total_no_leidos_ciudadano(self.usuario_actual["correo"])
        texto_pubs = "📋 Mis publicaciones" + self._texto_badge_no_leidos(badge_mensajes)

        opciones = [
            ("🏠 Inicio", lambda: self.mostrar_dashboard_ciudadano("inicio")),
            ("📦 Publicar material", lambda: self.mostrar_dashboard_ciudadano("publicar")),
            (texto_pubs, lambda: self.mostrar_dashboard_ciudadano("publicaciones")),
            ("👤 Mi perfil", lambda: self.mostrar_dashboard_ciudadano("perfil")),
        ]
        area = self._crear_estructura_dashboard("Panel del Ciudadano", opciones)

        if seccion == "inicio":
            self._seccion_bienvenida_ciudadano(area)
        elif seccion == "publicar":
            self._seccion_publicar_material(area)
        elif seccion == "publicaciones":
            self._seccion_mis_publicaciones(area)
        elif seccion == "perfil":
            self._seccion_perfil_ciudadano(area)

    def _seccion_bienvenida_ciudadano(self, area):
        t = self.tema()
        mis_pubs = [p for p in datos.obtener_publicaciones()
                    if p["ciudadano_correo"] == self.usuario_actual["correo"]]
        disponibles = sum(1 for p in mis_pubs if p["estado"] != "vendido")
        vendidos = sum(1 for p in mis_pubs if p["estado"] == "vendido")
        total_ofertas = sum(len(p["ofertas"]) for p in mis_pubs)
        mensajes_sin_leer = datos.total_no_leidos_ciudadano(self.usuario_actual["correo"])

        tk.Label(area, text=f'¡Bienvenido, {self.usuario_actual["nombres"]}! 🌿',
                  font=FUENTE_SECCION, bg=t["bg_principal"], fg=t["primario"]
                  ).pack(anchor="w", padx=30, pady=(30, 5))
        tk.Label(area, text="Publica tus materiales reciclables y conecta con recicladores de tu zona.",
                  font=FUENTE_NORMAL, bg=t["bg_principal"], fg=t["texto_claro"]
                  ).pack(anchor="w", padx=30, pady=(0, 20))

        tarjetas = tk.Frame(area, bg=t["bg_principal"])
        tarjetas.pack(anchor="w", padx=30)
        self._tarjeta_estadistica(tarjetas, "Publicaciones activas", disponibles,
                                   comando=lambda: self.mostrar_dashboard_ciudadano("publicaciones"))
        self._tarjeta_estadistica(tarjetas, "Materiales vendidos", vendidos,
                                   comando=lambda: self.mostrar_dashboard_ciudadano("publicaciones"))
        self._tarjeta_estadistica(tarjetas, "Ofertas recibidas", total_ofertas,
                                   comando=lambda: self.mostrar_dashboard_ciudadano("publicaciones"))
        self._tarjeta_estadistica(tarjetas, "Mensajes sin leer", mensajes_sin_leer,
                                   comando=lambda: self.mostrar_dashboard_ciudadano("publicaciones"))

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

        if pub.get("foto"):
            try:
                imagen = Image.open(pub["foto"])
                imagen.thumbnail((200, 200))
                foto_tk = ImageTk.PhotoImage(imagen)
                etiqueta_foto = tk.Label(tarjeta, image=foto_tk, bg=t["bg_panel"])
                etiqueta_foto.image = foto_tk
                etiqueta_foto.pack(anchor="w", pady=(8, 4))
            except Exception:
                tk.Label(tarjeta, text="📷 Tiene foto adjunta (no se pudo cargar)",
                          font=("Segoe UI", 9, "italic"), bg=t["bg_panel"], fg=t["secundario"]
                          ).pack(anchor="w", pady=(3, 0))

        tk.Label(tarjeta, text=f'Publicado: {pub["fecha_publicacion"]}',
                  font=("Segoe UI", 8), bg=t["bg_panel"], fg=t["texto_claro"]
                  ).pack(anchor="w", pady=(4, 8))

        ofertas_pendientes = [o for o in pub["ofertas"] if o["estado"] == "pendiente"]
        ofertas_rechazadas = [o for o in pub["ofertas"] if o["estado"] == "rechazada"]

        # ---- Ofertas pendientes: aceptar / rechazar / chatear ----
        if ofertas_pendientes:
            tk.Label(tarjeta, text=f"💰 {len(ofertas_pendientes)} oferta(s) pendiente(s):",
                      font=FUENTE_ETIQUETA, bg=t["bg_panel"], fg=t["primario"]).pack(anchor="w", pady=(4, 0))
            for oferta in ofertas_pendientes:
                fila_oferta = tk.Frame(tarjeta, bg=t["bg_panel"])
                fila_oferta.pack(fill="x", pady=4)

                reciclador = datos.buscar_reciclador_por_correo(oferta["reciclador_correo"])
                self._avatar(fila_oferta, reciclador.get("foto_perfil", "") if reciclador else "",
                             tamanio=38).pack(side="left", padx=(0, 8))

                promedio, cantidad = datos.promedio_calificacion_reciclador(oferta["reciclador_correo"])
                texto_estrellas = f' ({promedio}⭐, {cantidad})' if cantidad else ' (sin reseñas aún)'
                tk.Label(fila_oferta,
                          text=f'{oferta["reciclador_nombre"]} ofrece ${oferta["precio"]}{texto_estrellas}',
                          font=FUENTE_NORMAL, bg=t["bg_panel"], fg=t["texto"]).pack(side="left")

                no_leidos = datos.contar_mensajes_no_leidos(pub["id"], oferta["reciclador_correo"], "ciudadano")
                texto_chat = "💬 Chat" + self._texto_badge_no_leidos(no_leidos)

                tk.Button(fila_oferta, text="✔ Aceptar", bg=t["primario"], fg=t["blanco"],
                          relief="flat", cursor="hand2", font=("Segoe UI", 9, "bold"),
                          command=lambda p=pub, o=oferta: self._responder_oferta_ui(p, o, True)
                          ).pack(side="right", padx=3)
                tk.Button(fila_oferta, text="✘ Rechazar", bg=t["error"], fg=t["blanco"],
                          relief="flat", cursor="hand2", font=("Segoe UI", 9, "bold"),
                          command=lambda p=pub, o=oferta: self._responder_oferta_ui(p, o, False)
                          ).pack(side="right", padx=3)
                tk.Button(fila_oferta, text=texto_chat, bg=t["secundario"], fg=t["blanco"],
                          relief="flat", cursor="hand2", font=("Segoe UI", 9, "bold"),
                          command=lambda p=pub, o=oferta: self.mostrar_chat(
                              p, o["reciclador_nombre"], o["reciclador_correo"])
                          ).pack(side="right", padx=3)

        # ---- Ofertas rechazadas: se conserva el historial, pero se
        # puede seguir chateando con ese reciclador si se quiere, y él
        # (u otro) puede volver a ofertar desde "Materiales disponibles" ----
        if ofertas_rechazadas:
            tk.Label(tarjeta, text=f"🚫 {len(ofertas_rechazadas)} oferta(s) rechazada(s):",
                      font=FUENTE_ETIQUETA, bg=t["bg_panel"], fg=t["error"]).pack(anchor="w", pady=(8, 0))
            for oferta in ofertas_rechazadas:
                fila_oferta = tk.Frame(tarjeta, bg=t["bg_panel"])
                fila_oferta.pack(fill="x", pady=4)

                reciclador = datos.buscar_reciclador_por_correo(oferta["reciclador_correo"])
                self._avatar(fila_oferta, reciclador.get("foto_perfil", "") if reciclador else "",
                             tamanio=38).pack(side="left", padx=(0, 8))

                tk.Label(fila_oferta,
                          text=f'{oferta["reciclador_nombre"]} ofreció ${oferta["precio"]} (rechazada)',
                          font=FUENTE_NORMAL, bg=t["bg_panel"], fg=t["texto_claro"]).pack(side="left")

                no_leidos = datos.contar_mensajes_no_leidos(pub["id"], oferta["reciclador_correo"], "ciudadano")
                texto_chat = "💬 Chat" + self._texto_badge_no_leidos(no_leidos)

                tk.Button(fila_oferta, text=texto_chat, bg=t["secundario"], fg=t["blanco"],
                          relief="flat", cursor="hand2", font=("Segoe UI", 9, "bold"),
                          command=lambda p=pub, o=oferta: self.mostrar_chat(
                              p, o["reciclador_nombre"], o["reciclador_correo"])
                          ).pack(side="right", padx=3)

        oferta_aceptada = next((o for o in pub["ofertas"] if o["estado"] == "aceptada"), None)
        botonera = tk.Frame(tarjeta, bg=t["bg_panel"])
        botonera.pack(anchor="w", pady=(8, 0))
        if oferta_aceptada:
            no_leidos_aceptada = datos.contar_mensajes_no_leidos(
                pub["id"], oferta_aceptada["reciclador_correo"], "ciudadano")
            texto_chat_aceptada = f'💬 Chatear con {oferta_aceptada["reciclador_nombre"]}' \
                + self._texto_badge_no_leidos(no_leidos_aceptada)
            tk.Button(botonera, text=texto_chat_aceptada,
                      bg=t["secundario"], fg=t["blanco"], relief="flat", cursor="hand2",
                      font=("Segoe UI", 9, "bold"), padx=10, pady=4,
                      command=lambda p=pub, o=oferta_aceptada: self.mostrar_chat(
                          p, o["reciclador_nombre"], o["reciclador_correo"])
                      ).pack(side="left", padx=(0, 8))
            # Comprobante de Recolección (dirección + foto + precio)
            tk.Button(botonera, text="📄 Ver comprobante", bg=t["texto_claro"], fg=t["blanco"],
                      relief="flat", cursor="hand2", font=("Segoe UI", 9, "bold"), padx=10, pady=4,
                      command=lambda p=pub: self.mostrar_comprobante(p["id"])
                      ).pack(side="left", padx=(0, 8))
        if pub["estado"] != "vendido":
            tk.Button(botonera, text="📦 Marcar como vendido", bg=t["texto_claro"], fg=t["blanco"],
                      relief="flat", cursor="hand2", font=("Segoe UI", 9, "bold"), padx=10, pady=4,
                      command=lambda p=pub: self._marcar_vendido_ui(p)
                      ).pack(side="left")
        elif oferta_aceptada and not datos.ya_existe_calificacion(pub["id"]):
            tk.Button(botonera, text="⭐ Calificar reciclador", bg=t["advertencia"], fg=t["blanco"],
                      relief="flat", cursor="hand2", font=("Segoe UI", 9, "bold"), padx=10, pady=4,
                      command=lambda p=pub, o=oferta_aceptada: self.mostrar_calificar(p, o)
                      ).pack(side="left")

    def _responder_oferta_ui(self, publicacion, oferta, aceptar):
        datos.responder_oferta(publicacion["id"], oferta["id"], aceptar)
        accion = "aceptada" if aceptar else "rechazada"
        messagebox.showinfo("Listo", f'Oferta de {oferta["reciclador_nombre"]} {accion}.')
        self.mostrar_dashboard_ciudadano("publicaciones")

    def _marcar_vendido_ui(self, publicacion):
        if not messagebox.askyesno("Confirmar", "¿Marcar este material como vendido?\n"
                                                  "Ya no aparecerá para otros recicladores."):
            return
        datos.marcar_como_vendido(publicacion["id"])

        oferta_aceptada = next((o for o in publicacion["ofertas"] if o["estado"] == "aceptada"), None)
        if oferta_aceptada:
            if messagebox.askyesno("¡Venta registrada! 🎉",
                                    f'¿Deseas calificar a {oferta_aceptada["reciclador_nombre"]} ahora?\n'
                                    f'(Es opcional, puedes hacerlo después desde "Mis publicaciones")'):
                self.mostrar_calificar(publicacion, oferta_aceptada)
                return

        self.mostrar_dashboard_ciudadano("publicaciones")

    # ==============================================================
    # PERFIL — CIUDADANO
    # ==============================================================
    def _seccion_perfil_ciudadano(self, area):
        t = self.tema()
        tk.Label(area, text="👤 Mi perfil", font=FUENTE_SECCION,
                  bg=t["bg_principal"], fg=t["primario"]).pack(anchor="w", padx=30, pady=(25, 15))

        panel = tk.Frame(area, bg=t["bg_panel"], padx=35, pady=25,
                          highlightbackground=t["borde"], highlightthickness=1)
        panel.pack(anchor="w", padx=30, fill="x")

        fila_foto = tk.Frame(panel, bg=t["bg_panel"])
        fila_foto.pack(anchor="w", pady=(0, 15))
        contenedor_avatar = tk.Frame(fila_foto, bg=t["bg_panel"])
        contenedor_avatar.pack(side="left", padx=(0, 15))
        avatar_widget = {"frame": self._avatar(contenedor_avatar, self.usuario_actual.get("foto_perfil", ""))}
        avatar_widget["frame"].pack()

        def cambiar_foto():
            archivo = filedialog.askopenfilename(
                title="Selecciona tu foto de perfil",
                filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.gif *.bmp")]
            )
            if archivo:
                datos.actualizar_perfil_ciudadano(self.usuario_actual["correo"], foto_perfil=archivo)
                self._recargar_usuario_actual()
                self.mostrar_dashboard_ciudadano("perfil")

        tk.Button(fila_foto, text="📷 Cambiar foto de perfil", command=cambiar_foto,
                  bg=t["secundario"], fg=t["blanco"], relief="flat", cursor="hand2",
                  font=("Segoe UI", 9, "bold"), padx=10, pady=6).pack(side="left")

        tk.Label(panel, text=f'{self.usuario_actual["nombres"]} {self.usuario_actual["apellidos"]}',
                  font=("Segoe UI", 14, "bold"), bg=t["bg_panel"], fg=t["texto"]).pack(anchor="w")
        tk.Label(panel, text=self.usuario_actual["correo"], font=FUENTE_NORMAL,
                  bg=t["bg_panel"], fg=t["texto_claro"]).pack(anchor="w", pady=(0, 15))

        tk.Label(panel, text="Dirección (solo la verá el reciclador cuando aceptes su oferta)",
                  font=("Segoe UI", 9, "italic"), bg=t["bg_panel"], fg=t["texto_claro"]
                  ).pack(anchor="w", pady=(5, 0))

        e_ciudad = self._campo_texto(panel, "Ciudad", valor_inicial=self.usuario_actual.get("ciudad", ""))
        e_parroquia = self._campo_texto(panel, "Parroquia", valor_inicial=self.usuario_actual.get("parroquia", ""))
        e_barrio = self._campo_texto(panel, "Barrio", valor_inicial=self.usuario_actual.get("barrio", ""))
        e_referencia = self._campo_texto(panel, "Referencia (opcional)",
                                          valor_inicial=self.usuario_actual.get("referencia", ""))

        def guardar_direccion():
            datos.actualizar_perfil_ciudadano(
                self.usuario_actual["correo"],
                ciudad=e_ciudad.get().strip(),
                parroquia=e_parroquia.get().strip(),
                barrio=e_barrio.get().strip(),
                referencia=e_referencia.get().strip(),
            )
            self._recargar_usuario_actual()
            messagebox.showinfo("Guardado", "Tu dirección fue actualizada correctamente.")
            self.mostrar_dashboard_ciudadano("perfil")

        self._boton(panel, "💾 GUARDAR CAMBIOS", guardar_direccion, ancho=26).pack(pady=(20, 0), anchor="w")

    # ==============================================================
    # DASHBOARD — RECICLADOR
    # ==============================================================
    def mostrar_dashboard_reciclador(self, seccion="inicio"):
        self._limpiar()
        badge_mensajes = datos.total_no_leidos_reciclador(self.usuario_actual["correo"])
        texto_ofertas = "📑 Mis ofertas" + self._texto_badge_no_leidos(badge_mensajes)

        opciones = [
            ("🏠 Inicio", lambda: self.mostrar_dashboard_reciclador("inicio")),
            ("🔍 Materiales disponibles", lambda: self.mostrar_dashboard_reciclador("disponibles")),
            (texto_ofertas, lambda: self.mostrar_dashboard_reciclador("mis_ofertas")),
            ("👤 Mi perfil", lambda: self.mostrar_dashboard_reciclador("perfil")),
        ]
        area = self._crear_estructura_dashboard("Panel del Reciclador", opciones)

        if seccion == "inicio":
            self._seccion_bienvenida_reciclador(area)
        elif seccion == "disponibles":
            self._seccion_materiales_disponibles(area)
        elif seccion == "mis_ofertas":
            self._seccion_mis_ofertas(area)
        elif seccion == "perfil":
            self._seccion_perfil_reciclador(area)

    def _seccion_bienvenida_reciclador(self, area):
        t = self.tema()
        todas = datos.obtener_publicaciones()
        disponibles = sum(1 for p in todas if p["estado"] == "disponible")
        mis_ofertas = [o for p in todas for o in p["ofertas"]
                       if o["reciclador_correo"] == self.usuario_actual["correo"]]
        aceptadas = sum(1 for o in mis_ofertas if o["estado"] == "aceptada")
        mensajes_sin_leer = datos.total_no_leidos_reciclador(self.usuario_actual["correo"])

        tk.Label(area, text=f'¡Bienvenido, {self.usuario_actual["nombres"]}! ♻',
                  font=FUENTE_SECCION, bg=t["bg_principal"], fg=t["primario"]
                  ).pack(anchor="w", padx=30, pady=(30, 5))
        tk.Label(area, text=f'Zona de cobertura: {self.usuario_actual.get("zona_cobertura", "-")}',
                  font=FUENTE_NORMAL, bg=t["bg_principal"], fg=t["texto_claro"]
                  ).pack(anchor="w", padx=30, pady=(0, 5))

        promedio, cantidad = datos.promedio_calificacion_reciclador(self.usuario_actual["correo"])
        tk.Label(area, text=self._texto_estrellas(promedio, cantidad), font=FUENTE_NORMAL,
                  bg=t["bg_principal"], fg=t["estrella"]).pack(anchor="w", padx=30, pady=(0, 20))

        tarjetas = tk.Frame(area, bg=t["bg_principal"])
        tarjetas.pack(anchor="w", padx=30)
        self._tarjeta_estadistica(tarjetas, "Materiales disponibles", disponibles,
                                   comando=lambda: self.mostrar_dashboard_reciclador("disponibles"))
        self._tarjeta_estadistica(tarjetas, "Ofertas realizadas", len(mis_ofertas),
                                   comando=lambda: self.mostrar_dashboard_reciclador("mis_ofertas"))
        self._tarjeta_estadistica(tarjetas, "Ofertas aceptadas", aceptadas,
                                   comando=lambda: self.mostrar_dashboard_reciclador("mis_ofertas"))
        self._tarjeta_estadistica(tarjetas, "Mensajes sin leer", mensajes_sin_leer,
                                   comando=lambda: self.mostrar_dashboard_reciclador("mis_ofertas"))

    def _seccion_materiales_disponibles(self, area):
        t = self.tema()
        tk.Label(area, text="🔍 Materiales disponibles", font=FUENTE_SECCION,
                  bg=t["bg_principal"], fg=t["primario"]).pack(anchor="w", padx=30, pady=(25, 10))

        # Una publicación cuenta como "disponible" mientras no tenga una
        # oferta ACEPTADA y no haya sido marcada como vendida. Es decir,
        # aunque a un reciclador ya le hayan rechazado una oferta por
        # este material, sigue apareciendo aquí para todos (incluido
        # él mismo, quien podrá volver a ofertar).
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

        # ---- Encabezado: foto de perfil del ciudadano + su ciudad ----
        # (por privacidad no se muestra la dirección completa acá,
        # solo la ciudad; la dirección exacta solo aparece en el
        # Comprobante de Recolección una vez aceptada la oferta)
        ciudadano = datos.buscar_ciudadano_por_correo(pub["ciudadano_correo"])
        fila_encabezado = tk.Frame(tarjeta, bg=t["bg_panel"])
        fila_encabezado.pack(fill="x", anchor="w")
        self._avatar(fila_encabezado, ciudadano.get("foto_perfil", "") if ciudadano else "",
                     tamanio=48).pack(side="left", padx=(0, 10))
        info_ciudadano = tk.Frame(fila_encabezado, bg=t["bg_panel"])
        info_ciudadano.pack(side="left")
        tk.Label(info_ciudadano, text=pub["ciudadano_nombre"], font=("Segoe UI", 11, "bold"),
                  bg=t["bg_panel"], fg=t["texto"]).pack(anchor="w")
        ciudad_texto = ciudadano.get("ciudad", "") if ciudadano else ""
        if ciudad_texto:
            tk.Label(info_ciudadano, text=f'📍 {ciudad_texto}', font=("Segoe UI", 9),
                      bg=t["bg_panel"], fg=t["texto_claro"]).pack(anchor="w")

        tk.Label(tarjeta, text=f'{pub["tipo_material"]} — {pub["peso_kg"]} kg',
                  font=("Segoe UI", 13, "bold"), bg=t["bg_panel"], fg=t["texto"]
                  ).pack(anchor="w", pady=(10, 0))
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

        # ---- Historial de mis ofertas anteriores por este material ----
        mis_ofertas_previas = [o for o in pub["ofertas"]
                                if o["reciclador_correo"] == self.usuario_actual["correo"]]
        colores_estado_oferta = {"pendiente": t["advertencia"], "aceptada": t["exito"], "rechazada": t["error"]}
        for o in mis_ofertas_previas:
            tk.Label(tarjeta, text=f'Tu oferta: ${o["precio"]} — {o["estado"].upper()}',
                      font=("Segoe UI", 9, "bold"), bg=t["bg_panel"],
                      fg=colores_estado_oferta.get(o["estado"], t["texto"])
                      ).pack(anchor="w", pady=(6, 0))

        # Si el reciclador tiene una oferta pendiente o aceptada, no se
        # le vuelve a mostrar el formulario. Pero si su(s) oferta(s)
        # anterior(es) fueron rechazadas, sí puede ofertar de nuevo.
        oferta_activa = next((o for o in mis_ofertas_previas if o["estado"] in ("pendiente", "aceptada")), None)

        fila = tk.Frame(tarjeta, bg=t["bg_panel"])
        fila.pack(anchor="w", pady=(10, 0))

        if oferta_activa:
            texto_estado = "pendiente de respuesta" if oferta_activa["estado"] == "pendiente" else "aceptada"
            tk.Label(fila, text=f"✔ Ya tienes una oferta {texto_estado} por este material",
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

            texto_boton = "💰 Hacer nueva oferta" if mis_ofertas_previas else "💰 Hacer oferta"
            tk.Button(fila, text=texto_boton, command=enviar_oferta,
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

                # ---- Foto de perfil del ciudadano + su nombre ----
                ciudadano = datos.buscar_ciudadano_por_correo(pub["ciudadano_correo"])
                fila_ciudadano = tk.Frame(tarjeta, bg=t["bg_panel"])
                fila_ciudadano.pack(anchor="w", pady=(6, 0), fill="x")
                self._avatar(fila_ciudadano, ciudadano.get("foto_perfil", "") if ciudadano else "",
                             tamanio=36).pack(side="left", padx=(0, 8))
                tk.Label(fila_ciudadano, text=f'Ciudadano: {pub["ciudadano_nombre"]}', font=FUENTE_NORMAL,
                          bg=t["bg_panel"], fg=t["texto_claro"]).pack(side="left")

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

                # El chat ya no depende de que la oferta esté aceptada:
                # se puede chatear con el ciudadano sin importar si la
                # oferta está pendiente, aceptada o rechazada.
                no_leidos = datos.contar_mensajes_no_leidos(pub["id"], self.usuario_actual["correo"], "reciclador")
                texto_chat = f'💬 Chatear con {pub["ciudadano_nombre"]}' + self._texto_badge_no_leidos(no_leidos)

                botonera = tk.Frame(tarjeta, bg=t["bg_panel"])
                botonera.pack(anchor="w", pady=(8, 0))
                tk.Button(botonera, text=texto_chat,
                          bg=t["secundario"], fg=t["blanco"], relief="flat", cursor="hand2",
                          font=("Segoe UI", 9, "bold"), padx=10, pady=4,
                          command=lambda p=pub: self.mostrar_chat(
                              p, p["ciudadano_nombre"], self.usuario_actual["correo"])
                          ).pack(side="left", padx=(0, 8))

                if oferta["estado"] == "aceptada":
                    # El comprobante sí sigue dependiendo de la oferta
                    # aceptada, porque necesita la dirección y el precio
                    # ya acordado.
                    tk.Button(botonera, text="📄 Ver comprobante", bg=t["texto_claro"], fg=t["blanco"],
                              relief="flat", cursor="hand2", font=("Segoe UI", 9, "bold"), padx=10, pady=4,
                              command=lambda p=pub: self.mostrar_comprobante(p["id"])
                              ).pack(side="left")

        if not encontro_alguna:
            tk.Label(contenedor_scroll, text="Todavía no has hecho ninguna oferta.",
                      font=FUENTE_NORMAL, bg=t["bg_principal"], fg=t["texto_claro"]
                      ).pack(anchor="w", padx=10, pady=20)

    # ==============================================================
    # PERFIL — RECICLADOR
    # ==============================================================
    def _seccion_perfil_reciclador(self, area):
        t = self.tema()
        tk.Label(area, text="👤 Mi perfil", font=FUENTE_SECCION,
                  bg=t["bg_principal"], fg=t["primario"]).pack(anchor="w", padx=30, pady=(25, 15))

        panel = tk.Frame(area, bg=t["bg_panel"], padx=35, pady=25,
                          highlightbackground=t["borde"], highlightthickness=1)
        panel.pack(anchor="w", padx=30, fill="x")

        fila_foto = tk.Frame(panel, bg=t["bg_panel"])
        fila_foto.pack(anchor="w", pady=(0, 15))
        contenedor_avatar = tk.Frame(fila_foto, bg=t["bg_panel"])
        contenedor_avatar.pack(side="left", padx=(0, 15))
        self._avatar(contenedor_avatar, self.usuario_actual.get("foto_perfil", "")).pack()

        def cambiar_foto():
            archivo = filedialog.askopenfilename(
                title="Selecciona tu foto de perfil",
                filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.gif *.bmp")]
            )
            if archivo:
                datos.actualizar_perfil_reciclador(self.usuario_actual["correo"], foto_perfil=archivo)
                self._recargar_usuario_actual()
                self.mostrar_dashboard_reciclador("perfil")

        tk.Button(fila_foto, text="📷 Cambiar foto de perfil", command=cambiar_foto,
                  bg=t["secundario"], fg=t["blanco"], relief="flat", cursor="hand2",
                  font=("Segoe UI", 9, "bold"), padx=10, pady=6).pack(side="left")

        tk.Label(panel, text=f'{self.usuario_actual["nombres"]} {self.usuario_actual["apellidos"]}',
                  font=("Segoe UI", 14, "bold"), bg=t["bg_panel"], fg=t["texto"]).pack(anchor="w")
        tk.Label(panel, text=self.usuario_actual["correo"], font=FUENTE_NORMAL,
                  bg=t["bg_panel"], fg=t["texto_claro"]).pack(anchor="w", pady=(0, 10))

        promedio, cantidad = datos.promedio_calificacion_reciclador(self.usuario_actual["correo"])
        tk.Label(panel, text=self._texto_estrellas(promedio, cantidad),
                  font=("Segoe UI", 12, "bold"), bg=t["bg_panel"], fg=t["estrella"]
                  ).pack(anchor="w", pady=(0, 15))

        e_zona = self._campo_texto(panel, "Zona de cobertura",
                                    valor_inicial=self.usuario_actual.get("zona_cobertura", ""))

        def guardar_zona():
            datos.actualizar_perfil_reciclador(self.usuario_actual["correo"], zona_cobertura=e_zona.get().strip())
            self._recargar_usuario_actual()
            messagebox.showinfo("Guardado", "Tu zona de cobertura fue actualizada.")
            self.mostrar_dashboard_reciclador("perfil")

        self._boton(panel, "💾 GUARDAR CAMBIOS", guardar_zona, ancho=26).pack(pady=(15, 0), anchor="w")

        # ---- Lista de reseñas recibidas ----
        tk.Label(area, text="📝 Reseñas recibidas", font=FUENTE_SECCION,
                  bg=t["bg_principal"], fg=t["primario"]).pack(anchor="w", padx=30, pady=(25, 10))

        califs = datos.obtener_calificaciones_de_reciclador(self.usuario_actual["correo"])
        contenedor_scroll = self._crear_area_scroll(area)

        if not califs:
            tk.Label(contenedor_scroll, text="Todavía no tienes reseñas. ¡Sigue haciendo buen trabajo! 🌱",
                      font=FUENTE_NORMAL, bg=t["bg_principal"], fg=t["texto_claro"]
                      ).pack(anchor="w", padx=10, pady=10)
            return

        for c in reversed(califs):
            tarjeta = tk.Frame(contenedor_scroll, bg=t["bg_panel"], padx=15, pady=10,
                                highlightbackground=t["borde"], highlightthickness=1)
            tarjeta.pack(fill="x", padx=10, pady=5)
            tk.Label(tarjeta, text="⭐" * c["puntaje"] + "☆" * (5 - c["puntaje"]),
                      font=("Segoe UI", 12), bg=t["bg_panel"], fg=t["estrella"]).pack(anchor="w")
            tk.Label(tarjeta, text=f'— {c["ciudadano_nombre"]}', font=("Segoe UI", 9, "bold"),
                      bg=t["bg_panel"], fg=t["texto"]).pack(anchor="w")
            if c.get("comentario"):
                tk.Label(tarjeta, text=c["comentario"], font=FUENTE_NORMAL, wraplength=600,
                          justify="left", bg=t["bg_panel"], fg=t["texto_claro"]).pack(anchor="w", pady=(3, 0))

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
    # COMPROBANTE DE RECOLECCIÓN
    # ==============================================================
    def mostrar_comprobante(self, publicacion_id):
        self._limpiar()
        t = self.tema()
        fondo = tk.Frame(self.contenedor, bg=t["bg_principal"])
        fondo.pack(fill="both", expand=True)

        volver = (lambda: self.mostrar_dashboard_ciudadano("publicaciones")) if self.rol_actual == "ciudadano" \
            else (lambda: self.mostrar_dashboard_reciclador("mis_ofertas"))

        barra_top = tk.Frame(fondo, bg=t["bg_principal"])
        barra_top.pack(fill="x", padx=20, pady=(15, 0))
        self._boton(barra_top, "← Volver", volver, color=t["texto_claro"],
                    hover=t["texto"], ancho=14).pack(anchor="w")

        comprobante = datos.armar_comprobante_recoleccion(publicacion_id)
        if comprobante is None:
            tk.Label(fondo, text="Este comprobante todavía no está disponible.",
                      font=FUENTE_NORMAL, bg=t["bg_principal"], fg=t["texto_claro"]).pack(pady=40)
            return

        panel = tk.Frame(fondo, bg=t["bg_panel"], padx=40, pady=25,
                          highlightbackground=t["borde"], highlightthickness=1)
        panel.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(panel, text="📄 Comprobante de Recolección", font=FUENTE_SECCION,
                  bg=t["bg_panel"], fg=t["primario"]).pack(pady=(0, 15))

        filas = [
            ("Material", f'{comprobante["tipo_material"]} — {comprobante["peso_kg"]} kg'),
            ("Ciudadano (vendedor)", comprobante["ciudadano_nombre"]),
            ("Reciclador (comprador)", comprobante["reciclador_nombre"]),
            ("Dirección de recolección", comprobante["direccion"]),
            ("Precio acordado", f'${comprobante["precio_acordado"]} (efectivo, al momento de la entrega)'),
            ("Acuerdo cerrado el", comprobante["fecha_acuerdo"]),
        ]
        for etiqueta, valor in filas:
            fila = tk.Frame(panel, bg=t["bg_panel"])
            fila.pack(fill="x", pady=6, anchor="w")
            tk.Label(fila, text=etiqueta + ":", font=FUENTE_ETIQUETA,
                      bg=t["bg_panel"], fg=t["texto_claro"], width=22, anchor="w").pack(side="left")
            tk.Label(fila, text=str(valor), font=FUENTE_NORMAL,
                      bg=t["bg_panel"], fg=t["texto"], wraplength=320, justify="left", anchor="w"
                      ).pack(side="left", fill="x")

        if comprobante.get("foto"):
            try:
                imagen = Image.open(comprobante["foto"])
                imagen.thumbnail((260, 260))
                foto_tk = ImageTk.PhotoImage(imagen)
                etiqueta_foto = tk.Label(panel, image=foto_tk, bg=t["bg_panel"])
                etiqueta_foto.image = foto_tk
                etiqueta_foto.pack(pady=(15, 0))
            except Exception:
                pass

    # ==============================================================
    # CALIFICACIÓN
    # ==============================================================
    def mostrar_calificar(self, publicacion, oferta_aceptada):
        self._limpiar()
        t = self.tema()
        fondo = tk.Frame(self.contenedor, bg=t["bg_principal"])
        fondo.pack(fill="both", expand=True)

        volver = lambda: self.mostrar_dashboard_ciudadano("publicaciones")

        barra_top = tk.Frame(fondo, bg=t["bg_principal"])
        barra_top.pack(fill="x", padx=20, pady=(15, 0))
        self._boton(barra_top, "← Volver", volver, color=t["texto_claro"],
                    hover=t["texto"], ancho=14).pack(anchor="w")

        panel = tk.Frame(fondo, bg=t["bg_panel"], padx=40, pady=25,
                          highlightbackground=t["borde"], highlightthickness=1)
        panel.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(panel, text="⭐ Calificar a tu reciclador", font=FUENTE_SECCION,
                  bg=t["bg_panel"], fg=t["primario"]).pack(pady=(0, 4))
        tk.Label(panel, text=oferta_aceptada["reciclador_nombre"], font=("Segoe UI", 12, "bold"),
                  bg=t["bg_panel"], fg=t["texto"]).pack(pady=(0, 15))

        seleccion = {"puntaje": 0}
        fila_estrellas = tk.Frame(panel, bg=t["bg_panel"])
        fila_estrellas.pack(pady=(0, 15))
        botones_estrella = []

        def pintar_estrellas():
            for i, b in enumerate(botones_estrella, start=1):
                b.config(text="⭐" if i <= seleccion["puntaje"] else "☆")

        def elegir(n):
            seleccion["puntaje"] = n
            pintar_estrellas()

        for n in range(1, 6):
            b = tk.Button(fila_estrellas, text="☆", font=("Segoe UI", 22), bd=0, relief="flat",
                          bg=t["bg_panel"], fg=t["estrella"], activebackground=t["bg_panel"],
                          cursor="hand2", command=lambda n=n: elegir(n))
            b.pack(side="left", padx=3)
            botones_estrella.append(b)

        e_comentario = self._campo_texto(panel, "Comentario (opcional)", ancho=40)

        def enviar():
            if seleccion["puntaje"] == 0:
                messagebox.showerror("Falta la calificación", "Selecciona de 1 a 5 estrellas.")
                return
            nombre_ciudadano = f'{self.usuario_actual["nombres"]} {self.usuario_actual["apellidos"]}'
            datos.guardar_calificacion(
                publicacion["id"],
                oferta_aceptada["reciclador_correo"], oferta_aceptada["reciclador_nombre"],
                self.usuario_actual["correo"], nombre_ciudadano,
                seleccion["puntaje"], e_comentario.get().strip()
            )
            messagebox.showinfo("¡Gracias!", "Tu calificación fue registrada.")
            self.mostrar_dashboard_ciudadano("publicaciones")

        botones = tk.Frame(panel, bg=t["bg_panel"])
        botones.pack(pady=(20, 0))
        self._boton(botones, "ENVIAR CALIFICACIÓN", enviar, ancho=24).pack(pady=4)
        self._boton(botones, "Omitir por ahora", lambda: self.mostrar_dashboard_ciudadano("publicaciones"),
                    color=t["texto_claro"], hover=t["texto"], ancho=24).pack(pady=4)

    # ==============================================================
    # CHAT entre ciudadano y reciclador de una publicación
    #
    # Recibe también el correo del reciclador involucrado, porque cada
    # conversación se guarda por separado (publicación + reciclador).
    # Así, si varios recicladores interactúan con la misma
    # publicación, sus mensajes no se mezclan entre sí. No depende de
    # que la oferta esté aceptada: se puede chatear con cualquier
    # estado de oferta.
    #
    # Cada mensaje se dibuja como una "burbuja": los que yo escribí
    # a la derecha (con hora + ✓/✓✓ de "visto" + botón de borrar),
    # los del otro usuario a la izquierda.
    # ==============================================================
    def mostrar_chat(self, publicacion, nombre_otro, reciclador_correo):
        self._limpiar()
        t = self.tema()
        fondo = tk.Frame(self.contenedor, bg=t["bg_principal"])
        fondo.pack(fill="both", expand=True)

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

        contenedor_envio = tk.Frame(fondo, bg=t["bg_principal"])
        contenedor_envio.pack(side="bottom", fill="x", padx=30, pady=(10, 25))

        fila_envio = tk.Frame(contenedor_envio, bg=t["entrada_bg"], highlightthickness=1,
                               highlightbackground=t["borde"])
        fila_envio.pack(fill="x")

        entrada_mensaje = tk.Entry(fila_envio, font=("Segoe UI", 13), bg=t["entrada_bg"],
                                     fg=t["texto"], relief="flat", bd=0)
        entrada_mensaje.pack(side="left", fill="x", expand=True, ipady=12, padx=(12, 8))

        nombre_propio = f'{self.usuario_actual["nombres"]} {self.usuario_actual["apellidos"]}'

        # ---- Panel con scroll donde van las burbujas de mensajes ----
        panel = tk.Frame(fondo, bg=t["bg_panel"], highlightbackground=t["borde"], highlightthickness=1)
        panel.pack(fill="both", expand=True, padx=30, pady=(0, 10))

        canvas_msg = tk.Canvas(panel, bg=t["bg_panel"], highlightthickness=0)
        scrollbar_msg = ttk.Scrollbar(panel, orient="vertical", command=canvas_msg.yview)
        interior_msg = tk.Frame(canvas_msg, bg=t["bg_panel"])

        interior_msg.bind("<Configure>", lambda e: canvas_msg.configure(scrollregion=canvas_msg.bbox("all")))
        canvas_msg.create_window((0, 0), window=interior_msg, anchor="nw")
        canvas_msg.configure(yscrollcommand=scrollbar_msg.set)

        canvas_msg.pack(side="left", fill="both", expand=True)
        scrollbar_msg.pack(side="right", fill="y")

        def _rueda_msg(event):
            canvas_msg.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas_msg.bind_all("<MouseWheel>", _rueda_msg)

        def _ir_al_final():
            canvas_msg.update_idletasks()
            canvas_msg.configure(scrollregion=canvas_msg.bbox("all"))
            canvas_msg.yview_moveto(1.0)

        def eliminar_mensaje_ui(mensaje_id):
            if not messagebox.askyesno("Eliminar mensaje", "¿Eliminar este mensaje? Esta acción no se puede deshacer."):
                return
            datos.eliminar_mensaje(publicacion["id"], reciclador_correo, mensaje_id,
                                    self.usuario_actual["correo"])
            recargar_mensajes()

        def dibujar_burbuja(mensaje):
            es_propio = mensaje.get("autor_correo") == self.usuario_actual["correo"]
            color_burbuja = t["secundario"] if es_propio else t["borde"]
            color_texto = t["blanco"] if es_propio else t["texto"]

            fila = tk.Frame(interior_msg, bg=t["bg_panel"])
            fila.pack(fill="x", pady=4, padx=10)

            burbuja = tk.Frame(fila, bg=color_burbuja, padx=10, pady=6)
            burbuja.pack(side="right" if es_propio else "left",
                         anchor="e" if es_propio else "w")

            if not es_propio:
                tk.Label(burbuja, text=mensaje.get("autor", nombre_otro), font=("Segoe UI", 8, "bold"),
                          bg=color_burbuja, fg=t["primario"]).pack(anchor="w")

            tk.Label(burbuja, text=mensaje["texto"], font=FUENTE_NORMAL, bg=color_burbuja,
                      fg=color_texto, wraplength=380, justify="left").pack(anchor="w")

            hora = mensaje["hora"].split(" ")[1][:5]
            pie_texto = hora
            if es_propio:
                pie_texto += "  " + ("✓✓" if mensaje.get("leido") else "✓")

            fila_pie = tk.Frame(burbuja, bg=color_burbuja)
            fila_pie.pack(anchor="e", fill="x")
            tk.Label(fila_pie, text=pie_texto, font=("Segoe UI", 7),
                      bg=color_burbuja, fg=t["blanco"] if es_propio else t["texto_claro"]
                      ).pack(side="left")

            if es_propio and mensaje.get("id"):
                tk.Button(fila_pie, text="🗑", font=("Segoe UI", 8), bd=0, relief="flat",
                          bg=color_burbuja, fg=t["blanco"], cursor="hand2",
                          activebackground=color_burbuja,
                          command=lambda mid=mensaje["id"]: eliminar_mensaje_ui(mid)
                          ).pack(side="left", padx=(6, 0))

        def enviar(event=None):
            texto = entrada_mensaje.get().strip()
            if not texto:
                return
            datos.agregar_mensaje(publicacion["id"], reciclador_correo, nombre_propio,
                                   self.usuario_actual["correo"], self.rol_actual, texto)
            entrada_mensaje.delete(0, "end")
            recargar_mensajes()

        entrada_mensaje.bind("<Return>", enviar)
        tk.Button(fila_envio, text="Enviar ➤", command=enviar, bg=t["primario"], fg=t["blanco"],
                  relief="flat", cursor="hand2", font=("Segoe UI", 12, "bold"),
                  padx=20, pady=10).pack(side="right", padx=6, pady=6)

        def recargar_mensajes():
            for w in interior_msg.winfo_children():
                w.destroy()

            # Al abrir/recargar el chat, se marcan como leídos los
            # mensajes del OTRO usuario (así él verá el ✓✓ la próxima
            # vez que entre a este mismo chat).
            datos.marcar_mensajes_leidos(publicacion["id"], reciclador_correo, self.rol_actual)

            mensajes = datos.obtener_mensajes(publicacion["id"], reciclador_correo)
            if not mensajes:
                tk.Label(interior_msg, text="Todavía no hay mensajes. ¡Escribe el primero!",
                          font=FUENTE_NORMAL, bg=t["bg_panel"], fg=t["texto_claro"]).pack(pady=20)
            else:
                for m in mensajes:
                    dibujar_burbuja(m)

            _ir_al_final()

        recargar_mensajes()
        entrada_mensaje.focus_set()


# ======================================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# ======================================================================
if __name__ == "__main__":
    app = ReciGanaApp()
    app.mainloop()
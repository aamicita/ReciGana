# 🌿 Interfaz gráfica de ReciGana — Guía paso a paso (para principiantes)

## ⚠️ PRIMERO: aclarando tu estructura de carpetas

En tu proyecto tienes `backend/` y `fronted/`. Esos son de **otro intento**
distinto (con base de datos, tipo página web) — **NO los toques, no los
borres, no los necesitas**. Esta interfaz es completamente aparte y
funciona sola, sin necesitar esas dos carpetas.

Tu interfaz va a vivir en una carpeta nueva llamada `interfaz_recigana`,
**al mismo nivel** que `src`, `backend`, `fronted` y `tests` (no adentro
de ninguna de ellas).

---

## 🪜 PASO 1 — Descargar y descomprimir

1. Descarga el archivo `interfaz_recigana.zip` que te compartí.
2. Búscalo en tu carpeta de Descargas.
3. Haz **clic derecho** sobre el archivo → **"Extraer todo..."**
   (en Windows) → Extraer.
4. Esto va a crear una carpeta llamada `interfaz_recigana` con 4
   archivos adentro: `app_recigana.py`, `almacenamiento.py`,
   `estilos.py` y este mismo `LEEME.md`.

## 🪜 PASO 2 — Mover la carpeta a tu proyecto

1. Abre esa carpeta `interfaz_recigana` que acabas de extraer.
2. Cópiala completa (Ctrl + C).
3. Ve a la carpeta raíz de tu proyecto `RECIGANA` (donde están `src`,
   `backend`, `fronted`, `tests`).
4. Pégala ahí (Ctrl + V).

Tu proyecto debe quedar así:

```
RECIGANA/
 ├── backend/                  (no tocar)
 ├── fronted/                  (no tocar)
 ├── src/                      (no tocar)
 ├── tests/
 ├── interfaz_recigana/        ← 🆕 la carpeta que acabas de pegar
 │    ├── app_recigana.py
 │    ├── almacenamiento.py
 │    ├── estilos.py
 │    └── LEEME.md
 └── main.py
```

## 🪜 PASO 3 — Ejecutarla

1. Abre **Visual Studio Code**.
2. Abre una **terminal nueva** (menú Terminal → Nueva terminal, o
   `Ctrl + ñ`).
3. En la terminal escribe esto para entrar a la carpeta y dale Enter:
   ```
   cd interfaz_recigana
   ```
4. Ahora escribe esto y dale Enter para abrir la app:
   ```
   python app_recigana.py
   ```
   (si te da error de "comando no encontrado", prueba con `python3`
   en vez de `python`)
5. Se va a abrir una **ventana nueva** — ¡esa es tu app funcionando! 🎉

Cada vez que quieras volver a abrirla, repites el paso 3.

## 🪜 PASO 4 — Ver los usuarios registrados en Excel

Cuando registres usuarios desde la app, se van a crear estos archivos
dentro de `interfaz_recigana/data/` (esa carpeta `data` se crea sola,
no la crees tú a mano):

```
interfaz_recigana/
 └── data/
      ├── ciudadanos.csv      ← tabla de ciudadanos (ábrela con Excel)
      ├── recicladores.csv    ← tabla de recicladores (ábrela con Excel)
      ├── publicaciones.json  ← materiales publicados (no es para Excel)
      └── mensajes.json       ← chats (no es para Excel)
```

Para ver a tus usuarios en Excel:
1. Ve a la carpeta `interfaz_recigana/data/`.
2. Haz **doble clic** en `ciudadanos.csv` → se abre solo en Excel,
   con columnas: id, nombres, apellidos, ciudad, correo, contraseña
   (encriptada), fecha de registro.
3. Haz lo mismo con `recicladores.csv` para ver los recicladores.

Como pediste: **cada rol tiene su propia tabla, nunca se mezclan.**

> Nota: la columna `password_hash` no muestra la contraseña real,
> muestra un código encriptado (como hace cualquier sistema serio,
> por seguridad — así también lo hace tu clase `Usuarios` original).

---

## 🧭 ¿Cómo se usa la app una vez abierta?

1. **Pantalla principal**: "♻ ReciGana", la frase, y los botones
   Registrarse / Iniciar sesión / Salir + botón de 🌙 modo oscuro.
2. **Registrarse** → eliges Ciudadano o Reciclador (el Administrador
   no se registra aquí, como bien dijiste).
3. Llenas el formulario. Si algo está mal o vacío, te avisa con un
   mensaje claro.
4. **Iniciar sesión** → eliges tu rol, ingresas correo/contraseña.
   Si algo es incorrecto, dice "Correo o contraseña incorrectos".
   Puedes recuperar tu contraseña con el enlace de abajo.
5. Ya adentro, cada rol ve su propio panel:
   - **Ciudadano**: publicar material (tipo, peso, foto, descripción),
     ver ofertas recibidas, aceptar/rechazar, chatear, marcar como
     vendido.
   - **Reciclador**: ver materiales disponibles, hacer ofertas, ver
     el estado de sus ofertas, chatear si fue aceptada.

---

## ❓ Preguntas frecuentes

**¿Debo borrar `backend/` o `fronted/`?**
No. Simplemente no los uses. Para tu presentación, solo necesitas
correr `interfaz_recigana/app_recigana.py` — ni siquiera necesitas
mencionar esas otras carpetas si no quieres.

**¿Debo "conectar" esto con mis clases de `src/` (Ciudadano,
GestorSistema, Facade, etc.)?**
No es obligatorio. Tal como está, la app funciona completa, guarda
todo, y se ve bien — perfecta para presentar. "Conectar" significaría
hacer que estos formularios usen tus clases con los patrones de
diseño por dentro, en vez de guardar directo en archivos. Es un paso
extra y opcional para más adelante, si tu profesor lo pide
específicamente. Si no lo pide, no lo necesitas.

**Se me cerró la ventana o me marcó un error, ¿qué hago?**
Copia el mensaje de error completo que sale en la terminal y
compártemelo, lo revisamos juntos.

**¿Puedo cambiar colores, textos o campos?**
Sí, sin problema — solo dime qué quieres cambiar y te digo
exactamente qué línea modificar.

class GestorSistema:
    """
    PATRON SINGLETON — GestorSistema.

    Problema que resuelve:
    Si creamos varios objetos GestorSistema, cada uno tendria
    su propia lista de usuarios y materiales — datos separados
    y contradictorios. Con Singleton garantizamos que solo
    existe UNA instancia con UNA sola lista compartida.

    Uso:
        g1 = GestorSistema.obtener_instancia()
        g2 = GestorSistema.obtener_instancia()
        g1 is g2  →  True  (son el mismo objeto)
    """

    _instancia = None  # Aqui se guarda la unica instancia

    def __init__(self):
        # Lista de usuarios registrados en el sistema
        self._usuarios = []
        # Lista de materiales publicados en el sistema
        self._materiales = []
        # Contador de IDs autoincrementables
        self._contador_usuarios   = 1
        self._contador_materiales = 1

    @classmethod
    def obtener_instancia(cls):
        """
        Retorna siempre la misma instancia.
        Si no existe, la crea. Si ya existe, la reutiliza.
        Este es el corazon del patron Singleton.
        """
        if cls._instancia is None:
            cls._instancia = GestorSistema()
            print("GestorSistema: nueva instancia creada.")
        else:
            print("GestorSistema: reutilizando instancia existente.")
        return cls._instancia

    @classmethod
    def resetear(cls):
        """
        Solo para tests — resetea la instancia.
        En produccion nunca se llama este metodo.
        """
        cls._instancia = None

    # ---------- Usuarios ----------

    def registrar_usuario(self, usuario):
        """Agrega un usuario al sistema."""
        self._usuarios.append(usuario)
        print(f"Usuario '{usuario.nombre}' registrado en el sistema.")
        return usuario

    def obtener_usuarios(self):
        """Retorna copia de la lista de usuarios."""
        return list(self._usuarios)

    def buscar_usuario(self, id_usuario):
        """Busca un usuario por su ID."""
        for u in self._usuarios:
            if u.id == id_usuario:
                return u
        return None

    def siguiente_id_usuario(self):
        """Genera un ID unico para un nuevo usuario."""
        id_generado = self._contador_usuarios
        self._contador_usuarios += 1
        return id_generado

    # ---------- Materiales ----------

    def registrar_material(self, material):
        """Agrega un material al sistema."""
        self._materiales.append(material)
        print(f"Material '{material.get_tipo()}' registrado en el sistema.")
        return material

    def obtener_materiales(self):
        """Retorna copia de la lista de materiales."""
        return list(self._materiales)

    def siguiente_id_material(self):
        """Genera un ID unico para un nuevo material."""
        id_generado = self._contador_materiales
        self._contador_materiales += 1
        return id_generado

    # ---------- Resumen ----------

    def resumen(self):
        """Muestra el estado actual del sistema."""
        print("=" * 40)
        print("  RESUMEN DEL SISTEMA ReciGana")
        print("=" * 40)
        print(f"  Usuarios registrados : {len(self._usuarios)}")
        print(f"  Materiales publicados: {len(self._materiales)}")
        print("=" * 40)

    def __str__(self):
        return (
            f"GestorSistema("
            f"usuarios={len(self._usuarios)}, "
            f"materiales={len(self._materiales)})"
        )

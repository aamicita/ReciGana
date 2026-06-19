# Herencia: Ciudadano hereda de Usuarios
from .usuario import Usuarios


class Ciudadano(Usuarios):
    """
    Representa a un ciudadano de Manta registrado en ReciGana.
    Es el usuario que publica materiales reciclables para la venta.
    Hereda autenticación y datos básicos de la clase Usuarios.
    """

    def __init__(self, id_usuario, nombre, telefono, correo, contrasenia, direccion):
        # Llamamos al constructor de la clase padre para inicializar
        # id, nombre, teléfono, correo, contraseña y rol
        super().__init__(id_usuario, nombre, telefono, correo, contrasenia, rol="ciudadano")

        # Atributo propio del ciudadano: su dirección física en Manta
        self._direccion = direccion

        # Lista interna de materiales publicados por este ciudadano
        self._materiales_publicados = []

        # Lista interna de ofertas recibidas sobre sus materiales
        self._ofertas_recibidas = []

    # ---------- Propiedades ----------

    @property
    def direccion(self):
        """Retorna la dirección del ciudadano."""
        return self._direccion

    @direccion.setter
    def direccion(self, valor):
        """Actualiza la dirección solo si el valor no está vacío."""
        if isinstance(valor, str) and len(valor.strip()) >= 5:
            self._direccion = valor.strip()
        else:
            raise ValueError("La dirección debe tener al menos 5 caracteres.")

    @property
    def materiales_publicados(self):
        """Retorna una copia de la lista de materiales publicados."""
        return list(self._materiales_publicados)

    @property
    def ofertas_recibidas(self):
        """Retorna una copia de la lista de ofertas recibidas."""
        return list(self._ofertas_recibidas)

    # ---------- Métodos ----------

    def registrar(self):
        """
        Confirma que el ciudadano fue registrado correctamente en el sistema.
        Retorna True para indicar éxito.
        """
        print(f"Ciudadano '{self.nombre}' registrado exitosamente en ReciGana.")
        return True

    def publicar_material(self, tipo, peso, foto=None):
        """
        Publica un material reciclable en la plataforma.
        Parámetros:
            tipo  -- tipo de material (ej: 'plástico', 'cartón')
            peso  -- peso en kg del material
            foto  -- ruta o nombre de la foto (opcional)
        Retorna el diccionario del material publicado.
        """
        # Validamos que el tipo no esté vacío y el peso sea positivo
        if not tipo or not isinstance(tipo, str):
            raise ValueError("El tipo de material no puede estar vacío.")
        if not isinstance(peso, (int, float)) or peso <= 0:
            raise ValueError("El peso debe ser un número mayor a cero.")

        # Creamos el registro del material como diccionario
        material = {
            "tipo": tipo.strip(),
            "peso_kg": peso,
            "foto": foto,          # None si no se envió foto
            "estado": "disponible" # Estado inicial al publicar
        }

        # Lo agregamos a la lista interna del ciudadano
        self._materiales_publicados.append(material)

        if foto:
            print(f"Material publicado con foto: {tipo}, {peso} kg")
        else:
            print(f"Material publicado: {tipo}, {peso} kg")

        return material

    def recibir_oferta(self, oferta):
        """
        Registra una oferta recibida de un reciclador sobre un material.
        Parámetro:
            oferta -- diccionario con los datos de la oferta
        """
        self._ofertas_recibidas.append(oferta)
        print(f"Nueva oferta recibida: {oferta}")

    def aceptar_oferta(self, oferta):
        """
        Acepta una oferta recibida y marca el material como vendido.
        Parámetro:
            oferta -- diccionario con los datos de la oferta a aceptar
        Retorna True si se aceptó correctamente.
        """
        if oferta in self._ofertas_recibidas:
            oferta["estado"] = "aceptada"
            print(f"Oferta aceptada: {oferta}")
            return True
        print("La oferta no existe en la lista de ofertas recibidas.")
        return False

    def rechazar_oferta(self, oferta):
        """
        Rechaza una oferta recibida.
        Parámetro:
            oferta -- diccionario con los datos de la oferta a rechazar
        Retorna True si se rechazó correctamente.
        """
        if oferta in self._ofertas_recibidas:
            oferta["estado"] = "rechazada"
            print(f"Oferta rechazada: {oferta}")
            return True
        print("La oferta no existe en la lista de ofertas recibidas.")
        return False

    def __str__(self):
        """Representación legible del ciudadano."""
        return f"Ciudadano: {self.nombre} | Dirección: {self._direccion} | Materiales publicados: {len(self._materiales_publicados)}"
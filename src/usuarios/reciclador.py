# Herencia: Reciclador hereda de Usuarios
# Herencia: Reciclador hereda de Usuarios
from .usuario import Usuarios


class Reciclador(Usuarios):
    """
    Representa a un reciclador registrado en ReciGana.
    Es el usuario que busca materiales publicados por los ciudadanos,
    hace ofertas de compra y las gestiona.
    Hereda autenticación y datos básicos de la clase Usuarios.
    """

    def __init__(self, id_usuario, nombre, telefono, correo, contrasenia, zona_cobertura):
        # Llamamos al constructor padre asignando rol "ciudadano"
        # (el reciclador es un tipo especial de usuario registrado)
        super().__init__(id_usuario, nombre, telefono, correo, contrasenia, rol="ciudadano")

        # Zona geográfica de Manta donde opera el reciclador
        # Ejemplo: "Manta centro", "Los Esteros", "Tarqui"
        self._zona_cobertura = zona_cobertura

        # Lista interna de ofertas que este reciclador ha realizado
        self._ofertas_realizadas = []

        # Lista interna de materiales que ha comprado exitosamente
        self._materiales_comprados = []

    # ---------- Propiedades ----------

    @property
    def zona_cobertura(self):
        """Retorna la zona de cobertura del reciclador."""
        return self._zona_cobertura

    @zona_cobertura.setter
    def zona_cobertura(self, valor):
        """Actualiza la zona de cobertura solo si el valor es válido."""
        if isinstance(valor, str) and len(valor.strip()) >= 3:
            self._zona_cobertura = valor.strip()
        else:
            raise ValueError("La zona de cobertura debe tener al menos 3 caracteres.")

    @property
    def ofertas_realizadas(self):
        """Retorna una copia de las ofertas realizadas por el reciclador."""
        return list(self._ofertas_realizadas)

    @property
    def materiales_comprados(self):
        """Retorna una copia de los materiales comprados por el reciclador."""
        return list(self._materiales_comprados)

    # ---------- Métodos ----------

    def registrarse(self):
        """
        Confirma que el reciclador fue registrado correctamente en el sistema.
        Retorna True para indicar éxito.
        """
        print(f"Reciclador '{self.nombre}' registrado en la zona '{self._zona_cobertura}'.")
        return True

    def consultar_ofertas(self, materiales_disponibles):
        """
        Muestra los materiales disponibles que puede comprar el reciclador.
        Parámetro:
            materiales_disponibles -- lista de diccionarios con materiales publicados
        Retorna la lista de materiales disponibles.
        """
        # Filtramos solo los materiales con estado 'disponible'
        disponibles = [m for m in materiales_disponibles if m.get("estado") == "disponible"]

        if not disponibles:
            print("No hay materiales disponibles en este momento.")
            return []

        print(f"Materiales disponibles ({len(disponibles)}):")
        for material in disponibles:
            print(f"  - {material.get('tipo')} | {material.get('peso_kg')} kg | Estado: {material.get('estado')}")

        return disponibles

    def realizar_oferta(self, material, precio_ofrecido):
        """
        Realiza una oferta de compra sobre un material publicado.
        Parámetros:
            material        -- diccionario del material sobre el que se oferta
            precio_ofrecido -- precio en dólares que ofrece el reciclador
        Retorna el diccionario de la oferta creada.
        """
        # Validamos que el precio sea un número positivo
        if not isinstance(precio_ofrecido, (int, float)) or precio_ofrecido <= 0:
            raise ValueError("El precio ofrecido debe ser un número mayor a cero.")

        # Verificamos que el material esté disponible
        if material.get("estado") != "disponible":
            print("Este material ya no está disponible.")
            return None

        # Creamos el registro de la oferta
        oferta = {
            "reciclador": self.nombre,
            "material": material.get("tipo"),
            "peso_kg": material.get("peso_kg"),
            "precio_ofrecido": precio_ofrecido,
            "estado": "pendiente"  # Estado inicial de toda oferta
        }

        # La guardamos en la lista interna del reciclador
        self._ofertas_realizadas.append(oferta)
        print(f"Oferta realizada: {precio_ofrecido} USD por {material.get('tipo')} ({material.get('peso_kg')} kg)")

        return oferta

    def aceptar_oferta(self, oferta):
        """
        Confirma que una oferta fue aceptada por el ciudadano
        y registra el material como comprado.
        Parámetro:
            oferta -- diccionario de la oferta aceptada
        """
        if oferta in self._ofertas_realizadas:
            oferta["estado"] = "aceptada"
            # Registramos el material como comprado
            self._materiales_comprados.append(oferta)
            print(f"¡Oferta aceptada! Compraste {oferta.get('material')} por {oferta.get('precio_ofrecido')} USD.")
        else:
            print("La oferta no pertenece a este reciclador.")

    def rechazar_oferta(self, oferta):
        """
        Marca una oferta como rechazada por el ciudadano.
        Parámetro:
            oferta -- diccionario de la oferta rechazada
        """
        if oferta in self._ofertas_realizadas:
            oferta["estado"] = "rechazada"
            print(f"Oferta rechazada para {oferta.get('material')}.")
        else:
            print("La oferta no pertenece a este reciclador.")

    def __str__(self):
        """Representación legible del reciclador."""
        return (f"Reciclador: {self.nombre} | "
                f"Zona: {self._zona_cobertura} | "
                f"Ofertas realizadas: {len(self._ofertas_realizadas)} | "
                f"Materiales comprados: {len(self._materiales_comprados)}")
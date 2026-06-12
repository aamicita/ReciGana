# Clase de historial de reciclaje del sistema ReciGana
# Guarda y gestiona todos los intercambios de materiales
# que ha hecho un usuario en la plataforma

from datetime import datetime  # Para registrar fechas de cada transacción
import copy                    # Para poder clonar historiales (Patrón Prototype)


class HistorialDeReciclaje:
    """
    Guarda el historial completo de materiales reciclados o intercambiados
    por un usuario en la plataforma ReciGana.
    """

    def __init__(self, id_historial, registros=None):
        # Identificador único de este historial (uno por usuario)
        self.__id_historial = id_historial

        # Si nos pasan registros existentes los usamos,
        # si no, empezamos con lista vacía
        self.__registros = registros if registros is not None else []

    # ---------- Propiedades ----------

    @property
    def id_historial(self):
        # Permite leer el id del historial desde fuera de la clase
        return self.__id_historial

    @property
    def registros(self):
        # Retorna una copia para que nadie modifique la lista directamente
        return list(self.__registros)

    @property
    def total_registros(self):
        # Retorna cuántos registros hay en el historial
        return len(self.__registros)

    # ---------- Métodos ----------

    def agregar_registro(self, tipo_material, peso_kg, tipo_transaccion):
        """
        Agrega un nuevo registro cuando se completa un intercambio.
        Parámetros:
            tipo_material    -- tipo de material (ej: 'plástico', 'cartón')
            peso_kg          -- peso en kg del material intercambiado
            tipo_transaccion -- 'venta' si el ciudadano vendió,
                                'compra' si el reciclador compró
        """
        # Validamos que el peso sea un número positivo
        if not isinstance(peso_kg, (int, float)) or peso_kg <= 0:
            raise ValueError("El peso debe ser un número mayor a cero.")

        # Validamos que el tipo de transacción sea válido
        if tipo_transaccion not in ("venta", "compra"):
            raise ValueError("El tipo debe ser 'venta' o 'compra'.")

        # Creamos el registro con todos los datos del intercambio
        registro = {
            "tipo_material": tipo_material,
            "peso_kg": peso_kg,
            "tipo_transaccion": tipo_transaccion,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Agregamos el registro a la lista interna
        self.__registros.append(registro)
        print(
            f"Registro agregado: {tipo_transaccion} de "
            f"{tipo_material} ({peso_kg} kg)"
        )
        return registro

    def consultar_historial(self):
        """
        Muestra todos los registros del historial.
        Retorna la lista completa de registros.
        """
        print(
            f"Historial #{self.__id_historial} - "
            f"Total: {len(self.__registros)} registros"
        )

        # Si no hay registros informamos y salimos
        if not self.__registros:
            print("No hay registros en el historial.")
            return []

        # Recorremos e imprimimos cada registro numerado
        for i, registro in enumerate(self.__registros, start=1):
            print(
                f"  {i}. {registro['fecha']} | "
                f"{registro['tipo_transaccion'].upper()} | "
                f"{registro['tipo_material']} - {registro['peso_kg']} kg"
            )

        return self.__registros

    def filtrar_por_fecha(self, fecha):
        """
        Filtra los registros que coincidan con una fecha específica.
        Parámetro:
            fecha -- string con la fecha (formato: 'YYYY-MM-DD')
        """
        # Buscamos registros cuya fecha empiece con la fecha dada
        resultados = [
            r for r in self.__registros
            if r["fecha"].startswith(fecha)
        ]

        if not resultados:
            print(f"No se encontraron registros para la fecha {fecha}.")
        else:
            print(f"Registros del {fecha}: {len(resultados)} encontrados.")
            for r in resultados:
                print(
                    f"  - {r['tipo_transaccion'].upper()} | "
                    f"{r['tipo_material']} - {r['peso_kg']} kg"
                )

        return resultados

    def filtrar_por_tipo(self, tipo_material):
        """
        Filtra los registros por tipo de material.
        Parámetro:
            tipo_material -- tipo de material a buscar (ej: 'plástico')
        """
        # Comparamos en minúsculas para evitar problemas con mayúsculas
        resultados = [
            r for r in self.__registros
            if r["tipo_material"].lower() == tipo_material.lower()
        ]

        if not resultados:
            print(f"No hay registros de '{tipo_material}' en el historial.")
        else:
            print(f"Registros de '{tipo_material}': {len(resultados)} encontrados.")

        return resultados

    def clonar(self, nuevo_id):
        """
        PATRÓN PROTOTYPE — Clona este historial con un nuevo ID.

        ¿Para qué sirve?
        Imagina que necesitas crear el historial de un usuario nuevo
        que tiene la misma estructura de registros que otro usuario
        ya existente. En vez de agregar cada registro uno por uno,
        simplemente clonas el historial base y le cambias el ID.
        El clon es completamente independiente del original,
        así que agregar registros al clon no afecta al original.

        Parámetro:
            nuevo_id -- identificador para el historial clonado

        Ejemplo de uso:
            original = HistorialDeReciclaje(1)
            original.agregar_registro("plástico", 5, "venta")
            copia = original.clonar(nuevo_id=2)
            # copia tiene los mismos registros pero ID = 2
        """
        # Creamos una copia completamente independiente del original
        # deepcopy copia también todos los registros internos de la lista
        clon = copy.deepcopy(self)

        # Asignamos el nuevo ID al clon
        # Usamos _HistorialDeReciclaje__ porque el atributo es privado
        clon._HistorialDeReciclaje__id_historial = nuevo_id

        print(
            f"[Prototype] Historial clonado → "
            f"nuevo ID: {nuevo_id} | "
            f"Registros copiados: {len(clon.registros)}"
        )
        return clon

    def __str__(self):
        # Representación legible del historial
        return (
            f"Historial #{self.__id_historial} | "
            f"{len(self.__registros)} registros"
        )
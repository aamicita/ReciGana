# Clase de historial de reciclaje del sistema ReciGana
# Guarda y gestiona todos los intercambios de materiales que ha hecho un usuario

from datetime import datetime  # Para registrar fechas de cada transacción


class HistorialDeReciclaje:
    """
    Guarda el historial completo de materiales reciclados o intercambiados
    por un usuario en la plataforma ReciGana.
    """

    def __init__(self, id_historial, registros=None):
        # Identificador único de este historial (uno por usuario)
        self.__id_historial = id_historial

        # Si nos pasan una lista de registros existentes la usamos,
        # si no, empezamos con una lista vacía
        self.__registros = registros if registros is not None else []

    # ---------- Propiedades ----------

    @property
    def id_historial(self):
        # Permite leer el id del historial desde fuera de la clase
        return self.__id_historial

    @property
    def registros(self):
        # Retorna una copia de los registros para que nadie los modifique directamente
        return list(self.__registros)

    @property
    def total_registros(self):
        # Retorna cuántos registros hay en el historial
        return len(self.__registros)

    # ---------- Métodos ----------

    def agregar_registro(self, tipo_material, peso_kg, tipo_transaccion):
        """
        Agrega un nuevo registro al historial cuando se completa un intercambio.
        Parámetros:
            tipo_material     -- tipo de material (ej: 'plástico', 'cartón')
            peso_kg           -- peso en kg del material intercambiado
            tipo_transaccion  -- 'venta' si el ciudadano vendió, 'compra' si el reciclador compró
        """
        # Validamos que el peso sea un número positivo
        if not isinstance(peso_kg, (int, float)) or peso_kg <= 0:
            raise ValueError("El peso debe ser un número mayor a cero.")

        # Validamos que el tipo de transacción sea válido
        if tipo_transaccion not in ("venta", "compra"):
            raise ValueError("El tipo de transacción debe ser 'venta' o 'compra'.")

        # Creamos el registro con todos los datos del intercambio
        registro = {
            "tipo_material": tipo_material,       # Qué material fue
            "peso_kg": peso_kg,                   # Cuánto pesaba
            "tipo_transaccion": tipo_transaccion, # Si fue venta o compra
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Cuándo ocurrió
        }

        # Agregamos el registro a la lista interna
        self.__registros.append(registro)
        print(f"Registro agregado: {tipo_transaccion} de {tipo_material} ({peso_kg} kg)")
        return registro

    def consultar_historial(self):
        """
        Muestra todos los registros del historial.
        Retorna la lista completa de registros.
        """
        print(f"Historial #{self.__id_historial} - Total: {len(self.__registros)} registros")

        # Si no hay registros informamos y salimos
        if not self.__registros:
            print("No hay registros en el historial.")
            return []

        # Recorremos e imprimimos cada registro
        for i, registro in enumerate(self.__registros, start=1):
            print(f"  {i}. {registro['fecha']} | {registro['tipo_transaccion'].upper()} | "
                  f"{registro['tipo_material']} - {registro['peso_kg']} kg")

        return self.__registros

    def filtrar_por_fecha(self, fecha):
        """
        Filtra los registros que coincidan con una fecha específica.
        Parámetro:
            fecha -- string con la fecha a buscar (formato: 'YYYY-MM-DD')
        Retorna una lista con los registros que coincidan.
        """
        # Buscamos todos los registros cuya fecha empiece con la fecha dada
        resultados = [r for r in self.__registros if r["fecha"].startswith(fecha)]

        # Informamos cuántos resultados encontramos
        if not resultados:
            print(f"No se encontraron registros para la fecha {fecha}.")
        else:
            print(f"Registros del {fecha}: {len(resultados)} encontrados.")
            for r in resultados:
                print(f"  - {r['tipo_transaccion'].upper()} | {r['tipo_material']} - {r['peso_kg']} kg")

        return resultados

    def filtrar_por_tipo(self, tipo_material):
        """
        Filtra los registros por tipo de material.
        Parámetro:
            tipo_material -- tipo de material a buscar (ej: 'plástico')
        Retorna una lista con los registros que coincidan.
        """
        # Comparamos en minúsculas para evitar problemas con mayúsculas
        resultados = [r for r in self.__registros
                      if r["tipo_material"].lower() == tipo_material.lower()]

        if not resultados:
            print(f"No hay registros de '{tipo_material}' en el historial.")
        else:
            print(f"Registros de '{tipo_material}': {len(resultados)} encontrados.")

        return resultados

    def __str__(self):
        # Representación legible del historial cuando se imprime con print()
        return f"Historial #{self.__id_historial} | {len(self.__registros)} registros"
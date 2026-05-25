from abc import ABC, abstractmethod
from core.database import Database

class EntidadBD(ABC):
    def __init__(self):
        self.db = Database().obtener_conexion()

    @abstractmethod
    def guardar(self):
        pass

    @abstractmethod
    def listar_todos(self):
        pass

class Producto(EntidadBD):
    def __init__(self, nombre="", precio_base=0.0):
        super().__init__()
        self.nombre = nombre
        self.precio_base = precio_base

    def guardar(self):
        with self.db.cursor() as cursor:
            sql = "INSERT INTO Productos_Base (nombre, precio_base) VALUES (%s, %s)"
            cursor.execute(sql, (self.nombre, self.precio_base))

    def listar_todos(self):
        with self.db.cursor() as cursor:
            cursor.execute("SELECT id_producto, nombre, precio_base FROM Productos_Base")
            return cursor.fetchall()

class Venta(EntidadBD):
    def __init__(self, id_metodo, total_pagado):
        super().__init__()
        self.id_metodo = id_metodo
        self.total_pagado = total_pagado

    def guardar(self):
        with self.db.cursor() as cursor:
            sql = "INSERT INTO Ventas (id_metodo, total_pagado, estado) VALUES (%s, %s, 'Pagado')"
            cursor.execute(sql, (self.id_metodo, self.total_pagado))
            return cursor.lastrowid

    def listar_todos(self):
        with self.db.cursor() as cursor:
            cursor.execute("SELECT * FROM Ventas")
            return cursor.fetchall()

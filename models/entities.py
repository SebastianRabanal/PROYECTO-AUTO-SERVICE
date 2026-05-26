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
            self.db.commit()

    def listar_todos(self):
        with self.db.cursor() as cursor:
            cursor.execute("SELECT id_producto, nombre, precio_base FROM Productos_Base")
            return cursor.fetchall()
            
    def buscar_id_por_nombre(self, nombre_producto):
        with self.db.cursor() as cursor:
            sql = "SELECT id_producto FROM Productos_Base WHERE nombre = %s"
            cursor.execute(sql, (nombre_producto,))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
        
    def obtener_modificadores(self, id_producto):
        with self.db.cursor() as cursor:
            sql = """
                SELECT c.nombre_categoria, o.nombre_opcion, o.precio_adicional 
                FROM Producto_Categoria pc
                JOIN Categorias_Modificador c ON pc.id_categoria = c.id_categoria
                JOIN Opciones_Modificador o ON c.id_categoria = o.id_categoria
                WHERE pc.id_producto = %s
            """
            cursor.execute(sql, (id_producto,))
            resultados = cursor.fetchall()
            modificadores = {}
            for row in resultados:
                categoria = row['nombre_categoria']
                opcion = row['nombre_opcion']
                precio = float(row['precio_adicional'])
                
                if categoria not in modificadores:
                    modificadores[categoria] = []
                modificadores[categoria].append({"nombre": opcion, "precio": precio})
            
            return modificadores
        
    def obtener_id_y_precio_por_nombre(self, nombre):
        with self.db.cursor() as cursor:
            sql = "SELECT id_producto, precio_base FROM Productos_Base WHERE nombre = %s"
            cursor.execute(sql, (nombre,))
            row = cursor.fetchone()
            
            if row:
                return row['id_producto'], float(row['precio_base'])
            return None
        
    def obtener_precio_modificador(self, nombre_opcion):
        with self.db.cursor() as cursor:
            sql = "SELECT precio_adicional FROM Opciones_Modificador WHERE nombre_opcion = %s"
            cursor.execute(sql, (nombre_opcion,))
            row = cursor.fetchone()
            
            if row:
                return float(row['precio_adicional'])
            return 0.0
        
class Venta(EntidadBD):
    def __init__(self, id_metodo, total_pagado):
        super().__init__()
        self.id_metodo = id_metodo
        self.total_pagado = total_pagado

    def guardar(self):
        with self.db.cursor() as cursor:
            sql = "INSERT INTO Ventas (id_metodo, total_pagado, estado) VALUES (%s, %s, 'Pagado')"
            cursor.execute(sql, (self.id_metodo, self.total_pagado))
            self.db.commit()
            return cursor.lastrowid

    def listar_todos(self):
        with self.db.cursor() as cursor:
            cursor.execute("SELECT * FROM Ventas")
            return cursor.fetchall()

class DetalleVenta(EntidadBD):
    def __init__(self, id_venta, id_producto, subtotal_base, cantidad=1):
        super().__init__()
        self.id_venta = id_venta
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.subtotal_base = subtotal_base

    def guardar(self):
        with self.db.cursor() as cursor:
            sql = "INSERT INTO Detalle_Ventas (id_venta, id_producto, cantidad, subtotal_base) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (self.id_venta, self.id_producto, self.cantidad, self.subtotal_base))
            self.db.commit()
            return cursor.lastrowid

    def listar_todos(self):
        with self.db.cursor() as cursor:
            cursor.execute("SELECT * FROM Detalle_Ventas")
            return cursor.fetchall()
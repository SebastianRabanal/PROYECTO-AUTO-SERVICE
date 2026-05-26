from fastapi import APIRouter, HTTPException
from schemas.pydantic_models import PedidoCreate
from models.entities import Producto, Venta, DetalleVenta

router = APIRouter()

@router.get("/productos")
def obtener_carta():
    producto_model = Producto()
    return producto_model.listar_todos()

@router.post("/comprar")
def registrar_compra(pedido: PedidoCreate):
    if len(pedido.detalle_pedido) == 0 or pedido.total <= 0:
        raise HTTPException(status_code=400, detail="Transacción rechazada: El ticket está vacío o el monto es inválido.")
    
    # Mapeo de métodos de pago según la base de datos
    metodos_map = {"yape": 1, "plin": 2, "efectivo": 3}
    id_metodo = metodos_map.get(pedido.metodo_pago, 3)
    
    # 1. Guardar la cabecera de la venta
    venta_model = Venta(id_metodo=id_metodo, total_pagado=pedido.total)
    id_venta = venta_model.guardar()
    
    # Instanciar el modelo de Producto para buscar los IDs
    producto_model = Producto()
    
    # 2. Recorrer el ticket y guardar el detalle de productos
    for item in pedido.detalle_pedido:
        id_producto = producto_model.buscar_id_por_nombre(item.nombre)
        
        if id_producto:
            detalle_model = DetalleVenta(
                id_venta=id_venta, 
                id_producto=id_producto, 
                subtotal_base=item.subtotal
            )
            detalle_model.guardar()
            
            # (El guardado de modificadores en la tabla Seleccion_Modificadores 
            # puede añadirse aquí siguiendo la misma lógica de POO si lo requieren).

    return {
        "status": "success",
        "mensaje": "Voucher generado correctamente",
        "id_venta": id_venta,
        "total": pedido.total
    }

@router.get("/modificadores/{id_producto}")
def obtener_opciones(id_producto: int):
    producto_model = Producto()
    return producto_model.obtener_modificadores(id_producto)
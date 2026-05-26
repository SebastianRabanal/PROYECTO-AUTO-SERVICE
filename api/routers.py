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
    if len(pedido.detalle_pedido) == 0:
        raise HTTPException(status_code=400, detail="Transacción rechazada: El ticket está vacío.")
    
    producto_model = Producto()
    total_real_calculado = 0.0
    detalles_procesados = []
    
    # 1. Blindaje matemático: Calcular el total consultando MySQL
    for item in pedido.detalle_pedido:
        datos_producto = producto_model.obtener_id_y_precio_por_nombre(item.nombre)
        
        if not datos_producto:
            raise HTTPException(status_code=400, detail=f"Producto no válido o manipulado: {item.nombre}")
            
        id_producto, precio_base = datos_producto
        subtotal_item = precio_base
        
        # SUMAR LOS EXTRAS
        for nombre_extra in item.extras:
            precio_extra = producto_model.obtener_precio_modificador(nombre_extra)
            subtotal_item += precio_extra
            
        total_real_calculado += subtotal_item
        
        detalles_procesados.append({
            "id_producto": id_producto,
            "subtotal_final": subtotal_item
        })
        
    # Redondeo por seguridad (Evita errores de decimales como 19.000000001)
    total_real_calculado = round(total_real_calculado, 2)
        
    if total_real_calculado <= 0:
        raise HTTPException(status_code=400, detail="Monto total inválido.")

    # 2. Guardar la cabecera usando el total blindado
    metodos_map = {"yape": 1, "plin": 2, "efectivo": 3}
    id_metodo = metodos_map.get(pedido.metodo_pago, 3)
    
    venta_model = Venta(id_metodo=id_metodo, total_pagado=total_real_calculado)
    id_venta = venta_model.guardar()
    
    # 3. Guardar el detalle de productos
    for det in detalles_procesados:
        detalle_model = DetalleVenta(
            id_venta=id_venta, 
            id_producto=det["id_producto"], 
            subtotal_base=det["subtotal_final"]
        )
        detalle_model.guardar()

    return {
        "status": "success",
        "mensaje": "Voucher generado correctamente",
        "id_venta": id_venta,
        "total": total_real_calculado
    }

@router.get("/modificadores/{id_producto}")
def obtener_opciones(id_producto: int):
    producto_model = Producto()
    return producto_model.obtener_modificadores(id_producto)
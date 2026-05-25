from fastapi import APIRouter
from schemas.pydantic_models import PedidoCreate
from models.entities import Producto, Venta

router = APIRouter()

@router.get("/productos")
def obtener_carta():
    producto_model = Producto()
    return producto_model.listar_todos()

@router.post("/comprar")
def registrar_compra(pedido: PedidoCreate):
    metodos_map = {"yape": 1, "plin": 2, "efectivo": 3}
    id_metodo = metodos_map.get(pedido.metodo_pago, 3)
    
    venta_model = Venta(id_metodo=id_metodo, total_pagado=pedido.total)
    id_venta = venta_model.guardar()
    
    return {
        "status": "success",
        "mensaje": "Voucher generado correctamente",
        "id_venta": id_venta,
        "total": pedido.total
    }

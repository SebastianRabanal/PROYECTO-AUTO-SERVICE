from pydantic import BaseModel
from typing import List

# Esquema para cada producto dentro del ticket
class ItemPedido(BaseModel):
    nombre: str
    cremas: List[str]
    extras: List[str]
    subtotal: float

# Esquema principal que recibe el POST
class PedidoCreate(BaseModel):
    metodo_pago: str
    total: float
    detalle_pedido: List[ItemPedido]
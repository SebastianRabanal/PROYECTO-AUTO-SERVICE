from pydantic import BaseModel
from typing import List

class ItemTicket(BaseModel):
    nombre_item: str
    detalles: List[str]
    precio: float

class PedidoCreate(BaseModel):
    items: List[ItemTicket]
    total: float
    metodo_pago: str

from datetime import datetime
from pydantic import BaseModel
from typing import List

class Categoria(BaseModel):
    id: str
    title: str
    desc: str
    produtos: List[str]
    # status: bool
    # created_at: datetime
    # updated_at: datetime

class Produto(BaseModel):
    id: str
    title: str
    desc: str
    price: float
    qty: int
    categorias: List[str]
    # status: bool
    # created_at: datetime
    # updated_at: datetime
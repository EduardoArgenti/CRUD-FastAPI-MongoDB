from pydantic import BaseModel
from typing import List

class Categoria(BaseModel):
    id: str
    title: str
    desc: str
    produtos: List[str]

class Produto(BaseModel):
    id: str
    title: str
    desc: str
    price: float
    qty: int
    categorias: List[str]
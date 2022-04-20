from pydantic import BaseModel
from typing import List

class Categoria(BaseModel):
    id: int
    title: str
    desc: str
    produtos: List[int]

class Produto(BaseModel):
    id: int
    title: str
    desc: str
    price: float
    qty: int
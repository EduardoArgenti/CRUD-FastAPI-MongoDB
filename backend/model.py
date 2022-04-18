from pydantic import BaseModel
from typing import List

class Categoria(BaseModel):
    id: int
    title: str
    desc: str

class Produto(BaseModel):
    id: int
    title: str
    desc: str
    price: float
    qty: int
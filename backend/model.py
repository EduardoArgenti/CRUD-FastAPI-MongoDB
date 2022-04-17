from pydantic import BaseModel
from typing import List

class Categoria(BaseModel):
    id: int
    title: str
    desc: str


    
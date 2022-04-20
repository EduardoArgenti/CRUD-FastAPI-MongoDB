from model import Categoria, Produto
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List

# App Object
app = FastAPI()

from database import(
    fetch_one_categoria,
    fetch_all_categorias,
    create_categoria,
    update_categoria,
    remove_categoria,
    fetch_one_produto,
    fetch_all_produtos,
    create_produto,
    update_produto,
    remove_produto
)

origins = ['https://localhost:3000']

"""
# O front se comunica com o back pelo CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)
"""

@app.get("/")
def read_root():
    return {"Ping" : "Pong"}

# CRUD categorias

@app.get("/api/categoria")
async def get_categoria():
    response = await fetch_all_categorias()
    return response

@app.get("/api/categoria{id}", response_model = Categoria)
async def get_categoria_by_id(id:int):# Se não especificar o tipo do ID (int), a aplicação não localiza o registro.
    response = await fetch_one_categoria(id)
    if response:
        return response
    raise HTTPException(404, f"There is no Categoria item with this ID {id}")

@app.post("/api/categoria", response_model = Categoria)
async def post_categoria(categoria:Categoria):
    response = await create_categoria(categoria.dict())
    if response:
        return response
    raise HTTPException(400, f"Something went wrong / Bad Request")

@app.put("/api/categoria{id}/", response_model = Categoria)
async def put_categoria(id:int, title:str, desc:str, produtos:List[int]):
    response = await update_categoria(id, title, desc, produtos)
    if response:
        return response
    raise HTTPException(404, f"There is no Categoria item with this ID {id}")

@app.delete("/api/categoria{id}")
async def delete_categoria(id:int):
    response = await remove_categoria(id)
    if response:
        return "Successfully deleted Categoria item!"
    raise HTTPException(404, f"There is no Categoria item with this ID {id}")

# CRUD produtos

@app.get("/api/produto")
async def get_produto():
    response = await fetch_all_produtos()
    return response

@app.get("/api/produto{id}", response_model = Produto)
async def get_produto_by_id(id:int): # Se não especificar o tipo do ID (int), a aplicação não localiza o registro.
    response = await fetch_one_produto(id)
    if response:
        return response
    raise HTTPException(404, f"There is no Produto item with this ID {id}")

@app.post("/api/produto", response_model = Produto)
async def post_produto(produto:Produto):
    response = await create_produto(produto.dict())
    if response:
        return response
    raise HTTPException(400, f"Something went wrong / Bad Request")

@app.put("/api/produto{id}/", response_model = Produto)
async def put_produto(id:int, title:str, desc:str, price:float, qty:int):
    response = await update_produto(id, title, desc, price, qty)
    if response:
        return response
    raise HTTPException(404, f"There is no Produto item with this ID {id}")

@app.delete("/api/produto{id}/")
async def delete_produto(id:int):
    response = await remove_produto(id)
    if response:
        return "Successfully deleted Produto item!"
    raise HTTPException(404, f"There is no Produto item with this ID {id}")

# Testes
@app.get("/api/produto{id}/mostrar_preco")
async def mostrar_preco_produto(id:int): # Se não especificar o tipo do ID (int), a aplicação não localiza o registro.
    document = await fetch_one_produto(id)
    if document:
        return {"produto_id" : document["id"], "preco_produto" : document["price"]}
    raise HTTPException(404, f"There is no Produto item with this ID {id}")


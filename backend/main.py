from model import Categoria, Produto
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from database import *


# App Object
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello" : "World!"}

# CRUD categorias
@app.get("/api/categoria", status_code=status.HTTP_202_ACCEPTED)
async def buscar_todas_as_categorias():
    response = await fetch_all_categorias()
    return response

@app.get("/api/categoria{id}", response_model = Categoria, status_code=status.HTTP_202_ACCEPTED)
async def buscar_categoria_pelo_id(id:str):# Se não especificar o tipo do ID (str), a aplicação não localiza o registro.
    response = await fetch_one_categoria(id)
    if response:
        return response
    raise HTTPException(404, f"There is no Categoria item with this ID {id}")

@app.post("/api/categoria", response_model = Categoria, status_code=status.HTTP_201_CREATED)
async def criar_categoria(id:str, title:str, desc: str):
    categoria = {
        'id' : id,
        'title' : title,
        'desc' : desc,
        'produtos' : [] 
    }

    response = await create_categoria(categoria)
    if response:
        return response
    raise HTTPException(409, f"Category already exists / Conflict")

@app.put("/api/categoria{id}", response_model = Categoria, status_code=status.HTTP_202_ACCEPTED)
async def atualizar_categoria(id:str, title:str, desc:str):
    response = await update_categoria(id, title, desc)
    if response:
        return response
    raise HTTPException(404, f"There is no Categoria item with this ID {id}")

@app.delete("/api/categoria{id}", status_code=status.HTTP_202_ACCEPTED)
async def remover_categoria(id:str):
    response = await remove_categoria(id)
    if response:
        return "Successfully deleted Categoria item!"
    raise HTTPException(404, f"There is no Categoria item with this ID {id}")

# CRUD produtos
@app.get("/api/produto", status_code=status.HTTP_202_ACCEPTED)
async def buscar_todos_os_produtos():
    response = await fetch_all_produtos()
    return response

@app.get("/api/produto{id}", response_model = Produto, status_code=status.HTTP_202_ACCEPTED)
async def buscar_produto_pelo_id(id:str): # Se não especificar o tipo do ID (str), a aplicação não localiza o registro.
    response = await fetch_one_produto(id)
    if response:
        return response
    raise HTTPException(404, f"There is no Produto item with this ID {id}")

@app.post("/api/produto", response_model = Produto, status_code=status.HTTP_201_CREATED)
async def criar_produto(id:str, title:str, desc: str, price: float, qty: int):
    produto = {
        'id' : id,
        'title' : title,
        'desc' : desc,
        'price' : price,
        'qty' : qty,
        'categorias' : []
    }
    
    response = await create_produto(produto)
    if response:
        return response
    raise HTTPException(409, f"Product already exists / Conflict")

@app.put("/api/produto{id}", response_model = Produto, status_code=status.HTTP_202_ACCEPTED)
async def atualizar_produto(id:str, title:str, desc:str, price:float, qty:int):
    response = await update_produto(id, title, desc, price, qty)
    if response:
        return response
    raise HTTPException(404, f"There is no Produto item with this ID {id}")

@app.delete("/api/produto{id}", status_code=status.HTTP_202_ACCEPTED)
async def remover_produto(id:str):
    response = await remove_produto(id)
    if response:
        return "Successfully deleted Produto item!"
    raise HTTPException(404, f"There is no Produto item with this ID {id}")


# Vincular Categorias e Produtos
@app.put("/api/categoria{id}/vincula_produtos", response_model = Categoria, status_code=status.HTTP_202_ACCEPTED)
async def vincular_produtos_categoria(id_cat:str, id_produtos:List[str]):
    response = await vincula_produtos_categoria(id_cat, id_produtos)
    if response:
        return response
    raise HTTPException(404, f"Error: Category or Product does not exist.")

@app.put("/api/categoria{id}/desvincula_produtos", response_model = Categoria, status_code=status.HTTP_202_ACCEPTED)
async def desvincular_produtos_categoria(id_cat:str, id_produtos:List[str]):
    response = await desvincula_produtos_categoria(id_cat, id_produtos)
    if response:
        return response
    raise HTTPException(404, f"Error: The products could not be unlinked.")



# Funções diversas
@app.get("/api/produto{id}/mostrar_preco", status_code=status.HTTP_202_ACCEPTED)
async def mostrar_preco_do_produto(id:str): # Se não especificar o tipo do ID (int), a aplicação não localiza o registro.
    document = await fetch_one_produto(id)
    if document:
        return {"produto_id" : document["id"], "preco_produto" : document["price"]}
    raise HTTPException(404, f"There is no Produto item with this ID {id}")

@app.get("/api/categoria{id}/mostrar_produtos")
async def mostrar_produtos_da_categoria(id_cat:str, status_code=status.HTTP_202_ACCEPTED):
    categoria = await fetch_one_categoria(id_cat)
    if categoria:
        return {"categoria_id" : categoria["id"], "produtos_vinculados" : categoria["produtos"]}
    raise HTTPException(404, f"There is no Categoria item with this ID {id_cat}")
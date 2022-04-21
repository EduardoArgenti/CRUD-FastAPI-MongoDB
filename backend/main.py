from model import Categoria, Produto
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
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
    remove_produto,
    update_produtos_categoria
)


# App Object
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello" : "World!"}

# CRUD categorias
@app.get("/api/categoria")
async def buscar_todas_as_categorias():
    response = await fetch_all_categorias()
    return response

@app.get("/api/categoria{id}", response_model = Categoria)
async def buscar_categoria_pelo_id(id:str):# Se não especificar o tipo do ID (str), a aplicação não localiza o registro.
    response = await fetch_one_categoria(id)
    if response:
        return response
    raise HTTPException(404, f"There is no Categoria item with this ID {id}")

@app.post("/api/categoria", response_model = Categoria)
async def criar_categoria(categoria:Categoria):
    response = await create_categoria(categoria.dict())
    if response:
        return response
    raise HTTPException(400, f"Something went wrong / Bad Request")

@app.put("/api/categoria{id}", response_model = Categoria)
async def atualizar_categoria(id:str, title:str, desc:str, produtos:List[str]):
    response = await update_categoria(id, title, desc, produtos)
    if response:
        return response
    raise HTTPException(404, f"There is no Categoria item with this ID {id}")

@app.delete("/api/categoria{id}")
async def remover_categoria(id:str):
    response = await remove_categoria(id)
    if response:
        return "Successfully deleted Categoria item!"
    raise HTTPException(404, f"There is no Categoria item with this ID {id}")

# CRUD produtos
@app.get("/api/produto")
async def buscar_todos_os_produtos():
    response = await fetch_all_produtos()
    return response

@app.get("/api/produto{id}", response_model = Produto)
async def buscar_produto_pelo_id(id:str): # Se não especificar o tipo do ID (str), a aplicação não localiza o registro.
    response = await fetch_one_produto(id)
    if response:
        return response
    raise HTTPException(404, f"There is no Produto item with this ID {id}")

@app.post("/api/produto", response_model = Produto)
async def criar_produto(produto:Produto):
    response = await create_produto(produto.dict())
    if response:
        return response
    raise HTTPException(400, f"Something went wrong / Bad Request")

@app.put("/api/produto{id}", response_model = Produto)
async def atualizar_produto(id:str, title:str, desc:str, price:float, qty:int):
    response = await update_produto(id, title, desc, price, qty)
    if response:
        return response
    raise HTTPException(404, f"There is no Produto item with this ID {id}")

@app.delete("/api/produto{id}")
async def remover_produto(id:str):
    response = await remove_produto(id)
    if response:
        return "Successfully deleted Produto item!"
    raise HTTPException(404, f"There is no Produto item with this ID {id}")

# Testes
@app.get("/api/produto{id}/mostrar_preco")
async def mostrar_preco_do_produto(id:str): # Se não especificar o tipo do ID (int), a aplicação não localiza o registro.
    document = await fetch_one_produto(id)
    if document:
        return {"produto_id" : document["id"], "preco_produto" : document["price"]}
    raise HTTPException(404, f"There is no Produto item with this ID {id}")

# Vincular Categorias e Produtos
@app.put("/api/categoria{id}/vincula_produtos", response_model = Categoria)
async def vincular_produtos_categoria(id_cat:str, id_produtos:List[str]):
    response = await update_produtos_categoria(id_cat, id_produtos)
    if response:
        return response
    raise HTTPException(404, f"Error: The products could not be linked.")


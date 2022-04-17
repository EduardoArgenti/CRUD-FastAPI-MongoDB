from model import Categoria
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# App Object
app = FastAPI()

from database import(
    fetch_one_categoria,
    fetch_all_categorias,
    create_categoria,
    update_categoria,
    remove_categoria
)

origins = ['https://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.get("/")
def read_root():
    return {"Ping" : "Pong"}

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
async def put_categoria(id:int, title:str, desc:str):
    response = await update_categoria(id, title, desc)
    if response:
        return response
    raise HTTPException(404, f"There is no Categoria item with this ID {id}")

@app.delete("/api/categoria{id}")
async def delete_categoria(id:int):
    response = await remove_categoria(id)
    if response:
        return "Successfully deleted todo item!"
    raise HTTPException(404, f"There is no Categoria item with this ID {id}")
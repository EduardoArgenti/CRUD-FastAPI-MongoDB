import asyncio
import motor.motor_asyncio
from model import Categoria

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017/')

database = client.ListaCategoria
collection = database.categoria

# CRUD categorias
async def fetch_one_categoria(id):
    document = await collection.find_one({"id" : id})
    return document

async def fetch_all_categorias():
    todos = []
    cursor = collection.find({})
    async for document in cursor:
        todos.append(Categoria(**document))
    return todos

async def create_categoria(categoria):
    document = categoria
    result = await collection.insert_one(document)
    return document

async def update_categoria(id, title, desc):
    # Preparação da definição do update (necessário ao atualizar mais de 1 atributo)
    update = {
        'title' : title,
        'desc' : desc
    }

    await collection.update_one({"id" : id}, {"$set" : update})
    document = await collection.find_one({"id" : id})
    return document

async def remove_categoria(id):
    await collection.delete_one({"id" : id})
    return True
import motor.motor_asyncio # MongoDB driver
from model import Categoria, Produto

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017/')

database = client.ListaCategoria
collectionCategorias = database.categoria
collectionProdutos = database.produto

# CRUD categorias
async def fetch_one_categoria(id):
    document = await collectionCategorias.find_one({"id" : id})
    return document

async def fetch_all_categorias():
    categorias = []
    cursor = collectionCategorias.find({})
    async for document in cursor:
        categorias.append(Categoria(**document))
    return categorias

async def create_categoria(categoria):
    document = categoria
    result = await collectionCategorias.insert_one(document)
    return document

async def update_categoria(id, title, desc, produtos):
    # Preparação da definição do update (necessário ao atualizar mais de 1 atributo)
    update = {
        'title' : title,
        'desc' : desc,
        'produtos' : produtos
    }

    await collectionCategorias.update_one({"id" : id}, {"$set" : update})
    document = await collectionCategorias.find_one({"id" : id})
    return document

async def remove_categoria(id):
    if await collectionCategorias.find_one({"id" : id}): # Temos a categoria para deletar
        await collectionCategorias.delete_one({"id" : id})
        return True
    return False

# CRUD produtos
async def fetch_one_produto(id):
    document = await collectionProdutos.find_one({"id" : id})
    return document

async def fetch_all_produtos():
    produtos = []
    cursor = collectionProdutos.find({})
    async for document in cursor:
        produtos.append(Produto(**document))
    return produtos

async def create_produto(produto):
    document = produto
    result = await collectionProdutos.insert_one(document)
    return document

async def update_produto(id, title, desc, price, qty):
    # Preparação da definição do update (necessário ao atualizar mais de 1 atributo)
    update = {
        'title' : title,
        'desc' : desc,
        'price' : price,
        'qty' : qty
    }

    await collectionProdutos.update_one({"id" : id}, {"$set" : update})
    document = await collectionProdutos.find_one({"id" : id})
    return document

async def remove_produto(id):
    if await collectionProdutos.find_one({"id" : id}): # Temos o produto para deletar
        await collectionProdutos.delete_one({"id" : id})
        return True
    return False

# Testes


import motor.motor_asyncio # MongoDB driver
from model import Categoria, Produto

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017/')

database = client.Loja
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
    if await fetch_one_categoria(document["id"]): # Checa se categoria já existe no banco
        return False
    else:
        print("Categoria não existe")
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

async def remove_categoria(id_categoria):
    categoria_deletada = await collectionCategorias.find_one({"id" : id_categoria})
    
    if categoria_deletada: # Temos a categoria para deletar
        
        # Insira aqui o código de apagar a categoria dos produtos
        if categoria_deletada["produtos"]: # Categoria está associada a produtos
    
            for id_produto in categoria_deletada["produtos"]:
                produto = await fetch_one_produto(id_produto) # Puxamos do banco o produto vinculado
                produto["categorias"].remove(str(id_categoria)) # Apaga ID da categoria na lista do produto

                updateProd = {
                    "categorias" : produto["categorias"]
                }

                await collectionProdutos.update_one({"id" : id_produto}, {"$set" : updateProd}) # Atualiza produto no banco
            
            await collectionCategorias.delete_one({"id" : id_categoria})
            return True
        else:
            print("Category does not have products")
            await collectionCategorias.delete_one({"id" : id_categoria})
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

    if await fetch_one_produto(document["id"]): # Checa se produto já existe no banco
        return False
    else:
        print("Produto não existe")
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

async def remove_produto(id_produto):
    produto_deletado = await collectionProdutos.find_one({"id" : id_produto})

    if produto_deletado: # Temos o produto para deletar
        if produto_deletado["categorias"]: # Produto está associado a categorias
    
            for id_categoria in produto_deletado["categorias"]:
                categoria = await fetch_one_categoria(id_categoria) # Puxamos do banco a categoria vinculada
                categoria["produtos"].remove(str(id_produto)) # Apaga ID do produto na lista da categoria

                updateCat = {
                    "produtos" : categoria["produtos"]
                }

                await collectionCategorias.update_one({"id" : id_categoria}, {"$set" : updateCat}) # Atualiza categoria no banco
            await collectionProdutos.delete_one({"id" : id_produto})
            return True
        else:
            print("Product does not have categories.")
            await collectionProdutos.delete_one({"id" : id_produto})
            return True
    return False

# Atualiza Categorias e Produtos
async def vincula_produtos_categoria(id_cat, id_produtos):

    # Vincula os produtos numa categoria
    categoria = await fetch_one_categoria(id_cat)
    categoria["produtos"] = categoria["produtos"] + id_produtos # Concatena a lista antiga com os novos produtos

    categoria["produtos"] = list(dict.fromkeys(categoria["produtos"])) # Remove produtos duplicados, se houver

    updateCat = {
        'produtos' : categoria["produtos"]
    }

    await collectionCategorias.update_one({"id" : id_cat}, {"$set" : updateCat}) # Atualiza nova lista de produtos no banco

    # Vincula a categoria nos produtos
    for id_produto in id_produtos:
        produto = await fetch_one_produto(id_produto)
        produto["categorias"].append(id_cat)

        produto["categorias"] = list(dict.fromkeys(produto["categorias"])) # Remove categorias duplicadas, se houver

        updateProd = {
            'categorias' : produto["categorias"]
        }

        await collectionProdutos.update_one({"id" : id_produto}, {"$set" : updateProd})
    
    document = await collectionCategorias.find_one({"id": id_cat})
    return document

async def desvincula_produtos_categoria(id_cat, id_produtos):

    # remove produtos da categoria
    categoria = await fetch_one_categoria(id_cat)
    for id_produto in id_produtos:
        categoria["produtos"].remove(id_produto)

    updateCat = {
        'produtos' : categoria["produtos"]
    }

    await collectionCategorias.update_one({"id" : id_cat}, {"$set" : updateCat})

    # remove categoria dos produtos
    for id_produto in id_produtos:
        produto = await fetch_one_produto(id_produto)
        produto["categorias"].remove(id_cat)

        updateProd = {
            'categorias' : produto["categorias"]
        }

        await collectionProdutos.update_one({"id" : id_produto}, {"$set" : updateProd})

    document = await collectionCategorias.find_one({"id": id_cat})
    return document
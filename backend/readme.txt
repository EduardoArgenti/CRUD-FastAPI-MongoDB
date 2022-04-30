Dependências:

    - fastapi ==  0.65.1
    - uvicorn == 0.14.0
    - motor == 2.4.0

Organização do código:

    - main.py: arquivo com as rotas da FastAPI, que disparam funções localizadas no database.py
    - database.py: arquivo com conexão ao banco MongoDB e implementações dos CRUDs e vinculação das entidades (produtos e categorias)
    - model.py: implementação das classes utilizadas


Como utilizar a API:

    - Buscar todas as categorias/produtos: sem parâmetros
    - Buscar categoria/produto pelo ID: informar o ID
    - Criar categoria/produto:
        - O ID deve ser único e é diferente do _id atribuído pelo SGBD (API trata tentativas de cadastro de IDs já existentes)
        - Produtos/categorias devem ser vinculados APÓS sua criação, na função específica de vinculação
    - Atualizar categoria/produto:
        - O sistema não permite alterar o ID de registros.
        - Os itens vinculados (produtos e categorias) também não devem ser vinculados aqui, mas sim na função específica de vinculação.
    - Remover categoria/produto:
        - Assim que um produto é removido, ele é automaticamente desvinculado das categorias que o continham, e vice-versa.
    - Vincular produtos a uma categoria:
        - As categorias contêm uma lista de IDs de produtos vinculados e os produtos contêm uma lista de IDs de categorias. 
        - Ao informar uma lista de produtos a serem vinculados em uma categoria, ambas as entidades são atualizadas
        - OBS: com mais prática e tempo de estudo do MongoDB, acredito que seria possível tratar esta vinculação ao nível do banco de 
        dados, de maneira não-relacional.
    - Desvincular produtos de uma categoria:
        - Quando um deles é deletado, como um produto, a aplicação acessa todas as categorias vinculadas e remove o registro 
        do ID de lá, também. O contrário também ocorre para remoção de categorias.

Vídeo demonstrativo da aplicação:

    - https://www.youtube.com/watch?v=vZz4nXtg3Zg


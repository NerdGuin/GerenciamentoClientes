import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Carregando variáveis de ambiente do arquivo .env
load_dotenv()

# Obtendo a URL do MongoDB a partir das variáveis de ambiente
database_url = os.getenv('DATABASE_URL')

# Estabelecendo conexão com o MongoDB
client = MongoClient(database_url)
db = client['dados']
collection = db['clientes']

# Lista para armazenar os clientes
clientes = []

# Função para consultar e listar todos os clientes
def listar_clientes():
    clientes.clear()
    for doc in collection.find():
        clientes.append(doc)

# Função para inserir um novo cliente
def novo_cliente(nome, idade, quantidade):
    collection.insert_one({
        "nome": nome, 
        "idade": int(idade), 
        "quantidade": int(quantidade)
    })
    print('Novo cliente adicionado!')

# Função para excluir um cliente pelo ID
def excluir_cliente(id):
    collection.delete_one({"_id": id})
    print('Cliente removido!')

# Fechando a conexão com o MongoDB
# client.close()

import streamlit as st
from azure.storage.blob import BlobServiceClient
import pymssql
import uuid
import json
import os
import pandas as pd
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

# Configurações do Azure Storage
CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")  # aqui você vai inserir a connection string completa da sua conta de armazenamento
CONTAINER_NAME = os.getenv("AZURE_BLOB_CONTAINER_NAME")  # nome do container no Blob Storage
ACCOUNT_NAME = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")  # nome da conta de armazenamento

# Configurações do Azure SQL Server
SQL_SERVER   = os.getenv("AZURE_SQL_SERVER")    # endpoint do SQL Server ex: servidor.database.windows.net
SQL_DATABASE = os.getenv("AZURE_SQL_DATABASE")  # nome do banco de dados
SQL_USERNAME = os.getenv("AZURE_SQL_USERNAME")  # nome do usuário
SQL_PASSWORD = os.getenv("AZURE_SQL_PASSWORD")  # senha do usuário

# Título da aplicação
st.title("Cadastro de Produto - E-Commerce na Cloud")

# Formulário para cadastro do produto
product_name = st.text_input("Nome do Produto")
description = st.text_area("Descrição do Produto")
price = st.number_input("Preço do Produto", min_value=0.0, format="%.2f")
uploaded_file = st.file_uploader("Imagem do Produto", type=["png", "jpg", "jpeg"])

# Função para enviar imagem para o Azure Blob Storage
def upload_image(file):
    try:
        if file.size > 5_000_000:  # 5MB
            st.error("A imagem deve ter menos de 5MB")
            return None
        blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        blob_name = f"{uuid.uuid4()}.jpg"
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(file.read(), overwrite=True)
        image_url = f"https://{ACCOUNT_NAME}.blob.core.windows.net/{CONTAINER_NAME}/{blob_name}"
        return image_url
    except Exception as e:
        st.error(f"Erro ao enviar imagem: {e}")
        return None

# Função para inserir os dados do produto no Azure SQL Server usando pymssql
def insert_product_sql(product_data):
    try:
        conn = pymssql.connect(server=SQL_SERVER, user=SQL_USERNAME, password=SQL_PASSWORD, database=SQL_DATABASE)
        cursor = conn.cursor()
        insert_query = '''
        INSERT INTO dbo.Produtos (nome, descricao, preco, image_url)
        VALUES (%s, %s, %s, %s)
        '''
        cursor.execute(insert_query, (product_data["nome"], product_data["descricao"], product_data["preco"], product_data["image_url"]))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erro ao inserir no Azure SQL: {e}")
        return False

# Função para listar os produtos do Azure SQL Server
def list_products_sql():
    try:
        conn = pymssql.connect(server=SQL_SERVER, user=SQL_USERNAME, password=SQL_PASSWORD, database=SQL_DATABASE)
        cursor = conn.cursor(as_dict=True)
        query = "SELECT id, nome, descricao, preco, image_url FROM dbo.Produtos"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Exception as e:
        st.error(f"Erro ao listar produtos: {e}")
        return []

# Função para exibir a lista de produtos na tela
def list_produtos_screen():
    products = list_products_sql()
    if products:
        cards_por_linha = 3
        cols = st.columns(cards_por_linha)
        for i, product in enumerate(products):
            col = cols[i % cards_por_linha]
            with col:
                st.markdown(f"### {product['nome']}")
                st.write(f"**Descrição:** {product['descricao']}")
                st.write(f"**Preço:** R$ {product['preco']:.2f}")
                if product["image_url"]:
                    html_img = f'<img src="{product["image_url"]}" width="200" height="200" alt="Imagem do produto">'
                    st.markdown(html_img, unsafe_allow_html=True)
                st.markdown("---")
            if (i + 1) % cards_por_linha == 0 and (i + 1) < len(products):
                cols = st.columns(cards_por_linha)
    else:
        st.info("Nenhum produto encontrado.")

# Botão para cadastro do produto
if st.button("Cadastrar Produto"):
    if not product_name or not description or price is None:
        st.warning("Preencha todos os campos obrigatórios!")
    else:
        image_url = ""
        if uploaded_file is not None:
            image_url = upload_image(uploaded_file)
        product_data = {
            "nome": product_name,
            "descricao": description,
            "preco": price,
            "image_url": image_url
        }
        if insert_product_sql(product_data):
            st.success("Produto cadastrado com sucesso no Azure SQL!")
            list_produtos_screen()
        else:
            st.error("Houve um problema ao cadastrar o produto no Azure SQL.")
        file_path = "produtos.json"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    produtos = json.load(f)
                except json.JSONDecodeError:
                    produtos = []
        else:
            produtos = []
        produtos.append(product_data)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(produtos, f, ensure_ascii=False, indent=4)
        st.json(product_data)

st.header("Listagem dos Produtos")

# Botão para carregar e exibir a lista de produtos
if st.button("Listar Produtos"):
    list_produtos_screen()

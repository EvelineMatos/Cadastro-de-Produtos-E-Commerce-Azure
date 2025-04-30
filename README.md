# 🛒 Cadastro de Produtos - E-Commerce na Nuvem

Este projeto é uma aplicação de e-commerce baseada em nuvem desenvolvida com **Streamlit**. Ele permite cadastrar e listar produtos com nome, descrição, preço e imagem. Os dados são armazenados em **serviços da Azure**, integrando **SQL Database** e **Blob Storage** para armazenamento seguro e escalável.

---

## 🚀 Funcionalidades

- Formulário para cadastro de produtos com upload de imagem.
- Armazenamento de imagens em Blob Storage.
- Armazenamento de dados dos produtos em SQL Database.
- Listagem dinâmica de produtos cadastrados, exibidos em cards com imagem.

---

## 🖼️ Interface da Aplicação

### Formulário de Cadastro
![Formulário de Produto](/Laboratorio/assets/Formulário%20de%20Cadastro.png)

---

## ☁️ Infraestrutura na Nuvem (Azure)

A aplicação utiliza os seguintes **tipos de recursos da Azure**:

| Tipo de Recurso Azure     | Função                                    |
|---------------------------|-------------------------------------------|
| Conta de Armazenamento    | Armazena imagens dos produtos (Blob)      |
| Banco de Dados SQL        | Armazena informações dos produtos         |
| SQL Server                | Host do banco SQL                         |
| Grupo de Recursos         | Organização e gerenciamento dos serviços  |
| Assinatura Azure          | Controle de faturamento e permissões      |

---

## 📐 Arquitetura da Solução

A arquitetura do sistema é composta por três camadas principais:

1. **Frontend (Streamlit App)** – Interface web para cadastro e listagem de produtos.
2. **Armazenamento de Imagens (Blob Storage)** – As imagens são enviadas para o Azure Blob Storage e os links são armazenados no banco.
3. **Armazenamento de Dados (Azure SQL Database)** – Os metadados dos produtos (nome, descrição, preço, URL da imagem) são salvos em uma tabela no banco de dados.

### Diagrama:
![Arquitetura da Solução](/Laboratorio/assets/arquitetura.png)

---

## 🧪 Consulta SQL Utilizada

Abaixo está a query utilizada para consultar os produtos armazenados:

```sql
SELECT id, nome, descricao, image_url, preco 
FROM dbo.Produtos
```

### Resultado Visual da Consulta:
![Resultado da Consulta](/Laboratorio/assets/resultado%20query.png)

---

## ⚙️ Tecnologias Utilizadas

- **Python 3.8+**
- **Streamlit** – Framework para construção rápida de aplicações web em Python.
- **Azure Blob Storage SDK (`azure-storage-blob`)** – Para upload e gestão de imagens.
- **pymssql** – Cliente Python para conectar-se ao Azure SQL Database via TDS.
- **Pandas** – Para organização e estruturação dos dados.
- **UUID / JSON / OS** – Bibliotecas nativas utilizadas para geração de nomes únicos, persistência local e manipulação de arquivos.

---

## 📂 Estrutura do Projeto

```bash
├── main.py                # Código principal da aplicação
├── produtos.json          # Backup local dos dados (opcional)
├── README.md              # Este documento
├── requirements.txt       # Dependências do projeto
├── *.png                  # Imagens ilustrativas e de resultado
```

---

## 📦 Arquivo de Dependências

### `requirements.txt`

```txt
streamlit
azure-storage-blob
pymssql
pandas
```

---

## ▶️ Executando o Projeto

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Execute a aplicação:
```bash
streamlit run main.py
```

3. Acesse a interface no navegador e comece a cadastrar produtos.

---

## 🔒 Considerações de Segurança

As **credenciais do Azure** estão embutidas diretamente no código (hardcoded). Para ambientes de produção, é **altamente recomendado**:

- Usar variáveis de ambiente para armazenar secrets.
- Ou utilizar Azure Key Vault para segurança centralizada.
- Garantir que os arquivos `.py` não sejam expostos publicamente sem sanitização.

---

## 📬 Contato

Para dúvidas ou contribuições, entre em contato através do [meu LinkedIn](https://www.linkedin.com/in/eveline-matos-silva-a2a18526/).  
Fique à vontade para propor melhorias ou trocar ideias!


# 🌍 Projeto de Persistência Poliglota  
🚀 Uma jornada de dados com Python!

---

## 📌 Sobre o Projeto
Este projeto é uma demonstração de **persistência poliglota**, combinando:  
- A robustez de um banco de dados **relacional (SQLite)**  
- A flexibilidade de um banco de dados **NoSQL (MongoDB)**  

Tudo isso integrado com recursos de **geoprocessamento** em um sistema completo:  
- ⚡ Backend com **FastAPI**  
- 🎨 Frontend com **Streamlit**

---

## ✨ Funcionalidades
- 💾 **Armazenamento Híbrido**: Estados e cidades no SQLite, locais geográficos no MongoDB  
- 🗺️ **Geoprocessamento**: Cálculo de distâncias (Haversine) e busca por locais próximos  
- 🤝 **Integração Total**: Conexão entre cidades (SQLite) e locais (MongoDB)  
- 🌐 **Visualização Interativa**: Mapa dinâmico com Streamlit  

---

## ⚙️ Tecnologias Principais
- 🐍 **Python 3.10+**  
- ⚡ **FastAPI** → Backend (APIs REST)  
- 🗄️ **SQLite3** → Banco de dados relacional  
- 🍃 **MongoDB / PyMongo** → Banco de dados NoSQL  
- 🎨 **Streamlit** → Frontend interativo  
- 📐 **Geopy / Haversine** → Cálculo de distâncias  
- 📊 **Pandas** → Manipulação de dados  
- 🗺️ **st.map** (Streamlit) → Visualização em mapas  

---

## 🗂 Estrutura do Projeto
<img width="281" height="398" alt="image" src="https://github.com/user-attachments/assets/9af33519-426a-4551-ae1a-841c4690ec73" />



---

## ⚙️ Tecnologias utilizadas
- **Python 3.10+**
- **FastAPI** → Backend (API REST)
- **SQLite3** → Banco relacional
- **MongoDB / PyMongo** → Banco NoSQL (JSON)
- **Streamlit** → Frontend interativo
- **Geopy / Haversine** → Cálculo de distâncias
- **Pandas** → Manipulação de dados
- **st.map** (Streamlit) → Visualização em mapa

---

## 🚀 Como rodar o projeto

```
### Criar ambiente virtual (Linux/macOS)
python -m venv .venv
source .venv/bin/activate

### Criar ambiente virtual (Windows PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
```
### Vá para a pasta

##🔧 Backend (FastAPI)
### Vá para a pasta
```
cd backend
```
### Instale dependências
```
pip install -r requirements.txt
```
### Crie o arquivo .env
```
MONGO_URI=mongodb://localhost:27017
SQLITE_PATH=poliglota.db
```
### Inicie o servidor
```
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
### Acesse a documentação interativa
```
http://localhost:8000/docs


```cd frontend
```
### Instale dependências
```
pip install -r requirements.txt
```
### Crie frontend/.streamlit/secrets.toml
```
API_URL = "http://localhost:8000"
```
### Inicie o Streamlit
```
streamlit run app.py
```
### Acesse no navegador
```
http://localhost:8501
```
###🍃 Opções de MongoDB

### MongoDB Local
- Instale MongoDB Community
- Windows: net start MongoDB
- Linux: sudo systemctl start mongod
- Conexão padrão: mongodb://localhost:27017

### MongoDB Atlas (Nuvem, grátis)
- Crie conta em https://www.mongodb.com/atlas/database
- Copie a string de conexão e substitua no .env
MONGO_URI=mongodb+srv://usuario:senha@cluster.mongodb.net

### Testar sem instalar Mongo (mongomock)
pip install mongomock

# Edite db_mongo.py para usar:
import mongomock
client = mongomock.MongoClient()

##🔗 Endpoints principais (FastAPI)
```
POST /estado → cadastra estado
POST /cidade → cadastra cidade
GET /cidades → lista cidades
POST /local → cadastra local (MongoDB)
GET /cidades/{id}/locais → consulta integrada (SQLite + MongoDB)
GET /locais/proximos?lat=-7.11&lon=-34.86&raio_km=5 → locais próximos
```
##🧪 Exemplos de consultas


### Cadastro de estado
```
POST /estado
{
  "nome": "Paraíba"
}
```
### Cadastro de cidade
```
POST /cidade
{
  "nome": "João Pessoa",
  "estado_id": 1
}
```
### Cadastro de local
```
POST /local
{
  "nome_local": "Praça da Independência",
  "cidade": "João Pessoa",
  "coordenadas": {
    "latitude": -7.11532,
    "longitude": -34.861
  },
  "descricao": "Ponto turístico central"
}
```
### Consultar locais de uma cidade
```
GET /cidades/1/locais
```
### Consultar locais próximos
```
GET /locais/proximos?lat=-7.11532&lon=-34.861&raio_km=5
```

### 🖼 Prints da interface

<img width="1316" height="621" alt="image" src="https://github.com/user-attachments/assets/6f8bd026-dd96-4e03-933c-bb775ee70c29" />
<img width="1332" height="629" alt="image" src="https://github.com/user-attachments/assets/5627569d-aa18-4db1-8fb7-262d3ed58cf7" />
<img width="1160" height="580" alt="image" src="https://github.com/user-attachments/assets/52ed3536-19f8-4cb5-ad36-93a0094fa16c" />
<img width="1074" height="535" alt="image" src="https://github.com/user-attachments/assets/60258b4a-a1eb-42f5-92c7-ba4b2e29fa5e" />

### ✅ Conclusão
O projeto demonstra de forma prática o conceito de persistência poliglota, combinando:
- SQLite para dados estruturados (estados e cidades).
- MongoDB para dados flexíveis (locais com coordenadas).
- Com FastAPI + Streamlit, o sistema se torna moderno, interativo e fácil de estender.

### 👨‍💻 Autores
Este projeto foi realizado por:

- Arthur Vinicius de Albuquerque Pimentel
- Guilherme Vitorio Rodrigues de Carvalho






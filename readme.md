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
projeto_persistencia_poliglota/
├── backend/
│ ├── main.py # API principal (FastAPI)
│ ├── db_sqlite.py # Conexão com SQLite
│ ├── db_mongo.py # Conexão com MongoDB
│ ├── geoprocess.py # Funções geográficas
│ ├── models.py # Modelos (Pydantic)
│ ├── requirements.txt
│ └── .env.example # Exemplo de variáveis de ambiente
└── frontend/
├── app.py # Frontend (Streamlit)
├── requirements.txt
└── .streamlit/
└── secrets.toml.example
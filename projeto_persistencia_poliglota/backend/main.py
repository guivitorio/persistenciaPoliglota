"""
main.py
App FastAPI — serve como backend / API para o frontend Streamlit.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import db_sqlite as sqlite_db
import db_mongo as mongo_db
import geoprocess as gp
from models import EstadoIn, CidadeIn, LocalIn
import uvicorn
import os

app = FastAPI(title="API - Persistência Poliglota")

# CORS: permitindo todas origens aqui para facilitar desenvolvimento.
# Em produção limite apenas aos origins necessários.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# inicializa DB sqlite ao subir a aplicação
sqlite_db.init_db()

@app.post("/estado")
def criar_estado(payload: EstadoIn):
    """Cria / garante existência de um estado e retorna o id."""
    estado_id = sqlite_db.add_estado(payload.nome)
    return {"estado_id": estado_id, "nome": payload.nome}

@app.post("/cidade")
def criar_cidade(payload: CidadeIn):
    """Cria uma cidade associada a um estado (estado_id deve existir)."""
    # NOTA: aqui não validamos se estado_id existe; em produção validar.
    cid = sqlite_db.add_cidade(payload.nome, payload.estado_id)
    return {"cidade_id": cid, "nome": payload.nome, "estado_id": payload.estado_id}

@app.get("/cidades")
def listar_cidades():
    """Retorna as cidades com o nome do estado."""
    return sqlite_db.list_cidades()

@app.post("/local")
def criar_local(payload: LocalIn):
    """Insere um local no MongoDB."""
    local_doc = {
        "nome_local": payload.nome_local,
        "cidade": payload.cidade,
        "coordenadas": payload.coordenadas,
        "descricao": payload.descricao
    }
    id_local = mongo_db.insert_local(local_doc)
    return {"id": id_local}

@app.get("/locais")
def listar_locais(cidade: str = None):
    """Lista locais; se query param 'cidade' for fornecido, filtra por cidade."""
    if cidade:
        docs = mongo_db.find_by_city(cidade)
    else:
        docs = mongo_db.find_all()
    return docs

@app.get("/locais/proximos")
def locais_proximos(lat: float, lon: float, raio_km: float = 10.0):
    """
    Endpoint que retorna locais próximos a uma coordenada.
    Ex: /locais/proximos?lat=-7.1&lon=-34.86&raio_km=5
    """
    todos = mongo_db.find_all()
    proximos = gp.locais_proximos(lat, lon, todos, raio_km)
    return proximos

@app.get("/cidades/{cidade_id}/locais")
def locais_por_cidade(cidade_id: int):
    """
    Consulta integrada:
    Busca a cidade no SQLite pelo id e retorna os locais do Mongo relacionados.
    """
    cidade = sqlite_db.get_cidade_by_id(cidade_id)
    if not cidade:
        raise HTTPException(status_code=404, detail="Cidade não encontrada")

    locais = mongo_db.find_by_city(cidade["nome"])
    return {
        "cidade": cidade["nome"],
        "estado_id": cidade["estado_id"],
        "locais": locais
    }


if __name__ == "__main__":
    # Permite executar python main.py diretamente para desenvolvimento.
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

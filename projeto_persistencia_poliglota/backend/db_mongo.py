"""
db_mongo.py
Conexão com MongoDB e funções básicas para manipular a coleção `locais`.
"""

import os
from pymongo import MongoClient
from typing import Dict, List

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")

# cliente global (reaproveitado entre requisições)
client = MongoClient(MONGO_URI)
db = client["poliglota_db"]
collection = db["locais"]

def insert_local(local: Dict) -> str:
    """
    Insere documento do tipo:
    {
      "nome_local": "...",
      "cidade": "...",
      "coordenadas": {"latitude": -7.11, "longitude": -34.86},
      "descricao": "..."
    }
    Retorna string do ObjectId inserido.
    """
    res = collection.insert_one(local)
    return str(res.inserted_id)

def find_by_city(cidade: str) -> List[Dict]:
    """
    Busca locais por campo 'cidade'. Converte _id para string para JSON serializável.
    """
    docs = list(collection.find({"cidade": cidade}))
    for d in docs:
        d["_id"] = str(d["_id"])
    return docs

def find_all() -> List[Dict]:
    """
    Retorna todos documentos (útil para endpoints que filtram no backend).
    """
    docs = list(collection.find({}))
    for d in docs:
        d["_id"] = str(d["_id"])
    return docs

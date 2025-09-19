"""
models.py
Modelos Pydantic para validação de payloads nas rotas do FastAPI.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict

class EstadoIn(BaseModel):
    nome: str

class CidadeIn(BaseModel):
    nome: str
    estado_id: int

class LocalIn(BaseModel):
    nome_local: str
    cidade: str
    coordenadas: Dict[str, float] = Field(..., example={"latitude": -7.11532, "longitude": -34.861})
    descricao: Optional[str] = None

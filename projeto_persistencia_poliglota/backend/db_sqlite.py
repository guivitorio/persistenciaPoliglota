"""
db_sqlite.py
Funções de conexão e operações básicas com SQLite.
"""

import sqlite3
from typing import List, Dict
import os

# caminho do banco (pode ser substituído por variável de ambiente)
DB_PATH = os.environ.get("SQLITE_PATH", "poliglota.db")

def get_conn():
    """
    Retorna uma conexão com sqlite. check_same_thread=False permite
    acesso a partir de threads diferentes (uvicorn/fastapi usa threads/async).
    """
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    # row_factory permite acessar colunas por nome (row["nome"])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Cria as tabelas necessárias se não existirem:
    - estados (id, nome)
    - cidades (id, nome, estado_id)
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS estados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS cidades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        estado_id INTEGER,
        FOREIGN KEY(estado_id) REFERENCES estados(id)
    )
    """)
    conn.commit()
    conn.close()

def add_estado(nome: str) -> int:
    """
    Insere um estado (ou ignora se já existir) e retorna o id.
    """
    conn = get_conn()
    cur = conn.cursor()
    # INSERT OR IGNORE evita erro se nome já existir
    cur.execute("INSERT OR IGNORE INTO estados(nome) VALUES (?)", (nome,))
    conn.commit()
    cur.execute("SELECT id FROM estados WHERE nome = ?", (nome,))
    row = cur.fetchone()
    conn.close()
    return row["id"]

def add_cidade(nome: str, estado_id: int) -> int:
    """
    Insere uma cidade ligada a um estado e retorna o id criado.
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO cidades(nome, estado_id) VALUES (?, ?)", (nome, estado_id))
    conn.commit()
    cid = cur.lastrowid
    conn.close()
    return cid

def list_cidades() -> List[Dict]:
    """
    Retorna lista de cidades com o nome do estado associado.
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    SELECT c.id, c.nome as cidade, e.nome as estado
    FROM cidades c LEFT JOIN estados e ON c.estado_id = e.id
    """)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

def get_cidade_by_name(nome: str):
    """
    Busca a cidade pelo nome; retorna dict ou None.
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM cidades WHERE nome = ?", (nome,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def get_cidade_by_id(cid: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM cidades WHERE id = ?", (cid,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

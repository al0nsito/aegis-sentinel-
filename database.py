# database.py
import sqlite3
import json

DB_NAME = "aegis_sentinel.db"

def init_db():
    """Cria a tabela no SQLite caso não exista."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dispositivos (
            token TEXT PRIMARY KEY,
            nome TEXT NOT NULL,
            tipo TEXT NOT NULL,
            origem TEXT NOT NULL,
            status TEXT NOT NULL,
            caracteristicas_extra TEXT
        )
    ''')
    conn.commit()
    conn.close()

def salvar_dispositivo(token, nome, tipo, origem, status="Ativo", extras=None):
    """Salva ou atualiza um dispositivo no banco."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO dispositivos (token, nome, tipo, origem, status, caracteristicas_extra)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (token, nome, tipo, origem, status, json.dumps(extras or {}, ensure_ascii=False)))
    conn.commit()
    conn.close()

def carregar_dispositivos():
    """Carrega as câmeras salvas do banco de dados."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT token, nome, tipo, origem, status, caracteristicas_extra FROM dispositivos")
    rows = cursor.fetchall()
    conn.close()
    
    dispositivos = {}
    for row in rows:
        token, nome, tipo, origem, status, extras_str = row
        try:
            extras = json.loads(extras_str) if extras_str else {}
        except Exception:
            extras = {}
            
        dispositivos[token] = {
            "nome": nome, "tipo": tipo, "origem": origem, 
            "status": status, "extras": extras
        }
    return dispositivos

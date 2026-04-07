from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import sqlite3
import math
from datetime import datetime

# ─────────────────────────────────────────────
# Criação da instância FastAPI
# ─────────────────────────────────────────────
app = FastAPI(
    title="Calculadora API",
    description="API de Calculadora para Sistemas Distribuídos — Nível Intermediário",
    version="2.0.0",
)

# ─────────────────────────────────────────────
# CORS — permite que o frontend consuma a API
# ─────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────
# Banco de dados SQLite — inicialização
# ─────────────────────────────────────────────
DB_PATH = "calculadora.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historico (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario   TEXT    NOT NULL,
            operacao  TEXT    NOT NULL,
            numero1   REAL    NOT NULL,
            numero2   REAL,
            resultado REAL    NOT NULL,
            data_hora TEXT    NOT NULL
        )
    """)
    conn.commit()
    conn.close()


init_db()

# ─────────────────────────────────────────────
# Modelos Pydantic
# ─────────────────────────────────────────────

class OperacaoRequest(BaseModel):
    numero1: float
    numero2: float
    usuario: str = "anonimo"


class OperacaoUnariaRequest(BaseModel):
    numero1: float
    usuario: str = "anonimo"


class ResultadoResponse(BaseModel):
    operacao: str
    numero1: float
    numero2: Optional[float] = None
    resultado: float
    usuario: str
    data_hora: str


# ─────────────────────────────────────────────
# Função auxiliar — salvar no histórico
# ─────────────────────────────────────────────

def salvar_historico(conn, usuario, operacao, numero1, resultado, numero2=None):
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute(
        """INSERT INTO historico (usuario, operacao, numero1, numero2, resultado, data_hora)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (usuario, operacao, numero1, numero2, resultado, data_hora),
    )
    conn.commit()
    return data_hora


# ─────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────

@app.get("/")
def raiz():
    return {
        "mensagem": "Bem-vindo à Calculadora API v2.0!",
        "docs": "/docs",
        "versao": "2.0.0",
    }


# ── Soma ──────────────────────────────────────
@app.post("/somar", response_model=ResultadoResponse)
def somar(dados: OperacaoRequest, conn=Depends(get_db)):
    resultado = dados.numero1 + dados.numero2
    data_hora = salvar_historico(conn, dados.usuario, "soma", dados.numero1, resultado, dados.numero2)
    return ResultadoResponse(
        operacao="soma",
        numero1=dados.numero1,
        numero2=dados.numero2,
        resultado=resultado,
        usuario=dados.usuario,
        data_hora=data_hora,
    )


# ── Subtração ─────────────────────────────────
@app.post("/subtrair", response_model=ResultadoResponse)
def subtrair(dados: OperacaoRequest, conn=Depends(get_db)):
    resultado = dados.numero1 - dados.numero2
    data_hora = salvar_historico(conn, dados.usuario, "subtracao", dados.numero1, resultado, dados.numero2)
    return ResultadoResponse(
        operacao="subtracao",
        numero1=dados.numero1,
        numero2=dados.numero2,
        resultado=resultado,
        usuario=dados.usuario,
        data_hora=data_hora,
    )


# ── Multiplicação ─────────────────────────────
@app.post("/multiplicar", response_model=ResultadoResponse)
def multiplicar(dados: OperacaoRequest, conn=Depends(get_db)):
    resultado = dados.numero1 * dados.numero2
    data_hora = salvar_historico(conn, dados.usuario, "multiplicacao", dados.numero1, resultado, dados.numero2)
    return ResultadoResponse(
        operacao="multiplicacao",
        numero1=dados.numero1,
        numero2=dados.numero2,
        resultado=resultado,
        usuario=dados.usuario,
        data_hora=data_hora,
    )


# ── Divisão ───────────────────────────────────
@app.post("/dividir", response_model=ResultadoResponse)
def dividir(dados: OperacaoRequest, conn=Depends(get_db)):
    if dados.numero2 == 0:
        raise HTTPException(status_code=400, detail="Divisão por zero não é permitida!")
    resultado = dados.numero1 / dados.numero2
    data_hora = salvar_historico(conn, dados.usuario, "divisao", dados.numero1, resultado, dados.numero2)
    return ResultadoResponse(
        operacao="divisao",
        numero1=dados.numero1,
        numero2=dados.numero2,
        resultado=resultado,
        usuario=dados.usuario,
        data_hora=data_hora,
    )


# ── Potência ──────────────────────────────────
@app.post("/potencia", response_model=ResultadoResponse)
def potencia(dados: OperacaoRequest, conn=Depends(get_db)):
    resultado = dados.numero1 ** dados.numero2
    data_hora = salvar_historico(conn, dados.usuario, "potencia", dados.numero1, resultado, dados.numero2)
    return ResultadoResponse(
        operacao="potencia",
        numero1=dados.numero1,
        numero2=dados.numero2,
        resultado=resultado,
        usuario=dados.usuario,
        data_hora=data_hora,
    )


# ── Raiz Quadrada ─────────────────────────────
@app.post("/raiz", response_model=ResultadoResponse)
def raiz_quadrada(dados: OperacaoUnariaRequest, conn=Depends(get_db)):
    if dados.numero1 < 0:
        raise HTTPException(status_code=400, detail="Não é possível calcular a raiz quadrada de um número negativo!")
    resultado = math.sqrt(dados.numero1)
    data_hora = salvar_historico(conn, dados.usuario, "raiz_quadrada", dados.numero1, resultado)
    return ResultadoResponse(
        operacao="raiz_quadrada",
        numero1=dados.numero1,
        resultado=resultado,
        usuario=dados.usuario,
        data_hora=data_hora,
    )


# ── Query Parameters ──────────────────────────
@app.get("/calcular")
def calcular_query(numero1: float, numero2: float, operacao: str, usuario: str = "anonimo", conn=Depends(get_db)):
    operacoes = {
        "soma":          lambda a, b: a + b,
        "subtracao":     lambda a, b: a - b,
        "multiplicacao": lambda a, b: a * b,
        "divisao":       lambda a, b: a / b,
        "potencia":      lambda a, b: a ** b,
    }
    if operacao not in operacoes:
        raise HTTPException(status_code=400, detail=f"Operação inválida. Use: {list(operacoes.keys())}")
    if operacao == "divisao" and numero2 == 0:
        raise HTTPException(status_code=400, detail="Divisão por zero!")
    resultado = operacoes[operacao](numero1, numero2)
    data_hora = salvar_historico(conn, usuario, operacao, numero1, resultado, numero2)
    return {
        "operacao": operacao,
        "numero1": numero1,
        "numero2": numero2,
        "resultado": resultado,
        "usuario": usuario,
        "data_hora": data_hora,
    }


# ── Histórico por usuário ─────────────────────
@app.get("/historico/{usuario}")
def historico_usuario(usuario: str, conn=Depends(get_db)):
    rows = conn.execute(
        "SELECT * FROM historico WHERE usuario = ? ORDER BY id DESC",
        (usuario,),
    ).fetchall()
    if not rows:
        raise HTTPException(status_code=404, detail=f"Nenhum histórico encontrado para o usuário '{usuario}'.")
    return {"usuario": usuario, "total": len(rows), "historico": [dict(r) for r in rows]}


# ── Todos os históricos ───────────────────────
@app.get("/historico")
def historico_geral(conn=Depends(get_db)):
    rows = conn.execute("SELECT * FROM historico ORDER BY id DESC").fetchall()
    return {"total": len(rows), "historico": [dict(r) for r in rows]}

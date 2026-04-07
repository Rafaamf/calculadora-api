# 🧮 Calculadora API

> Projeto Avaliativo desenvolvido para disciplina Programação de Sistemas Distribuídos da Universidade do Grandes Lagos - UNILAGO sob supervisão do Professor Gleydes Oliveira — [@gleydes](https://github.com/gleydes)

API RESTful de calculadora construída com **FastAPI**, **SQLite** e frontend em **HTML + JavaScript puro**, desenvolvida como projeto avaliativo da disciplina de Sistemas Distribuídos.

---

## 👥 Integrantes

| Nome | RA |
|------|----|
| Gabriel Henrique Mendes Angelo Alvarenga | — |
| Rafael Martins Fernandes | — |

---

## ✨ Funcionalidades

- ➕ Soma, ➖ Subtração, ✖️ Multiplicação, ➗ Divisão
- 🔢 Potência e √ Raiz Quadrada
- 📋 Histórico de cálculos por usuário (SQLite)
- 🌐 CORS habilitado para consumo pelo frontend
- 📄 Documentação automática via Swagger UI
- 🖥️ Frontend responsivo em HTML + JS puro

---

## 🛠️ Tecnologias

| Tecnologia | Uso |
|------------|-----|
| Python 3.8+ | Linguagem principal |
| FastAPI 0.115 | Framework da API |
| Uvicorn 0.30 | Servidor ASGI |
| Pydantic 2.9 | Validação de dados |
| SQLite | Banco de dados local |
| HTML + JS | Frontend |

---

## 📁 Estrutura do Projeto

```
calculadora-api/
├── main.py              # API principal
├── requirements.txt     # Dependências
├── test_client.py       # Script de testes em Python
├── calculadora.db       # Banco SQLite (gerado automaticamente)
├── frontend/
│   └── index.html       # Interface web
└── README.md
```

> ⚠️ A pasta `venv/` **não** deve ser commitada. Adicione-a ao `.gitignore`.

---

## 🚀 Como Executar

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/calculadora-api.git
cd calculadora-api
```

### 2. Crie e ative o ambiente virtual

```bash
# Criar
python -m venv venv

# Ativar — Linux/macOS
source venv/bin/activate

# Ativar — Windows
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Inicie o servidor

```bash
uvicorn main:app --reload
```

### 5. Acesse

| URL | Descrição |
|-----|-----------|
| http://localhost:8000 | Mensagem de boas-vindas |
| http://localhost:8000/docs | Swagger UI (documentação interativa) |
| http://localhost:8000/redoc | ReDoc |
| `frontend/index.html` | Abra no navegador (arquivo local) |

---

## 📡 Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Boas-vindas |
| POST | `/somar` | Soma dois números |
| POST | `/subtrair` | Subtrai dois números |
| POST | `/multiplicar` | Multiplica dois números |
| POST | `/dividir` | Divide (valida divisão por zero) |
| POST | `/potencia` | Calcula a potência |
| POST | `/raiz` | Calcula a raiz quadrada |
| GET | `/calcular` | Operação via query parameters |
| GET | `/historico/{usuario}` | Histórico por usuário |
| GET | `/historico` | Todo o histórico |

### Exemplo de requisição

```bash
curl -X POST "http://localhost:8000/somar" \
     -H "Content-Type: application/json" \
     -d '{"numero1": 10, "numero2": 5, "usuario": "gabriel"}'
```

```json
{
  "operacao": "soma",
  "numero1": 10.0,
  "numero2": 5.0,
  "resultado": 15.0,
  "usuario": "gabriel",
  "data_hora": "2026-03-24 10:30:00"
}
```

---

## 🧪 Executar testes Python

Com o servidor rodando em outro terminal:

```bash
python test_client.py
```

---

## 📋 Códigos de Status HTTP

| Código | Significado |
|--------|-------------|
| 200 | Sucesso |
| 400 | Dado inválido (ex: divisão por zero) |
| 404 | Recurso não encontrado |
| 422 | Falha na validação Pydantic |
| 500 | Erro interno do servidor |

---

## 📚 Disciplina

**Programação de Sistemas Distribuídos** — UNILAGO  
Professor: Eng. Gleydes Oliveira

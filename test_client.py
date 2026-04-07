import urllib.request, json

BASE_URL = "http://localhost:8000"
USUARIO = "gabriel"


def post(endpoint, dados):
    req = urllib.request.Request(
        f"{BASE_URL}{endpoint}",
        data=json.dumps(dados).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())


def get(path):
    with urllib.request.urlopen(f"{BASE_URL}{path}") as r:
        return json.loads(r.read())


print("=" * 40)
print("  TESTES — Calculadora API v2.0")
print("=" * 40)

r = post("/somar",        {"numero1": 10, "numero2": 5,  "usuario": USUARIO})
print(f"Soma:           {r['resultado']}")  # 15.0

r = post("/subtrair",     {"numero1": 10, "numero2": 3,  "usuario": USUARIO})
print(f"Subtração:      {r['resultado']}")  # 7.0

r = post("/multiplicar",  {"numero1": 4,  "numero2": 5,  "usuario": USUARIO})
print(f"Multiplicação:  {r['resultado']}")  # 20.0

r = post("/dividir",      {"numero1": 10, "numero2": 2,  "usuario": USUARIO})
print(f"Divisão:        {r['resultado']}")  # 5.0

r = post("/potencia",     {"numero1": 2,  "numero2": 10, "usuario": USUARIO})
print(f"Potência:       {r['resultado']}")  # 1024.0

r = post("/raiz",         {"numero1": 144,               "usuario": USUARIO})
print(f"Raiz Quadrada:  {r['resultado']}")  # 12.0

print()
h = get(f"/historico/{USUARIO}")
print(f"Histórico de '{USUARIO}': {h['total']} registro(s)")
for item in h["historico"]:
    print(f"  [{item['data_hora']}] {item['operacao']}: resultado = {item['resultado']}")

import json
import os
from datetime import datetime

from Produto import Produto

ARQUIVO_DADOS = "dados.json"
ARQUIVO_LOG = "operacoes.log"


def salvar_dados(produtos: list[Produto]) -> None:
    dados = [p.to_dict() for p in produtos]
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def carregar_dados() -> list[Produto]:
    if not os.path.exists(ARQUIVO_DADOS):
        return []
    with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
        try:
            dados = json.load(f)
        except json.JSONDecodeError:
            return []
    return [Produto.from_dict(d) for d in dados]


def registrar_log(operacao: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(ARQUIVO_LOG, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {operacao}\n")
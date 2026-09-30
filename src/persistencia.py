"""Leitura e gravacao dos dados em arquivo JSON.

Este modulo so cuida de arquivo + JSON. Ele nao conhece as regras do
dominio: recebe/entrega um `dict` simples. Quem sabe traduzir esse dict
em objetos e o `SistemaProducao` (ver `src.sistema`).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

CAMINHO_PADRAO = Path("dados.json")


def carregar(caminho: Path = CAMINHO_PADRAO) -> dict[str, Any]:
    """Le o JSON e devolve o dict. Devolve {} se o arquivo nao existir
    ou estiver ilegivel, para o programa comecar do zero sem quebrar."""
    if not caminho.exists():
        return {}
    try:
        return json.loads(caminho.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        print(f"[aviso] nao foi possivel ler '{caminho}'; iniciando vazio.")
        return {}


def salvar(dados: dict[str, Any], caminho: Path = CAMINHO_PADRAO) -> None:
    """Grava o dict como JSON formatado, preservando acentos."""
    caminho.write_text(
        json.dumps(dados, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

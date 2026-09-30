"""Distribuicao das pecas aprovadas em caixas de capacidade fixa.

Regra do desafio: cada caixa comporta no maximo 10 pecas; ao encher, e
fechada e uma nova comeca.

As caixas NAO sao persistidas. Sao sempre reconstruidas a partir da lista
de pecas aprovadas, na ordem de cadastro. Assim, remover uma peca
reorganiza tudo automaticamente, sem risco de numeracao furada.
"""

from __future__ import annotations

from collections.abc import Iterable

from src.modelos import Caixa, Peca


def montar_caixas(pecas: Iterable[Peca]) -> list[Caixa]:
    """Constroi as caixas a partir das pecas aprovadas."""
    aprovadas = [p for p in pecas if p.aprovada]

    caixas: list[Caixa] = []
    for indice, peca in enumerate(aprovadas):
        if indice % Caixa.CAPACIDADE == 0:
            caixas.append(Caixa(numero=len(caixas) + 1))
        caixas[-1].adicionar(peca)
    return caixas


def caixas_fechadas(pecas: Iterable[Peca]) -> list[Caixa]:
    """Somente as caixas que ja atingiram a capacidade maxima."""
    return [caixa for caixa in montar_caixas(pecas) if caixa.fechada]


def caixa_aberta(pecas: Iterable[Peca]) -> Caixa | None:
    """A caixa em preenchimento, se houver (a ultima, quando nao esta cheia)."""
    caixas = montar_caixas(pecas)
    if caixas and not caixas[-1].fechada:
        return caixas[-1]
    return None


def total_caixas(pecas: Iterable[Peca]) -> int:
    """Quantidade de caixas utilizadas (fechadas + a aberta, se houver)."""
    return len(montar_caixas(pecas))

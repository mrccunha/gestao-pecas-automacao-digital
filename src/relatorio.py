"""Geracao do relatorio consolidado.

So LE o `SistemaProducao` e devolve texto pronto para o terminal.
Nenhuma funcao aqui altera o estado.
"""

from __future__ import annotations

from collections import Counter

from src.modelos import Caixa
from src.sistema import SistemaProducao

_LARGURA = 54


def _regua(caractere: str = "=") -> str:
    return caractere * _LARGURA


def contar_motivos(sistema: SistemaProducao) -> Counter[str]:
    """Quantas vezes cada motivo de reprovacao apareceu."""
    contador: Counter[str] = Counter()
    for peca in sistema.reprovadas:
        contador.update(peca.motivos)
    return contador


def gerar(sistema: SistemaProducao) -> str:
    """Monta o texto do relatorio final."""
    aprovadas = sistema.aprovadas
    reprovadas = sistema.reprovadas
    caixas = sistema.caixas
    fechadas = [c for c in caixas if c.fechada]
    aberta = next((c for c in caixas if not c.fechada), None)

    linhas: list[str] = [
        _regua(),
        "RELATORIO FINAL - CONTROLE DE PRODUCAO E QUALIDADE",
        _regua(),
        f"Total de pecas cadastradas : {len(sistema.pecas)}",
        f"Total de pecas APROVADAS   : {len(aprovadas)}",
        f"Total de pecas REPROVADAS  : {len(reprovadas)}",
        "",
        "Motivos das reprovacoes:",
    ]

    if reprovadas:
        for motivo, qtd in contar_motivos(sistema).most_common():
            linhas.append(f"  - {motivo}: {qtd} ocorrencia(s)")
        linhas.append("")
        linhas.append("Detalhamento das pecas reprovadas:")
        for peca in reprovadas:
            linhas.append(f"  - Peca #{peca.id}: {'; '.join(peca.motivos)}")
    else:
        linhas.append("  (nenhuma peca reprovada)")

    linhas.append("")
    linhas.append(f"Caixas utilizadas no total : {len(caixas)}")
    linhas.append(f"Caixas fechadas (cheias)   : {len(fechadas)}")
    if aberta is not None:
        linhas.append(
            f"Caixa aberta               : caixa {aberta.numero} com "
            f"{len(aberta.pecas)}/{Caixa.CAPACIDADE} pecas"
        )
    else:
        linhas.append("Caixa aberta               : nenhuma")
    linhas.append(_regua())

    return "\n".join(linhas)

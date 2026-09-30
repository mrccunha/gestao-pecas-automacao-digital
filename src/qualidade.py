"""Regras de qualidade da linha de montagem.

Uma peca so e aprovada quando atende, ao mesmo tempo, aos tres criterios:
    - peso entre 95g e 105g (limites inclusive);
    - cor azul ou verde;
    - comprimento entre 10cm e 20cm (limites inclusive).

Todo o conhecimento sobre "o que e uma peca boa" fica concentrado aqui.
Se a engenharia mudar um limite, so este arquivo muda.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from src.modelos import Peca

# --- Parametros de qualidade (constantes tipadas) --------------------------
PESO_MINIMO: float = 95.0
PESO_MAXIMO: float = 105.0

COMPRIMENTO_MINIMO: float = 10.0
COMPRIMENTO_MAXIMO: float = 20.0

CORES_ACEITAS: frozenset[str] = frozenset({"azul", "verde"})


@dataclass
class ResultadoAvaliacao:
    """Resultado da inspecao de uma peca."""

    aprovada: bool
    motivos: list[str] = field(default_factory=list)


def _normalizar_cor(cor: str) -> str:
    return cor.strip().lower()


def avaliar(peca: Peca) -> ResultadoAvaliacao:
    """Aplica os tres criterios e devolve o resultado.

    Registra *todos* os motivos de reprovacao, nao apenas o primeiro: no
    chao de fabrica interessa ver tudo o que esta fora do padrao de uma vez.
    """
    motivos: list[str] = []

    if not (PESO_MINIMO <= peca.peso <= PESO_MAXIMO):
        motivos.append(
            f"peso fora do padrao ({peca.peso:g}g; esperado entre "
            f"{PESO_MINIMO:g}g e {PESO_MAXIMO:g}g)"
        )

    if _normalizar_cor(peca.cor) not in CORES_ACEITAS:
        motivos.append(
            f"cor fora do padrao ('{peca.cor}'; esperado azul ou verde)"
        )

    if not (COMPRIMENTO_MINIMO <= peca.comprimento <= COMPRIMENTO_MAXIMO):
        motivos.append(
            f"comprimento fora do padrao ({peca.comprimento:g}cm; esperado "
            f"entre {COMPRIMENTO_MINIMO:g}cm e {COMPRIMENTO_MAXIMO:g}cm)"
        )

    return ResultadoAvaliacao(aprovada=not motivos, motivos=motivos)

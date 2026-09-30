"""Entidades do dominio.

Uso `@dataclass` para ter algo parecido com uma `class` enxuta de TypeScript:
campos tipados, construtor automatico e igualdade por valor (util nos testes).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, ClassVar


@dataclass
class Peca:
    """Uma peca produzida na linha de montagem.

    `aprovada` e `motivos` sao preenchidos pela avaliacao de qualidade
    (ver `src.qualidade`). Quando a peca e aprovada, `motivos` fica vazio.
    """

    id: int
    peso: float
    cor: str
    comprimento: float
    aprovada: bool = False
    motivos: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, dados: dict[str, Any]) -> Peca:
        return cls(
            id=int(dados["id"]),
            peso=float(dados["peso"]),
            cor=str(dados["cor"]),
            comprimento=float(dados["comprimento"]),
            aprovada=bool(dados.get("aprovada", False)),
            motivos=list(dados.get("motivos", [])),
        )


@dataclass
class Caixa:
    """Caixa que agrupa pecas aprovadas.

    A capacidade e fixa (regra do desafio: 10 pecas por caixa). `fechada`
    e derivado da quantidade de pecas, entao nunca fica inconsistente.
    """

    CAPACIDADE: ClassVar[int] = 10

    numero: int
    pecas: list[Peca] = field(default_factory=list)

    @property
    def fechada(self) -> bool:
        return len(self.pecas) >= self.CAPACIDADE

    @property
    def vagas(self) -> int:
        return max(0, self.CAPACIDADE - len(self.pecas))

    def adicionar(self, peca: Peca) -> None:
        if self.fechada:
            raise ValueError(f"caixa {self.numero} ja esta cheia")
        self.pecas.append(peca)

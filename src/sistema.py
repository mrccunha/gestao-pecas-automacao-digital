"""SistemaProducao: fachada do dominio.

Concentra o estado (lista de pecas + proximo id) e as operacoes de negocio.
A CLI e os testes falam so com esta classe; nao mexem nas listas por fora.
Estilo parecido com um "service" / store: consultas via @property, mudancas
via metodos de comando.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src import armazenamento, persistencia, qualidade
from src.modelos import Caixa, Peca


class SistemaProducao:
    def __init__(
        self,
        pecas: list[Peca] | None = None,
        proximo_id: int = 1,
    ) -> None:
        self._pecas: list[Peca] = list(pecas) if pecas else []
        self._proximo_id: int = proximo_id

    # ------------------------------------------------------------------ #
    # Consultas
    # ------------------------------------------------------------------ #
    @property
    def pecas(self) -> list[Peca]:
        return list(self._pecas)  # copia: ninguem altera o estado por fora

    @property
    def aprovadas(self) -> list[Peca]:
        return [p for p in self._pecas if p.aprovada]

    @property
    def reprovadas(self) -> list[Peca]:
        return [p for p in self._pecas if not p.aprovada]

    @property
    def caixas(self) -> list[Caixa]:
        return armazenamento.montar_caixas(self._pecas)

    def buscar(self, peca_id: int) -> Peca | None:
        return next((p for p in self._pecas if p.id == peca_id), None)

    # ------------------------------------------------------------------ #
    # Comandos (alteram o estado)
    # ------------------------------------------------------------------ #
    def cadastrar(self, peso: float, cor: str, comprimento: float) -> Peca:
        """Cria a peca, avalia a qualidade e guarda no estado."""
        peca = Peca(
            id=self._proximo_id,
            peso=peso,
            cor=cor.strip().lower(),
            comprimento=comprimento,
        )
        resultado = qualidade.avaliar(peca)
        peca.aprovada = resultado.aprovada
        peca.motivos = resultado.motivos

        self._pecas.append(peca)
        self._proximo_id += 1
        return peca

    def remover(self, peca_id: int) -> bool:
        """Remove a peca pelo id. Retorna True se removeu, False se nao achou."""
        peca = self.buscar(peca_id)
        if peca is None:
            return False
        self._pecas.remove(peca)
        return True

    # ------------------------------------------------------------------ #
    # Serializacao / persistencia
    # ------------------------------------------------------------------ #
    def to_dict(self) -> dict[str, Any]:
        return {
            "proximo_id": self._proximo_id,
            "pecas": [p.to_dict() for p in self._pecas],
        }

    @classmethod
    def from_dict(cls, dados: dict[str, Any]) -> SistemaProducao:
        pecas = [Peca.from_dict(d) for d in dados.get("pecas", [])]
        proximo_id = int(dados.get("proximo_id", len(pecas) + 1))
        return cls(pecas=pecas, proximo_id=proximo_id)

    def salvar(self, caminho: Path = persistencia.CAMINHO_PADRAO) -> None:
        persistencia.salvar(self.to_dict(), caminho)

    @classmethod
    def carregar(
        cls, caminho: Path = persistencia.CAMINHO_PADRAO
    ) -> SistemaProducao:
        return cls.from_dict(persistencia.carregar(caminho))

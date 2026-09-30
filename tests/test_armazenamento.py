"""Testes da distribuicao das pecas aprovadas em caixas de 10."""

from src.armazenamento import (
    caixa_aberta,
    caixas_fechadas,
    montar_caixas,
    total_caixas,
)
from src.modelos import Caixa, Peca


def pecas_aprovadas(quantidade: int) -> list[Peca]:
    return [
        Peca(id=i, peso=100.0, cor="azul", comprimento=15.0, aprovada=True)
        for i in range(1, quantidade + 1)
    ]


def test_sem_pecas_nao_gera_caixa():
    assert montar_caixas([]) == []
    assert total_caixas([]) == 0
    assert caixa_aberta([]) is None


def test_pecas_reprovadas_nao_entram_em_caixa():
    reprovadas = [
        Peca(id=1, peso=80.0, cor="rosa", comprimento=5.0, aprovada=False)
    ]
    assert montar_caixas(reprovadas) == []


def test_dez_aprovadas_fecham_exatamente_uma_caixa():
    caixas = montar_caixas(pecas_aprovadas(10))
    assert len(caixas) == 1
    assert caixas[0].fechada is True
    assert caixas[0].vagas == 0
    assert caixa_aberta(pecas_aprovadas(10)) is None


def test_onze_aprovadas_geram_uma_fechada_e_uma_aberta():
    pecas = pecas_aprovadas(11)
    caixas = montar_caixas(pecas)

    assert len(caixas) == 2
    assert caixas[0].fechada is True
    assert caixas[1].fechada is False
    assert len(caixas[1].pecas) == 1

    assert len(caixas_fechadas(pecas)) == 1
    aberta = caixa_aberta(pecas)
    assert aberta is not None and aberta.numero == 2


def test_numeracao_das_caixas_e_sequencial():
    caixas = montar_caixas(pecas_aprovadas(25))
    assert [c.numero for c in caixas] == [1, 2, 3]
    assert total_caixas(pecas_aprovadas(25)) == 3


def test_caixa_cheia_recusa_nova_peca():
    caixa = Caixa(numero=1, pecas=pecas_aprovadas(Caixa.CAPACIDADE))
    try:
        caixa.adicionar(Peca(id=99, peso=100.0, cor="azul", comprimento=15.0))
    except ValueError:
        pass
    else:
        raise AssertionError("esperava ValueError ao encher caixa cheia")

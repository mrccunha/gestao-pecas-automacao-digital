"""Testes das regras de qualidade.

Cobrem: peca perfeita, cada criterio violado isoladamente, varios motivos
ao mesmo tempo, os limites exatos (fronteira) e normalizacao da cor.
"""

import pytest

from src.modelos import Peca
from src.qualidade import (
    COMPRIMENTO_MAXIMO,
    COMPRIMENTO_MINIMO,
    PESO_MAXIMO,
    PESO_MINIMO,
    avaliar,
)


def nova_peca(peso=100.0, cor="azul", comprimento=15.0) -> Peca:
    """Peca aprovada por padrao; cada teste muda so o que quer avaliar."""
    return Peca(id=1, peso=peso, cor=cor, comprimento=comprimento)


def test_peca_dentro_de_todos_os_criterios_e_aprovada():
    resultado = avaliar(nova_peca())
    assert resultado.aprovada is True
    assert resultado.motivos == []


@pytest.mark.parametrize("cor", ["azul", "verde", "AZUL", " Verde "])
def test_cores_aceitas_com_variacoes_de_caixa_e_espaco(cor):
    assert avaliar(nova_peca(cor=cor)).aprovada is True


@pytest.mark.parametrize("cor", ["vermelha", "amarelo", "azulado", ""])
def test_cor_fora_do_padrao_reprova(cor):
    resultado = avaliar(nova_peca(cor=cor))
    assert resultado.aprovada is False
    assert any("cor fora do padrao" in m for m in resultado.motivos)


@pytest.mark.parametrize("peso", [94.9, 0.1, 105.1, 200.0])
def test_peso_fora_da_faixa_reprova(peso):
    resultado = avaliar(nova_peca(peso=peso))
    assert resultado.aprovada is False
    assert any("peso fora do padrao" in m for m in resultado.motivos)


@pytest.mark.parametrize("peso", [PESO_MINIMO, PESO_MAXIMO])
def test_peso_nos_limites_exatos_e_aprovado(peso):
    assert avaliar(nova_peca(peso=peso)).aprovada is True


@pytest.mark.parametrize("comprimento", [9.9, 20.1, 0.5, 50.0])
def test_comprimento_fora_da_faixa_reprova(comprimento):
    resultado = avaliar(nova_peca(comprimento=comprimento))
    assert resultado.aprovada is False
    assert any("comprimento fora do padrao" in m for m in resultado.motivos)


@pytest.mark.parametrize("comprimento", [COMPRIMENTO_MINIMO, COMPRIMENTO_MAXIMO])
def test_comprimento_nos_limites_exatos_e_aprovado(comprimento):
    assert avaliar(nova_peca(comprimento=comprimento)).aprovada is True


def test_varios_criterios_violados_geram_varios_motivos():
    resultado = avaliar(nova_peca(peso=80.0, cor="rosa", comprimento=5.0))
    assert resultado.aprovada is False
    assert len(resultado.motivos) == 3

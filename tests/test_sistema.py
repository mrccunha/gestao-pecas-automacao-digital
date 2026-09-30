"""Testes do SistemaProducao: cadastro, remocao, caixas e persistencia."""

from src.sistema import SistemaProducao


def test_cadastrar_peca_aprovada_entra_em_aprovadas_e_incrementa_id():
    sistema = SistemaProducao()
    peca = sistema.cadastrar(peso=100.0, cor="verde", comprimento=12.0)

    assert peca.id == 1
    assert peca.aprovada is True
    assert sistema.aprovadas == [peca]
    assert sistema.reprovadas == []

    proxima = sistema.cadastrar(peso=100.0, cor="azul", comprimento=12.0)
    assert proxima.id == 2


def test_cadastrar_peca_reprovada_guarda_motivos():
    sistema = SistemaProducao()
    peca = sistema.cadastrar(peso=50.0, cor="preto", comprimento=3.0)

    assert peca.aprovada is False
    assert len(peca.motivos) == 3
    assert peca in sistema.reprovadas


def test_cor_e_normalizada_no_cadastro():
    sistema = SistemaProducao()
    peca = sistema.cadastrar(peso=100.0, cor="  AZUL ", comprimento=15.0)
    assert peca.cor == "azul"
    assert peca.aprovada is True


def test_remover_peca_existente_e_inexistente():
    sistema = SistemaProducao()
    sistema.cadastrar(peso=100.0, cor="azul", comprimento=15.0)

    assert sistema.remover(1) is True
    assert sistema.pecas == []
    assert sistema.remover(999) is False


def test_remover_peca_reorganiza_as_caixas():
    sistema = SistemaProducao()
    for _ in range(11):
        sistema.cadastrar(peso=100.0, cor="azul", comprimento=15.0)
    assert len(sistema.caixas) == 2  # 1 fechada + 1 aberta

    sistema.remover(1)
    caixas = sistema.caixas
    assert len(caixas) == 1
    assert caixas[0].fechada is True  # sobraram exatamente 10 aprovadas


def test_to_dict_e_from_dict_preservam_o_estado():
    original = SistemaProducao()
    original.cadastrar(peso=100.0, cor="azul", comprimento=15.0)      # aprovada
    original.cadastrar(peso=10.0, cor="rosa", comprimento=99.0)       # reprovada

    copia = SistemaProducao.from_dict(original.to_dict())

    assert copia.to_dict() == original.to_dict()
    assert len(copia.aprovadas) == 1
    assert len(copia.reprovadas) == 1
    # o proximo id continua de onde parou
    assert copia.cadastrar(peso=100.0, cor="azul", comprimento=15.0).id == 3


def test_carregar_de_arquivo_inexistente_comeca_vazio(tmp_path):
    caminho = tmp_path / "nao_existe.json"
    sistema = SistemaProducao.carregar(caminho)
    assert sistema.pecas == []


def test_salvar_e_carregar_em_arquivo(tmp_path):
    caminho = tmp_path / "dados.json"
    sistema = SistemaProducao()
    sistema.cadastrar(peso=100.0, cor="verde", comprimento=15.0)
    sistema.salvar(caminho)

    recarregado = SistemaProducao.carregar(caminho)
    assert recarregado.to_dict() == sistema.to_dict()

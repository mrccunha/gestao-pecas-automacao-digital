"""Menu interativo de terminal.

Camada fina: le a entrada do usuario, chama o `SistemaProducao` e mostra
o resultado. Toda decisao de negocio esta nos outros modulos.
"""

from __future__ import annotations

from collections.abc import Callable

from src import relatorio
from src.modelos import Caixa
from src.sistema import SistemaProducao

# --------------------------------------------------------------------------- #
# Leitura de entrada com validacao
# --------------------------------------------------------------------------- #
def ler_str(rotulo: str) -> str:
    while True:
        valor = input(rotulo).strip()
        if valor:
            return valor
        print("  >> valor obrigatorio.")


def ler_float(rotulo: str, minimo: float = 0.0) -> float:
    while True:
        bruto = input(rotulo).strip().replace(",", ".")
        try:
            valor = float(bruto)
        except ValueError:
            print("  >> digite um numero valido (ex: 100 ou 12.5).")
            continue
        if valor <= minimo:
            print(f"  >> o valor deve ser maior que {minimo:g}.")
            continue
        return valor


def ler_int(rotulo: str) -> int:
    while True:
        try:
            return int(input(rotulo).strip())
        except ValueError:
            print("  >> digite um numero inteiro valido.")


# --------------------------------------------------------------------------- #
# Comandos do menu
# --------------------------------------------------------------------------- #
def cmd_cadastrar(sistema: SistemaProducao) -> None:
    print("\n--- Cadastro de nova peca ---")
    peso = ler_float("Peso (g): ")
    cor = ler_str("Cor: ")
    comprimento = ler_float("Comprimento (cm): ")

    peca = sistema.cadastrar(peso, cor, comprimento)

    if peca.aprovada:
        numero = sistema.caixas[-1].numero
        print(f"\n[APROVADA] Peca #{peca.id} guardada na caixa {numero}.")
    else:
        print(f"\n[REPROVADA] Peca #{peca.id} nao atende aos criterios:")
        for motivo in peca.motivos:
            print(f"  - {motivo}")

    sistema.salvar()


def _mostrar_pecas(titulo: str, pecas: list) -> None:
    print(f"\n--- {titulo} ---")
    if not pecas:
        print("  (nenhuma)")
        return
    for p in pecas:
        print(
            f"  #{p.id:>3} | peso {p.peso:g}g | cor {p.cor} | "
            f"comprimento {p.comprimento:g}cm"
        )
        for motivo in p.motivos:
            print(f"        motivo: {motivo}")


def cmd_listar(sistema: SistemaProducao) -> None:
    _mostrar_pecas("Pecas APROVADAS", sistema.aprovadas)
    _mostrar_pecas("Pecas REPROVADAS", sistema.reprovadas)


def cmd_remover(sistema: SistemaProducao) -> None:
    if not sistema.pecas:
        print("\nNao ha pecas cadastradas para remover.")
        return

    cmd_listar(sistema)
    alvo = ler_int("\nId da peca a remover (0 para cancelar): ")
    if alvo == 0:
        print("Operacao cancelada.")
        return

    if sistema.remover(alvo):
        sistema.salvar()
        print(f"Peca #{alvo} removida. As caixas foram reorganizadas.")
    else:
        print(f"Nao existe peca com id #{alvo}.")


def cmd_caixas_fechadas(sistema: SistemaProducao) -> None:
    fechadas = [c for c in sistema.caixas if c.fechada]
    print("\n--- Caixas fechadas ---")
    if not fechadas:
        print("  (nenhuma caixa foi fechada ainda)")
        return
    for caixa in fechadas:
        ids = ", ".join(f"#{p.id}" for p in caixa.pecas)
        print(f"  Caixa {caixa.numero} (cheia - {Caixa.CAPACIDADE} pecas): {ids}")


def cmd_relatorio(sistema: SistemaProducao) -> None:
    print()
    print(relatorio.gerar(sistema))


# --------------------------------------------------------------------------- #
# Laco principal
# --------------------------------------------------------------------------- #
Comando = Callable[[SistemaProducao], None]

MENU: dict[str, tuple[str, Comando]] = {
    "1": ("Cadastrar nova peca", cmd_cadastrar),
    "2": ("Listar pecas aprovadas/reprovadas", cmd_listar),
    "3": ("Remover peca cadastrada", cmd_remover),
    "4": ("Listar caixas fechadas", cmd_caixas_fechadas),
    "5": ("Gerar relatorio final", cmd_relatorio),
}


def _exibir_menu() -> None:
    print("\n" + "=" * 54)
    print(" SISTEMA DE AUTOMACAO DIGITAL - GESTAO DE PECAS")
    print("=" * 54)
    for chave, (rotulo, _) in MENU.items():
        print(f"  {chave} - {rotulo}")
    print("  0 - Sair")
    print("=" * 54)


def executar() -> None:
    sistema = SistemaProducao.carregar()
    print(f"Dados carregados: {len(sistema.pecas)} peca(s) em memoria.")

    while True:
        _exibir_menu()
        escolha = input("Escolha uma opcao: ").strip()

        if escolha == "0":
            sistema.salvar()
            print("\nDados salvos. Encerrando o sistema. Ate logo!")
            return

        item = MENU.get(escolha)
        if item is None:
            print("\nOpcao invalida. Escolha um numero de 0 a 5.")
            continue

        _, comando = item
        comando(sistema)

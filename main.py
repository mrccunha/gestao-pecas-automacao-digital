"""Ponto de entrada do sistema de automacao digital de pecas.

    python main.py

Carrega 'dados.json' (se existir), abre o menu interativo e grava as
alteracoes a cada acao.
"""

from src.cli import executar


def main() -> None:
    try:
        executar()
    except KeyboardInterrupt:
        print("\n\nInterrompido pelo usuario (Ctrl+C). Ate logo!")


if __name__ == "__main__":
    main()

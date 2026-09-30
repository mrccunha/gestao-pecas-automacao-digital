# Desafio de Automação Digital — Gestão de Peças, Qualidade e Armazenamento

Protótipo em **Python** (biblioteca padrão — nenhuma dependência para rodar)
que simula o controle de produção e qualidade de uma linha de montagem
industrial.

O sistema recebe os dados de cada peça, decide automaticamente se ela é
**aprovada** ou **reprovada**, guarda as peças aprovadas em **caixas de 10
unidades** e gera **relatórios consolidados**.

---

## 1. Critérios de qualidade

Uma peça só é **aprovada** quando atende, ao mesmo tempo, aos três critérios:

| Critério     | Faixa aceita (limites inclusive) |
|--------------|----------------------------------|
| Peso         | 95 g a 105 g                     |
| Cor          | azul **ou** verde                |
| Comprimento  | 10 cm a 20 cm                    |

Se qualquer critério for violado, a peça é **reprovada** e o sistema registra
**todos** os motivos — não só o primeiro.

---

## 2. Como funciona

1. **Cadastro** — o usuário informa `peso`, `cor` e `comprimento`. O `id` é
   gerado automaticamente (sequencial).
2. **Avaliação** — `qualidade.avaliar()` compara os dados com os critérios e
   devolve um `ResultadoAvaliacao(aprovada, motivos)`.
3. **Armazenamento** — as peças aprovadas são distribuídas em caixas na ordem
   de cadastro. Ao atingir **10 peças** a caixa é fechada e outra começa. As
   caixas são sempre **recalculadas** a partir da lista de aprovadas, então
   remover uma peça reorganiza tudo automaticamente.
4. **Persistência** — a cada ação o estado é gravado em `dados.json`; ao abrir
   o programa de novo, os dados são recarregados.
5. **Relatórios** — total de aprovadas, total de reprovadas com os motivos
   agrupados e a quantidade de caixas utilizadas.

### Arquitetura

```
.
├── main.py                 # ponto de entrada (python main.py)
├── src/
│   ├── modelos.py          # Peca e Caixa (dataclasses tipadas)
│   ├── qualidade.py        # regras de aprovação/reprovação + constantes
│   ├── armazenamento.py    # distribuição das peças em caixas de 10
│   ├── persistencia.py     # leitura/gravação do dados.json
│   ├── sistema.py          # SistemaProducao: estado + operações (fachada)
│   ├── relatorio.py        # geração do relatório consolidado
│   └── cli.py              # menu interativo de terminal
├── tests/                  # suíte pytest (36 testes)
├── pyproject.toml          # config do projeto e do pytest
├── requirements.txt        # só pytest (para os testes)
└── dados.json              # gerado em execução (fora do versionamento)
```

**Uma responsabilidade por módulo.** `SistemaProducao` é a única porta de
entrada do domínio: a CLI e os testes falam só com ela, nunca com as listas
por dentro. Consultas são `@property`; mudanças de estado são métodos de
comando (`cadastrar`, `remover`). Se a engenharia mudar um limite de
qualidade, só `src/qualidade.py` muda.

---

## 3. Como rodar

**Pré-requisito:** Python 3.10 ou superior (desenvolvido no 3.14). Nenhuma
biblioteca externa é necessária para executar.

```bash
cd "Algoritmos e Lógica de Programação"
python main.py
```

> Windows: se `python` não funcionar, use `py main.py`.
> Linux/macOS: pode ser `python3 main.py`.

Menu inicial:

```
======================================================
 SISTEMA DE AUTOMACAO DIGITAL - GESTAO DE PECAS
======================================================
  1 - Cadastrar nova peca
  2 - Listar pecas aprovadas/reprovadas
  3 - Remover peca cadastrada
  4 - Listar caixas fechadas
  5 - Gerar relatorio final
  0 - Sair
======================================================
```

---

## 4. Rodando os testes

```bash
pip install -r requirements.txt
pytest
```

Saída esperada: `36 passed`. Os testes cobrem os limites exatos dos critérios
(95/105 g, 10/20 cm), reprovação com múltiplos motivos, fechamento de caixa
aos 10, reorganização das caixas ao remover peça e o ciclo salvar/carregar.

---

## 5. Exemplos de entrada e saída

### Exemplo A — peça aprovada

```
Escolha uma opcao: 1

--- Cadastro de nova peca ---
Peso (g): 100
Cor: azul
Comprimento (cm): 15

[APROVADA] Peca #1 guardada na caixa 1.
```

### Exemplo B — peça reprovada (vários motivos)

```
Escolha uma opcao: 1

--- Cadastro de nova peca ---
Peso (g): 90
Cor: vermelha
Comprimento (cm): 5

[REPROVADA] Peca #2 nao atende aos criterios:
  - peso fora do padrao (90g; esperado entre 95g e 105g)
  - cor fora do padrao ('vermelha'; esperado azul ou verde)
  - comprimento fora do padrao (5cm; esperado entre 10cm e 20cm)
```

### Exemplo C — relatório final

```
======================================================
RELATORIO FINAL - CONTROLE DE PRODUCAO E QUALIDADE
======================================================
Total de pecas cadastradas : 12
Total de pecas APROVADAS   : 11
Total de pecas REPROVADAS  : 1

Motivos das reprovacoes:
  - cor fora do padrao ('vermelha'; esperado azul ou verde): 1 ocorrencia(s)

Detalhamento das pecas reprovadas:
  - Peca #2: cor fora do padrao ('vermelha'; esperado azul ou verde)

Caixas utilizadas no total : 2
Caixas fechadas (cheias)   : 1
Caixa aberta               : caixa 2 com 1/10 pecas
======================================================
```

### Exemplo D — caixas fechadas

```
Escolha uma opcao: 4

--- Caixas fechadas ---
  Caixa 1 (cheia - 10 pecas): #1, #3, #4, #5, #6, #7, #8, #9, #10, #11
```

---

## 6. Boas práticas aplicadas

- **Separação de responsabilidades** — um módulo, um assunto; `SistemaProducao`
  como fachada do domínio.
- **Type hints** em todo o código (o projeto veio de um dev TypeScript).
- **Constantes nomeadas** para os limites de qualidade — nada de número mágico.
- **Testes automatizados** com `pytest`, incluindo casos de fronteira.
- **Validação de entrada** — não quebra com texto onde deveria ir número;
  aceita vírgula ou ponto decimal.
- **Tratamento de erros** na leitura do arquivo e no `Ctrl+C`.
- **Dados derivados, não duplicados** — as caixas nascem da lista de aprovadas,
  então nunca ficam inconsistentes.

---

## 7. Como este protótipo evoluiria para um cenário real

Ver [PARTE_TEORICA.md](PARTE_TEORICA.md), seção 4: substituir o teclado por
**sensores** (balança, sensor de cor RGB, medidor a laser), acrescentar
**visão computacional** para detectar defeitos que não aparecem nas medidas
(trincas, rebarbas) e integrar a um **painel industrial** com banco de dados e
acionamento físico de esteira.

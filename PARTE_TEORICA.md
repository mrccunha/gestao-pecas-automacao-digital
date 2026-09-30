# Parte Teórica — Análise e Discussão

**Aluno:** Mauro Cunha
**Curso:** Tecnologia em Inteligência Artificial e Automação Digital — UniFECAF
**Disciplina:** Algoritmos e Lógica de Programação

---

## 1. Contextualização do desafio: por que a automação é importante na indústria

A inspeção manual de peças em uma linha de montagem é um gargalo clássico. Um
operador precisa medir peso, conferir cor e medir comprimento de cada peça,
anotar o resultado e separar aprovadas de reprovadas. É lento, cansativo e
sujeito a erro humano: quanto maior o volume de produção, maior a chance de uma
peça fora do padrão passar — ou de uma peça boa ser descartada por engano.

A automação digital ataca exatamente esse ponto. Ao transformar os critérios de
qualidade em **regras de software**, a decisão "aprova ou reprova" deixa de
depender da atenção do operador e passa a ser **objetiva, instantânea e
rastreável**. Além disso, o próprio sistema organiza o armazenamento (as
caixas) e gera relatórios em tempo real, reduzindo atrasos, retrabalho de
conferência e custo de operação. É o primeiro passo de um caminho que, adiante,
inclui sensores lendo os dados sozinhos e algoritmos de IA detectando defeitos
que nem estão na lista de critérios atual.

Neste trabalho o objetivo não é o sistema industrial completo, e sim
**prototipar a lógica central** em Python: receber os dados de uma peça,
aplicar as regras de qualidade, armazenar o resultado e consolidar em
relatórios.

---

## 2. Como estruturei o raciocínio lógico

Antes de escrever código, quebrei o desafio em quatro perguntas e resolvi cada
uma com um recurso da linguagem.

### 2.1. "Esta peça está dentro do padrão?" → decisões e condições

O coração do sistema é a função `avaliar()`, em `qualidade.py`. Ela recebe uma
peça e testa **três condições independentes**:

- o peso está entre 95 g e 105 g?
- a cor é azul ou verde?
- o comprimento está entre 10 cm e 20 cm?

Cada condição que **falha** adiciona uma frase a uma lista `motivos`. No fim, se
a lista está vazia a peça é aprovada; se tem algum item, é reprovada — e o
sistema já sabe exatamente **por quê**. Optei por registrar *todos* os motivos,
e não parar no primeiro, porque no chão de fábrica interessa saber tudo o que
está errado de uma vez.

Os limites (95, 105, 10, 20) não estão soltos no meio do código: são
**constantes com nome** (`PESO_MINIMO`, `PESO_MAXIMO`, etc.), tipadas. Se a
engenharia mudar uma faixa, muda-se uma linha, num único arquivo.

### 2.2. "Onde guardo as peças aprovadas?" → repetição e controle de capacidade

Em `armazenamento.py`, a função `montar_caixas()` percorre as peças aprovadas
com um laço `for`. A cada **10 peças** ela fecha a caixa atual e começa outra —
usei o resto da divisão (`indice % 10 == 0`) para achar o momento de abrir
caixa nova.

Decisão de projeto importante: as caixas **não são salvas**, são
**recalculadas** sempre a partir da lista de aprovadas. Assim, se o usuário
remover uma peça, a organização das caixas se ajusta sozinha, sem numeração
furada. Isso é um exemplo de "dado derivado, não duplicado".

### 2.3. "Como o usuário interage?" → repetição + decisões (menu)

`cli.py` tem um laço `while True` que mostra as opções, lê a escolha e chama a
função correspondente. Um dicionário (`MENU`) liga cada número a um rótulo e a
uma função — para adicionar uma opção nova, acrescento uma linha. Escrevi
funções de leitura (`ler_float`, `ler_str`, `ler_int`) que **repetem a
pergunta** até a entrada ser válida, então o programa não quebra se alguém
digitar "abc" no campo de peso.

### 2.4. "Como não perder os dados?" → funções e persistência em arquivo

`persistencia.py` converte o estado em texto **JSON** e grava em `dados.json`.
Ao abrir o programa, lê esse arquivo e reconstrói tudo. Se o arquivo não
existir (primeira execução) ou estiver corrompido, o sistema começa vazio em
vez de travar.

### 2.5. Organização geral: uma responsabilidade por módulo

| Módulo             | Responsabilidade                                    |
|--------------------|----------------------------------------------------|
| `modelos.py`       | entidades `Peca` e `Caixa` (dataclasses tipadas)   |
| `qualidade.py`     | decidir se uma peça é aprovada ou reprovada        |
| `armazenamento.py` | distribuir as aprovadas em caixas de 10            |
| `persistencia.py`  | ler e gravar os dados em arquivo                   |
| `sistema.py`       | `SistemaProducao`: estado + operações (fachada)    |
| `relatorio.py`     | montar o texto do relatório                        |
| `cli.py`           | conversar com o usuário no terminal                |

A `SistemaProducao` é a única porta de entrada do domínio: a CLI e os testes
falam só com ela, nunca com as listas por dentro. Consultas são `@property`;
mudanças de estado são métodos de comando (`cadastrar`, `remover`).

### 2.6. Uma nota honesta sobre o processo (dev JS aprendendo Python)

Trabalho com JavaScript nos últimos 5 anos, então minha primeira versão tinha
"cara de JS": um objeto de estado global e um monte de função solta manipulando
esse objeto. Funcionava, mas não era o jeito mais limpo em Python. Refatorei
para:

- **classes com `@dataclass`** (parecido com uma `class` enxuta de ES6/TS),
- **type hints em todo o código** (o hábito vem do TypeScript),
- **uma classe de fachada** (`SistemaProducao`) no lugar do estado global,
- **testes automatizados com `pytest`** — 36 casos, incluindo os limites
  exatos dos critérios e o fechamento de caixa aos 10.

Escrever os testes foi, na prática, a parte em que mais *pensei no problema*:
casos de fronteira (peso exatamente 95, comprimento exatamente 20), o que
acontece ao remover a peça que "segura" uma caixa cheia, o ciclo
salvar/carregar.

Vale registrar que usei um assistente de IA como par de programação durante o
desenvolvimento — o que, considerando o curso, é exatamente a ferramenta que a
formação me prepara para usar bem. A IA acelerou a digitação do código e sugeriu
a estrutura inicial dos módulos, mas as decisões de arquitetura foram minhas:
foi ali que resolvi trocar o estado global por uma classe de fachada, mudei o
jeito de tratar as caixas (de "salvar" para "recalcular") depois de identificar
o bug de numeração furada ao remover peça, e defini quais casos de fronteira os
testes precisavam cobrir. Usar IA como ferramenta e saber explicar cada decisão
é, na minha visão, a diferença entre automatizar o pensamento e automatizar a
digitação — e é essa segunda coisa que busquei aqui.

---

## 3. Benefícios percebidos e desafios enfrentados

### Benefícios da solução

- **Objetividade:** a mesma peça sempre recebe o mesmo veredito.
- **Rastreabilidade:** todo motivo de reprovação fica registrado e aparece
  agrupado no relatório final.
- **Velocidade:** veredito e alocação em caixa são instantâneos.
- **Manutenção fácil:** critérios num só arquivo, com constantes nomeadas.
- **Confiabilidade:** testes automatizados travam regressões; entradas
  inválidas não derrubam o programa; os dados sobrevivem ao fechamento.

### Desafios enfrentados

- **Decidir como tratar as caixas.** A versão que persistia as caixas quebrava
  a numeração ao remover uma peça. A solução foi recalcular a partir das
  aprovadas — mais simples e sempre coerente.
- **Sair do "sotaque" JavaScript.** Trocar estado global + funções por classe,
  `@dataclass` e type hints; entender `@property`, `frozenset`, `Counter` e o
  `from __future__ import annotations`.
- **Validação de entrada.** Prever tudo que o usuário digita errado: texto no
  lugar de número, vírgula em vez de ponto, campo vazio, id inexistente.
- **Manter os módulos realmente desacoplados**, sem import circular (ex.:
  `relatorio` usa `SistemaProducao`, mas `sistema` não conhece `relatorio`).
- **Ambiente Windows.** No meu dia a dia uso Node/JS, então tive que me
  situar de novo no ecossistema Python no Windows — o launcher `py` no lugar
  do `python`, e configurar o `pyproject.toml` (`pythonpath = ["."]`) para o
  `pytest` conseguir importar o pacote `src` a partir da pasta `tests`.
- **Git do zero neste projeto.** Optei por não fazer um único commit
  gigante e sim separar por camada (modelos, regras, armazenamento,
  persistência, fachada, relatório, CLI, testes, docs) — ficou mais fácil de
  revisar e reflete melhor a ordem em que o raciocínio foi montado.

---

## 4. Reflexão final: como expandir este protótipo para um cenário real

O protótipo lê os dados pelo teclado, mas a lógica que ele contém — os
critérios, a alocação em caixas e os relatórios — é a mesma que rodaria num
cenário industrial. A evolução teria três frentes:

1. **Sensores no lugar do teclado.** Uma balança digital, um sensor de cor RGB
   e um medidor de distância a laser enviariam `peso`, `cor` e `comprimento`
   automaticamente, via porta serial ou protocolo industrial (MQTT, OPC-UA). A
   função `avaliar()` continuaria idêntica — só mudaria a origem dos dados.
   Como o domínio já está isolado da entrada (a CLI é uma casca fina), trocar
   o teclado por um sensor é trocar só a camada `cli.py`.

2. **Inteligência artificial para defeitos "invisíveis".** Os critérios atuais
   são limites fixos. Um modelo de visão computacional treinado com fotos de
   peças boas e defeituosas poderia detectar trincas, rebarbas e manchas que
   não aparecem no peso nem no comprimento. O resultado do modelo entraria
   como mais um "motivo de reprovação", sem mudar o resto do fluxo.

3. **Integração industrial de verdade.** Trocar o `dados.json` por um banco de
   dados, expor os relatórios num painel web em tempo real, acionar um
   desviador de esteira para separar fisicamente aprovadas de reprovadas, e
   disparar alertas quando a taxa de reprovação subir acima de um limite —
   sinal de que a máquina precisa de ajuste.

Em resumo: o protótipo já resolve a parte mais importante — **a decisão
lógica** — e foi construído (módulos isolados, domínio separado da interface,
critérios num só lugar) de um jeito que permite plugar sensores, IA e
integração sem reescrever o núcleo.

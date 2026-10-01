# Roteiro do Vídeo Pitch (até 4 minutos)

> Cronômetro à vista. Os tempos são sugestões.
>
> **Objetivo implícito deste roteiro:** deixar claro que você *pensou no
> problema* e *domina o código* — que a IA foi ferramenta, não autora. Isso se
> faz mostrando decisões, trade-offs e uma edição ao vivo, não com disclaimer.

## Gravação (OBS com 2 cenas)

- **Cena `Abertura`:** Captura de Janela (VSCode) + webcam em PiP num canto.
  Usada só no bloco **[0:00–0:25]** — olhe pra webcam enquanto se apresenta.
- **Cena `Demo`:** só a Captura de Janela do VSCode, sem webcam. Usada do
  **[0:25] em diante** — narração em áudio sobre a tela, sem rosto aparecendo.

Microfone ativo no Mixer de Áudio em ambas as cenas. Troque de `Abertura` pra
`Demo` ao vivo (clicando na lista de Cenas) assim que terminar a fala de
apresentação — é um corte instantâneo, sem precisar editar depois.

Pode manter o `ROTEIRO_VIDEO.md` aberto numa outra janela sobreposta à do
VSCode na sua tela — como a fonte é Captura de Janela, só o VSCode entra na
gravação.

---

## [0:00 – 0:25] Abertura, contexto e problema — cena `Abertura` (webcam)

> "Olá, meu nome é **[seu nome]**, do curso de Tecnologia em Inteligência
> Artificial e Automação Digital da UniFECAF. Sou desenvolvedor há mais de 30
> anos, os últimos 5 em JavaScript — então este trabalho também foi meu
> exercício de **pensar em Python**.
>
> O problema: hoje a inspeção de peças na linha de montagem é **manual**. Um
> operador confere peso, cor e comprimento peça por peça. É lento, cansa, gera
> erro de conferência e custa caro. A ideia é transformar essa conferência em
> **regras de software** que decidem na hora se a peça passa."

**→ Troque para a cena `Demo` agora** (clique na lista de Cenas do OBS).
Daqui até o fim é só tela, sem webcam.

---

## [0:25 – 1:00] Como pensei o problema (antes do código) — cena `Demo`

> "Antes de escrever qualquer linha, quebrei o desafio em quatro perguntas:
>
> 1. **Esta peça está no padrão?** → decisão com três critérios que valem ao
>    mesmo tempo: peso 95–105 g, cor azul ou verde, comprimento 10–20 cm.
> 2. **Onde guardo as aprovadas?** → caixas de 10; ao encher, fecha e abre outra.
> 3. **Como o usuário interage?** → menu de terminal com repetição e validação.
> 4. **Como não perder os dados?** → salvar num arquivo JSON.
>
> Cada pergunta virou um módulo com uma responsabilidade só."

---

## [1:00 – 1:40] Decisões de projeto e trade-offs

> "Três decisões que valem comentar:
>
> - **Caixas eu não salvo — eu recalculo.** Minha primeira versão guardava as
>   caixas junto com as peças, mas ao remover uma peça a numeração furava.
>   Passei a reconstruir as caixas a partir da lista de aprovadas: mais simples
>   e sempre coerente.
>
> - **Vim do JavaScript, então a v1 tinha cara de JS:** um objeto de estado
>   global e funções soltas. Refatorei para uma classe `SistemaProducao` que
>   encapsula o estado — consultas por *property*, mudanças por método — e
>   coloquei **type hints** em tudo, que é o que eu já uso com TypeScript.
>
> - **Registro todos os motivos de reprovação, não só o primeiro**, porque no
>   chão de fábrica interessa ver tudo o que está fora do padrão de uma vez."

---

## [1:40 – 3:00] Demonstração ao vivo (terminal)

> "Rodando com `py main.py`."

**Faça nesta ordem:**

1. **Peça aprovada** (opção 1): peso `100`, cor `azul`, comprimento `15`.
   → mostrar `[APROVADA] ... guardada na caixa 1`.
2. **Peça reprovada** (opção 1): peso `90`, cor `vermelha`, comprimento `5`.
   → mostrar os **três motivos**.
3. **Mais uma aprovada** (opção 1): peso `102`, cor `verde`, comprimento `12`.
4. **Listar** (opção 2): aprovadas e reprovadas separadas, com motivos.
5. **Remover** (opção 3): remover a reprovada pelo `id` — comentar *"as caixas
   se reorganizam sozinhas"*.
6. **Relatório final** (opção 5): consolidado com aprovadas, reprovadas e caixas.
7. **Sair** (opção 0): *"os dados ficaram no `dados.json`"* — abrir o arquivo
   rapidamente se der tempo.

### Edição ao vivo (o momento mais importante)

> "Pra mostrar que domino a estrutura, vou mudar uma regra agora."

- Abrir `src/qualidade.py`, alterar `PESO_MAXIMO` de `105.0` para, por exemplo,
  `101.0` (ou adicionar um 4º critério simples).
- Salvar, rodar de novo, cadastrar uma peça de `103 g` e mostrar que agora ela
  **reprova por peso**.
- Comentar: *"um limite, um arquivo — por isso as regras ficam isoladas."*
- **Desfazer a alteração** ao final (ou deixar claro que é só demonstração).

### Testes

> "E tem suíte de testes: `pytest`." — rodar e mostrar `36 passed`.
> "Os testes cobrem os limites exatos — 95 e 105 gramas, 10 e 20 centímetros —
> o fechamento da caixa aos 10 e a reorganização ao remover peça."

---

## [3:00 – 3:35] Boas práticas aplicadas

> "Boas práticas:
> - separação de responsabilidades, com `SistemaProducao` como fachada;
> - type hints em todo o código;
> - constantes nomeadas para os limites, sem número mágico;
> - testes automatizados, inclusive de fronteira;
> - validação de entrada — não quebra com dado inválido;
> - dados derivados em vez de duplicados (as caixas nascem das aprovadas).
> No Git dá pra ver os **commits incrementais**, cada etapa da lógica separada."

---

## [3:35 – 4:00] Fechamento

> "O protótipo resolve o essencial: a **decisão lógica** da qualidade. E foi
> feito de um jeito que dá pra evoluir — trocar o teclado por **sensores**
> (balança, sensor de cor RGB, medidor a laser), somar **visão computacional**
> pra pegar trinca e rebarba que não aparecem nas medidas, e ligar num
> **painel industrial** com banco de dados e acionamento de esteira.
>
> A IA me ajudou a acelerar; as decisões de arquitetura e o entendimento do
> código são meus — e acabei de mostrar isso mexendo nele ao vivo. Obrigado!"

---

## Checklist antes de gravar

- [ ] No OBS: as duas cenas prontas — `Abertura` (VSCode + webcam em PiP) e
      `Demo` (só VSCode) — e a barrinha do Mic/Aux se mexendo ao falar nas duas.
- [ ] Testar a troca de cena `Abertura` → `Demo` clicando na lista, pra saber
      exatamente onde clicar na hora de gravar valendo.
- [ ] Gravar um teste de 10s (com a troca de cena incluída), reproduzir e
      confirmar que: tela + webcam + áudio aparecem certos, o corte de cena é
      limpo, e a janela do roteiro sobreposta **não** aparece.
- [ ] Terminal e editor do VSCode com fonte grande (`Ctrl +` ou
      `terminal.integrated.fontSize` nas configurações).
- [ ] Apagar o `dados.json` antes de começar (demo do zero) — ou pré-cadastrar
      10 aprovadas se quiser mostrar uma caixa cheia na opção 4.
- [ ] Ensaiar o roteiro uma vez, principalmente a edição ao vivo.
- [ ] Ter o editor já aberto no `src/qualidade.py`.
- [ ] Áudio limpo, sem eco. Vídeo com menos de 4 minutos.
- [ ] Reverter a alteração de teste no `qualidade.py` antes do commit final.
- [ ] Parar a gravação no OBS, conferir o arquivo gerado (pasta definida em
      Configurações → Saída) antes de subir.
- [ ] Subir o vídeo como **público ou não listado** (YouTube, Loom, Drive) e
      colar o link na entrega.

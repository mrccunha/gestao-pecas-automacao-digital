"""Sistema de automacao digital para controle de qualidade de pecas.

Modulos
-------
modelos        -> entidades do dominio (Peca, Caixa)
qualidade      -> regras de aprovacao/reprovacao
armazenamento  -> distribuicao das pecas aprovadas em caixas
persistencia   -> leitura/gravacao dos dados em JSON
sistema        -> SistemaProducao: estado + operacoes (fachada do dominio)
relatorio      -> geracao do relatorio consolidado
cli            -> menu interativo de terminal
"""

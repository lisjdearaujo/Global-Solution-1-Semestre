# Uso de Inteligência Artificial

## Geração dos dados simulados de telemetria

Utilizamos IA para gerar o conteúdo do arquivo `data/dados.csv`. Descrevemos o contexto da missão espacial e solicitamos que os dados respeitassem as faixas operacionais estabelecidas no enunciado, incluindo os seis módulos críticos, as leituras de energia em seis horários distintos, as variáveis ambientais e o log de eventos com ao menos uma inconsistência proposital.

A validação foi feita manualmente pela equipe, então revisamos cada valor gerado verificando se era coerente com o cenário (por exemplo, se a geração solar às 21h era baixa, se a reserva de energia decrescia conforme o consumo superava a geração e se a inconsistência do sensor de temperatura estava dentro do log em um horário plausível). Os dados só foram aceitos após essa conferência.

## Revisão de texto

Utilizamos IA para revisar os textos do README e deste arquivo, com foco em coerência, correção gramatical e clareza. O conteúdo, os argumentos e as conclusões foram elaborados pela equipe, a IA atuou apenas como revisora.

A validação consistiu em reler os textos revisados e verificar se o sentido original havia sido preservado e se nenhuma informação técnica havia sido alterada ou inserida indevidamente.


# Sistema Inteligente de Monitoramento de Missões Espaciais

> Global Solution — 1º Semestre - FIAP 2026

---

##  Equipe

| Nome | RM |
|------|----|
| Eduardo Alves da Silva | RM 568601 |
| Gabrielly Drosda da Silva | RM571793 |
| Lisandra Jacinto de Araujo | RM 574055 |
| Nathan Caio da Silva | RM 568750 |

---

##  Resumo do Problema

Missões espaciais tripuladas operam em ambientes extremamente hostis e de difícil acesso, onde qualquer falha técnica pode ser fatal. O problema central é a ausência de um sistema automatizado capaz de monitorar continuamente os módulos críticos da missão, interpretar dados de telemetria em tempo real e antecipar riscos antes que se tornem irreversíveis.

Este projeto propõe um sistema de diagnóstico e previsão em Python que lê dados de telemetria de uma missão espacial fictícia (FIAP-1), organiza as informações em estruturas de dados adequadas, aplica regras lógicas para detectar anomalias e utiliza regressão linear para prever o comportamento futuro da reserva de energia  gerando um relatório completo com alertas e recomendações de ação.

---

##  Estrutura do Projeto

```
Global-Solution-1-Semestre/
│
├── data/
│   └── dados.csv            # Arquivo de telemetria da missão
│
├── docs/
│   ├── link_video.txt        # Link do vídeo de apresentação
│   ├── relatorio             # Relatório técnico
│   └── uso_ia.md             # Documentação do uso de IA
│
└── src/
    ├── sistema.py            # Arquivo principal (ponto de entrada)
    ├── leitura.py            # Leitura e parsing do CSV
    ├── estruturas.py         # Organização nas estruturas de dados
    ├── diagnostico.py        # Regras lógicas e geração de alertas
    ├── previsao.py           # Previsão por regressão linear
    └── relatorio.py          # Exibição formatada do relatório
```

---

##  Estruturas de Dados Utilizadas

| Estrutura | Onde é usada | Finalidade |
|-----------|-------------|------------|
| **Dicionário** (`dict`) | `estruturas.py` | Armazenar os módulos da missão (`nome → {status, descrição}`) e as variáveis ambientais (`variavel → {valor, unidade, faixa}`) |
| **Listas** (`list`) | `estruturas.py` | Armazenar séries temporais de energia: `horarios`, `geracao`, `consumo`, `reserva` |
| **Matriz** (lista de listas) | `estruturas.py` | `matriz_energia`: cada linha representa um horário com [hora, geração, consumo, reserva] |
| **Pilha** (lista com `append`/`pop`) | `estruturas.py` | `pilha_eventos`: armazena os 5 eventos críticos mais recentes; o último evento inserido é exibido primeiro (LIFO) |
| **Fila** (`collections.deque`) | `estruturas.py` / `diagnostico.py` | `fila_alertas`: alertas gerados são enfileirados e processados na ordem de chegada (FIFO) |

---

##  Regras Lógicas Principais

O módulo `diagnostico.py` aplica 6 regras de negócio sobre os dados organizados:

| # | Condição | Nível | Ação recomendada |
|---|----------|-------|-----------------|
| 1 | Módulo de **suporte à vida offline** |  CRÍTICO | Ativar sistemas de emergência imediatamente |
| 2 | **Energia < 50%** + **comunicação offline** simultaneamente |  CRÍTICO | Desligar sistemas não essenciais; priorizar suporte à vida |
| 3 | **Energia entre 50% e 65%** |  ALERTA | Reduzir consumo do laboratório e sistemas secundários |
| 4 | **Radiação > 5 mSv/h** |  ALERTA | Mover tripulação para zona protegida do habitat |
| 5 | **Comunicação offline** ou **qualidade < 80%** |  ALERTA | Tentar roteamento pelo canal de backup |
| 6 | **Qualquer outro módulo offline** |  ALERTA | Verificar e tentar reiniciar o módulo afetado |

O **status geral** da missão é definido como `CRÍTICO` se ao menos uma regra crítica for acionada, `ALERTA` se apenas alertas forem encontrados, ou `NORMAL` caso nenhuma regra seja disparada.

---

##  Técnica de Previsão

O módulo `previsao.py` implementa **regressão linear simples** para prever a reserva de energia nos próximos ciclos.

**Fórmula:** `y = a·x + b`

- `x` = índice temporal de cada leitura (0, 1, 2, ...)
- `y` = percentual de reserva de energia em cada leitura
- `a` = inclinação da reta (tendência por ciclo — positiva: recuperação; negativa: queda)
- `b` = intercepto calculado pela média dos dados

Os coeficientes são calculados **manualmente** (sem bibliotecas externas como NumPy), usando as fórmulas:

```
a = Σ[(xi - x̄)(yi - ȳ)] / Σ[(xi - x̄)²]
b = ȳ - a·x̄
```

O sistema prevê os **próximos 2 ciclos** e emite um aviso adicional caso a previsão do segundo ciclo fique abaixo de 30%.

---

## Como Executar o Código

### Pré-requisitos

- Python 3.8 ou superior instalado
- Nenhuma biblioteca externa é necessária (apenas módulos da biblioteca padrão)

### Passos

```bash
# 1. Clone ou extraia o repositório
cd Global-Solution-1-Semestre-main

# 2. Execute o arquivo principal
python src/sistema.py
```

> A cada execução, o sistema sorteia aleatoriamente um dos dois cenários disponíveis (`CRITICO` ou `NORMAL`) e sobrescreve o arquivo `data/dados.csv` com os dados do cenário escolhido antes de processar.

---

## Exemplo de Entrada / Saída

### Entrada — `data/dados.csv` (Cenário Crítico)

```
[modulos]
nome,status,descricao
suporte_vida,1,Sistemas de oxigenio e pressao
comunicacao,0,Link com a Terra
...

[energia_horaria]
horario,geracao_kwh,consumo_kwh,reserva_pct
06:00,30,45,80
...
21:00,5,80,48

[variaveis_ambientais]
variavel,valor,unidade,faixa_normal
radiacao,7.2,mSv/h,0-5
qualidade_comunicacao,0,pct,80-100
```

### Saída — Terminal (Cenário Crítico)

```
cenario sorteado: CRITICO

lendo os dados...
organizando as estruturas...
diagnosticando a missao...
calculando previsao...
verificando inconsistencias...

============================================================
   SISTEMA DE MONITORAMENTO - MISSAO ESPACIAL FIAP-1
============================================================

[ STATUS GERAL DA MISSAO: CRITICO ]

--- MODULOS CRITICOS ---
Nome                 Status     Descricao
-------------------------------------------------------
suporte_vida         OK         Sistemas de oxigenio e pressao
energia              OK         Geracao e distribuicao de energia
comunicacao          FALHA      Link com a Terra
...

--- LEITURAS DE ENERGIA POR HORARIO ---
Hora     Geracao(kWh)    Consumo(kWh)    Reserva(%)
-------------------------------------------------------
06:00    30.0            45.0            80.0
...
21:00    5.0             80.0            48.0

--- VARIAVEIS AMBIENTAIS ---
  radiacao: 7.2 mSv/h (faixa normal: 0-5)
  qualidade_comunicacao: 0 pct (faixa normal: 80-100)
  ...

--- ULTIMOS EVENTOS CRITICOS ---
  [CRITICO] 2026-06-01 16:30 - Reserva de energia caiu abaixo de 65 pct
  [ALERTA] 2026-06-01 09:45 - Nivel de radiacao acima do normal
  ...

--- PREVISAO DE ENERGIA ---
  Tendencia por ciclo: -6.4%
  Reserva atual: 48.0%
  Previsao proximo ciclo:   34.2%
  Previsao ciclo seguinte:  27.8%
  !! ATENCAO: reserva pode chegar em nivel critico em breve!

--- ALERTAS E RECOMENDACOES ---

  [1] CRITICO - Energia critica (48%) e comunicacao offline ao mesmo tempo!
       -> Acao: Desligar todos os sistemas nao essenciais. Priorizar suporte a vida.

  [2] ALERTA - Radiacao elevada: 7.2 mSv/h (limite e 5 mSv/h).
       -> Acao: Mover a tripulacao para a zona protegida do habitat.

  [3] ALERTA - Comunicacao com a Terra comprometida (0%).
       -> Acao: Tentar roteamento pelo canal de backup.

============================================================
   FIM DO RELATORIO
============================================================
```

---

## Vídeo de Apresentação

🔗 _(link a ser adicionado em `docs/link_video.txt`)_

---

## Conclusões e aprendizados

O projeto demonstrou que a escolha da estrutura de dados é fundamental para o funcionamento correto do sistema, influenciando todas as etapas de desenvolvimento. A implementação de um parser próprio para leitura do arquivo CSV e da regressão linear sem bibliotecas externas proporcionou maior compreensão sobre o processamento e análise de dados. Além disso, o trabalho reforçou a importância de desenvolver sistemas capazes de lidar com informações inconsistentes, e garante maior confiabilidade em cenários reais, principalmente no espaço.



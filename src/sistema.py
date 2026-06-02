# sistema.py
# arquivo principal - chama todos os outros modulos em ordem
# para rodar: python src/sistema.py
#
# feito por: (seus nomes aqui)
# Global Solution 2026

import sys
import os
import random

# adiciona a pasta src no caminho pra conseguir importar os outros arquivos
sys.path.insert(0, os.path.dirname(__file__))

from leitura import ler_dados
from estruturas import organizar
from diagnostico import diagnosticar
from previsao import prever_energia
from relatorio import exibir

# ------------------------------------------------
# cenarios possiveis da missao
# ------------------------------------------------

cenario_critico = """## TELEMETRIA - MISSAO ESPACIAL FIAP-1
## Status dos modulos: 1 = operacional, 0 = falha

[modulos]
nome,status,descricao
suporte_vida,1,Sistemas de oxigenio e pressao
energia,1,Geracao e distribuicao de energia
comunicacao,0,Link com a Terra
habitat,1,Temperatura e condicoes do habitat
laboratorio,1,Equipamentos cientificos
armazenamento,1,Suprimentos e combustivel

[energia_horaria]
horario,geracao_kwh,consumo_kwh,reserva_pct
06:00,30,45,80
09:00,55,60,75
12:00,70,65,78
15:00,65,70,72
18:00,20,75,62
21:00,5,80,48

[variaveis_ambientais]
variavel,valor,unidade,faixa_normal
temperatura_interna,22.5,Celsius,18-26
temperatura_externa,-180.0,Celsius,N/A
radiacao,7.2,mSv/h,0-5
qualidade_comunicacao,0,pct,80-100
velocidade_vento,45.0,km/h,0-60

[log_eventos]
timestamp,tipo,descricao
2026-06-01 04:15,ALERTA,Queda na qualidade do sinal de comunicacao
2026-06-01 05:30,FALHA,Modulo de comunicacao offline
2026-06-01 06:00,INFO,Inicio do ciclo de geracao solar
2026-06-01 09:45,ALERTA,Nivel de radiacao acima do normal
2026-06-01 11:00,REINICIO,Sistema de comunicacao reiniciado sem sucesso
2026-06-01 13:00,ALERTA,Consumo energetico superando geracao
2026-06-01 16:30,CRITICO,Reserva de energia caiu abaixo de 65 pct
2026-06-01 20:00,ECONOMIA,Modo de economia ativado no laboratorio
2026-06-01 21:00,INCONSISTENCIA,Sensor de temperatura interna reportou -5C por 2 min
"""

cenario_normal = """## TELEMETRIA - MISSAO ESPACIAL FIAP-1
## Status dos modulos: 1 = operacional, 0 = falha

[modulos]
nome,status,descricao
suporte_vida,1,Sistemas de oxigenio e pressao
energia,1,Geracao e distribuicao de energia
comunicacao,1,Link com a Terra
habitat,1,Temperatura e condicoes do habitat
laboratorio,1,Equipamentos cientificos
armazenamento,1,Suprimentos e combustivel

[energia_horaria]
horario,geracao_kwh,consumo_kwh,reserva_pct
06:00,60,40,90
09:00,80,45,92
12:00,90,50,94
15:00,85,48,93
18:00,50,42,88
21:00,20,38,85

[variaveis_ambientais]
variavel,valor,unidade,faixa_normal
temperatura_interna,22.0,Celsius,18-26
temperatura_externa,-180.0,Celsius,N/A
radiacao,2.1,mSv/h,0-5
qualidade_comunicacao,95,pct,80-100
velocidade_vento,30.0,km/h,0-60

[log_eventos]
timestamp,tipo,descricao
2026-06-01 06:00,INFO,Inicio do ciclo de geracao solar
2026-06-01 07:30,INFO,Comunicacao com a Terra estabelecida
2026-06-01 09:00,INFO,Todos os modulos operando normalmente
2026-06-01 11:00,INFO,Coleta de amostras no laboratorio iniciada
2026-06-01 13:00,INFO,Geracao solar no pico do dia
2026-06-01 15:00,INFO,Reserva de energia estavel acima de 85 pct
2026-06-01 17:00,INFO,Rotina de manutencao preventiva concluida
2026-06-01 19:00,INFO,Tripulacao em periodo de descanso
2026-06-01 21:00,INFO,Sistemas em modo noturno sem anomalias
"""

# ------------------------------------------------
# sorteia um cenario aleatoriamente
# ------------------------------------------------

caminho_base = os.path.dirname(os.path.abspath(__file__))
caminho_csv = os.path.join(caminho_base, "..", "data", "dados.csv")

cenario_escolhido = random.choice(["critico", "normal"])

if cenario_escolhido == "critico":
    conteudo = cenario_critico
else:
    conteudo = cenario_normal

# sobrescreve o dados.csv com o cenario sorteado
arquivo = open(caminho_csv, "w", encoding="utf-8")
arquivo.write(conteudo)
arquivo.close()

print("cenario sorteado: " + cenario_escolhido.upper())
print("")

# ---- 1. le o arquivo de dados ----
print("lendo os dados...")
modulos_bruto, energia_bruto, ambiente_bruto, log_bruto = ler_dados()

# ---- 2. organiza nas estruturas (dicionario, listas, pilha, fila, matriz) ----
print("organizando as estruturas...")
modulos, horarios, geracao, consumo, reserva, matriz_energia, ambiente, pilha_eventos, fila_alertas = organizar(modulos_bruto, energia_bruto, ambiente_bruto, log_bruto)

# ---- 3. aplica as regras logicas e gera os alertas ----
print("diagnosticando a missao...")
status_geral, fila_alertas = diagnosticar(modulos, reserva, ambiente, fila_alertas)

# ---- 4. calcula a previsao de energia ----
print("calculando previsao...")
a, previsao_ciclo1, previsao_ciclo2 = prever_energia(reserva)

# ---- 5. verifica inconsistencias nos dados ----
print("verificando inconsistencias...")
inconsistencias = []
temp_interna = ambiente["temperatura_interna"]["valor"]
if temp_interna < 10 or temp_interna > 35:
    inconsistencias.append("Temperatura interna suspeita: " + str(temp_interna) + "C (esperado entre 10 e 35).")
for linha_log in log_bruto:
    if linha_log[1].strip() == "INCONSISTENCIA":
        inconsistencias.append("Log registrou: " + linha_log[2].strip())

# ---- 6. exibe o relatorio completo ----
exibir(modulos, matriz_energia, ambiente, inconsistencias,
       pilha_eventos, reserva, a, previsao_ciclo1, previsao_ciclo2,
       status_geral, fila_alertas)
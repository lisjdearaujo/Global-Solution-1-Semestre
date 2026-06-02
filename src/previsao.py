# previsao.py
# calcula a tendencia da reserva de energia usando regressao linear simples
# e prevê os proximos 2 ciclos

def prever_energia(reserva):

    # regressao linear: y = a*x + b
    # a = inclinacao (quanto sobe ou desce por ciclo)
    # b = ponto inicial da reta

    n = len(reserva)
    x = list(range(n))  # posicoes no tempo: 0, 1, 2, 3, 4, 5
    y = reserva

    # calcula a media de x
    soma_x = 0
    for i in x:
        soma_x = soma_x + i
    media_x = soma_x / n

    # calcula a media de y
    soma_y = 0
    for v in y:
        soma_y = soma_y + v
    media_y = soma_y / n

    # calcula a inclinacao (a) e o ponto inicial (b)
    numerador = 0
    denominador = 0
    for i in range(n):
        numerador = numerador + (x[i] - media_x) * (y[i] - media_y)
        denominador = denominador + (x[i] - media_x) ** 2

    a = numerador / denominador  # tendencia por ciclo
    b = media_y - a * media_x   # ponto inicial

    # prevê os proximos 2 ciclos
    previsao_ciclo1 = a * (n) + b
    previsao_ciclo2 = a * (n + 1) + b

    # limita entre 0 e 100 pra nao dar valor impossivel
    if previsao_ciclo1 < 0:
        previsao_ciclo1 = 0
    if previsao_ciclo1 > 100:
        previsao_ciclo1 = 100

    if previsao_ciclo2 < 0:
        previsao_ciclo2 = 0
    if previsao_ciclo2 > 100:
        previsao_ciclo2 = 100

    previsao_ciclo1 = round(previsao_ciclo1, 1)
    previsao_ciclo2 = round(previsao_ciclo2, 1)

    return a, previsao_ciclo1, previsao_ciclo2

# diagnostico.py
# responsavel por aplicar as regras logicas e gerar os alertas

def diagnosticar(modulos, reserva, ambiente, fila_alertas):

    # pego os valores que vou usar nas regras
    suporte_vida_ok = modulos["suporte_vida"]["status"] == 1
    comunicacao_ok = modulos["comunicacao"]["status"] == 1

    reserva_agora = reserva[-1]  # ultimo valor registrado de reserva
    radiacao = ambiente["radiacao"]["valor"]
    qualidade_com = ambiente["qualidade_comunicacao"]["valor"]

    # limites de energia
    energia_critica = reserva_agora < 50  # abaixo de 50% = critico
    energia_alerta = reserva_agora < 65   # abaixo de 65% = alerta

    alertas_encontrados = []

    # REGRA 1: suporte a vida offline = emergencia maxima
    if not suporte_vida_ok:
        alertas_encontrados.append({
            "nivel": "CRITICO",
            "mensagem": "Modulo de suporte a vida OFFLINE!",
            "acao": "Ativar sistemas de emergencia imediatamente."
        })

    # REGRA 2: energia critica E comunicacao offline ao mesmo tempo
    if energia_critica and not comunicacao_ok:
        alertas_encontrados.append({
            "nivel": "CRITICO",
            "mensagem": "Energia critica (" + str(int(reserva_agora)) + "%) e comunicacao offline ao mesmo tempo!",
            "acao": "Desligar todos os sistemas nao essenciais. Priorizar suporte a vida."
        })

    # REGRA 3: energia em alerta mas ainda nao critica
    if energia_alerta and not energia_critica:
        alertas_encontrados.append({
            "nivel": "ALERTA",
            "mensagem": "Reserva de energia em " + str(int(reserva_agora)) + "% (abaixo de 65%).",
            "acao": "Reduzir consumo do laboratorio e sistemas secundarios."
        })

    # REGRA 4: radiacao alta demais
    if radiacao > 5:
        alertas_encontrados.append({
            "nivel": "ALERTA",
            "mensagem": "Radiacao elevada: " + str(radiacao) + " mSv/h (limite e 5 mSv/h).",
            "acao": "Mover a tripulacao para a zona protegida do habitat."
        })

    # REGRA 5: comunicacao ruim ou offline
    if not comunicacao_ok or qualidade_com < 80:
        alertas_encontrados.append({
            "nivel": "ALERTA",
            "mensagem": "Comunicacao com a Terra comprometida (" + str(int(qualidade_com)) + "%).",
            "acao": "Tentar roteamento pelo canal de backup."
        })

    # REGRA 6: outros modulos com problema
    for nome_modulo in modulos:
        if modulos[nome_modulo]["status"] == 0 and nome_modulo != "comunicacao":
            alertas_encontrados.append({
                "nivel": "ALERTA",
                "mensagem": "Modulo '" + nome_modulo + "' esta OFFLINE.",
                "acao": "Verificar e tentar reiniciar o modulo " + nome_modulo + "."
            })

    # coloca os alertas na fila
    for alerta in alertas_encontrados:
        fila_alertas.append(alerta)

    # define o status geral
    tem_critico = False
    tem_alerta = False
    for alerta in alertas_encontrados:
        if alerta["nivel"] == "CRITICO":
            tem_critico = True
        if alerta["nivel"] == "ALERTA":
            tem_alerta = True

    if tem_critico:
        status_geral = "CRITICO"
    elif tem_alerta:
        status_geral = "ALERTA"
    else:
        status_geral = "NORMAL"

    return status_geral, fila_alertas

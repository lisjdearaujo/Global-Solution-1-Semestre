# relatorio.py
# responsavel por imprimir tudo no terminal de forma organizada

def exibir(modulos, matriz_energia, ambiente, inconsistencias,
           pilha_eventos, reserva, a, previsao_ciclo1, previsao_ciclo2,
           status_geral, fila_alertas):

    print("")
    print("=" * 60)
    print("   SISTEMA DE MONITORAMENTO - MISSAO ESPACIAL FIAP-1")
    print("=" * 60)

    print("")
    print("[ STATUS GERAL DA MISSAO:", status_geral, "]")

    # tabela de modulos
    print("")
    print("--- MODULOS CRITICOS ---")
    print("Nome                 Status     Descricao")
    print("-" * 55)
    for nome_mod in modulos:
        if modulos[nome_mod]["status"] == 1:
            status_txt = "OK"
        else:
            status_txt = "FALHA"
        print(nome_mod.ljust(21) + status_txt.ljust(11) + modulos[nome_mod]["descricao"])

    # matriz de energia
    print("")
    print("--- LEITURAS DE ENERGIA POR HORARIO ---")
    print("Hora     Geracao(kWh)    Consumo(kWh)    Reserva(%)")
    print("-" * 55)
    for linha_matriz in matriz_energia:
        print(str(linha_matriz[0]).ljust(9) + str(linha_matriz[1]).ljust(16) + str(linha_matriz[2]).ljust(16) + str(linha_matriz[3]))

    # variaveis ambientais
    print("")
    print("--- VARIAVEIS AMBIENTAIS ---")
    for v in ambiente:
        print("  " + v + ": " + str(ambiente[v]["valor"]) + " " + ambiente[v]["unidade"] + " (faixa normal: " + ambiente[v]["faixa"] + ")")

    # inconsistencias
    if len(inconsistencias) > 0:
        print("")
        print("--- INCONSISTENCIAS DETECTADAS ---")
        for inc in inconsistencias:
            print("  !! " + inc)

    # pilha de eventos (do mais recente pro mais antigo)
    print("")
    print("--- ULTIMOS EVENTOS CRITICOS ---")
    i = len(pilha_eventos) - 1
    while i >= 0:
        ev = pilha_eventos[i]
        print("  [" + ev["tipo"] + "] " + ev["timestamp"] + " - " + ev["descricao"])
        i = i - 1

    # previsao
    print("")
    print("--- PREVISAO DE ENERGIA ---")
    print("  Tendencia por ciclo: " + str(round(a, 2)) + "%")
    print("  Reserva atual: " + str(reserva[-1]) + "%")
    print("  Previsao proximo ciclo:   " + str(previsao_ciclo1) + "%")
    print("  Previsao ciclo seguinte:  " + str(previsao_ciclo2) + "%")
    if previsao_ciclo2 < 30:
        print("  !! ATENCAO: reserva pode chegar em nivel critico em breve!")

    # alertas e recomendacoes (criticos primeiro)
    print("")
    print("--- ALERTAS E RECOMENDACOES ---")

    if len(fila_alertas) == 0:
        print("  Nenhum alerta. Missao em condicoes normais.")
    else:
        criticos = []
        alertas_nivel = []
        for al in fila_alertas:
            if al["nivel"] == "CRITICO":
                criticos.append(al)
            else:
                alertas_nivel.append(al)

        contador = 1
        for al in criticos:
            print("")
            print("  [" + str(contador) + "] " + al["nivel"] + " - " + al["mensagem"])
            print("       -> Acao: " + al["acao"])
            contador = contador + 1

        for al in alertas_nivel:
            print("")
            print("  [" + str(contador) + "] " + al["nivel"] + " - " + al["mensagem"])
            print("       -> Acao: " + al["acao"])
            contador = contador + 1

    print("")
    print("=" * 60)
    print("   FIM DO RELATORIO")
    print("=" * 60)
    print("")

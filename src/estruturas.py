# estruturas.py
# responsavel por organizar os dados brutos nas estruturas certas
# (dicionario, listas, matriz, pilha e fila)

from collections import deque

def organizar(modulos_bruto, energia_bruto, ambiente_bruto, log_bruto):

    # --- dicionario de modulos ---
    # dicionario serve pra acessar qualquer modulo pelo nome
    modulos = {}
    for m in modulos_bruto:
        nome = m[0].strip()
        status = int(m[1].strip())
        descricao = m[2].strip()
        modulos[nome] = {"status": status, "descricao": descricao}

    # --- listas de energia e matriz ---
    # listas separadas pra cada variavel ao longo do tempo
    horarios = []
    geracao = []
    consumo = []
    reserva = []

    # matriz = lista de listas, cada linha e um horario diferente
    matriz_energia = []

    for e in energia_bruto:
        h = e[0].strip()
        g = float(e[1].strip())
        c = float(e[2].strip())
        r = float(e[3].strip())

        horarios.append(h)
        geracao.append(g)
        consumo.append(c)
        reserva.append(r)
        matriz_energia.append([h, g, c, r])

    # --- dicionario de variaveis ambientais ---
    ambiente = {}
    for a in ambiente_bruto:
        variavel = a[0].strip()
        valor = a[1].strip()
        unidade = a[2].strip()
        faixa = a[3].strip()

        try:
            valor = float(valor)
        except:
            pass

        ambiente[variavel] = {"valor": valor, "unidade": unidade, "faixa": faixa}

    # --- pilha dos ultimos eventos criticos ---
    # pilha = o ultimo que entra e o primeiro a sair
    # guarda so os 5 eventos mais recentes
    pilha_eventos = []
    for evento in log_bruto:
        tipo = evento[1].strip()
        if tipo == "ALERTA" or tipo == "CRITICO" or tipo == "FALHA":
            novo_evento = {
                "timestamp": evento[0].strip(),
                "tipo": tipo,
                "descricao": evento[2].strip()
            }
            pilha_eventos.append(novo_evento)
            if len(pilha_eventos) > 5:
                pilha_eventos.pop(0)

    # --- fila de alertas (sera preenchida no diagnostico) ---
    # fila = o primeiro que entra e o primeiro que sai
    fila_alertas = deque()

    return modulos, horarios, geracao, consumo, reserva, matriz_energia, ambiente, pilha_eventos, fila_alertas

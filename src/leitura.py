# leitura.py
# responsavel por abrir o arquivo dados.csv e separar as informacoes

import os

def ler_dados():
    # pega o caminho da pasta onde esta o leitura.py e sobe um nivel pra achar o data/
    caminho_base = os.path.dirname(os.path.abspath(__file__))
    caminho_csv = os.path.join(caminho_base, "..", "data", "dados.csv")

    arquivo = open(caminho_csv, "r", encoding="utf-8")
    linhas = arquivo.readlines()
    arquivo.close()

    secao = ""

    modulos_bruto = []
    energia_bruto = []
    ambiente_bruto = []
    log_bruto = []

    for linha in linhas:
        linha = linha.strip()

        # pula linhas vazias e comentarios
        if linha == "" or linha.startswith("##"):
            continue

        # verifica se mudou de secao
        if linha == "[modulos]":
            secao = "modulos"
            continue
        elif linha == "[energia_horaria]":
            secao = "energia"
            continue
        elif linha == "[variaveis_ambientais]":
            secao = "ambiente"
            continue
        elif linha == "[log_eventos]":
            secao = "log"
            continue

        # pula os cabecalhos de cada secao
        if linha.startswith("nome,") or linha.startswith("horario,") or linha.startswith("variavel,") or linha.startswith("timestamp,"):
            continue

        # separa os valores por virgula e adiciona na lista certa
        partes = linha.split(",")

        if secao == "modulos":
            modulos_bruto.append(partes)
        elif secao == "energia":
            energia_bruto.append(partes)
        elif secao == "ambiente":
            ambiente_bruto.append(partes)
        elif secao == "log":
            log_bruto.append(partes)

    return modulos_bruto, energia_bruto, ambiente_bruto, log_bruto
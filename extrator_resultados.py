import re
import pandas as pd

# funcao para ler o txt e extrair os dados de cada instancia
def gerar_tabela_resultados(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        texto_completo = arquivo.read()

    # divide o arquivo em blocos, separando cada instancia
    blocos = texto_completo.split('RESOLVENDO')
    linhas_tabela = []

    # ignora o primeiro bloco pois e apenas o cabecalho antes da instancia 1
    for bloco in blocos[1:]:
        dados_instancia = {}

        # extrai o id da instancia
        busca_id = re.search(r'INSTÂNCIA\s+(\d+)', bloco)
        dados_instancia['id_instancia'] = int(busca_id.group(1)) if busca_id else None

        # extrai o tempo de execucao
        busca_tempo = re.search(r'Tempo de Execução:\s+([\d.]+)', bloco)
        dados_instancia['tempo_s'] = float(busca_tempo.group(1)) if busca_tempo else None

        # extrai o valor da funcao objetivo
        busca_fo = re.search(r'Valor da FO:\s+([\d.-]+)', bloco)
        dados_instancia['fo'] = float(busca_fo.group(1)) if busca_fo else None

        # verifica os pares estrategicos (norma l2)
        # captura todos os valores da norma l2 que aparecem antes da explicacao de linha reta
        buscas_estrategicos = re.findall(r'=\s+([\d.]+)\s+->\s+\(Distância em linha reta\)', bloco)
        if buscas_estrategicos:
            # confere se todas as distancias euclidianas dos pares bateram 1.00
            tudo_ok = all(float(valor) == 1.0 for valor in buscas_estrategicos)
            dados_instancia['pares_estrategicos'] = 'OK (Todos = 1.00)' if tudo_ok else 'Falhou'
        else:
            dados_instancia['pares_estrategicos'] = 'N/A'

        # extrai as estatisticas de conflitos (focando na l2 para a tabela ficar legivel)
        busca_media_l2 = re.search(r'media l2 \(linha reta\):\s+([\d.]+)', bloco)
        dados_instancia['conflito_media_l2'] = float(busca_media_l2.group(1)) if busca_media_l2 else None

        busca_min_l2 = re.search(r'menor l2 \(linha reta\):\s+([\d.]+)', bloco)
        dados_instancia['conflito_min_l2'] = float(busca_min_l2.group(1)) if busca_min_l2 else None

        # adiciona a linha na tabela se encontrou o id
        if dados_instancia['id_instancia'] is not None:
            linhas_tabela.append(dados_instancia)

    # cria o dataframe final com nomes de colunas apresentaveis
    tabela = pd.DataFrame(linhas_tabela)
    tabela.columns = [
        'ID Instância', 
        'Tempo (s)', 
        'F.O.', 
        'Pares Estratégicos (L2)', 
        'Média L2 (Conflitos)', 
        'Menor L2 (Conflitos)'
    ]
    
    return tabela


nome_do_arquivo = 'resultados.txt'
tabela_final = gerar_tabela_resultados(nome_do_arquivo)
print(tabela_final.to_string(index=False))
tabela_final.to_csv('tabela_resumo_30_instancias.csv', index=False, sep=';', decimal=',')
import re

# funcao para extrair apenas os mapas de sala do log completo
def extrair_apenas_mapas(caminho_entrada, caminho_saida):
    # abre o arquivo com o log do terminal
    with open(caminho_entrada, 'r', encoding='utf-8') as arquivo:
        texto_completo = arquivo.read()

    # divide o arquivo em blocos usando a palavra resolvendo
    blocos = texto_completo.split('RESOLVENDO')
    
    # abre o arquivo de saida no modo de escrita
    with open(caminho_saida, 'w', encoding='utf-8') as arquivo_saida:
        
        # ignora o primeiro bloco que e so cabecalho
        for bloco in blocos[1:]:
            
            # procura o numero da instancia
            busca_id = re.search(r'INSTÂNCIA\s+(\d+)', bloco)
            id_instancia = busca_id.group(1) if busca_id else "desconhecida"
            
            # procura o bloco inteiro do mapa usando expressao regular
            # o re.dotall faz o .* englobar as quebras de linha
            padrao_mapa = r'(={20,}\s+MAPA DA SALA DE AULA\s+={20,}.*?Legenda:[^\n]+)'
            busca_mapa = re.search(padrao_mapa, bloco, re.DOTALL)
            
            if busca_mapa:
                mapa_texto = busca_mapa.group(1)
                
                # escreve o cabecalho da instancia e o mapa no arquivo novo
                arquivo_saida.write(f"Instância {id_instancia}\n")
                arquivo_saida.write(mapa_texto + "\n\n")
                arquivo_saida.write("-" * 80 + "\n\n")

# =======================================================
# execucao do script
# =======================================================

arquivo_com_log = 'resultados.txt'
arquivo_apenas_mapas = 'mapas_das_30_instancias.txt'

extrair_apenas_mapas(arquivo_com_log, arquivo_apenas_mapas)

print("pronto! os mapas foram extraidos com sucesso.")
print(f"abra o arquivo '{arquivo_apenas_mapas}' para ver o resultado.")
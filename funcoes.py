from banco_de_dados import *
import os

global colunas

# Pega a tabela do banco de dados e imprime ao usuário
def mostra_notas(host,user,pw,database,table):
    # Pega os dados
    ler_tabela = f"""
    SELECT *
    FROM {table};
    """
    connection = create_db_connection(host,user,pw,database)
    aux = read_query(connection,ler_tabela)
    
    leituras = []
    
    for i in aux:
        i = list(i)
        leituras.append(i)
    
    return leituras

# Calcula a média
def calcula_media_fernando(av1,av2,av3,ava1,ava2,avd,avds):
    soma = 0
    av1 += ava1
    av2 += ava2
    if av1 > 10: av1 = 10
    if av2 > 10: av2 = 10
    if av1 < av2:
        soma += av2
        if av1 > av3: soma += av1 
        else: soma += av3
    else:
        soma += av1
        if av2 > av3: soma+= av2
        else: soma += av3
    if avd > avds: soma += avd
    else: soma += avds
    media = round(soma / 3,2)
    return media

# Preenche a tabela com as informções que o usuário insere
def insere_materias_fernando(host,user,pw,database,table,materia,codigo,av1,av2,av3,ava1,ava2,avd,avds):
    media = calcula_media_fernando(av1,av2,av3,ava1,ava2,avd,avds)
    
    # Cria os comandos em SQL
    inserir_dados = f"insert into {table}(materia,codigo,carga,av1,av2,av3,ava1,ava2,avd,avds,media) value ('{materia}','{codigo}',80,{av1},{av2},{av3},{ava1},{ava2},{avd},{avds},{media})"
    # Faz a conexão com a DB e comita os comandos
    connection = create_db_connection(host,user,pw,database)
    execute_query(connection,inserir_dados)

# Calcula o CR usando a DB
def calcula_cr(host,user,pw,database,table):
    # Pega os dados
    ler_tabela = f"SELECT * FROM {table};"
    
    connection = create_db_connection(host,user,pw,database)
    leituras = read_query(connection,ler_tabela)
    
    # Calcula e mostra ao usuário
    soma_media = 0
    soma_carga = 0
    for leitura in leituras:
        soma_media += leitura[-1] * leitura[3]
        soma_carga += leitura[3]
    cr = round(soma_media / soma_carga,2)
    return f"CR: {cr}.  De {leituras[-1][0]} matérias cursadas."

def calcula_media_clarissa(p1,p2,p3,ef,seg):
    if p3 == '--': media_parcial = round((p1+p2)/2,1)
    else: media_parcial = round((p1+p2+p3)/3,1)
    
    if media_parcial < 7:
        if ef < 7: media_final = seg
        else: media_final = ef
    else: media_final = media_parcial
    
    return media_final

def insere_materias_clarissa(host,user,pw,database,table,materia,codigo,carga,p1,p2,p3,p3_check,ef,seg):
    if not p3_check: p3 = '--'
    
    media = calcula_media_clarissa(p1,p2,p3,ef,seg)
    
    inserir_dados = f"insert into {table}(materia,codigo,carga,p1,p2,p3,exame_final,segunda_epoca,media_final) value ('{materia}','{codigo}',{carga},{p1},{p2},'{p3}',{ef},{seg},{media})"
    
    connection = create_db_connection(host,user,pw,database)
    execute_query(connection,inserir_dados)
import pandas as pd
from funcoes import *
from banco_de_dados import *
import PySimpleGUI as sg

global host,user,database,table,pw
host = 'localhost'
database = 'notas'

# Janelas
def janela_login():
    sg.theme('DarkBlue1')
    layout = [
        [sg.Titlebar('UrGrade')],
        [sg.Text('Para continuar, insira algumas informações: ')],
        [sg.Text('Usuário: '),sg.Input(key='user',size=(20,1), do_not_clear=False)],
        [sg.Text('Senha: '),sg.Input(key='senha',password_char='*',size=(20,1), do_not_clear=False)],
        [sg.Button('Entrar')]
    ]
    return sg.Window('login',layout,finalize='true')

def janela_login_erro():
    sg.theme('DarkBlue1')
    layout = [
        [sg.Titlebar('UrGrade')],
        [sg.Text('Para continuar, insira algumas informações: ')],
        [sg.Text('Usuário: '),sg.Input(key='user',size=(20,1), do_not_clear=False)],
        [sg.Text('Senha: '),sg.Input(key='senha',password_char='*',size=(20,1), do_not_clear=False)],
        [sg.Button('Entrar')],
        [sg.Text('Informações erradas, por favor tente novamente.')]
    ]
    return sg.Window('login',layout,finalize='true')

def janela_admin():
    sg.theme('DarkBlue1')
    layout = [
        [sg.Titlebar('UrGrade')],
        [sg.Text('Escrever código:')],
        [sg.Multiline(key='comandos',size=(50,20), do_not_clear=False)],
        [sg.Button('OK'),sg.Button('Voltar')]
    ]
    return sg.Window('admin',layout,finalize='true')

def janela_inicio():
    sg.theme('DarkBlue1')
    layout = [
        [sg.Titlebar('UrGrade')],
        [sg.Text('Seja bem-vindo! O que você gostaria de fazer?')],
        [sg.Button('Olhar as notas')],
        [sg.Button('Inserir matérias')],
        [sg.Button('Trocar usuário')]
    ]
    return sg.Window('inicio',layout,finalize='true')

def janela_tabela():
    sg.theme('DarkBlue1')
    
    tabela = mostra_notas(host,user,pw,database,table)
    
    if user == 'Fernando':
        colunas = ['ID', 'Matéria', 'Cód.', 'Carga', 'AV1', 'AV2', 'AV3', 'AVA1', 'AVA2', 'AVD', 'AVDS', 'Média']
    elif user == 'Clarissa':
        colunas = ['ID', 'Matéria', 'Cód.', 'Carga', 'P1', 'P2', 'P3', 'Exame Final', 'Segunda Época', 'Média']
    
    layout = [
        [sg.Titlebar('UrGrade')],
        [sg.Text(calcula_cr(host,user,pw,database,table))],
        [sg.Table(
            values=tabela,
            headings=colunas,
            max_col_width=40,
            auto_size_columns=True,
            justification='right',
            key='-TABLE-',
            row_height=35
        )],
        [sg.Button('Voltar')]
    ]
    
    return sg.Window('notas',layout,finalize='true')

def janela_dados_fernando():
    sg.theme('DarkBlue1')
    layout = [
        [sg.Titlebar('UrGrade')],
        [sg.Text('Se alguma das avaliações não foi realizada, coloque 0')],
        [sg.Text('Matéria: '),sg.Input(key='materia',size=(50,1), do_not_clear=False)],
        [sg.Text('Código: '),sg.Input(key='codigo',size=(10,1), do_not_clear=False)],
        [sg.Text('AV1: '),sg.Input(key='av1',size=(4,1), do_not_clear=False)],
        [sg.Text('AV2: '),sg.Input(key='av2',size=(4,1), do_not_clear=False)],
        [sg.Text('AV3: '),sg.Input(key='av3',size=(4,1), do_not_clear=False)],
        [sg.Text('AVA1: '),sg.Input(key='ava1',size=(4,1), do_not_clear=False)],
        [sg.Text('AVA2: '),sg.Input(key='ava2',size=(4,1), do_not_clear=False)],
        [sg.Text('AVD: '),sg.Input(key='avd',size=(4,1), do_not_clear=False)],
        [sg.Text('AVDS: '),sg.Input(key='avds',size=(4,1), do_not_clear=False)],
        [sg.Button('Voltar'),sg.Button('Ok')]
    ]
    return sg.Window('dados',layout,finalize='true')

def janela_dados_clarissa():
    sg.theme('DarkBlue1')
    layout = [
        [sg.Titlebar('UrGrade')],
        [sg.Text('Se alguma das avaliações não foi realizada, coloque 0')],
        [sg.Text('Matéria: '),sg.Input(key='materia',size=(70,1), do_not_clear=False)],
        [sg.Text('Código: '),sg.Input(key='codigo',size=(10,1), do_not_clear=False)],
        [sg.Text('Carga: '),sg.Input(key='carga',size=(5,1), do_not_clear=False)],
        [sg.Text('Prova 1: '),sg.Input(key='p1',size=(4,1), do_not_clear=False)],
        [sg.Text('Prova 2: '),sg.Input(key='p2',size=(4,1), do_not_clear=False)],
        [sg.Text('Prova 3: '),sg.Input(key='p3',size=(4,1), do_not_clear=False),sg.Checkbox('A matéria tem P3?',key='p3_check')],
        [sg.Text('Exame final: '),sg.Input(key='ef',size=(4,1), do_not_clear=False)],
        [sg.Text('Segunda época: '),sg.Input(key='seg',size=(4,1), do_not_clear=False)],
        [sg.Button('Voltar'),sg.Button('Ok')]
    ]
    return sg.Window('dados',layout,finalize='true')

# Cria a janela inicial
janela1, janela2, janela3, janela4, janela5, janela6, janela7 = janela_login(), None, None, None, None, None, None

# Cria um loop de leitura de eventos
while True:
    window,event,values = sg.read_all_windows()
    
    # Fecha as janelas
    if event == sg.WIN_CLOSED: break
    
    # Janelas 1 e 2, dão acesso à janela de inicio ou admin
    if (window == janela1 or window == janela2) and event == 'Entrar':
        if not verifica_senha_connection(host,values['user'],values['senha']):
            janela2 = janela_login_erro()
            janela1.hide()
        else:
            if values['user'] == 'Fernando':
                user = values['user']
                table = 'fernando'
                pw = values['senha']
                janela4 = janela_inicio()
                if window == janela1: janela1.hide()
                if window == janela2: janela2.hide()
            elif values['user'] == 'Clarissa':
                user = values['user']
                table = 'clarissa'
                pw = values['senha']
                janela4 = janela_inicio()
                if window == janela1: janela1.hide()
                if window == janela2: janela2.hide()
            elif values['user'] == 'root':
                user = values['user']
                pw = values['user']
                janela3 = janela_admin()
                if window == janela1: janela1.hide()
                if window == janela2: janela2.hide()
    
    # Janela 3, admin
    if window == janela3 and event == 'Ok':
        connection = create_db_connection(host,user,pw,database)
        execute_query(connection,values['comandos'])
    
    if window == janela3 and event == 'Voltar':
        janela1.UnHide()
        janela3.hide()
    
    # Janela 4, escolhe a operação
    if window == janela4 and event == 'Olhar as notas':
        janela5 = janela_tabela()
        janela4.hide()
        
    if window == janela4 and event == 'Inserir matérias':
        if user == 'Fernando':
            janela6 = janela_dados_fernando()
            janela4.hide()
        if user == 'Clarissa':
            janela7 = janela_dados_clarissa()
            janela4.hide()
    
    if window == janela4 and event == 'Trocar usuário':
        janela1.UnHide()
        janela4.hide()
    
    # Janela 5, mostra as notas
    if window == janela5 and event == 'Voltar':
        janela5.hide()
        janela4.UnHide()
        
    # Janela 6, insere as matérias 
    if window == janela6 and event == 'Ok':
        insere_materias_fernando(host,user,pw,database,table,values['materia'],values['codigo'],float(values['av1']),float(values['av2']),float(values['av3']),float(values['ava1']),float(values['ava2']),float(values['avd']),float(values['avds']))
        if janela5 == janela_tabela:
            janela5.UnHide()
            janela6.hide()
        else:
            janela5 = janela_tabela()
            janela6.hide()
    
    if window == janela6 and event == 'Voltar':
        janela4.UnHide()
        janela6.hide()
    
    # Janela 7, insere as matérias
    if window == janela7 and event == 'Ok':
        insere_materias_clarissa(host,user,pw,database,table,values['materia'],values['codigo'],values['carga'],float(values['p1']),float(values['p2']),float(values['p3']),values['p3_check'],float(values['ef']),float(values['seg']))
        if janela5 == janela_tabela:
            janela5.UnHide()
            janela7.hide()
        else:
            janela5 = janela_tabela()
            janela7.hide()
    
    if window == janela7 and event == 'Voltar':
        janela4.UnHide()
        janela7.hide()
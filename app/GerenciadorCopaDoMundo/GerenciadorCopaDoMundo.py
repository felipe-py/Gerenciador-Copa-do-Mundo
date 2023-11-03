'''/**********************************************************************************
Autor: Luis Felipe Cunha Silva
Componente Curricular: MI algoritmos 
Concluido em:10/12/2022
Declaro que este código foi elaborado por mim de forma individual e não contém nenhum 
trecho de código de colega ou de outro autor, tais como provindos de livros e apostilas
, e páginas ou documentos eletrônicos da internet. Qualquer trecho de código de outra
autoria que não a minha está destacado com uma citação do autor e a fonte do código, e estou 
ciente que estes trechos não serão considerados para fins de avaliação.
/*************************************************************************************'''

import json

class Equipes:
    def __init__(self):             #classe que aloca em memoria o grupo e as quatro selecoes no momento
        self.grupo = ''             #de cadastro dos grupos.
        self.t1 = ''
        self.t2 = ''
        self.t3 = ''
        self.t4 = ''

class Informacoes_partida:          #classe que aloca em memoria o dia, horario e local do confrontos
    def __init__(self):             #formados a partir das equipes cadastradas.
        self.dia = ''
        self.local = ''
        self.horario = ''


def preencher_arquivo(arquivo,dicionario):
    '''Preenche os arquivos no momento de cadastro dos grupos e equipes
        -Parametros:
        arquivo que sera preenchido e dicionario que sera inserido no arquivo
        -retorno:
        nenhum
    '''
    with open(arquivo, 'r+') as arq:
        dados = json.load(arq)
        dados.append(dicionario)
        arq.seek(0)
        json.dump(dados,arq)

def verifica_time_edicao(grupo,dados):
    '''Cria uma lista contendo as selecoes de um grupo para verificacoes nos menus
        -Parametros:
        grupo que sera verificado e dados do arquivo dos grupos
        -retorno:
        lista com as equipes que fazem parte do grupo
    '''
    for info in dados:
        for chaves in info:
            if chaves == grupo:
                lista = info[chaves]
    return lista

def editar_grupo(grupo,selecao_sair,selecao_entrar):
    '''Realiza a edicao de um grupo em todos os arquivos usados pelo programa
        -Parametros:
        Grupo que sera editado, selecao que sera retirada e inserida no grupo
        -retorno:
        nenhum
    '''
    #EDITA SELECAO NO ARQUIVO DOS GRUPOS
    lista = []
    with open("out_files/Grupos.json",'r') as a_file:  
        json_object = json. load(a_file)            #Carrega o arquivo dos grupos,formado por uma lista de dicionario que tem como chave
                                                    #o grupo e valor uma lista das quatro selecoes participantes desse grupo.
    for itens in json_object:                       
        for chave in itens:
            if chave == grupo:                      #Encontra o grupo entre as chaves, localiza a selecao que sera retirada da lista e a 
                for selecao in itens[chave]:        #troca pela selecao que sera inserida.
                    if selecao == selecao_sair:
                        selecao = selecao_entrar
                    lista.append(selecao)           #Uma nova lista carrega as selecoes apos a alteracao.

    for itens in json_object:
        for chave in itens:                         #A grupo que foi alterado e carregado novamente e a ele e atribuido como valor a lista com a alte-
            if chave == grupo:                      #racao realizada.
                itens[chave] = lista

    with open("out_files/Grupos.json",'w') as a_file:         #Arquivo json e atualizado com as mudancas.
        json. dump(json_object, a_file)

    #EDITA SELECAO NO ARQUIVO DOS CONFRONTOS

    with open("out_files/Confrontos.json",'r') as df:
        dados = json.load(df)

    data = {}                                       #Para edicao de grupos no arquivos dos confrontos e resultados, a selecao que sera retirada e encontrada
                                                    #e a funcao replace e utiliza para troca-la com a selecao que sera inserida.
    for itens in dados:
        for chave in itens:
            if chave == grupo:
                for confronto in itens[chave]:
                    for times in confronto:                                 #O arquivo esta organizado como uma lista de dicionarios que possuem como chave o grupo
                        if selecao_sair in times:                           #e valor uma lista de dicionarios com chaveamento feito pelos confrontos entre as equipes,
                            x = times.replace(selecao_sair,selecao_entrar)  #e valor uma lista contendo o dia, horario e local em um dicionario.
                            data[x] = confronto[times]
                        
    for itens in dados:                                                     #Um dicionario provisorio e utilizado para carregar os confrontos que tiveram sua chave 
        for chave in itens:                                                 #alterada e em seguida carregar os que nao foram alterados.
            if chave == grupo:
                for confronto in itens[chave]:
                    for times in confronto:
                        if selecao_sair not in times:                       
                            data[times] = confronto[times]
    lista = [data]
    for itens in dados:
        for chave in itens:                     #O arquivo e recarregado e o grupo que foi alterado tem como novo valor atribuido a lista contendo o
            if chave == grupo:                  #dicionario peenchido durante a edicao.
                itens[chave] = lista

    with open("out_files/Confrontos.json",'w') as df:
        json. dump(dados, df)

    #EDITA SELECAO NO ARQUIVO DOS RESULTADOS

    with open("out_files/Resultados.json",'r') as arquivo:
        results = json.load(arquivo)

    new_results = {}

    for itens in results:
        for chave in itens:                             #Para edicao no arquivo dos resultados o mesmo processo realizado no arquivo dos confrontos e feito.
            if chave == grupo:                          #Os dois arquivos estao organizados no mesmo formato.
                for confrontos in itens[chave]:
                    for times in confrontos:
                        if selecao_sair in times:
                            d = times.replace(selecao_sair,selecao_entrar)
                            new_results[d] = confrontos[times]

    for itens in results:
        for chave in itens:
            if chave == grupo:
                for confrontos in itens[chave]:
                    for times in confrontos:
                        if selecao_sair not in times:
                            new_results[times] = confrontos[times]
    
    lista_results = [new_results]
    for itens in results:
        for chave in itens:
            if chave == grupo:
                itens[chave] = lista_results

    with open("out_files/Resultados.json",'w') as arq:
        json. dump(results,arq)

    #EDITA SELECAO NO ARQUIVO DAS TABELAS

    with open("out_files/Tabela.json",'r') as df_tabela:
        dados_tabela = json.load(df_tabela)

    novo_dici = {}
    for itens in dados_tabela:
        for chave in itens:
            if chave == grupo:                                          #O arquivo das tabelas contendo os pontos, saldo de gols e gols marcados, esta organizado
                for info in itens[chave]:                               #como uma lista de dicionarios que possuem como chave os grupos e valor uma lista de dicionarios
                    for selecoes in info:                               #chaveados com as selecoes e as informacoes estatisticas em uma lista como valor.
                        if selecoes == selecao_sair:
                            novo_dici[selecao_entrar] = info[selecoes]

    for itens in dados_tabela:
        for chave in itens:
            if chave == grupo:
                for info in itens[chave]:                                   #Um dicionario provisorio e utilizado para carregar o time que foi inserido como chave,
                    for selecoes in info:                                   #e os valores do antigo time que estava no local como valor.
                        if selecoes != selecao_sair:                        #Apos o processo de troca ele carrega as informacoes que nao foram alteradas.
                            novo_dici[selecoes] = info[selecoes]
                        
    for itens in dados_tabela:
        for chave in itens:                     #O arquivo e carregado novamente e a chave que foi alterada recebe como valor uma lista contendo o dicionario
            if chave == grupo:                  #provisorio.
                itens[chave] = [novo_dici]

    with open("out_files/Tabela.json",'w') as a_file:
        json. dump(dados_tabela, a_file)

def excluir_grupo(grupo):
    '''Realiza a exclusao de um grupo em todos os arquivos usados pelo programa
        -Parametros:
        Grupo que sera excluido
        -retorno:
        nenhum
    '''
    #EXCLUI GRUPO NO ARQUIVO DOS GRUPOS
    with open("out_files/Grupos.json",'r') as a_file:  
        json_object = json. load(a_file)

    alteracao = {}
                                                    
    for itens in json_object:                       #Para excluir um grupo, o dicionario alteracao carrega todos os grupos presentes no arquivo, com excessao daquele
        for chave in itens:                         #que sera excluido, este novo dicionario e atribuido a variavel que carrega o arquivo.
            if chave != grupo:
                alteracao[chave] = itens[chave]

    json_object = [alteracao]

    with open("out_files/Grupos.json",'w') as a_file:
        json. dump(json_object, a_file)

    #EXCLUI GRUPO NO ARQUIVO DOS CONFRONTOS

    with open("out_files/Confrontos.json",'r') as df:
        dados = json.load(df)                                   #o mesmo processo e feito para os outros tres arquivos, usando um dicionario para carregar todo o
                                                                #arquivo com excessao da chave que sera excluida e atribuindo este dicionario para a variavel que 
    alteracao_confrontos = {}                                   #carrega o arquivo.

    for itens in dados:
        for chave in itens:
            if chave != grupo:
                alteracao_confrontos[chave] = itens[chave]

    dados = [alteracao_confrontos]

    with open("out_files/Confrontos.json",'w') as df:
        json. dump(dados, df)

    #EXCLUI GRUPO NO ARQUIVO DOS RESULTADOS

    with open("out_files/Resultados.json",'r') as arquivo:
        results = json.load(arquivo)

    alteracao_resultados = {}

    for itens in results:
        for chave in itens:
            if chave != grupo:
                alteracao_resultados[chave] = itens[chave]

    results = [alteracao_resultados]

    with open("out_files/Resultados.json",'w') as arq:
        json. dump(results,arq)
    
     #EXCLUI GRUPO NO ARQUIVO DAS TABELAS

    with open("out_files/Tabela.json",'r') as data_tabela:
        df_tab = json.load(data_tabela)

    alteracao_tabela = {}

    for itens in df_tab:
        for chave in itens:
            if chave != grupo:
                alteracao_tabela[chave] = itens[chave]

    nova_alteracao = [alteracao_tabela]

    with open("out_files/Tabela.json",'w') as df:
        json. dump(nova_alteracao,df)

def cadastro_informacoes_confrontos(grupo,info):
    '''Atualiza arquivo dos confrontos com o dia, horario e local
        -Parametros:
        Grupo que tera seus confrontos cadastrados e dados do arquivo dos confrontos
        -retorno:
        nenhum
    '''
    for itens in info:
        for chave in itens:                                                      #Para cada atributo (DIA,HORARIO E LOCAL) o usuario cadastra uma informacao.
            if chave == grupo:                                                   #A classe e utilizada para alocacao em moria e atribuicao no dicionario do arquivo.
                for confrontos in itens[chave]:
                    for chapa in confrontos:
                        for atributos in confrontos[chapa]:
    
                            i = Informacoes_partida
                            if atributos['DIA'] == None and atributos['HORARIO'] == None and atributos['LOCAL'] == None:
                                print("VOCE IRA CADASTRAR O DIA - LOCAL - HORARIO DAS PARTIDAS =>\n")
                                print('\nVOCE IRA CADASTRAR O CONFRONTO A SEGUIR \n => {} <=\n'.format(chapa))
                                i.dia = input('DIGITE A DATA DESSE CONFRONTO: \n').upper().strip()
                                i.local = input("\nDIGITE O LOCAL DESSE CONFRONTO: \n").upper().strip()
                                i.horario = input("\nDIGITE O HORARIO DESSE CONFRONTO: \n").upper().strip()
                                atributos['DIA'] = i.dia
                                atributos['HORARIO'] = i.horario
                                atributos['LOCAL'] = i.local

    print('\n=-=-=-=-TODAS AS INFROMACOES RELACIONADAS AOS CONFRONTOS DO GRUPO {} ESTAO DEVIDAMENTE PREENCHIDAS=-=-=-=-'.format(grupo))

    with open("out_files/Confrontos.json",'w') as dados_confrontos:
        json.dump(info,dados_confrontos)

def verifica_preenchimento(grupo,info):
    '''Verifica o peenchimento do dia, horario e local do confrontos de um grupo, evitando que o usuario acesse o cadastro de algo que ja foi feito.
        -Parametros:
        Grupo e dados dos confrontos
        -retorno:
        retorna True caso ja exista um cadastro.
    '''
    for itens in info:
        for chave in itens:
            if chave == grupo:
                for confrontos in itens[chave]:
                    for chapa in confrontos:
                        for atributos in confrontos[chapa]:
                            if atributos['DIA'] != None and atributos['HORARIO'] != None and atributos['LOCAL'] != None:
                                return True

def realizar_edicao_do_confronto(se1,se2,modificador,nova_info,grupo,info):
    '''Edita um atributo escolhido pelo usuario em um confronto
        -Parametros:
        Grupo, as duas selecoes que fazem parte do confronto, o modificador que sera editado(dia,horario ou local) e a nova informacao que sera alocada no local.
        -retorno:
        nenhum
    '''
    for itens in info:
        for chave in itens:
            if chave == grupo:
                for confrontos in itens[chave]:
                    for chapa in confrontos:                        #Encontra o confronto com as duas selecoes e modifica o atributo escolhido pelo usuario
                        if se1 in chapa and se2 in chapa:           #alocando o novo valor.
                            for atributos in confrontos[chapa]:
                                atributos[modificador] = nova_info
    with open("out_files/Confrontos.json",'w') as dados_confrontos:
        json.dump(info,dados_confrontos)

def print_confronto(grupo,dados_confrontos):
    '''Exibe para o usuario os dias, horarios e locais de todos os confrontos de um grupo para o usuario.
        -Parametros:
        Grupo que tera seus confrontos exibidos e dados do arquivo dos confrontos
        -retorno:
        print dos confrontos
    '''
    for itens in dados_confrontos:
        for chave in itens:
            if chave == grupo:
                for informacoes in itens[chave]:
                    for confronto in informacoes:
                        print(confronto, " => ",informacoes[confronto])

def print_resultado(grupo,data):
    '''Exibe para o usuario os resultados todos os confrontos de um grupo para o usuario.
        -Parametros:
        Grupo que tera seus resultados exibidos e dados do arquivo dos resultados
        -retorno:
        print dos resultados
    '''
    for itens in data:
        for chave in itens:
            if chave == grupo:
                for info in itens[chave]:
                    for chapa in info:
                        for informacoes in info[chapa]:
                            print("{} ==> {}".format(chapa,informacoes))

def excluir_dados_confrontos(grupo,info):
    '''Exclui o dia, horario e local de todos os confrontos de um grupo.
        -Parametros:
        Grupo que tera os dados de confrontos excluidos e dados do arquivo dos confrontos
        -retorno:
        nenhum
    '''
    for itens in info:
        for chave in itens:
            if chave == grupo:
                for confrontos in itens[chave]:
                    for chapa in confrontos:
                        for atributos in confrontos[chapa]: 
                            if atributos['DIA'] != None and atributos['HORARIO'] != None and atributos['LOCAL'] != None:
                                atributos['DIA'] = None 
                                atributos['HORARIO'] = None 
                                atributos['LOCAL'] = None  

    print("\n>>>>INFORMACOES RELACIONADAS AOS CONFRONTOS DO GRUPO {} FORAM APAGADAS".format(grupo))

    with open('Confrontos.json','w') as dados_confrontos:
            json.dump(info,dados_confrontos)

def excluir_dados_de_um_confronto(se1,se2,grupo,info):
    '''Exclui o dia, horario e local de apenas um confronto de um grupo.
        -Parametros:
        Grupo que tera os dados de um de seusconfrontos excluidos, as duas selecoes do confronto e dados do arquivo dos confrontos
        -retorno:
        nenhum
    '''
    for itens in info:
        for chave in itens:
            if chave == grupo:
                for confrontos in itens[chave]:
                    for chapa in confrontos:
                        if se1 in chapa and se2 in chapa:           #Encontra o confronto com as duas selecoes e apaga seu dia, horario e local.
                            for atributos in confrontos[chapa]:
                                atributos['DIA'] = None 
                                atributos['HORARIO'] = None 
                                atributos['LOCAL'] = None  
    
    print("\n>>>>INFORMACOES RELACIONADAS AOS CONFRONTOS  DE {} E {} DO GRUPO {} FORAM APAGADAS".format(se1,se2,grupo))

    with open("out_files/Confrontos.json",'w') as dados_confrontos:
        json.dump(info,dados_confrontos) 

def calculo_verificacao_confrontos(grupo,df):
    '''Realiza o calculo para verificar se todos os confrontos estao com seus dias, horarios e locais cadastrados.
        -Parametros:
        Grupo para analise e dados dos confrontos
        -retorno:
        soma
    '''
    soma = 0
    for itens in df:
        for chave in itens:
            if chave == grupo:                                      #Cada confronto com dia, horario e local diferente de nulo, soma-se 1
                for confrontos in itens[chave]:
                    for chapa in confrontos:
                        for atributos in confrontos[chapa]:
                            if atributos['DIA'] != None and atributos['HORARIO'] != None and atributos['LOCAL'] != None:
                                soma+=1
    return soma

def calculo_verificacao_resultados(grupo,dados_resultados):
    '''Realiza o calculo para verificar se todos os confrontos estao com seus resultados cadastrados.
        -Parametros:
        Grupo para analise e dados dos resultados
        -retorno:
        soma
    '''
    soma = 0
    for dados in dados_resultados:
        for chave in dados:
            if chave == grupo:
                for info in dados[chave]:                                    #Cada confronto com resultado diferente de nulo, soma-se 1
                    for confronto in info:
                        for resultados in info[confronto]:
                            if resultados['RESULTADO TIME 01'] != None and resultados['RESULTADO TIME 02'] != None:
                                soma += 1
    return soma

def verifica_gols(selecao):
    '''Funcao que recebe o numero de gols que cada equipe marcou em um jogo, com verificacao para evitar ValueError
        -Parametros:
        Selecao que tera seu numero de gols cadastrados
        -retorno:
        numero de gols
    '''
    while True:
        try:   
            numero_gols = int(input("\nQUAL FOI O NUMERO DE GOLS DA SELECAO >>> {}\n".format(selecao)))
            break
        except ValueError:
            print("\n>>>DIGITE APENAS NUMEROS INTEIROS<<<\n")
    return numero_gols

def cadastra_resultado(grupo,se1,se2,dados_resultados,dados_tabela):
    '''Cadastra o resultado do confronto entre duas equipes e calculo os pontos, saldo e numero de gols para formacao da tabela de classificacao
        -Parametros:
        Grupo que tera seu resultado cadastrado, duas selecoes que fazem parte do confronto, dados dos resultados e da tabela de classificao
        -retorno:
        nenhum
    '''
    for itens in dados_resultados:
        for chave in itens:
            if chave == grupo:                  #Encontra o grupo
                for info in itens[chave]:
                    for chapa in info:
                        if se1  in chapa and se2 in chapa:                      #Encontra o confronto com as duas selecoes
                            for atributos in info[chapa]:
                                x = chapa.split()
                                gols1 = verifica_gols(x[2])                 #.split e atribuido na chave para separar as palavras na chave do dicionario do confronto
                                gols2 = verifica_gols(x[6])                 #e encontrar as selecoes, funcao para cadastrar os gols e chamada com cada selecao pelo 
                                atributos["RESULTADO TIME 01"] = gols1      #indice criado no .split.
                                atributos["RESULTADO TIME 02"] = gols2      #Chave com o resultado de cada time e preenchida com o numero de gols de cada.

                                for itens in dados_tabela:
                                    for chave in itens:
                                        if chave == grupo:
                                            for info in itens[chave]:
                                                    
                                                if gols1 > gols2:
                                                    if info[x[2]][0] == None:
                                                        info[x[2]][0] = 3               #Para o arquivo das tabelas uma lista disposta da sequinte forma => [pontos,
                                                    elif info[x[2]][0] != None:         #gols marcados, saldo de gols] e atribuida a cada selecao no arquivo tabelas.
                                                        info[x[2]][0] += 3              
                                                                                        
                                                    if info[x[6]][0] == None:           #Para os pontos e calculado quem possui maior numero de gols entre as duas
                                                        info[x[6]][0] = 0               #selecoes, caso o valor seja igual, um ponto e atribuido para cada selecao
                                                    elif info[x[6]][0] != None:         #, em outra situacao a selecao que ganou o confronto recebe tres pontos.
                                                        info[x[6]][0] += 0
                                                
                                                elif gols1 == gols2:
                                                    if info[x[2]][0] == None:
                                                        info[x[2]][0] = 1
                                                    elif info[x[2]][0] != None:
                                                        info[x[2]][0] += 1
                                                    if info[x[6]][0] == None:
                                                        info[x[6]][0] = 1
                                                    elif info[x[6]][0] != None:
                                                        info[x[6]][0] += 1
                                        
                                                elif gols2 > gols1:
                                                    if info[x[6]][0] == None:
                                                        info[x[6]][0] = 3
                                                    elif info[x[6]][0] != None:
                                                        info[x[6]][0] += 3
                                                    if info[x[2]][0] == None:
                                                        info[x[2]][0] = 0
                                                    elif info[x[2]][0] != None:
                                                        info[x[2]][0] += 0
                                                
                                                if info[x[2]][1] == None:
                                                        info[x[2]][1] = gols1           #Para os gols marcados soma-se o valor preexistente com o novo valor
                                                elif info[x[2]][1] != None:
                                                    info[x[2]][1] += gols1
                                                
                                                if info[x[6]][1] == None:
                                                        info[x[6]][1] = gols2
                                                elif info[x[6]][1] != None:
                                                    info[x[6]][1] += gols2
                                                
                                                if info[x[2]][2] == None:
                                                        info[x[2]][2] = gols1 - gols2  #O saldo de gols e calculado subtraindo o numero de gols de uma selecao pelo da 
                                                elif info[x[2]][2] != None:            #outra.
                                                    info[x[2]][2] += gols1 - gols2
                                                
                                                if info[x[6]][2] == None:
                                                        info[x[6]][2] = gols2 - gols1
                                                elif info[x[6]][2] != None:
                                                    info[x[6]][2] += gols2 - gols1      #x[2] e x[6] representam os indices em que as selecoes ficaram no .split
                                                                                        #No arquivo das tabelas a selecao e a chave de um dicionario de listas.
    print("\nRESULTADO CADASTRADO\n")                                                   #Cada indice da lista e atribuido a uma estatisca e estes sao alocados ao valor
    with open("out_files/Resultados.json",'w') as df:                                             #da selecao.
        json.dump(dados_resultados,df)                                                  #indice 0 => pontos, indice 1 => gols marcados e indice 2 => saldo de gols.
    with open("out_files/Tabela.json","w") as df_tabela:
        json.dump(dados_tabela,df_tabela)

def verifica_resultado(grupo,se1,se2,dados_resultados):
    '''Verifica se o resultado de um confronto ja nao esta cadastrado evitando que o usuario cometa um erro de cadastro
        -Parametros:
        Grupo que tera seu resultado cadastrado, duas selecoes que fazem parte do confronto e dados dos resultados
        -retorno:
        True caso o resultado esteja disponivel para cadastro
    '''
    for itens in dados_resultados:
        for chave in itens:
            if chave == grupo:
                for info in itens[chave]:
                    for chapa in info:
                        if se1 in chapa and se2 in chapa:
                            for atributos in info[chapa]:
                                if atributos["RESULTADO TIME 01"] == None and atributos["RESULTADO TIME 02"] == None:
                                    return True

def verifica_resultado_grupo(grupo,data):
    '''Verifica se todos os resultados dos confrontos de um grupo estao disponiveis para cadastro
        -Parametros:
        Grupo que tera seus resultados verificados e dados dos resultados
        -retorno:
        True caso todos os confrontos de um grupo estejam com seus resultados disponiveis para cadastro
    '''
    for itens in data:
        for chave in itens:
            if chave == grupo:
                for info in itens[chave]:
                    for chapa in info:
                        for atributos in info[chapa]:
                            if atributos["RESULTADO TIME 01"] == None and atributos["RESULTADO TIME 02"] == None:
                                return True

def exclui_resultado(grupo,se1,se2,dados_resultados,dados_tabela):
    '''exclui o resultado de um confronto
        -Parametros:
        Grupo que tera o resultado de um de seus confrontos excluido, as duas selecoes que fazem parte do confronto, dados dos resultados e da tabela
        -retorno:
        nenhum
    '''
    for itens in dados_resultados:
        for chave in itens:
            if chave == grupo:                      #Encontra o grupo
                for info in itens[chave]:
                    for chapa in info:
                        if se1  in chapa and se2 in chapa:          #Encontra o confronto com as duas selecoes
                            for atributos in info[chapa]:
                                x = chapa.split()
                                for itens in dados_tabela:
                                    for chave in itens:
                                        if chave == grupo:
                                            for info in itens[chave]:
                                                    
                                                if atributos['RESULTADO TIME 01'] > atributos['RESULTADO TIME 02']:  #Realiza o processo para diminuicao dos pontos,
                                                    info[x[2]][0] -= 3                                               #gols marcados e saldo
                                                
                                                elif atributos['RESULTADO TIME 01'] == atributos['RESULTADO TIME 02']:
                                                    info[x[2]][0] -= 1
                                                    info[x[6]][0] -= 1
                                                    
                                                elif atributos['RESULTADO TIME 01'] < atributos['RESULTADO TIME 02']:
                                                    info[x[6]][0] -= 3
                                                   
                                                info[x[2]][1] -= atributos['RESULTADO TIME 01']
                                                info[x[6]][1] -= atributos['RESULTADO TIME 02']
                                                
                                                info[x[2]][2] -= atributos['RESULTADO TIME 01'] - atributos['RESULTADO TIME 02']
                                                info[x[6]][2] -= atributos['RESULTADO TIME 02'] - atributos['RESULTADO TIME 01']
                                atributos["RESULTADO TIME 01"] = None         
                                atributos["RESULTADO TIME 02"] = None          #Apaga o resultado

    print("\nRESULTADO EXCLUIDO\n")
    with open("out_files/Resultados.json",'w') as df:
        json.dump(dados_resultados,df)
    with open("out_files/Tabela.json",'w') as df_tab:
        json.dump(dados_tabela,df_tab)

def soma_gols(grupo,dados_tabela):
    '''Soma todos os gols marcados em um grupo
        -Parametros:
        Grupo para soma dos gols e dados da tabela
        -retorno:
        Soma de todos os gols marcados no grupo
    '''
    soma_gols = 0
    for itens in dados_tabela:
        for chave in itens:
            if chave == grupo:
                for info in itens[chave]:
                    for selecoes in info:
                        soma_gols += info[selecoes][1]
    return soma_gols

def print_jogo_mais_gol(data,dados):
    '''Encontra o maior numero de gols marcado por uma selecao em um jogo
        -Parametros:
        Dados dos confrontos e dos resultados
        -retorno:
        Print jo jogo em que uma selecao fez mais gols, com dia, horario, local e resultado do jogo em que isso ocorreu
    '''
    maior = 0 
    for itens in data:
        for grupo in itens:
            for info in itens[grupo]:
                for confronto in info:
                    for resultados in info[confronto]:                  #Encontra o maior numero de gols em um confronto a partir dos resultados
                        if resultados['RESULTADO TIME 01'] > maior:
                            maior = resultados['RESULTADO TIME 01']
                        if resultados['RESULTADO TIME 02'] > maior:
                            maior = resultados['RESULTADO TIME 01']
                            
    for itens in data:
        for grupo in itens:
            for info in itens[grupo]:                                   #A partir do maior numero de gols encontrado, busca-se em que confronto esse valor 
                for confronto in info:                                  #surgiu exibindo o dia, horario e local do confronto. Em caso de empate a informacao
                    for resultados in info[confronto]:                  #continua sendo exibida sem incoerencias.
                        if resultados['RESULTADO TIME 01'] == maior or resultados['RESULTADO TIME 02'] == maior:
                            x = confronto.split()
                            for elementos in dados:
                                for chave in elementos:
                                    for confrontos in elementos[chave]:
                                        for chapa in confrontos:
                                            if x[2] in chapa and x[6] in chapa:
                                                print(confronto,"==>",confrontos[chapa],'RESULTADO ==>',resultados['RESULTADO TIME 01'],'X',resultados['RESULTADO TIME 02'])

def print_tabela_grupo(grupo,dados_tabela,escolha):
    '''Exibe em ordem as selecoes de um grupo com seus pontos, gols marcados e saldo
        -Parametros:
        Grupo que tera sua tabela exibida, dados da tabela e opcao escolhida pelo usuario no menu
        -retorno:
        Print da tabela caso esta seja a opcao escolhida pelo usuario, ou lista das selecoes por pontos, para formacao das oitavas
    '''
    dici_selecao = {}
    for itens in dados_tabela:
        for chave in itens:
            if chave == grupo:
                for info in itens[chave]:
                    for selecao in info:    #Encontra a selecao e atribui a um dicionario os pontos, saldo e gols marcados a aprtir da lista com os valores.
                        dici_selecao[selecao] = {"PONTOS": info[selecao][0],"SALDO DE GOLS":info[selecao][2],"GOLS MARCADOS":info[selecao][1]}

    ordenado_pontos = sorted(dici_selecao, key=lambda selecao: dici_selecao[selecao]["PONTOS"],reverse=True)
    ordenado_saldo = sorted(dici_selecao, key=lambda selecao: dici_selecao[selecao]["SALDO DE GOLS"],reverse=True)      #Ordenacao do dicionario
    ordenado_gols = sorted(dici_selecao, key=lambda selecao: dici_selecao[selecao]["GOLS MARCADOS"],reverse=True)

    if escolha == '4':

        print('\nORDEM DE PONTOS, GOLS E SALDO DO GRUPO {}'.format(grupo))
        print("\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n")  #print em ordem por cada atributo de cada selecao
        for i in range(len(ordenado_pontos)):
            print("{}° COLOCADO EM PONTOS ==> {} COM {} PONTOS".format(i+1,ordenado_pontos[i],dici_selecao[ordenado_pontos[i]]["PONTOS"]))
        print("\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n")
        for i in range(len(ordenado_saldo)):
            print("{}° COLOCADO EM SALDO DE GOLS ==> {} COM SALDO DE {} GOLS".format(i+1,ordenado_saldo[i],dici_selecao[ordenado_saldo[i]]["SALDO DE GOLS"]))
        print("\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n")
        for i in range(len(ordenado_gols)):
            print("{}° COLOCADO EM GOLS MARCADOS ==> {} COM {} GOLS".format(i+1,ordenado_gols[i],dici_selecao[ordenado_gols[i]]["GOLS MARCADOS"]))
        print("\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n")
    
    else:
        return ordenado_pontos

def formar_oitavas(lista1,lista2):
    '''Forma as oitavas a partir da lista ordenada das selecoes por pontos gerada na funcao acima
        -Parametros:
        Duas listas com as equipes de dois grupos ordenada
        -retorno:
        Print dos confrontos formados
    '''
    confronto1 = "{} X {}".format(lista1[0],lista2[1])  #Seguindo regra da FIFA, primeiro de uma lista com segundo da outra e segundo de uma com primeira da outra
    confronto2 = "{} X {}".format(lista1[1],lista2[0])
    print(confronto1)
    print("=============================")
    print(confronto2)

def oitavas():
    '''Gera as listas ordenadas com as selecoes pelo numero de pontos e chama a funcao para formacao das oitavas a apartir das listas geradas 
        -Parametros:
        nenhum
        -retorno:
        Print a aprtir da funcao formar oitavas
    '''
    with open("out_files/Tabela.json",'r') as arq:
        df = json.load(arq)
    pa = print_tabela_grupo("A",df,0)
    pb = print_tabela_grupo("B",df,0)
    pc = print_tabela_grupo("C",df,0)
    pd = print_tabela_grupo("D",df,0)
    pe = print_tabela_grupo("E",df,0)
    pf = print_tabela_grupo("F",df,0)
    pg = print_tabela_grupo("G",df,0)
    ph = print_tabela_grupo("H",df,0)

    formar_oitavas(pa,pb)
    formar_oitavas(pc,pd)
    formar_oitavas(pe,pf)
    formar_oitavas(pg,ph)

def escolha_grupo(lista):
    '''Funcao em que o usuario escolhe o grupo para a utilizacao nos mais diversos menus
        -Parametros:
        lista dos grupos para verificacao
        -retorno:
        grupo escolhido
    '''
    grupo = input("ESCOLHA O GRUPO:").upper().strip()
    while grupo not in lista:
        grupo = input("GRUPO INVALIDO ==> ESCOLHA O GRUPO:").upper().strip()
    return grupo

def leitura_dos_arquivos(arquivo):
    '''Realiza leitura dos dados de um arquivo
        -Parametros:
        Arquivo que sera carregado
        -retorno:
        dados do arquivo
    '''
    with open(arquivo, 'r+') as arq:
        dados = json.load(arq)
    return dados

#Declaracao das variaveis, listas e dicionarios utilizados ao longo do programa
menu_resultado = 2 ; cont = 3 ; tabelao = {} ; escolha_atributo = 4 ; lista_grupos_confrontos = [] ; escolha = 2 ; resultado = {}  ; confronto = {} ; cadastro = 0 ;cadastro_confrontos = 0 ; agrupamento = {} ; lista_selecoes = [] ; opcao = 3 ; lista_grupos = [] ; lista_grupos_parcial = [] ; lista_selecoes = [] ; lista_selecoes_parcial = [] ; edicao = 5
#lista dos grupos oficiais para controle
grupos_oficiais = ['A','B','C','D','E','F','G','H']

print(" "*25,'BEM VINDO AO COPA+\n')
print("\nAVISO IMPORTANTE >>>>>> SELECOES COM MAIS DE UMA PALAVRA EM SEU NOME, EXEMPLO: ESTADOS UNIDOS, DEVEM SER CADASTRADAS SEM O ESPACO\nEXEMPLO => ESTADOSUNIDOS")
print("\nCASO ALGUM ATRIBUTO OU RESULTADO ESTEJA COM UM 'NONE', SIGNIFICA QUE ESTA INFORMACAO ESTA NULA\n")
print(" "*8,'>>>>APOS QUALQUER ACAO FEITA NO MENU DOS GRUPOS O PROGRAMA DEVE SER REINICIADO<<<<\n')
#Menu inicial com sete opcoes disponiveis
while True:
    print(" "*22,"ESCOLHA UMA OPCAO ABAIXO\n")
    print('[1] MENU DOS GRUPOS\n[2] MENU DOS JOGOS\n[3] MENU DOS RESULTADOS\n[4] VISUALIZAR TABELA\n[5] ESTATISTICAS DA PRIMEIRA FASE\n[6] OITAVAS DE FINAL\n[7] SAIR')
    opcao = input("\nQUAL OPCAO DESEJA SEGUIR: ").strip()

    if opcao == '1':
        #Opcao dos grupos carrega os dados do arquivo dos grupos e carrega as listas com os grupos e selecoes cadastrados para controle
        dados_grupos = leitura_dos_arquivos("out_files/Grupos.json")
    
        lista_grupos.clear()       #Lista e zerada para evitar erros nas informacoes
        lista_selecoes.clear()

        for info in dados_grupos:
            for chaves in info:
                lista_grupos.append(chaves)
                for selecoes in info[chaves]:
                    lista_selecoes.append(selecoes)

        print('\n',' '*23,'BEM VINDO AO CADASTRAMENTO DOS GRUPOS DA COPA DO MUNDO FIFA 2022')
        while cadastro != '4':
            print("\n[1] CADASTRAR GRUPOS\n[2] EDITAR GRUPO\n[3] EXCLUIR GRUPO\n[4] SAIR DO CADASTRO")
            cadastro = input("\nQUAL OPCAO DESEJA ACESSAR:\n").strip()

#Caso a opcao seja a de cadastro e ainda exista grupos faltantes para cadastramento ele sera redirecionado para os inputs de cadastro
            if cadastro == '1' and len(lista_grupos) < 9:

                while cont != '2':
                    print("\nDESEJA SEGUIR ==> [1] SIM | [2] NAO\n")   #O usuario tem a opcao de continuar o cadastro ou sair 
                    cont = input("Digite uma opcao acima:")

                    if cont == '1':

#Classe e tupla das equipes sao declaradas
                        e = Equipes()
                        tupla = ()

#Print com os grupos que ja foram cadastrados anteriomente e os que estao sendo cadastrados atualmente colocado
                        print('\nGRUPOS CADASTRADOS: {}\n'.format(lista_grupos))
                        print('ULTIMOS CADASTROS: {}\n'.format(lista_grupos_parcial))

#Inputs para escolha dos grupos e selecoes com whiles de verificacao que evitam a repeticao do cadastro
                        e.grupo = input("Grupo: ").upper().strip()
                        while e.grupo in lista_grupos or e.grupo in lista_grupos_parcial or e.grupo not in grupos_oficiais:
                            e.grupo = input("\nGRUPO INVALIDO: Qual grupo deseja cadastrar =>").upper().strip()
                        lista_grupos_parcial.append(e.grupo)
                        
                        e.t1 = input("\nPRIMEIRA SELECAO: ").upper().strip()
                        while e.t1 in lista_selecoes or e.t1 in lista_selecoes_parcial:
                            e.t1 = input("\nSELECAO ESCOLHIDA JA FOI CADASTRADA: Qual selecao deseja cadastrar =>").upper().strip()
                        lista_selecoes_parcial.append(e.t1)
                        
                        e.t2 = input("\nSEGUNDA SELECAO: ").upper().strip()
                        while e.t2 in lista_selecoes or e.t2 in lista_selecoes_parcial:
                            e.t2 = input("\nSELECAO ESCOLHIDA JA FOI CADASTRADA: Qual selecao deseja cadastrar =>").upper().strip()
                        lista_selecoes_parcial.append(e.t2)

                        e.t3= input("\nTERCEIRA SELECAO: ").upper().strip()
                        while e.t3 in lista_selecoes or e.t3 in lista_selecoes_parcial:
                            e.t3= input("\nSELECAO ESCOLHIDA JA FOI CADASTRADA: Qual selecao deseja cadastrar =>").upper().strip()
                        lista_selecoes_parcial.append(e.t3)
                        
                        e.t4 = input("\nQUARTA SELECAO: ").upper().strip()
                        while e.t4 in lista_selecoes or e.t4 in lista_selecoes_parcial:
                            e.t4 = input("\nSELECAO ESCOLHIDA JA FOI CADASTRADA: Qual selecao deseja cadastrar =>").upper().strip()
                        lista_selecoes_parcial.append(e.t4)

#tupla e carregada com as quatro selecoes e dicionario que tem como chave o grupo e valor a tupla e gerado                   
                        tupla = (e.t1,e.t2,e.t3,e.t4) 
                        agrupamento[e.grupo] = tupla

#A lista para o arquivo tabela e gerada, preenchida com um dicionario que tem como chave a selecao e valor uma lista com valores 
#nulos que recebera os pontos, gols marcados e saldo de gols de cada equipe
                        lista_tabela = [{e.t1:[None,None,None],e.t2:[None,None,None],e.t3:[None,None,None],e.t4:[None,None,None]}]
                        tabelao[e.grupo] = lista_tabela

#Os dicionarios que armazenam o confronto com o resultado sao gerados, possuindo como chave as duas equipes do confronto e valor uma lista de dicionarios que possui
#como chave o resultado de cada equipe e valor o numero de gols correspondente ao resultado
                        resultado1 = {"TIME 01: {} VS TIME 02: {}".format(e.t1,e.t2): [{"RESULTADO TIME 01": None,"RESULTADO TIME 02": None}]}
                        resultado2 = {"TIME 01: {} VS TIME 02: {}".format(e.t1,e.t3): [{"RESULTADO TIME 01": None,"RESULTADO TIME 02": None}]}
                        resultado3 = {"TIME 01: {} VS TIME 02: {}".format(e.t1,e.t4): [{"RESULTADO TIME 01": None,"RESULTADO TIME 02": None}]}
                        resultado4 = {"TIME 01: {} VS TIME 02: {}".format(e.t2,e.t3): [{"RESULTADO TIME 01": None,"RESULTADO TIME 02": None}]}
                        resultado5 = {"TIME 01: {} VS TIME 02: {}".format(e.t2,e.t4): [{"RESULTADO TIME 01": None,"RESULTADO TIME 02": None}]}
                        resultado6 = {"TIME 01: {} VS TIME 02: {}".format(e.t3,e.t4): [{"RESULTADO TIME 01": None,"RESULTADO TIME 02": None}]}
#uma lista recebe os dicionarios de confrontos gerados e um dicionario que tem como chave o grupo recebe a lista de confrontos como valor                      
                        lista_resultados = [resultado1,resultado2,resultado3,resultado4,resultado5,resultado6]
                        resultado[e.grupo] = lista_resultados

#Os dicionarios que armazenam os confrontos com as informacoes de dia, horario e local de cada um e gerado nos mesmos moldes do formato anterior
                        confronto1 = {"{} VS {}".format(e.t1,e.t2): [{"DIA": None,"LOCAL": None,"HORARIO": None}]}
                        confronto2 = {"{} VS {}".format(e.t1,e.t3): [{"DIA": None,"LOCAL": None,"HORARIO": None}]}
                        confronto3 = {"{} VS {}".format(e.t1,e.t4): [{"DIA": None,"LOCAL": None,"HORARIO": None}]}
                        confronto4 = {"{} VS {}".format(e.t2,e.t3): [{"DIA": None,"LOCAL": None,"HORARIO": None}]}
                        confronto5 = {"{} VS {}".format(e.t2,e.t4): [{"DIA": None,"LOCAL": None,"HORARIO": None}]}
                        confronto6 = {"{} VS {}".format(e.t3,e.t4): [{"DIA": None,"LOCAL": None,"HORARIO": None}]}
                        lista_confrontos = [confronto1,confronto2,confronto3,confronto4,confronto5,confronto6]
                        confronto[e.grupo] = lista_confrontos

#Caso o len da lista de grupos chegue a 9, 8 grupos + 1 coringa gerado automaticamente pelo arquivo o cadastro e encerrado
                        if len(lista_grupos) + len(lista_grupos_parcial) == 9:
                            print(' '*25,"\nTODOS OS GRUPOS FORAM CADASTRADOS")
                            break

#caso o usuario escolha a opcao de cadastro mas todos os grupos ja estejam cadastrados, ou seja, len de lista grupos = 9, o usuario sera avisado
            elif cadastro == '1' and len(lista_grupos) == 9:    
                print("\n"," "*25,"TODOS OS GRUPOS ESTAO CADASTRADOS")

            elif cadastro == '2':

#Neste menu o usuario podera editar uma selecao em um grupo 
                if len(lista_grupos) > 1:
                    print(" "*20,'VOCE ESCOLHERA UM GRUPO, UM TIME PARA SAIR E OUTRO PARA ENTRAR NESSE GRUPO:\n')
                    print('LISTA DOS GRUPOS CADASTRADOS:\n')
                    for gp in lista_grupos:
                        print(gp,end=' ')
                    print(" ")
                    print(" ")
                    
#O usuario escolhe o grupo em que fara a alteracao a partir da funcao escolha grupo que realiza este controle                   
                    grupo = escolha_grupo(lista_grupos)
                    print("\n>>>NAO É PERMITIDO A ESCOLHA DE UMA SELECAO QUE JA ESTA INSERIDA EM UM GRUPO<<<\n")
                    
#Sera escolhido um time para entrar no grupo, este nao podera ser igual a um time que ja foi cadastrado                   
                    time_entrar = input("\nSELECAO QUE SERA INSERIDA NO GRUPO:").upper().strip()
                    while time_entrar in lista_selecoes:
                        time_entrar = input("\nSELECAO INVALIDA => DIGITE A SELECAO QUE SERA INSERIDA NO GRUPO:").upper().strip()
                    lista_selecoes.append(time_entrar)

#Sera escolhido um time para sair do0 grupo, este deve estar inserido no grupo para ser retirado, lista de verificacao e gerada para esta verificacao                    
                    lista_verificacao = verifica_time_edicao(grupo,dados_grupos)
                    print("\nSELECOES DISPONIVEIS NO GRUPO ==> {}\n".format(lista_verificacao))
                    time_sair = input("\nSELECAO QUE SERA RETIRADA DO GRUPO:").upper().strip()
                    while time_sair not in lista_verificacao:
                        time_sair = input("\nSELECAO INVALIDA => DIGITE A SELECAO QUE SERA RETIRADA DO GRUPO:").upper().strip()
                    lista_selecoes.remove(time_sair)

#Funcao editar grupo realiza a acao
                    editar_grupo(grupo,time_sair,time_entrar)
                    print("\n>>>ALTERACAO REALIZADA<<<")

                else:
                    print(" "*20,">>>>NAO EXISTEM GRUPOS PARA EDITAR<<<<")

            elif cadastro == '3':

#Menu para excluir um grupo cadastrado, usuario so pode fazer isso caso o len da lista grupos dseja maior que, o que significa que existe um grupo para excluir
                if len(lista_grupos) > 1:
                    print(" "*44,"MENU PARA EXCLUIR GRUPO\n")
                    print(lista_grupos)
                    
                    grupo_excluir = escolha_grupo(lista_grupos)

                    excluir_grupo(grupo_excluir)
                    print("\nGRUPO {} REMOVIDO\n".format(grupo_excluir))
                
                else:
                    print(" "*20,">>>>NAO EXISTEM GRUPOS PARA REMOVER<<<<")
        
        if agrupamento != {}:
            preencher_arquivo("out_files/Grupos.json",agrupamento)       #Informacoes de cadastro da opcao 1 ficam alocadas em memoria enquanto o usuario desejar continuar o 
            preencher_arquivo("out_files/Confrontos.json",confronto)     #cadastro, ao sair do while as informacoes sao colocadas a disposicao para as funcoes que preenchem
            preencher_arquivo("out_files/Resultados.json",resultado)     #os arquivos, isto so ocorre caso exista um conteudo no dicionario dos grupos, evitando que informacoes
            preencher_arquivo("out_files/Tabela.json",tabelao)           #vazias cheguem ao arquivo

    elif opcao == '2':
        
        dados_grupos = leitura_dos_arquivos("Grupos.json")   #Acesso ao menu dos jogos que estara disponivel assim que pelo menos um grupo esteja cadastrado
    
        lista_grupos.clear()
        lista_selecoes.clear()

        for info in dados_grupos:
            for chaves in info:
                lista_grupos.append(chaves)                 #Lista com os grupos e selecoes e carregada para verificacoes
                for selecoes in info[chaves]:
                    lista_selecoes.append(selecoes)

        if len(lista_grupos) > 1:     #Verificacao para descobrir se existem grupos cadastrados
            
            print(" "*32,'BEM VINDO AO MENU DOS JOGOS\n')
            print(" "*35,"ESCOLHA UMA OPCAO ABAIXO\n")
            while cadastro_confrontos != '5':
                print("\n[1] VISUALIZAR CONFRONTOS\n[2] CADASTRAR INFORMACOES DOS CONFRONTOS\n[3] EDITAR INFORMACOES DOS CONFRONTOS\n[4] EXCLUIR INFORMACOES DOS CONFRONTOS\n[5] SAIR ")
                cadastro_confrontos = input("\nDIGITE A OPCAO QUE DESEJA SEGUIR: ")

                dados_confrontos = leitura_dos_arquivos("out_files/Confrontos.json")

                r1 = calculo_verificacao_confrontos("A",dados_confrontos) ; r2 = calculo_verificacao_confrontos("B",dados_confrontos) ; r3 = calculo_verificacao_confrontos("C",dados_confrontos) ; r4 = calculo_verificacao_confrontos("D",dados_confrontos) ; r5 = calculo_verificacao_confrontos("E",dados_confrontos) ; r6 = calculo_verificacao_confrontos("F",dados_confrontos) ; r7 = calculo_verificacao_confrontos("G",dados_confrontos); r8 = calculo_verificacao_confrontos("H",dados_confrontos)
                soma_de_verificacao = r1+r2+r3+r4+r5+r6+r7+r8
                #Uma funcao de soma e usada para verificar quantos cadastro de dia, horario e local ja foram feitos
                print(" ")

                if cadastro_confrontos == '1':
                    print('LISTA DOS GRUPOS CADASTRADOS:\n')
                    for gp in lista_grupos:                                             #Para visualizacao dos confrontos o usuario escolhe o grupo que
                        print(gp,end=' ')                                               #para exibir seus confrontos
                    grupo_visualizar_confronto = escolha_grupo(lista_grupos)
                    print(" ")
                    print_confronto(grupo_visualizar_confronto,dados_confrontos)

                elif cadastro_confrontos == '2':
                    
                    if soma_de_verificacao < 48:
                        print("\nNESTA SECAO VOCE IRA CADASTRAR O DIA, HORARIO E LOCAL DOS JOGOS \n\nAVISO ===> VOCE ESCOLHERA UM GRUPO E IRA REALAZIR O CADASTRO DOS SEIS CONFRONTOS UMA UNICA VEZ\n")
                        print("\nCASO O GRUPO ESCOLHIDO JA TENHA AS INFORMACOES PREENCHIDAS, VOCE SERA AVISADO")
                        print(" ")
                        print('LISTA DOS GRUPOS CADASTRADOS:\n')
                        for gp in lista_grupos:                                                #Caso a soma de verificacao seja menor que 48, e permitido o acesso
                            print(gp,end=' ')                                                  #ao cadastro dos confrontos, pois ainda existes informacoes faltantes
                        
                        grupo_cadastrar_confronto = escolha_grupo(lista_grupos)

                        cadastro_informacoes_confrontos(grupo_cadastrar_confronto,dados_confrontos)
                    
                    else:
                        print("\n>>>>TODOS OS CONFRONTOS ESTAO CADASTRADOS<<<<")             #O usuario e avisado caso todos os confrontos estejam com os seus dias,
                                                                                             #horarios e locais preenchidos
                elif cadastro_confrontos == '3':
                    print("\nNESTA SECAO VOCE IRA EDITAR UM CONFRONTO PREVIAMENTE PREENCHIDO")
                    print(" ")
                    print('LISTA DOS GRUPOS CADASTRADOS:\n')
                    for gp in lista_grupos:                                                         #Neste menu o usuario ira editar um atributo de um confronto(dia,horario,
                        print(gp,end=' ')                                                           #local), escolhendo o grupo e as duas selecoes que fazem parte do confronto
                                                                                                    #que tera seu atributo editado
                    confronto_edicao = escolha_grupo(lista_grupos)
                    print(" ")
                    if verifica_preenchimento(confronto_edicao,dados_confrontos):
                        print_confronto(confronto_edicao,dados_confrontos)
                        
                        lista_verificacao2 = verifica_time_edicao(confronto_edicao,dados_grupos)

                        print("\nESCOLHA O CONFRONTO QUE DESEJA MODIFICAR PELO NOME DAS SELECOES ===>")
                        print("\nDIGITE O NOME DAS SELECOES QUE FAZEM DO CONFRONTO:")
                        
                        selecao_1 = input("\nDigite o nome da selecao 1:").upper().strip()
                        while selecao_1 not in lista_verificacao2:
                            selecao_1 = input("\nSELECAO NAO LISTADA NOS CONFRONTOS ==> Informe uma selecao valida: ").upper().strip()
                        
                        selecao_2 = input("\nDigite o nome da selecao 2:").upper().strip()
                        while selecao_2 not in lista_verificacao2:
                            selecao_2 = input("\nSELECAO NAO LISTADA NOS CONFRONTOS ==> Informe uma selecao valida: ").upper().strip()

                        print("ESCOLHA O ATRIBUTO DO CONFRONTO QUE IRA EDITAR:")
                        while escolha_atributo != '1' and escolha_atributo != "2" and escolha_atributo != "3":
                            print("\n[1] DIA\n[2] HORARIO\n[3] LOCAL\n")
                            escolha_atributo = input("Qual atributo ira modificar no confronto: ")

#O usuario escolhera qual atributo sera modificado e qual seraa a nova informacao atribuida a ele
#A funcao realiza edicao do confronto e chamada para realizar esta acao
                            if escolha_atributo == '1':
                                modificador = 'DIA'
                                novo_dia = input("\nQual sera o novo dia para a partida: ").strip()
                                realizar_edicao_do_confronto(selecao_1,selecao_2,modificador,novo_dia,confronto_edicao,dados_confrontos)
                                print("\n>>>MODIFICACAO REALIZADA COM SUCESSO<<<\n")
                            
                            elif escolha_atributo == '2':
                                modificador = 'HORARIO'
                                novo_horario = input("\nQual sera o novo horario do confronto: ").strip()
                                realizar_edicao_do_confronto(selecao_1,selecao_2,modificador,novo_horario,confronto_edicao,dados_confrontos)
                                print("\n>>>MODIFICACAO REALIZADA COM SUCESSO<<<\n")
                            
                            elif escolha_atributo == '3':
                                modificador = 'LOCAL'
                                novo_local = input("\nQual o novo local do confronto:").upper().strip()
                                realizar_edicao_do_confronto(selecao_1,selecao_2,modificador,novo_local,confronto_edicao,dados_confrontos)
                                print("\n>>>MODIFICACAO REALIZADA COM SUCESSO<<<\n")

#A funcao verifica preenchimento informa se o cadastro de um grupo esta pendente ,evitando que o usuario edite algo que nao exista
                    else:
                        print("\nO GRUPO INFORMADO POSSUI CADASTRO PENDENTE NOS CONFRONTOS")
                
                elif cadastro_confrontos == '4':

#Neste menu o usuario pode apagar o dia,horario e local de um confronto ou de todos os confrontos de um grupo                   
                    print("\nVOCE IRA EXCLUIR DADOS REFERENTES AO CONFRONTO DE UM GRUPO")
                    print("\nEXISTEM DUAS FORMAS DE FAZER ESTA ACAO ==>\n")
                    print(" "*35,'>>>APAGAR TODOS OS ATRIBUTOS DE TODOS OS CONFRONTOS REFERENTES A UM GRUPO\n\n')
                    print(" "*35,'>>>APAGAR DADOS DE APENAS UM CONFRONTO')
                    print('\nDIGITE A OPCAO PARA SEGUIR EM FRENTE =>')
                    print("\n[1] APAGAR DADOS DE TODOS OS CONFRONTO DO GRUPO\n[2] APAGAR DADOS DE APENAS UM CONFRONTO")
                    
                    opcao_exclusao = input("\nDIGITE A OPCAO EM QUE DESEJA SEGUIR:")
                    while opcao_exclusao != '1' and opcao_exclusao != "2":                                         #Escolha do tipo de exclusao
                        opcao_exclusao = input("\nOPCAO INVALIDA ===> DIGITE A OPCAO EM QUE DESEJA SEGUIR:")
                    
                    if opcao_exclusao =='1':
                        print("\nESCOLHA O GRUPO QUE TERA OS DADOS DE SEUS CONFRONTOS EXCLUIDOS:\n")
                        print(" ")
                        
                        print('LISTA DOS GRUPOS CADASTRADOS:\n')
                        for gp in lista_grupos:                                                     
                            print(gp,end=' ')                                   #Escolhe o grupo que tera todos as informacoes de seus confrontos apagadas
                        
                        grupo_confronto_exclusao = escolha_grupo(lista_grupos)
                        
                        if verifica_preenchimento(grupo_confronto_exclusao,dados_confrontos):
                            print(" ")
                            print_confronto(grupo_confronto_exclusao,dados_confrontos)          #Verifica-se o grupo possui seus confrontos cadastrados, se sim
                                                                                                #a exclusao e feita mostrando o antes e depois.Caso o cadastro
                            excluir_dados_confrontos(grupo_confronto_exclusao,dados_confrontos) #esteja pendente o usuario sera avisado

                            print(" ")
                            print_confronto(grupo_confronto_exclusao,dados_confrontos)
                        
                        else:
                            print("\n>>>>O GRUPO INFORMADO POSSUI CADASTRO PENDENTE NOS CONFRONTOS<<<<")
                    
                    elif opcao_exclusao == '2':
                        print("\nESCOLHA O GRUPO QUE TERA OS DADOS DE APENAS UM DE SEUS CONFRONTOS EXCLUIDOS:\n")
                        print(" ")
                        
                        print('LISTA DOS GRUPOS CADASTRADOS:\n')
                        for gp in lista_grupos:
                            print(gp,end=' ')
                        
                        grupo_confronto_exclusao = escolha_grupo(lista_grupos)                              #Escolhendo apagar as informacoes de apenas um confronto
                                                                                                            #ele escolhera o grupo e as duas selecoes que fazem parte
                        if verifica_preenchimento(grupo_confronto_exclusao,dados_confrontos):               #do confronto que tera seus atributos apagados

                            lista_verificacao2 = verifica_time_edicao(grupo_confronto_exclusao,dados_grupos)

                            print(" ")
                            print_confronto(grupo_confronto_exclusao,dados_confrontos)

                            print("\nESCOLHA O CONFRONTO QUE DESEJA MODIFICAR PELO NOME DAS SELECOES ===>")
                            print("\nDIGITE O NOME DAS SELECOES QUE FAZEM DO CONFRONTO:")
                            
                            selecao_1 = input("\nDigite o nome da selecao 1:").upper().strip()
                            while selecao_1 not in lista_verificacao2:
                                selecao_1 = input("\nSELECAO NAO LISTADA NOS CONFRONTOS ==> Informe uma selecao valida: ").upper().strip()
                            
                            selecao_2 = input("\nDigite o nome da selecao 2:").upper().strip()
                            while selecao_2 not in lista_verificacao2:
                                selecao_2 = input("\nSELECAO NAO LISTADA NOS CONFRONTOS ==> Informe uma selecao valida: ").upper().strip()
                            
                            excluir_dados_de_um_confronto(selecao_1,selecao_2,grupo_confronto_exclusao,dados_confrontos)

                            print(" ")                                                          #Exclusao e feita e resultado e mostrado
                            print_confronto(grupo_confronto_exclusao,dados_confrontos)
                        
                        else:
                            print("\n>>>>O GRUPO INFORMADO POSSUI CADASTRO PENDENTE NOS CONFRONTOS<<<<")
        else:
            print("\n=====>>> DISPONIVEL APENAS COM O CADASTRAMENTO DE PELO MENOS UM GRUPO\n")
            
    elif opcao == '3':
        
#Menu para cadastro dos resultados de cada confronto      
        dados_grupos = leitura_dos_arquivos("out_files/Grupos.json")
        dados_confrontos = leitura_dos_arquivos("out_files/Confrontos.json")  #Dados de todos os arquivos sao carregados para verificaoes futuras no menu
        dados_resultados = leitura_dos_arquivos("out_files/Resultados.json")
        dados_tabela = leitura_dos_arquivos("out_files/Tabela.json")

        r1 = calculo_verificacao_confrontos("A",dados_confrontos) ; r2 = calculo_verificacao_confrontos("B",dados_confrontos) ; r3 = calculo_verificacao_confrontos("C",dados_confrontos) ; r4 = calculo_verificacao_confrontos("D",dados_confrontos) ; r5 = calculo_verificacao_confrontos("E",dados_confrontos) ; r6 = calculo_verificacao_confrontos("F",dados_confrontos) ; r7 = calculo_verificacao_confrontos("G",dados_confrontos); r8 = calculo_verificacao_confrontos("H",dados_confrontos)
        soma_de_verificacao = r1+r2+r3+r4+r5+r6+r7+r8
        
        if soma_de_verificacao == 48:   #Verificacao para atestar que todos os confrontos estao com seus dias, horarios e locais 
                                        #preenchidos, permitindo o cadastro dos resultados          
            print("\nMENU PARA CADASTRO DOS RESULTADOS DOS JOGOS\n")
            print('\nVOCE PODERA CADASTRAR OU EXCLUIR O RESULTADO DOS CONFRONTOS\n')
            print("\nA EDICAO DE UM RESULTADO NAO É PERMITIDA AINDA\n")

            while menu_resultado != '4':
                print("\n[1] CADASTRAR RESULTADO\n[2] EXCLUIR RESULTADO\n[3] VISUALIZAR RESULTADOS\n[4] SAIR")
                menu_resultado = input("\n==> QUAL OPCAO DESEJA SEGUIR:")

                lista_grupos.clear()
                lista_selecoes.clear()

                for info in dados_grupos:             #Lista com os grupos e selecoes e carregada para verificacoes
                    for chaves in info:
                        lista_grupos.append(chaves)
                        for selecoes in info[chaves]:
                            lista_selecoes.append(selecoes)

                if menu_resultado == '1':
                    
                    print('LISTA DOS GRUPOS CADASTRADOS:\n')
                    for gp in lista_grupos:
                        print(gp,end=' ')                                                   
                    
                    print('\nO CADASTRO DO RESULTADO DOS JOGOS SERA FEITO ====>>>\n')
                    
                    grupo_cadastra_resultado = escolha_grupo(lista_grupos)      #usuario escolhe qual grupo tera o resultado de um de seus confrontos cadastrado
                    
                    if verifica_resultado_grupo(grupo_cadastra_resultado,dados_resultados):  #verifica-se o preenchimento de todos os resultados do grupo escolhido
                        print(" ")                                                           #,caso tudo esteja preenchido no grupo, o usuario sera avisado
                        print_confronto(grupo_cadastra_resultado,dados_confrontos)
                        
                        lista_verificacao3 = verifica_time_edicao(grupo_cadastra_resultado,dados_grupos)
                        
                        print("\nESCOLHA AS DUAS SELECOES QUE FAZEM PARTE DO CONFRONTO PARA CADASTRAR O RESULTADO:")
                        print("\nSELECOES QUE FAZEM PARTE DO GRUPO {} >>>\n".format(grupo_cadastra_resultado))
                        print(lista_verificacao3)
                        print(" ")

                        selecao1_cadastrar_resultado = input("\nPRIMEIRA SELECAO:\n").upper().strip()            #Escolha das duas selecoes do confronto
                        while selecao1_cadastrar_resultado not in lista_verificacao3:
                            selecao1_cadastrar_resultado = input("\nSELECAO INVALIDA ==> PRIMEIRA SELECAO:\n").upper().strip()
                        
                        selecao2_cadastrar_resultado = input("\nSEGUNDA SELECAO:\n").upper().strip()
                        while selecao2_cadastrar_resultado not in lista_verificacao3:
                            selecao2_cadastrar_resultado = input("\nSELECAO INVALIDA ==> SEGUNDA SELECAO:\n").upper().strip()

#Uma nova verificacao e feita para verificar se o resultado entre as duas selecoes escolhiidas ja nao foi preenchido, caso esteja, o usuario sera avisado
                        if verifica_resultado(grupo_cadastra_resultado,selecao1_cadastrar_resultado,selecao2_cadastrar_resultado,dados_resultados):
                            cadastra_resultado(grupo_cadastra_resultado,selecao1_cadastrar_resultado,selecao2_cadastrar_resultado,dados_resultados,dados_tabela)
                        
                        else:
                            print("\n >>> O RESULTADO ENTRE {} E {} JA FOI CADASTRADO <<<".format(selecao1_cadastrar_resultado,selecao2_cadastrar_resultado))
                    
                    else:
                        print("\nTODOS OS CONFRONTOS DO GRUPO {} ESTAO COM SEUS RESULTADOS CADASTRADOS".format(grupo_cadastra_resultado))

#Usuario podera escolher um confronto que tera os seus resultados excluidos
                elif menu_resultado == '2':
                    print("\nMENU PARA EXCLUSAO DE UM RESULTADO")
                    print("\nESCOLHA O GRUPO QUE TERA O RESULTADO DE UM DE SEUS CONFRONTOS EXCLUIDO:")
                    print('\nLISTA DOS GRUPOS CADASTRADOS:\n')
                    for gp in lista_grupos:
                        print(gp,end=' ')
                    print(" ")
                    print(" ")
                    grupo_excluir_resultado = escolha_grupo(lista_grupos)       #grupo e escolhido

                    lista_verificacao5 = verifica_time_edicao(grupo_excluir_resultado,dados_grupos)

                    print_resultado(grupo_excluir_resultado,dados_resultados)

                    print("\nESCOLHA AS DUAS SELECOES QUE FAZEM PARTE DO CONFRONTO PARA EXCLUSAO DO RESULTADO:")
                    print("\nSELECOES QUE FAZEM PARTE DO GRUPO {} >>>\n".format(grupo_excluir_resultado))
                    print(lista_verificacao5)
                    print(" ")

                    selecao1_excluir_resultado = input("\nPRIMEIRA SELECAO:\n").upper().strip()
                    while selecao1_excluir_resultado not in lista_verificacao5:                                             #as duas selecoes que fazem parte do confronto
                        selecao1_excluir_resultado = input("\nSELECAO INVALIDA ==> PRIMEIRA SELECAO:\n").upper().strip()    #sao escolhidas
                    
                    selecao2_excluir_resultado = input("\nSEGUNDA SELECAO:\n").upper().strip()
                    while selecao2_excluir_resultado not in lista_verificacao5:
                        selecao2_excluir_resultado = input("\nSELECAO INVALIDA ==> SEGUNDA SELECAO:\n").upper().strip()
                    
                    if verifica_resultado(grupo_excluir_resultado,selecao1_excluir_resultado,selecao2_excluir_resultado,dados_resultados):   #Verifica-se o preenchimeto
                        print("\nO CONFRONTO NAO POSSUI CADASTRO PARA EXCLUIR")                                                              #do resultado para atestar
                                                                                                                                             #exclusao
                    else:
                        exclui_resultado(grupo_excluir_resultado,selecao1_excluir_resultado,selecao2_excluir_resultado,dados_resultados,dados_tabela)
                
                elif menu_resultado == '3':
                    print("\nVISUALIZACAO DO RESULTADOS DOS CONFRONTOS ==>> AVISO:CASO O RESULTADO NAO ESTEJA CADASTRADO A PALAVRA >> NONE << SERA EXIBIDA\n")
                    print("GRUPOS ==>\n ")
                    print(lista_grupos)
                    print(" ")                  
                    grupo_visualizar_resultado = escolha_grupo(lista_grupos)    #Usuario escolhera um grupo para visualizar os resultados de todos os confrontos do grupo.
                    print(" ")
                    print_resultado(grupo_visualizar_resultado,dados_resultados)

        else:
            print("\nO CADASTRO DOS RESULTADOS ESTARA APENAS DISPONIVEL COM O PREENCHIMENTO DE DADOS EM TODOS OS CONFRONTOS\n")
            
    elif opcao == '4':
        dados_grupos = leitura_dos_arquivos("out_files/Grupos.json")
        dados_confrontos = leitura_dos_arquivos("out_files/Confrontos.json")   #Arquivos sao carregados
        dados_resultados = leitura_dos_arquivos("out_files/Resultados.json")
        dados_tabela = leitura_dos_arquivos("out_files/Tabela.json")

#calculo de verificacao e feito para permitir que o usuario visualize as tabelas apenas com o cadastramento de todos os resultados
        rj1 = calculo_verificacao_resultados("A",dados_resultados) ; rj2 = calculo_verificacao_resultados("B",dados_resultados) ; rj3 = calculo_verificacao_resultados("C",dados_resultados) ; rj4 = calculo_verificacao_resultados("D",dados_resultados) ; rj5 = calculo_verificacao_resultados("E",dados_resultados) ; rj6 = calculo_verificacao_resultados("F",dados_resultados) ; rj7 = calculo_verificacao_resultados("G",dados_resultados); rj8 = calculo_verificacao_resultados("H",dados_resultados)
        soma_de_verificacao_resultados = rj1+rj2+rj3+rj4+rj5+rj6+rj7+rj8
        lista_grupos.clear()
        lista_selecoes.clear()

        for info in dados_grupos:
            for chaves in info:
                lista_grupos.append(chaves)
                for selecoes in info[chaves]:
                    lista_selecoes.append(selecoes)

        if soma_de_verificacao_resultados == 48:    #Caso todos os resultados estejam cadastrados, a visualizacao das tabelas e permitida
            
            print("\nVOCE PODERA VISUALIZAR A TABELA CONTENDO OS PONTOS - SALDO DE GOLS E GOLS MARCADOS DE UM GRUPO\n")
            print('\nLISTA DOS GRUPOS CADASTRADOS:\n')
            for gp in lista_grupos:
                print(gp,end=' ')                           #Usuario escolhe grupo, para visualizar sua tabela de pontos, gols marcados e saldo de gols ordenada
            print(" ")
            print(" ")                                                    
            grupo_visualizar_tabela = input("GRUPO QUE DESEJA VISUALIZAR TABELA:").upper().strip()  
            while grupo_visualizar_tabela not in lista_grupos:
                grupo_visualizar_tabela = input("GRUPO INVALIDO ==> GRUPO QUE DESEJA VISUALIZAR TABELA:").upper().strip()
            
            print_tabela_grupo(grupo_visualizar_tabela,dados_tabela,opcao)
        
        else:
            print("\nTABELA DISPONIVEL APENAS COM TODOS OS DADOS CADASTRADOS\n")    #Aviso caso exista resultados faltantes no cadastro
    
    elif opcao == '5':
        dados_grupos = leitura_dos_arquivos("out_files/Grupos.json")
        dados_confrontos = leitura_dos_arquivos("out_files/Confrontos.json")      #Arquivos sao carregados
        dados_resultados = leitura_dos_arquivos("out_files/Resultados.json")
        dados_tabela = leitura_dos_arquivos("out_files/Tabela.json")

#calculo de verificacao e feito para permitir que o usuario visualize as estatisticas apenas com o cadastramento de todos os resultados
        rj1 = calculo_verificacao_resultados("A",dados_resultados) ; rj2 = calculo_verificacao_resultados("B",dados_resultados) ; rj3 = calculo_verificacao_resultados("C",dados_resultados) ; rj4 = calculo_verificacao_resultados("D",dados_resultados) ; rj5 = calculo_verificacao_resultados("E",dados_resultados) ; rj6 = calculo_verificacao_resultados("F",dados_resultados) ; rj7 = calculo_verificacao_resultados("G",dados_resultados); rj8 = calculo_verificacao_resultados("H",dados_resultados)
        soma_de_verificacao_resultados = rj1+rj2+rj3+rj4+rj5+rj6+rj7+rj8
        
        if soma_de_verificacao_resultados == 48:   #Com o cadastro de todos os resultados a exibicao e permitida
            print('\nEXIBICAO DAS MEDIAS DE GOL POR GRUPO E GERAL, ALÉM DAS INFORMACOES DO JOGO COM A SELECAO QUE FEZ MAIS GOLS\n')
            
            sa = soma_gols("A",dados_tabela) ; sb = soma_gols("B",dados_tabela) ; sc = soma_gols("C",dados_tabela) ; sd = soma_gols("D",dados_tabela) ; se = soma_gols("E",dados_tabela) ; sf = soma_gols("F",dados_tabela) ; sg = soma_gols("G",dados_tabela) ; sh = soma_gols("H",dados_tabela)
            print("\nSEGUE ABAIXO AS MEDIAS DE GOL EM CADA GRUPO ==>")
            print("\n>{:.2f} GOLS NO GRUPO A".format(sa/6))
            print("\n>{:.2f} GOLS NO GRUPO B".format(sb/6))
            print("\n>{:.2f} GOLS NO GRUPO C".format(sc/6))
            print("\n>{:.2f} GOLS NO GRUPO D".format(sd/6))                  #E calculada a quantidade de gols em cada grupo atraves da funcao soma gols,
            print("\n>{:.2f} GOLS NO GRUPO E".format(se/6))                  #e logo em seguida e dividida por seis, para calculo da media de cada grupo
            print("\n>{:.2f} GOLS NO GRUPO F".format(sf/6))
            print("\n>{:.2f} GOLS NO GRUPO G".format(sg/6))
            print("\n>{:.2f} GOLS NO GRUPO H".format(sh/6))
            print("\nMEDIA DE GOLS GERAL ==> {:.2f} GOLS".format((sa+sb+sc+sd+se+sf+sg+sh) / 48))     #Media geral e calculado somando a quantidade de gols de todos
                                                                                                      #os grupos e dividindo po 48(quantidade de confrontos totais)
            print("\nJOGO(S) EM QUE UMA SELECAO FEZ MAIS GOLS ==>")
            print_jogo_mais_gol(dados_resultados,dados_confrontos)      #O print do confronto em que uma selecao fez mais gols e mostrado

        else:
            print("\nESTATISTICAS DISPONIVEIS APENAS COM TODOS OS DADOS CADASTRADOS\n")  #Aviso caso estejam faltando cadastros
    
    elif opcao == '6':
        dados_grupos = leitura_dos_arquivos("out_files/Grupos.json")
        dados_confrontos = leitura_dos_arquivos("out_files/Confrontos.json")    #Arquivos sao carregados
        dados_resultados = leitura_dos_arquivos("out_files/Resultados.json")
        dados_tabela = leitura_dos_arquivos("out_files/Tabela.json")

#calculo de verificacao e feito para permitir que o usuario visualize a formacao das oitavas apenas com o cadastramento de todos os resultados
        rj1 = calculo_verificacao_resultados("A",dados_resultados) ; rj2 = calculo_verificacao_resultados("B",dados_resultados) ; rj3 = calculo_verificacao_resultados("C",dados_resultados) ; rj4 = calculo_verificacao_resultados("D",dados_resultados) ; rj5 = calculo_verificacao_resultados("E",dados_resultados) ; rj6 = calculo_verificacao_resultados("F",dados_resultados) ; rj7 = calculo_verificacao_resultados("G",dados_resultados); rj8 = calculo_verificacao_resultados("H",dados_resultados)
        soma_de_verificacao_resultados = rj1+rj2+rj3+rj4+rj5+rj6+rj7+rj8

#Sistema leva em consideracao apenas os pontos, caso exista cadastros faltantes nos resultados o usuario sera avisado       
        if soma_de_verificacao_resultados == 48:
            print("\n"," "*35,"SISTEMA EM DESENVOLVIMENTO\n")
            print("\nA FORMACAO DAS OITAVAS ESTA LEVANDO EM CONSIDERANCAO APENAS OS PONTOS, POR CONSEQUENCIA INCOERENCIAS PODEM SER OBSERVADAS\n")
            oitavas()        #Funcao oitavas e chamada para exibir os confrontos formados
        else:
            print("\nDISPONIVEL APENAS COM O CADASTRO DE TODOS OS RESULTADOS\n")

    elif opcao == '7':
        break

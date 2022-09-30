import fileinput
from collections import deque
from random import randint

paginas = []

for line in fileinput.input():
    paginas.append(line.rstrip())

qtd_molduras = int(paginas[0])

def segunda_chance():
    countFalta = 0
    paginasRef = {}
    molduras = deque(maxlen= qtd_molduras) # cria fila com o tamanho máximo igual ao número de molduras

    for i in range(1, len(paginas)):

        if i % 4 == 0: # zera o bit R de todas as páginas de 4 em 4 referências
            for key, values in paginasRef.items():
                paginasRef[key] = 0

        if not str(paginas[i]) in molduras: # caso a pag não esteja na fila de molduras
            countFalta += 1

            if len(molduras) == qtd_molduras: # verifica se a fila está cheia
                for p in molduras.copy():
                    if paginasRef[p] == 1: # caso o bit R da pag seja igual 1, ele é setado para 0
                        paginasRef[str(p)] = 0
                    else: # caso já seja 0, a pag é removida da fila
                        molduras.remove(p)
                        break

            paginasRef[paginas[i]] = 1 # atualiza o bit de referência para 1

            molduras.appendleft(paginas[i])
        else: # caso a pag já esteja na fila, o bit de referência é setado para 1
            if paginasRef.get(paginas[i]) == 0:
                paginasRef[str(paginas[i])] = 1

    print("SC " + str(countFalta))


def otimo():
    molduras = []
    countFalta = 0
    qtdInstrucoes = []
    
    for i in range(1, len(paginas)):
        
        if not str(paginas[i]) in molduras: # caso a pag não esteja nas molduras
            countFalta += 1

            if len(molduras) == qtd_molduras: # caso todas as molduras estejam sendo utilizadas
                qtdInst = -1

                for pag in molduras:
                    for j in range(i+1, len(paginas)-1): # pra cada pag na lista de molduras é encontrada a prox vez que ela é referenciada 
                        if pag == paginas[j]: # encontrou a proxima referencia da pag
                            qtdInst = j - i
                            break
                    qtdInstrucoes.append(qtdInst) # adiciona -1 caso nao tenha encontrado nenhuma referencia

                if -1 in qtdInstrucoes: # caso exista alguma pag nas moduras que nao vai ser mais referenciada
                    indexM = qtdInstrucoes.index(-1) # indice da moldura a ser atualizada
                else:
                    indexM = 0
                    maior = -1
                    for q in range(0, len(molduras)):
                        if qtdInstrucoes[q] > maior: # encontra a pag que mais vai demorar a ser referenciada
                            maior = qtdInstrucoes[q]
                            indexM = q

                molduras[indexM] = paginas[i] # atualiza a moldura que tinha a pag a ser removida
                qtdInstrucoes = []

            else: # caso a lista de molduras nao esteja cheia
                molduras.append(paginas[i])

    print("OTM " + str(countFalta))


def conjunto_trabalho():
    molduras = []
    limiar = int(qtd_molduras / 2) + 1
    TVA = 0 # tempo virtual atual
    countFalta = 0

    for i in range(1, len(paginas)): #itera na lista de páginas
        TVA += 1
        
        if i % 4 == 0: # zera o bit R de todas as páginas de 4 em 4 referências
            for m in molduras:
                m['R'] = 0

        paginaNaMoldura = False

        for m in molduras: # itera nas molduras e verifica se a página está na lista de molduras
            if m['pag'] == int(paginas[i]):
                paginaNaMoldura = True
                break

        if not paginaNaMoldura: 

            countFalta += 1
            if len(molduras) == qtd_molduras: # verifica se todas a lista de molduras está cheia
                
                maiorIdade = -1 
                indexPagMA = -1 # indice da pag mais antiga

                indexPagR = -1 # indice da pag a ser removida

                for j in range(0, len(molduras)): # vasculha todas páginas nas molduras
                    if molduras[j]['R'] == 1:
                        molduras[j]['R'] = 0
                        molduras[j]['IUU'] = TVA
                    else:
                        age = TVA - molduras[j]['IUU']
            
                        if age > limiar:
                            indexPagR = j
                            break
                        else:
                            if age > maiorIdade:
                                maiorIdade = age
                                indexPagMA = j
                
                if indexPagR != -1: # caso tenha encontrado uma pag a ser removida
                    molduras[indexPagR] = {'pag': int(paginas[i]), 'R': 1, 'IUU': TVA}
                else:
                    if indexPagMA != -1: # caso tenha encontrado a pag mais velha
                        molduras[indexPagMA] = {'pag': int(paginas[i]), 'R': 1, 'IUU': TVA}
                    else:
                        molduras[randint(0, qtd_molduras-1)] = {'pag': int(paginas[i]), 'R': 1, 'IUU': TVA} # remove uma pag aleatoriamente

            else: # caso a lista de molduras não esteja cheia
                molduras.append({'pag': int(paginas[i]), 'R': 1, 'IUU': TVA})
        else: # caso a pag já esteja nas molduras
            for m in molduras:
                if m['pag'] == int(paginas[i]):
                    m['R'] = 1
                    m['IUU'] = TVA
                    break

    print("CT " + str(countFalta))


segunda_chance()
otimo()
conjunto_trabalho()
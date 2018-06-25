# -*- coding: utf-8 -*-
import sys
import math
import numpy as np
import grafo as G
import priorityQueue as fila
import tabulate as tabela


# Classe que representa um estado da árvore para a execução do A*
class Estado:
    def __init__(self, valor, estado):
        self.antecessores = []
        self.filhos = []
        self.valor = valor

        if estado != None:
            self.pai = estado
            self.distancia = self.get_dist(self.valor,self.pai.valor)
        else:
            self.pai = None
            self.distancia = 0

    # Calculando a distância do estado
    def get_dist(self, x, y):
        dist = 0
        i = 0
        while i < len(x):
            dist += math.pow((x[i] - y[i]), 2)
            i += 1
        return round(math.sqrt(dist),3)

    def __str__(self):
        return "Estado: " + str(self.valor) + "\nFilhos: " + str(self.filhos)

# Classe para representar o A*
class A_Estrela:
    def __init__(self): #, inicio, mapa):
        self.estado_inicial = None #Estado(inicio,None)
        self.fila_de_prioridade = fila.PriorityQueue()
        self.objetivo = None #Estado(inicio,None)
        self.mapa = None#mapa

    # Algoritmo A*
    def algoritmo(self, inicio, mapa, tipo=1):
        self.estado_inicial = Estado(inicio,None)
        self.objetivo = Estado(inicio,None)
        self.mapa = mapa

        self.fila_de_prioridade.insert(self.estado_inicial, 0)
        explorados = set()
        qtd_gerados = 0
        while True:
            if self.fila_de_prioridade.empty():
                print "Soluçao não encontrada!!.."
                return

            estado = self.fila_de_prioridade.extract_min()

            if self.isObjetivo(estado):
                return tipo,len(explorados), qtd_gerados, estado.antecessores  + [estado]

            self.expandir(estado)
            qtd_gerados += len(estado.filhos)

            explorados.add(estado)

            for filho in estado.filhos:
                if not estado in filho.antecessores:
                    filho.antecessores.append(estado)
                g = self.g(filho)
                h = self.h(filho, tipo)
                f = g + h
                print "Cidade Atual: "+ str(filho.valor) + "\ng(s): " + str(g) + ", h(s): " + str(h) + ", f(s): " + str(f) + "\n"
                if not filho in explorados and not self.fila_de_prioridade.exist((filho,f)):
                    self.fila_de_prioridade.insert(filho,f)

    # Custo da árvore geradora mínima da raiz com o nós que não foram visitados ainda, 
    #excluindo aqueles que estão no percurso
    def h(self, estado,tipo):
        if tipo == 1:
            self.expandir(estado)
            if len(estado.antecessores) > 1:
                primeiro = estado.antecessores[0] # Garanto que o primeiro é a cidade inicial? SIM
                ultimo = estado.antecessores[-1]
                nos_agm = [primeiro] + estado.filhos + [ultimo]
            else:
                nos_agm = [self.estado_inicial] + estado.filhos
        
            lista = []
            for x in nos_agm:
                lista.append(x.valor)
            matriz = calculaMatriz(lista)
            cidades = [i for i in xrange(1,(len(nos_agm)+1))]
            arestas = []
            for c1 in cidades:
                for c2 in cidades:
                    arestas.append((c1,c2, matriz[c1-1][c2-1]))

            grafo = G.Grafo(cidades, arestas)
            agm, custo = grafo.kruskal() #Gerar todas as arestas entre esses caras e executar o Kruskal
            return custo
        elif tipo == 2:
            self.expandir(estado)
            if len(estado.antecessores) > 1:
                ultimo = estado.antecessores[-1]
                nos_agm = estado.filhos + [ultimo]
            else:
                nos_agm = [self.estado_inicial] + estado.filhos

            lista = []
            for x in nos_agm:
                lista.append(x.valor)
            matriz = calculaMatriz(lista)
            cidades = [i for i in xrange(1, (len(nos_agm) + 1))]
            arestas = []
            for c1 in cidades:
                for c2 in cidades:
                    arestas.append((c1, c2, matriz[c1 - 1][c2 - 1]))

            grafo = G.Grafo(cidades, arestas)
            agm, custo = grafo.kruskal()  # Gerar todas as arestas entre esses caras e executar o Kruskal
            return custo
        else:
            return "ERRO: HEURISTICA INEXISTENTE!!!"


    # Custo do percurso, ou seja, custo da raiz até o nó atual
    def g(self, estado):
        dist = 0
        for e in estado.antecessores:
            dist += e.distancia
        return dist

        # Expandir um estado
    def expandir(self, estado):
        # Estado incial
        if estado.antecessores == []:
            for cidade in self.mapa:
                if cidade != estado.valor:
                    estado.filhos.append(Estado(cidade,estado))
        else: # Caso de um estado do meio da árvore
            for filho in [ant.valor for ant in estado.pai.filhos]:
                if estado.valor != filho:
                    std = Estado(filho, estado)
                    std.antecessores = estado.antecessores[:]
                    if not std.valor in [ f.valor for f in estado.filhos]:
                        estado.filhos.append(std)
            if len(estado.antecessores)==(len(self.mapa)-1): #Adicionando ultimo filho de cada nó
                for cidade in self.mapa:
                    if not cidade in [a.valor for a in estado.antecessores]:
                        std = Estado(cidade, estado)
                        std.antecessores = estado.pai.antecessores[:]
                        estado.filhos.append(std)
        if len(estado.antecessores) == len(self.mapa): # Adicionando o objetivo, ou seja, o nó inicial.
            raiz = estado.antecessores[0].valor
            std = Estado(raiz, estado)
            std.antecessores = estado.pai.antecessores[:]
            estado.filhos.append(std)

    def isObjetivo(self, estado):
        if len(estado.antecessores) == len(self.mapa):
            if estado.valor == self.objetivo.valor:
                return  True
        else:
            return  False

# Para cada linha do arquivo lido, cria uma tupla do tipo (x,y) e retorna uma lista de tuplas
def lerArquivo(linhas):
    ln = []
    for linha in linhas:
        linha = linha[0:-1].split(' ')
        i = 0
        while i < len(linha):
            linha[i] = float(linha[i])
            i += 1
        ln.append(linha)
    tuplas = []
    i = 0
    while i < len(ln)-1:
        j = 0
        while j < len(ln[i]):
            tuplas.append(tuple((ln[i][j], ln[i+1][j])))
            j += 1
        i += 1
    return tuplas

# Calcula a distância euclidiana entre duas cidades...
def distancia(x,y):
    dist = 0
    i = 0
    while i < len(x):
        dist += math.pow((x[i] - y[i]), 2)
        i += 1
    return round(math.sqrt(dist),3)

# Matriz de distâncias
def calculaMatriz(cidades):
    n = len(cidades)
    matriz = np.zeros((n,n))
    i = 0
    while i < n:
        j = 0
        while j < n:
            matriz[i][j] = distancia(cidades[i], cidades[j])
            j += 1
        i +=1
    return matriz

def escreverArquivo(linha, coluna):
    arquivo = open("saida_1", 'wb')
    arquivo.write((tabela.tabulate(linha, coluna, tablefmt="grid")) + "\n")
    arquivo.close()

# Principal
def main(arg):
    nome_arquivo = arg[0]
    arquivo = open(nome_arquivo, 'r')

    # Mapa das cidades
    mapa = lerArquivo(arquivo.readlines())

    # Estado Inicial é uma cidade qualquer do mapa
    # Questão 1
    linha = []
    coluna = ["Tamanho da Entrada", "Iteracao", "Cidade Inicial", "Heuristica", "Explorados", "Gerados"]

    # Uso da heurística
    comEstadoInicial = True

    if comEstadoInicial:
        i = 0
        while i < len(mapa):
            print "\nIteração: ", i + 1, ", Heurística 1"
            a_estrela = A_Estrela()
            tipo,explorados, gerados, resultado = a_estrela.algoritmo(mapa[i], mapa)
            custo = 0
            for cidade in resultado:
                print  cidade.valor, cidade.distancia
                custo += cidade.distancia

            print  "Custo do caminho: " + str(custo), "\n"
            linha.append([len(mapa), (i+1),mapa[i], tipo,explorados,gerados])
            i += 1
    else:

        i = 0
        while i < len(mapa):
            print "\nIteração: ", i + 1, ", Heurística 2"
            a_estrela = A_Estrela()
            tipo, explorados, gerados, resultado = a_estrela.algoritmo(mapa[i], mapa,2)
            custo = 0
            for cidade in resultado:
                print  cidade.valor, cidade.distancia
                custo += cidade.distancia

            print  "Custo do caminho: " + str(custo), explorados, gerados, "\n"
            linha.append([len(mapa), (i+1), mapa[i], tipo, explorados, gerados])
            i += 1

    escreverArquivo(linha, coluna)


if __name__ == '__main__':
    main(sys.argv[1:3])

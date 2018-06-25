# -*- coding: utf-8 -*-

import numpy as np

class Grafo:
    vertices = None                         # Conjunto de vertices
    arestas = None                          # Conjunto de arestas na forma (vertice1. vertice2, peso)
    matriz_adjacencia = None                # Representação do grafo
    pai = None                              # pai de um vertice, ou seja, seu representante...
    ordem = None                            # limite superior sobre a altura de x..

    def __init__(self, vertices, arestas):
        self.vertices = list(vertices)
        self.arestas = list(arestas)
        self.pai = dict()
        self.ordem = dict()
        self.gerarMatriz()

    # Inseri uma nova aresta ao grafo
    def inserirAresta(self, aresta):
        if not aresta in self.arestas:
            self.arestas.append(aresta)
            v1 = aresta[0]
            v2 = aresta[1]
            p = aresta[2]
            self.matriz_adjacencia[v1-1][v2-1] = p

    # Gera a matriz de adjacência que representa o grafo
    def gerarMatriz(self):
        n = len(self.vertices)
        self.matriz_adjacencia = np.zeros((n,n))
        # Acrescentando valores padrões
        for v in self.vertices:
            for a in self.vertices:
                if self.matriz_adjacencia[v-1][a-1] == 0:
                    self.matriz_adjacencia[v-1][a-1] = int(-1) # Valor padrão

        # Adicionando arestas
        for aresta in self.arestas:
            v1 = aresta[0]
            v2 = aresta[1]
            p = aresta[2]
            self.matriz_adjacencia[v1-1][v2-1] = p  #Indices vão de 0 a n-1, por isso reduzir um
            self.matriz_adjacencia[v2-1][v1-1] = p

    # Ordena as arestas por seu peso 
    def ordenarPorPeso(self):
        n = len(self.arestas)
        i = 0
        while i < n:
            j = 0
            while j < n:
                if self.arestas[i][2] < self.arestas[j][2]:
                    self.swap(self.arestas[i], self.arestas[j])
                j += 1
            i += 1
        return self.arestas

    # Cria um conjunto para cada vertice
    def makeSet(self,vertice):
        self.pai[vertice] = vertice
        self.ordem[vertice] = 0

    # Procura o pai (representante) de vertice
    def findSet(self,vertice):
        if self.pai[vertice] != vertice:
            self.pai[vertice] = self.findSet(self.pai[vertice])
        return self.pai[vertice]

    # Faz a união de dois componentes desconexos
    def union(self,vertice1, vertice2):
        pai1 = self.findSet(vertice1)
        pai2 = self.findSet(vertice2)
        if pai1 != pai2:
            if self.ordem[pai1] > self.ordem[pai2]:
                self.pai[pai2] = pai1
            else:
                self.pai[pai1] = pai2
                if self.ordem[pai1] == self.ordem[pai2]: self.ordem[pai2] += 1

    # Algoritmo de kruskal
    def kruskal(self):
        # Conjunto de arestas da AGM
        agm = []
        for v in self.vertices:
            self.makeSet(v-1)
        # Ordenando arestas de acordo com seu peso
        self.ordenarPorPeso()
        for aresta in self.arestas:
            u = aresta[0]-1
            v = aresta[1]-1
            if self.findSet(u) != self.findSet(v): # Se não possuem o mesmo pai, ou seja, estão em conjuntos distintos
                self.union(u,v)
                agm.append(aresta)
        return agm , self.calculaCustoAgm(agm)

    # Calcula o custo total da árvore geradora mínima
    def calculaCustoAgm(self,agm):
        custo = 0
        for aresta in agm:
            custo += aresta[2]

        return custo

    # Efetua a troca de duas arestas
    def swap(self, p, q):
        p1 = self.arestas.index(p)
        p2 = self.arestas.index(q)
        aux = self.arestas[p2]
        self.arestas[p2] = self.arestas[p1]
        self.arestas[p1] = aux

    def __str__(self):
        return str(self.matriz_adjacencia)


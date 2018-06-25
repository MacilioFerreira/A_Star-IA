# -*- coding: utf-8 -*-

import heapq
import math
from cStringIO import StringIO


class PriorityQueue:

    def __init__(self):
        self.elementos = []

    def empty(self):
        return len(self.elementos) == 0

    def insert(self, item, prioridade):
        #Inseri de acordo com a prioridade dele
        heapq.heappush(self.elementos,(prioridade,item))

    def extract_min(self):
        if not self.empty():
            minimo = heapq.heappop(self.elementos)
            # Retorna de acordo com a inserção..
            return minimo[1]

    def exist(self, item):
        return item in self.elementos

    def swap(self, item1, item2):
        if item1[0] < item2[1]:
            i = self.elementos.index(item1)
            self.elementos[i] = item2
    def custoEstado(self, item):
        if item in self.elementos:
            i = self.elementos.index(item)
            estado = self.elementos[i]
            return  estado[0]
        else:
            return 0


    def __str__(self, total_width=40, fill=' '):

        output = StringIO()
        last_row = -1
        for i, n in enumerate(self.elementos):
            if i:
                row = int(math.floor(math.log(i+1, 2)))
            else:
                row = 0
            if row != last_row:
                output.write('\n')
            columns = 2**row
            col_width = int(math.floor((total_width * 1.0) / columns))
            output.write(str(n).center(col_width, fill))
            last_row = row
        print output.getvalue()
        print '-' * total_width
        print
        return ""


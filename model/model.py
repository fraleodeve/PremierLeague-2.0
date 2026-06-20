import copy

import networkx as nx
from database.DAO import DAO

class Model:

    def __init__(self):
        self._grafo = nx.DiGraph()

        self._idMapGiocatori = {}
        for el in DAO.getAllGiocatori():
            self._idMapGiocatori[el.PlayerID] = el

        self._bestPath = []
        self._bestScore = 0

    def getBestPath(self, k):
        self._bestPath = []
        self._bestScore = 0

        self.ricorsione([], k)

        return self._bestPath, self._bestScore

    def ricorsione(self, parziale, k):
        if len(parziale) == k:
            if self.gradoTitolarita(parziale) > self._bestScore:
                self._bestPath = copy.deepcopy(parziale)
                self._bestScore = self.gradoTitolarita(parziale)

        if len(parziale) == k:
            return

        nodiVietati = []
        for el in parziale:
            for e in self._grafo.out_edges(el):
                nodiVietati.append(e[1])
            # nodiVietati.append(self._grafo.out_edges(el))

        for n in self._grafo.nodes():
            if n not in parziale and n not in nodiVietati:
                parziale.append(n)
                self.ricorsione(parziale, k)
                parziale.pop()

    def gradoTitolarita(self, parziale):
        score = 0
        for n in parziale:
            for e in self._grafo.out_edges(n, data=True):
                score += e[2]["weight"]
            for e in self._grafo.in_edges(n, data=True):
                score -= e[2]["weight"]
        return score

    def buildGraph(self, goal: float):
        self._grafo.clear()
        media = DAO.getMedia(goal)
        for el in media:
            self._grafo.add_node(self._idMapGiocatori[el.PlayerID])

        myEdges = DAO.getEdges(goal)

        lista = []
        for el in myEdges:
            if el.minuti > 0:
                lista.append((el.p1, el.p2, el.minuti))
            if el.minuti < 0:
                valore = - el.minuti
                lista.append((el.p2, el.p1, valore))

        for el in lista:
            giocatore1 = self._idMapGiocatori[el[0]]
            giocatore2 = self._idMapGiocatori[el[1]]
            if self._grafo.has_edge(giocatore1, giocatore2):
                self._grafo[giocatore1][giocatore2]["weight"] += el[2]
            elif self._grafo.has_edge(giocatore2, giocatore1):
                self._grafo[giocatore2][giocatore1]["weight"] -= el[2]
            else:
                self._grafo.add_edge(giocatore1, giocatore2, weight = el[2])

        for u, v, data in list(self._grafo.edges(data=True)):
            if data["weight"] < 0:
                peso = -data["weight"]
                self._grafo.remove_edge(u, v)
                self._grafo.add_edge(v, u, weight=peso)

    def getNodoMaggiore(self):
        lista = []
        for n in self._grafo.nodes():
            score = self._grafo.out_degree(n)
            lista.append((n, score))
        lista.sort(key = lambda x: x[1], reverse = True)
        output = []
        for el in self._grafo.out_edges(lista[0][0], data = True):
            output.append((el[1], el[2]["weight"]))
        output.sort(key = lambda x: x[1], reverse = True)
        return lista[0][0], output

    def getDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)





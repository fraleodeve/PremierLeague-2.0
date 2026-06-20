import itertools
from collections import defaultdict

import networkx as nx
from database.DAO import DAO

class Model:

    def __init__(self):
        self._grafo = nx.DiGraph()

        self._dictSquadre = {}
        self._dictClassifica = defaultdict(int)

    def getAllSquadre(self):
        squadre = DAO.getAllSquadre()
        squadre.sort(key=lambda x: x.Name)
        return squadre

    def buildGraph(self):
        self._grafo.clear()

        squadre = DAO.getAllSquadre()
        for el in squadre:
            self._dictSquadre[el.TeamID] = el
        self._grafo.add_nodes_from(squadre)

        self.classifica()

        myEdges = []
        for el in DAO.getAllPartite():
            myEdges.append((self._dictSquadre[el.TeamHomeID], self._dictSquadre[el.TeamAwayID]))
        for ed in myEdges:
            if self._dictClassifica[ed[0].TeamID] > self._dictClassifica[ed[1].TeamID]:
                self._grafo.add_edge(ed[0], ed[1], weight = self._dictClassifica[ed[0].TeamID] - self._dictClassifica[ed[1].TeamID])
            elif self._dictClassifica[ed[0].TeamID] > self._dictClassifica[ed[1].TeamID]:
                self._grafo.add_edge(ed[1], ed[0], weight = self._dictClassifica[ed[1].TeamID] - self._dictClassifica[ed[0].TeamID])

    def classifica(self):
        partite = DAO.getAllPartite()
        for el in partite:
            if el.ResultOfTeamHome == 1:
                self._dictClassifica[el.TeamHomeID] += 3
            if el.ResultOfTeamHome == 0:
                self._dictClassifica[el.TeamAwayID] += 1
                self._dictClassifica[el.TeamHomeID] += 1
            if el.ResultOfTeamHome == -1:
                self._dictClassifica[el.TeamAwayID] += 3

    def getPunti(self, s):
        listaSup = []
        listaInf = []
        squadra = self.getSquadra(s)
        for key, val in self._dictClassifica.items():
            if key != squadra.TeamID and self._dictClassifica[squadra.TeamID] > val:
                listaInf.append((self._dictSquadre[key].Name, self._dictClassifica[squadra.TeamID] - val))
            if key != squadra.TeamID and self._dictClassifica[squadra.TeamID] < val:
                listaSup.append((self._dictSquadre[key].Name, val - self._dictClassifica[squadra.TeamID]))
        listaSup.sort(key=lambda x: x[1])
        listaInf.sort(key=lambda x: x[1])
        return listaSup, listaInf

    def getDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def getSquadra(self, s):
        for el in DAO.getAllSquadre():
            if el.Name == s:
                return self._dictSquadre[el.TeamID]
        return None


import flet as ft

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._ddS = None

    def handleCreaGrafo(self, e):
        valore = self._view._goalFatti.value
        if valore == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione! Inserire un valore", color = "red"))
            self._view.update_page()
            return

        try:
            val = float(valore)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione! Inserire un valore numerico", color="red"))
            self._view.update_page()
            return

        self._view.txt_result.controls.clear()
        self._model.buildGraph(val)
        nodi, archi = self._model.getDetails()

        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato!", color = "red"))
        self._view.txt_result.controls.append(ft.Text(f"Nodi: {nodi}"))
        self._view.txt_result.controls.append(ft.Text(f"Archi: {archi}"))

        self._view._btnTopPlayer.disabled = False

        self._view.update_page()

    def handleTopPlayer(self, e):
        nodo, lista = self._model.getNodoMaggiore()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"TOP PLAYER: {nodo}"))
        self._view.txt_result.controls.append(ft.Text())
        self._view.txt_result.controls.append(ft.Text(f"AVVERSARI BATTUTI: "))
        for el in lista:
            self._view.txt_result.controls.append(ft.Text(f"{el[0]} | {el[1]}"))

        self._view._numeroGiocatori.disabled = False
        self._view._btnDreamTeam.disabled = False

        self._view.update_page()


    def handleDreamTeam(self, e):
        valore = self._view._numeroGiocatori.value
        if valore == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione! Inserire un valore", color="red"))
            self._view.update_page()
            return

        try:
            val = int(valore)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione! Inserire un valore numerico", color="red"))
            self._view.update_page()
            return

        self._view.txt_result.controls.clear()
        percorso, punteggio = self._model.getBestPath(val)

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Punteggio: {punteggio}"))
        self._view.txt_result.controls.append(ft.Text())
        self._view.txt_result.controls.append(ft.Text(f"Di seguito i giocatori del dream team: "))
        for el in percorso:
            self._view.txt_result.controls.append(ft.Text(f"{el}"))

        self._view.update_page()
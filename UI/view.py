import flet as ft

class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Lab12-Simulazione esame"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self._goalFatti = None
        self._btnCreaGrafo = None
        self._btnTopPlayer = None
        self._numeroGiocatori = None
        self._btnDreamTeam = None
        self.txt_result = None

    def load_interface(self):
        # title
        self._title = ft.Text("PremierLeague", color="blue", size=24)
        self._page.controls.append(self._title)

        self._goalFatti = ft.TextField(label="Goal Fatti (x)")
        self._btnCreaGrafo = ft.ElevatedButton(text="Crea Grafo", on_click=self._controller.handleCreaGrafo)
        row1 = ft.Row([self._goalFatti, self._btnCreaGrafo], alignment=ft.MainAxisAlignment.CENTER)
                      # vertical_alignment=ft.CrossAxisAlignment.END)
        self._page.controls.append(row1)

        self._btnTopPlayer = ft.ElevatedButton(text="Top Player", on_click=self._controller.handleTopPlayer,
                                             disabled=True)

        row2 = ft.Row([self._btnTopPlayer], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        self._numeroGiocatori = ft.TextField(label="Numero Giocatori (k)", disabled=True)
        self._btnDreamTeam = ft.ElevatedButton(text="Classifica squadra", on_click=self._controller.handleDreamTeam,
                                                disabled=True)
        row3 = ft.Row([self._numeroGiocatori, self._btnDreamTeam], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row3)

        # List View where the reply is printed
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()

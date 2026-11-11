from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QWidget


class AppWindow(QMainWindow):
    """Unique fenêtre de l'application : les pages sont empilées dedans."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Rackeur")
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self._pages: dict[str, QWidget] = {}

    def switch_to(self, cle: str, fabrique) -> None:
        page = self._pages.get(cle)

        if page is None:
            page = fabrique(self)
            self._pages[cle] = page
            self.stack.addWidget(page)

        if hasattr(page, "refresh"):
            page.refresh()

        self.stack.setCurrentWidget(page)

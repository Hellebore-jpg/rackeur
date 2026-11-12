from __future__ import annotations # Gère l'annotation des classes dans leurs propres fonctions

# Importation de Qt et de ses Widgets
from PyQt6.QtGui import (
    QIcon,
)
from PyQt6.QtWidgets import (
    QApplication, QDialog,
)

import sys # Permet l'interaction avec le système d'exploitation

from src.utils.bootstrap import load_database
from src.utils.helpers import load_stylesheet
from src import config
from src.utils import utils_config

#=============================================================================#
# IMPORTATION DES FENÊTRES                                                    #
#=============================================================================#
from src.ui.source_dialog import SourceDialog
from src.ui.auth_window import AuthWindow
from src.ui.app_pages import AppWindow

#=============================================================================#
# DEMARRAGE DE L'APPLICATION                                                  #
#=============================================================================#
def main() -> int:
    """Démarre et gère l'application dans sa globalité.

    Returns:
        int: Code de fermeture de l'application.
    """
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(str(config.FAVICON_PATH)))
    app.setStyle("Fusion")
    app.setStyleSheet(load_stylesheet())
 
    # Demande le type de BDD à l'utilisateur
    dialog = SourceDialog()
    if dialog.exec() != QDialog.DialogCode.Accepted.value:
        return 0  # Quitter l'app si l'utilisateur ferme la fenêtre sans choisir
 
    # Charger la base de données
    utils_config.CSV = dialog.is_csv()
    load_database()
 
    window = AppWindow()
    window.switch_to("auth")
    window.showMaximized()

    return app.exec()

if __name__ == '__main__':
    sys.exit(main())

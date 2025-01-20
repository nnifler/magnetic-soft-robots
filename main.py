"""This script is the main script of the package. It starts the software."""

from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow

app = QApplication([])
window = MainWindow()
window.show()
app.exec()

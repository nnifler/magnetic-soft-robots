"""This script is the main script of the package. It starts the software."""

import multiprocessing as mp
from PySide6.QtWidgets import QApplication
from gui import MainWindow

if __name__ == '__main__':
    mp.set_start_method('spawn')
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

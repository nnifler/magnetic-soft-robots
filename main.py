"""This script is the main script of the package. It starts the software."""

import multiprocessing as mp
from PySide6.QtWidgets import QApplication
from gui import MainWindow

if __name__ == '__main__':
    # Dispatching processes with forking is much nicer, but sadly not supported on Windows.
    mp.set_start_method('spawn')
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

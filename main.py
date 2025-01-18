from PySide6.QtWidgets import QApplication
from gui.mainWindow import MainWindow

app = QApplication([])
window = MainWindow()
window.show()
app.exec()

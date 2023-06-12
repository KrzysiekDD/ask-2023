from PySide6.QtWidgets import QApplication
from gui import MainMenuWindow
import sys
import random
random.seed(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainMenuWindow()
    window.show()
    sys.exit(app.exec())

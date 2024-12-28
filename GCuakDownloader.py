from PyQt5.QtWidgets import QApplication
from Screens.MainScreen import MainWindow

def main() :
    window = MainWindow()
    window.show()
    app.exec()
    
app = QApplication([])
main()
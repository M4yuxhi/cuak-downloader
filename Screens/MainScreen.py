import os
from PyQt5.QtWidgets import QComboBox, QGraphicsItem, QLabel, QLineEdit, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from Classes.YouTubeDLManager import YouTubeDLManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.url = ""
        self.mode = "Video"
        self.setWindowTitle("gCuak Downloader")
        self.setMinimumSize(500, 250)

        widget = QWidget()
        layout = QVBoxLayout()

        # Calcular la ruta absoluta de la imagen
        current_dir = os.path.dirname(os.path.abspath(__file__))  # Carpeta de este archivo
        image_path = os.path.join(current_dir, "../Images/CuakDownloader.png")

        logo_label = QLabel()
        logo_pixmap = QPixmap(image_path)
        
        if not logo_pixmap.isNull():
            logo_pixmap = logo_pixmap.scaled(400, 400)  # Ajustar la imagen a 400x400
            logo_label.setPixmap(logo_pixmap)
        else:
            logo_label.setText("No se pudo cargar la imagen.")
        
        logo_label.setScaledContents(True)

        url_label = QLabel("URL del Video")
        
        # Crear el campo de entrada de texto
        url_text_input = QLineEdit()
        # Conectar la señal 'textChanged' a la función updateURL
        url_text_input.textChanged.connect(self.updateURL)

        mode_label = QLabel("Modo de Descarga")

        downloadtype_combobox = QComboBox()
        downloadtype_combobox.addItem("Video")
        downloadtype_combobox.addItem("Audio")
        downloadtype_combobox.currentIndexChanged.connect(self.updateMode)

        dowload_button = QPushButton("Descargar", widget)
        dowload_button.clicked.connect(self.download)

        layout.addWidget(logo_label)
        layout.addWidget(url_label)
        layout.addWidget(url_text_input)
        layout.addWidget(mode_label)
        layout.addWidget(downloadtype_combobox)
        layout.addWidget(dowload_button)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def download(self):
        print("Descargando desde: " + self.url)
        youtube = YouTubeDLManager()
        youtube.download(self.url, self.mode)

    def updateURL(self, url):
        # Actualiza el atributo 'url' con el texto del campo de entrada
        self.url = url
        print("URL actualizada: " + self.url)

    def updateMode(self, mode):

        mode = str(mode)

        if mode == '0' :
            self.mode = "Video"
        elif mode == '1' :
            self.mode = "Audio"

        #self.mode = mode
        print("Nuevo modo: " + self.mode)
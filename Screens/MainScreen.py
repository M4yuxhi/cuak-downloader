from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QComboBox, QLabel, QLineEdit, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTabWidget
from PyQt5.QtGui import QPixmap
import os
from Classes.YouTubeDLManager import YouTubeDLManager


class DownloadThread(QThread):
    # Señales para actualizar el progreso, notificar la finalización y cancelación
    progress_updated = pyqtSignal(dict)
    download_finished = pyqtSignal()
    download_canceled = pyqtSignal()  # Nueva señal para la cancelación

    def __init__(self, url, mode, manager):
        super().__init__()
        self.url = url
        self.mode = mode
        self.manager = manager
        self.manager.progress_callback = self.emit_progress  # Configura el callback
        self._is_canceled = False  # Bandera para cancelar

    def emit_progress(self, progress):
        self.progress_updated.emit(progress)  # Emite la señal de progreso

    def cancel(self):
        """Marca el hilo como cancelado."""
        self._is_canceled = True

    def is_canceled(self):
        """Devuelve True si se solicitó la cancelación."""
        return self._is_canceled

    def run(self):
        """Ejecuta la descarga."""
        try:
            self.manager.download(self.url, self.mode, self.is_canceled)
            if not self._is_canceled:
                self.download_finished.emit()  # Notificar finalización
            else:
                self.download_canceled.emit()  # Notificar cancelación
        except Exception as e:
            print(f"Error en la descarga: {e}")
            self.download_canceled.emit()  # En caso de error, emitir cancelación



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.url = ""
        self.mode = "Video"
        self.manager = YouTubeDLManager()

        self.setWindowTitle("gCuak Downloader")
        self.setMinimumSize(500, 300)

        # Crear un QTabWidget para las pestañas
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Agregar pestañas
        self.download_tab = self.create_download_tab()
        self.progress_tab = self.create_progress_tab()

        self.tabs.addTab(self.download_tab, "Descargar")
        self.tabs.addTab(self.progress_tab, "Progreso")

        self.download_thread = None

    def create_download_tab(self):
        """
        Crea la pestaña de descarga.
        """
        widget = QWidget()
        layout = QVBoxLayout()

        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "../Images/CuakDownloader.png")

        logo_label = QLabel()
        logo_pixmap = QPixmap(image_path)

        if not logo_pixmap.isNull():
            logo_pixmap = logo_pixmap.scaled(400, 400)
            logo_label.setPixmap(logo_pixmap)
        else:
            logo_label.setText("No se pudo cargar la imagen.")

        logo_label.setScaledContents(True)

        url_label = QLabel("URL del Video")
        url_text_input = QLineEdit()
        url_text_input.textChanged.connect(self.updateURL)

        mode_label = QLabel("Modo de Descarga")

        downloadtype_combobox = QComboBox()
        downloadtype_combobox.addItem("Video")
        downloadtype_combobox.addItem("Audio")
        downloadtype_combobox.currentIndexChanged.connect(self.updateMode)

        download_button = QPushButton("Descargar")
        download_button.clicked.connect(self.start_download)

        layout.addWidget(logo_label)
        layout.addWidget(url_label)
        layout.addWidget(url_text_input)
        layout.addWidget(mode_label)
        layout.addWidget(downloadtype_combobox)
        layout.addWidget(download_button)

        widget.setLayout(layout)
        return widget

    def create_progress_tab(self):
        """
        Crea la pestaña de progreso.
        """
        widget = QWidget()
        layout = QVBoxLayout()

        self.status_label = QLabel("Estado: idle")
        self.percentage_label = QLabel("Progreso: 0.0%")
        self.speed_label = QLabel("Velocidad: N/A")
        self.eta_label = QLabel("Tiempo estimado: N/A")

        self.cancel_button = QPushButton("Cancelar la Descarga")
        self.cancel_button.clicked.connect(self.cancel_download)

        layout.addWidget(self.status_label)
        layout.addWidget(self.percentage_label)
        layout.addWidget(self.speed_label)
        layout.addWidget(self.eta_label)
        layout.addWidget(self.cancel_button)

        widget.setLayout(layout)
        return widget

    def cancel_download(self):
        if self.download_thread and self.download_thread.isRunning():
            self.download_thread.cancel()
            self.status_label.setText("Estado: Cancelando...")
            self.download_thread.wait()  # Esperar que el hilo termine
            self.status_label.setText("Estado: Descarga cancelada.")

    def start_download(self):
        if not self.url:
            self.status_label.setText("Estado: Por favor, ingresa una URL.")
            return

        self.download_thread = DownloadThread(self.url, self.mode, self.manager)
        self.download_thread.progress_updated.connect(self.update_progress)
        self.download_thread.download_finished.connect(self.download_complete)
        self.download_thread.download_canceled.connect(self.download_canceled)
        self.download_thread.start()

        self.status_label.setText("Estado: Descargando...")

    def download_canceled(self):
        self.status_label.setText("Estado: Descarga cancelada.")

    def update_progress(self, progress):
        """
        Actualiza los datos de progreso en la pestaña de progreso.
        """
        self.status_label.setText(f"Estado: {progress['status']}")
        self.percentage_label.setText(f"Progreso: {progress['percentage']}")
        self.speed_label.setText(f"Velocidad: {progress['speed']}")
        self.eta_label.setText(f"Tiempo estimado: {progress['eta']}")

    def download_complete(self):
        """
        Maneja el evento de descarga completada.
        """
        self.status_label.setText("Estado: Descarga completada.")

    def updateURL(self, url):
        self.url = url
        print("URL actualizada: " + self.url)

    def updateMode(self, mode):
        if mode == 0:
            self.mode = "Video"
        elif mode == 1:
            self.mode = "Audio"
        print("Nuevo modo: " + self.mode)

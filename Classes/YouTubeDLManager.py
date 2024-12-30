import os
from yt_dlp import YoutubeDL

class YouTubeDLManager:
    def __init__(self):
        self.progress_data = {
            'percentage': "0.0%",
            'speed': "N/A",
            'eta': "N/A",
            'status': "idle"  # Estado inicial
        }

        self.progress_callback = None  # Callback para reportar progreso

    def download(self, url, mode, is_canceled_callback):
        """
        Realiza la descarga del video o audio utilizando yt-dlp.
        
        Parameters:
            url (str): URL del video.
            mode (str): Modo de descarga ('Video' o 'Audio').
            is_canceled_callback (callable): Función para verificar si se ha solicitado la cancelación.
        """
        # Configurar el formato según el modo (Video o Audio)
        if mode == "Video":
            format_option = 'bestvideo+bestaudio/best'
            extension = 'mp4'
        elif mode == "Audio":
            format_option = 'bestaudio'
            extension = 'mp3'

        output_dir = os.path.join("Downloads", mode)

        # Crear el directorio de salida si no existe
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Extraer información del video para obtener el título
        with YoutubeDL() as ydl:
            info = ydl.extract_info(url, download=False)  # Solo extraer info, no descargar
            title = info.get('title', 'unknown_title').replace('/', '_')  # Evitar caracteres no válidos

        # Configurar las opciones de descarga
        ydl_opts = {
            'format': format_option,
            'outtmpl': os.path.join(output_dir, f'{title}.{extension}'),  # Nombre del archivo
            'progress_hooks': [self.progress_hook],  # Función para manejar actualizaciones de progreso
        }

        # Descargar el video o audio
        print(f"Downloading {mode}: {title}... This may take a few moments.")
        try:
            with YoutubeDL(ydl_opts) as ydl:
                result = ydl.download([url])
                for _ in result:
                    if is_canceled_callback():  # Verificar si se solicitó la cancelación
                        print("Descarga cancelada por el usuario.")
                        break
        except Exception as e:
            print(f"Error durante la descarga: {e}")
        else:
            if not is_canceled_callback():
                print(f"Download complete: {os.path.join(output_dir, f'{title}.{extension}')}")

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            self.progress_data['percentage'] = d.get('_percent_str', '0.0%').strip()
            self.progress_data['eta'] = d.get('eta', 'N/A')  # Tiempo estimado
            self.progress_data['speed'] = d.get('_speed_str', 'N/A')  # Velocidad
            self.progress_data['status'] = 'descargando'
        elif d['status'] == 'finished':
            self.progress_data['status'] = 'finalizado'
        elif d['status'] == 'error':
            self.progress_data['status'] = 'error'

        if self.progress_callback:
            self.progress_callback(self.progress_data)  # Llama al callback

    def get_progress(self):
        """
        Devuelve los datos actuales del progreso.
        """
        return self.progress_data
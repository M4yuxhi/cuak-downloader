from yt_dlp import YoutubeDL

class YouTubeDLManager:
    def __init__(self):
        pass

    def download(self, url, mode):
        # Configurar el formato según el modo (Video o Audio)
        if mode == "Video":
            format_option = 'bestvideo'
            extension = 'mp4'
        elif mode == "Audio":
            format_option = 'bestaudio'
            extension = 'mp3'

        # Extraer información del video para obtener el título
        with YoutubeDL() as ydl:
            info = ydl.extract_info(url, download=False)  # Solo extraer info, no descargar
            title = info.get('title', 'unknown_title').replace('/', '_')  # Reemplazar caracteres no válidos

        # Configurar las opciones de descarga
        ydl_opts = {
            'format': format_option,
            'outtmpl': f'{title}.{extension}',  # Usar el título como nombre del archivo
        }

        # Descargar el video o audio
        print(f"Downloading {mode}: {title}... This may take a few moments.")
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        print(f"Download complete: {title}.{extension}")

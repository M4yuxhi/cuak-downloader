from yt_dlp import YoutubeDL

# Solicitar enlace del video
link = input("Enter a YouTube link to download: ")

# Preguntar al usuario si quiere descargar video o audio
mode = input("Do you want to download 'video' or 'audio' only? (type 'v' or 'a' or 'b'): ").strip().lower()

# Configurar la extensión y formato según la elección
if mode == 'v':
    format_option = 'bestvideo'
    extension = 'mp4'
elif mode == 'a':
    format_option = 'bestaudio'
    extension = 'mp3'
elif mode == 'b':
    format_option = 'best*'
    extension = 'mp4'
else:
    print("Invalid option. Please choose 'v' or 'a'.")
    exit()

# Solicitar el nombre del archivo de salida
output_name = input(f"Enter the output file name (without extension): ").strip()

# Configuración de descarga
ydl_opts = {
    'format': format_option,  # Descargar el mejor formato según la elección
    'outtmpl': f'{output_name}.{extension}',  # Nombre y extensión del archivo de salida
}

# Descargar el archivo
print(f"Downloading {mode}... This may take a few moments.")
with YoutubeDL(ydl_opts) as ydl:
    ydl.download([link])

print(f"Download complete: {output_name}.{extension}")
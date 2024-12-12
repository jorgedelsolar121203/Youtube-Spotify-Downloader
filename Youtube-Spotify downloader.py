import yt_dlp
import sys
import os
import re
from moviepy.editor import AudioFileClip
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Configuración de autenticación de Spotify
CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
REDIRECT_URI = 'http://localhost:8888/callback'
SCOPE = 'playlist-read-private'

# Autenticación de Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=SCOPE))

def buscar_video_youtube(query):
    """
    Busca el primer video en YouTube que coincide con el término de búsqueda proporcionado,
    priorizando versiones con 'lyrics'.
    """   
    query_with_lyrics = f"{query} lyrics"  # Añadir "lyrics" a la búsqueda
    options = {'quiet': True, 'extract_flat': True, 'force_generic_extractor': True}
    with yt_dlp.YoutubeDL(options) as ydl:
        result = ydl.extract_info(f"ytsearch:{query_with_lyrics}", download=False)
    if 'entries' in result and result['entries']:
        video_url = result['entries'][0]['url']
        print(f"Video encontrado: {video_url}")
        return video_url
    print("No se encontraron resultados.")
    return None


def extraer_urls_playlist(playlist_url):
    """
    Extrae las URLs de todos los videos de una lista de reproducción de YouTube.
    """
    options = {'quiet': True, 'extract_flat': True}
    with yt_dlp.YoutubeDL(options) as ydl:
        result = ydl.extract_info(playlist_url, download=False)
    if 'entries' in result and result['entries']:
        video_urls = [entry['url'] for entry in result['entries']]
        print(f"Se encontraron {len(video_urls)} videos en la lista de reproducción.")
        return video_urls
    print("No se encontraron videos en la lista de reproducción.")
    return []

def limpiar_nombre_archivo(nombre):
    """
    Limpia el nombre del archivo para evitar caracteres no permitidos, incluyendo emojis y caracteres especiales.
    Solo permite letras, números, espacios, paréntesis, guiones y guiones bajos.
    """
    # Remover emojis
    nombre = re.sub(r'[\U00010000-\U0010FFFF]', '', nombre, flags=re.UNICODE)
    # Remover caracteres no permitidos
    nombre = re.sub(r'[^a-zA-Z0-9 áéíóúÁÉÍÓÚñÑ\-()_]', '', nombre)
    # Reemplazar múltiples espacios por un único espacio
    nombre = re.sub(r'\s+', ' ', nombre).strip()
    return nombre


def descargar_video(url):
    """
    Descarga un video de YouTube y lo convierte a MP3.
    """
    videos_folder = os.path.join(os.path.expanduser("~"), "Videos")
    music_folder = os.path.join(os.path.expanduser("~"), "Music")

    if not os.path.exists(videos_folder):
        print("No se encontró la carpeta Videos en tu sistema.")
        sys.exit(1)
    if not os.path.exists(music_folder):
        print("No se encontró la carpeta Música en tu sistema.")
        sys.exit(1)

    options = {
        'format': 'best',
        'outtmpl': os.path.join(videos_folder, '%(title)s.%(ext)s'),
        'retries': 10,
        'fragment-retries': 10,
        'noplaylist': True,
        'quiet': False,
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            print(f"Descargando video de {url}...")
            info_dict = ydl.extract_info(url, download=True)
            video_title = limpiar_nombre_archivo(info_dict['title'])

            # Renombrar el archivo descargado
            original_video_file = os.path.join(videos_folder, f"{info_dict['title']}.mp4")
            cleaned_video_file = os.path.join(videos_folder, f"{video_title}.mp4")

            if os.path.exists(original_video_file):
                os.rename(original_video_file, cleaned_video_file)

            # Convertir el video descargado a MP3
            print(f"Convirtiendo {cleaned_video_file} a MP3...")
            audio = AudioFileClip(cleaned_video_file)
            mp3_file = os.path.join(music_folder, f"{video_title}.mp3")
            audio.write_audiofile(mp3_file, codec='mp3')
            print(f"Archivo MP3 guardado en {mp3_file}")
            os.remove(cleaned_video_file)

    except yt_dlp.utils.DownloadError as e:
        print(f"Error al intentar descargar el video {url}: {e}")
    except Exception as e:
        print(f"Ocurrió un error durante la descarga del video {url}: {e}")



def obtener_url_playlist_desde_video(video_url):
    """
    Extrae la URL de una lista de reproducción a partir de la URL de un video de la lista.
    """
    match = re.search(r"list=([a-zA-Z0-9_-]+)", video_url)
    if match:
        playlist_url = f"https://www.youtube.com/playlist?list={match.group(1)}"
        print(f"URL de la lista de reproducción: {playlist_url}")
        return playlist_url
    print("No se encontró un ID de lista de reproducción en la URL proporcionada.")
    return None

def obtener_titulos_playlist_spotify(playlist_id):
    """
    Obtiene los títulos de las canciones en una lista de reproducción de Spotify.
    """
    results = sp.playlist_tracks(playlist_id)
    return [track['track']['name'] for track in results['items']]

def mostrar_menu():
    """
    Muestra el menú principal y gestiona la opción seleccionada por el usuario.
    """
    print("\nBienvenido al descargador de videos y canciones!")
    print("Seleccione una opción:")
    print("1) Buscar y descargar un video de YouTube")
    print("2) Ingresar URLs de videos para descargar")
    print("3) Descargar todos los videos de una lista de reproducción de YouTube")
    print("4) Descargar canciones de una lista de reproducción de Spotify")

    opcion = input("Elige una opción (1/2/3/4): ").strip()
    return opcion

def main():
    while True:
        opcion = mostrar_menu()

        if opcion == '1':
            query = input("Introduce el término de búsqueda en YouTube: ").strip()
            if query:
                video_url = buscar_video_youtube(query)
                if video_url:
                    descargar_video(video_url)

        elif opcion == '2':
            urls_input = input("Introduce las URLs de los videos de YouTube (separadas por comas): ").strip()
            urls = [url.strip() for url in urls_input.split(",")]
            for url in urls:
                descargar_video(url)

        elif opcion == '3':
            playlist_url = input("Introduce la URL de un video de la lista de reproducción de YouTube: ").strip()
            playlist_url = obtener_url_playlist_desde_video(playlist_url)
            if playlist_url:
                video_urls = extraer_urls_playlist(playlist_url)
                for url in video_urls:
                    descargar_video(url)

        elif opcion == '4':
            spotify_playlist_url = input("Introduce la URL de la playlist de Spotify: ").strip()
            match = re.search(r"playlist/([a-zA-Z0-9_-]+)", spotify_playlist_url)
            if match:
                playlist_id = match.group(1)
                titles = obtener_titulos_playlist_spotify(playlist_id)
                no_encontrados = []
                for title in titles:
                    video_url = buscar_video_youtube(title)
                    if video_url:
                        descargar_video(video_url)
                    else:
                        no_encontrados.append(title)
                if no_encontrados:
                    print("\nNo se encontraron videos para los siguientes títulos:")
                    for titulo in no_encontrados:
                        print(f"- {titulo}")
            else:
                print("No se encontró una playlist válida en la URL de Spotify.")
        
        else:
            print("Opción no válida. Intente de nuevo.")
        
        continuar = input("¿Desea realizar otra operación? (s/n): ").strip().lower()
        if continuar != 's':
            print("Gracias por usar el descargador. ¡Hasta la próxima!")
            break

if __name__ == "__main__":
    main()
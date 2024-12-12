# Youtube-Spotify-Downloader
Simple Youtube - Spotify Downloader
Descripción
Este proyecto es un descargador de videos de YouTube y canciones de playlists de Spotify. Permite a los usuarios buscar y descargar videos de YouTube por términos de búsqueda y descargar canciones de listas de reproducción de Spotify directamente en su dispositivo. Además, convierte videos descargados a archivos de audio MP3.

Características
Búsqueda y descarga de videos de YouTube: Permite buscar videos en YouTube por términos específicos, incluyendo versiones con 'lyrics'.
Descarga de listas de reproducción de YouTube: Extrae todas las URLs de videos de una lista de reproducción y permite descargarlos.
Conversión de videos a MP3: Convierte videos descargados a archivos de audio MP3.
Integración con Spotify: Permite descargar canciones de playlists de Spotify y busca sus versiones de YouTube.
Requisitos
Python 3.x
Librerías necesarias:
moviepy==1.0.3
spotipy==2.24.0
yt_dlp==2024.12.6
Puedes instalar las librerías necesarias usando pip:

bash
Copiar código
pip install moviepy==1.0.3 spotipy==2.24.0 yt_dlp==2024.12.6
Configuración
Configuración de autenticación de Spotify:

Crea un nuevo proyecto en Spotify Developer Dashboard para obtener las credenciales CLIENT_ID, CLIENT_SECRET y REDIRECT_URI.
Sustituye las variables en el código con tus credenciales.
Usa el descargador:

Buscar y descargar un video de YouTube: Ejecuta el script y selecciona la opción 1. Introduce un término de búsqueda y selecciona el video deseado para descargar.
Ingresar URLs de videos para descargar: Selecciona la opción 2 y introduce las URLs de los videos de YouTube separadas por comas.
Descargar todos los videos de una lista de reproducción de YouTube: Selecciona la opción 3 y proporciona la URL de un video en la lista de reproducción. El script extraerá las URLs y las descargará.
Descargar canciones de una lista de reproducción de Spotify: Selecciona la opción 4, introduce la URL de la playlist de Spotify y el script buscará versiones de los títulos de la playlist en YouTube y las descargará.
Archivos de salida:

Los videos descargados se guardan en una carpeta Videos en el sistema.
Los archivos MP3 convertidos se guardan en una carpeta Music en el sistema.
Ejemplo de uso
bash
Copiar código
python script.py
Contribuir
Si deseas contribuir a este proyecto, siéntete libre de hacerlo creando un pull request con tus cambios.

Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

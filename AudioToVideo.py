import os
import random
import glob
import moviepy.editor as mpe
import subprocess

#### METODOS ####
RUTA_SALIDA = "Resultados/"
RUTA_VIDEO = "Convertir/"
RUTA_MUSICA = "Musica/"
CONFIGURATION_FILE = "config.txt"

# Crear un diccionario para realizar el seguimiento del uso de las canciones
cancion_uso = {}
# Máximo de repeticiones de una canción
MAX_REPETICIONES = 3
# Delay del video a la hora de crearlo en segundos
DELAY_VIDEO = 4
# Extensión del video
EXTENSION_VIDEO = ".mp4"
# Extensión del audio
EXTENSION_AUDIO = ".mp3"
def agregar_canciones_aleatorias_a_videos(NOMBRE_VIDEOS_SALIDA):
    # Directorio que contiene los videos
    videos_folder = RUTA_VIDEO

    # Patrón para buscar archivos de video en la carpeta
    video_pattern = '*'+ EXTENSION_VIDEO

    # Obtener la lista de nombres de archivo de los videos
    video_files = glob.glob(videos_folder + video_pattern)

    # Directorio que contiene las canciones
    music_folder = RUTA_MUSICA

    # Obtener la lista de nombres de archivo de las canciones
    music_files = glob.glob(music_folder + '*'+ EXTENSION_AUDIO)

    # Contador para el índice del video
    video_index = 1

    # Cantidad de canciones necesarias dependiendo de la cantidad de videos y el máximo de repeticiones
    cantidad_canciones_necesarias = len(video_files)/MAX_REPETICIONES

    if (cantidad_canciones_necesarias < len(music_files)):
        # Procesar cada video
        for video_file in video_files:
            # Seleccionar una canción aleatoria
            selected_music = random.sample(music_files, 1)

            # Obtener el nombre del archivo de canción sin la extensión
            cancion_filename = os.path.splitext(os.path.basename(selected_music[0]))[0]

            # Comprobamos si la canción se ha usado ya el máximo de veces
            if cancion_filename in cancion_uso and len(cancion_uso[cancion_filename]) >= MAX_REPETICIONES:
                # Si se ha usado el máximo de veces, la eliminamos de la lista de canciones
                music_files.remove(selected_music[0])
                # Seleccionar una canción aleatoria de la lista actualizada
                selected_music = random.sample(music_files, 1)

            agregar_cancion_a_video(video_file, selected_music[0], NOMBRE_VIDEOS_SALIDA +"-"+ str(video_index), cancion_filename)
            video_index += 1

        # Mostrar los resultados de uso de las canciones
        print("-" * 30)
        print("Uso de canciones:")
        print("-" * 30)
        for cancion, videos in cancion_uso.items():
            print(f"Canción: {cancion}")
            print("Videos:")
            for video in videos:
                print(video)
            print("-" * 20)
    else:
        print("No hay suficientes canciones para todos los videos, agrega al menos "+ (cantidad_canciones_necesarias - len(music_files)) +" canciones más.")
def agregar_cancion_a_video(video_path, audio_path, video_filename, cancion_filename):
    # Cargar el video
    video = mpe.VideoFileClip(video_path)

    # Obtener la duración del video
    video_duration = video.duration

    # Construir el nombre de archivo de salida
    output_filename = f'{video_filename}{EXTENSION_VIDEO}'
    output_path = os.path.join(RUTA_SALIDA, output_filename)

    # Muxear el audio al video utilizando FFmpeg
    muxear_audio(video_path, video_duration, audio_path, output_path)

    # Añadimos un fade-out al final del video
    # El fade del logo se ha hecho con el comando  ffmpeg -i logo.mp4 -vf "fade=t=in:st=0:d=1" logo_fade.mp4
    output_filename_fade = f'{video_filename}_fade{EXTENSION_VIDEO}'
    output_path_fade = os.path.join(RUTA_SALIDA, output_filename_fade)

    fade_to_video(output_path,video_duration,output_path_fade)

    # Modificamos en el config.txt el nombre dla primera linea para que coincida con la ruta del video
    with open(CONFIGURATION_FILE, 'r') as file:
        data = file.readlines()
    data[0] = "file '" + output_path_fade + "'\n"
    with open(CONFIGURATION_FILE, 'w') as file:
        file.writelines(data)

    #Concatenamos el logo
    # Con esto se hace el video del logo -> ffmpeg -loop 1 -i ./logo.jpg -c:v libx264 -t 5 -pix_fmt yuv420p -vf scale=1072:1440 .\logo.mp4
    muxear_logo(video_filename)

    # Actualizar el seguimiento de uso de canciones
    if cancion_filename not in cancion_uso:
        cancion_uso[cancion_filename] = [video_filename]
    else:
        cancion_uso[cancion_filename].append(video_filename)

    # Eliminar el video original y el video con fade
    os.remove(output_path)
    os.remove(output_path_fade)

def muxear_audio(video_path, video_duration, audio_path, output_path):
    print("Muxeando video: "+ video_path +" en: "+ output_path)
    # Comando de FFmpeg para muxear el audio al video
    comando = f'ffmpeg -i {video_path} -i "{audio_path}" -c:a aac -map 0:v:0 -map 1:a:0 -ss 00:00:00 -to {video_duration + DELAY_VIDEO} {output_path}'
    # Ejecutar el comando de FFmpeg
    subprocess.call(comando, shell=True)

def fade_to_video(video_path,video_duration,output_path):
    print("Aplicando fade-out a: "+ video_path)
    # Comando de FFmpeg para aplicar el fade-out al video
    comando = f'ffmpeg -i {video_path} -vf "fade=t=out:st={video_duration - 1}:d=0.5" {output_path}'
    # Ejecutar el comando de FFmpeg
    subprocess.call(comando, shell=True)
def muxear_logo(video_filename):
    print("Muxeando logo")

    # Construir el nombre de archivo final de salida
    output_filename = f'VV_{video_filename}{EXTENSION_VIDEO}'
    output_path = os.path.join(RUTA_SALIDA, output_filename)

    # Comando de FFmpeg para concatenar los videos
    comando = f'ffmpeg -f concat -safe 0 -i {CONFIGURATION_FILE} -c copy {output_path} '
    # Ejecutar el comando de FFmpeg
    subprocess.call(comando, shell=True)
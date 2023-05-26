import tkinter as tk
from tkinter import scrolledtext
import AudioToVideo as atov

NOMBRE_VIDEOS_SALIDA = "ComunionGema"

if __name__ == '__main__':

    # Crear la ventana principal en el centro del monitor
    root = tk.Tk()
    root.title('Aplicación de videos y música')
    root.geometry('400x300')
    root.eval('tk::PlaceWindow . center')

    # Crear un ScrolledText para mostrar el resultado de cancion_uso
    st = scrolledtext.ScrolledText(root, width=40, height=10)
    st.pack()

    def agregar_canciones_a_videos_y_mostrar_resultado():
        # Llamar a la función en main.py
        atov.agregar_canciones_aleatorias_a_videos(NOMBRE_VIDEOS_SALIDA)

        # Mostrar el resultado en el ScrolledText
        st.delete('1.0', tk.END)  # Limpiar el ScrolledText
        for cancion, videos in atov.cancion_uso.items():
            st.insert(tk.END, f"Canción: {cancion}\nVideos:\n")
            for video in videos:
                st.insert(tk.END, f"{video}\n")
            st.insert(tk.END, '-' * 20 + '\n')

    # Crear un botón que llame a la función cuando se haga clic en él
    boton = tk.Button(root, text='Agregar canciones a videos', command=agregar_canciones_a_videos_y_mostrar_resultado)
    boton.pack()

    # Ejecutar la aplicación
    root.mainloop()
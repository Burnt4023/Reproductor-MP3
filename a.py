import pygame
import customtkinter as CTk
from tkinter import filedialog
from PIL import Image, ImageTk
import os

Archivo = None
Archivos = []
Current = -1
Paused = False
# Fotos
png_play = CTk.CTkImage(Image.open("assets/play.jpg"), size=(26, 26))
png_pause = CTk.CTkImage(Image.open("assets/pause.jpg"), size=(26, 26))
png_next = CTk.CTkImage(Image.open("assets/next.jpg"), size=(26, 26))
png_rewind = CTk.CTkImage(Image.open("assets/rewind.jpg"), size=(26, 26))
png_previous = CTk.CTkImage(Image.open("assets/previous.jpg"), size=(26, 26))

def load_files():
    global Archivos
    archivos = filedialog.askopenfiles(filetypes=[("Archivos de audio", "*.mp3")])
    if archivos:
        Archivos.extend(archivo.name for archivo in archivos)
        print(f"{len(archivos)} archivos mp3 cargados correctamente.")
    else:
        print("No se seleccionó ningún archivo mp3.")


def load_playlist():
    global Archivos
    playlist_file = filedialog.askopenfile(filetypes=[("Archivos de texto", "*.txt")])
    if playlist_file:
        with open(playlist_file.name, "r") as playlist:
            for song_path in playlist:
                song_path = song_path.strip()
                if os.path.exists(song_path):
                    Archivos.append(song_path)
            root.title(f"Alexa, play: {len(Archivos)} archivos cargados")
        print(f"Playlist {os.path.basename(playlist_file.name)} cargada correctamente.")
    else:
        print("No se seleccionó ningún archivo de texto.")

def save_playlist():
    global Archivos
    filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])
    if filename:
        with open(filename, 'w') as playlist_file:
            for song_path in Archivos:
                playlist_file.write(song_path + "\n")
        print("Playlist guardada correctamente.")
    else:
        print("No se seleccionó ningún archivo para guardar.")

def Menu_Opciones_fn(opcion):
    if opcion == "Añadir varios Archivos":
        load_files()
    elif opcion == "Cargar Playlist":
        load_playlist()
    elif opcion == "Guardar Playlist":
        save_playlist()


def play_next():
    global Current
    global Paused
    Paused = False
    if Archivos and Current < len(Archivos) - 1:
        Current += 1
        pygame.mixer.music.load(Archivos[Current])
        pygame.mixer.music.play()
        root.title(f"Alexa, play: {os.path.basename(Archivos[Current])}")
    else:
        print("No hay más canciones en la lista.")

def play_previous():
    global Current
    global Paused
    Paused = False
    if Archivos and Current > 0:
        Current -= 1
        pygame.mixer.music.load(Archivos[Current])
        pygame.mixer.music.play()
        root.title(f"Alexa, play: {os.path.basename(Archivos[Current])}")
    else:
        print("No hay canciones anteriores en la lista.")

def play_button():
    global Paused
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        Paused = True
        BotonPlay.configure(image=png_play)
    else:
        pygame.mixer.music.unpause()
        Paused = False
        BotonPlay.configure(image=png_pause)


def check_music():
    if not pygame.mixer.music.get_busy() and Archivos:
        if not Paused:
            play_next()
    root.after(1000, check_music)


# Inicializar la ventana principal
root = CTk.CTk()
root.title("Alexa, play:")
root.geometry("800x600")

# Inicializar el subsistema de video de Pygame
pygame.mixer.init()

# Crear el menú de opciones
Menu_Opciones = CTk.CTkOptionMenu(
    root,
    values=["Añadir varios Archivos", "Cargar Playlist", "Guardar Playlist"],
    fg_color="white",  # Color de fondo del OptionMenu
    text_color="grey",  # Color del texto del OptionMenu
    button_color="white",  # Color del botón del OptionMenu
    button_hover_color="grey",  # Color del botón al pasar el mouse
    corner_radius=0,
    command=Menu_Opciones_fn
)
Menu_Opciones.place(x=0, y=0)

# Crear el botón de reproducción con la imagen PNG como fondo
BotonPlay = CTk.CTkButton(
    root,
    text="",
    image=png_play,
    command=play_button,
    width=0,
    height=0,
    fg_color=root.cget("background")
)
BotonPlay.place(x=380, y=500)

BotonNext = CTk.CTkButton(
    root,
    text="",
    image=png_next,
    command=play_next,
    width=0,
    height=0,
    fg_color=root.cget("background")
)
BotonNext.place(x=420, y=500)

BotonRewind = CTk.CTkButton(
    root,
    text="",
    image=png_rewind,
    command=pygame.mixer.music.rewind,
    width=0,
    height=0,
    fg_color=root.cget("background")
)
BotonRewind.place(x=340, y=500)

BotonPrevious= CTk.CTkButton(
    root,
    text="",
    image=png_previous,
    command=play_previous,
    width=0,
    height=0,
    fg_color=root.cget("background")
)
BotonPrevious.place(x=300, y=500)

# Bucle principal de la aplicación
check_music()
root.mainloop()
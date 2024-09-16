import os
from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move as shutil_move
from time import sleep
import logging
from tkinter import *
from tkinter import filedialog

source_f = ''

def source_button():
    global source_f
    source_f = filedialog.askdirectory()
    folder_path.set(source_f)
    print(source_f)

#definire fisiere
dest_f_sfx = r"C:\Users\vasil\Downloads\SFX"
dest_f_video = r"C:\Users\vasil\Downloads\Video"
dest_f_music = r"C:\Users\vasil\Downloads\Muzica"
dest_f_image = r"C:\Users\vasil\Downloads\Poze"
dest_f_documents = r"C:\Users\vasil\Downloads\Documente"
dest_f_torrents = r"C:\Users\vasil\Downloads\Torrente"
dest_f_altele = r"C:\Users\vasil\Downloads\Altele"
#definire extensii
image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw", ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg", ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]
audio_extensions = [".m4a", ".flac", ".mp3", ".wav", ".wma", ".aac"]
document_extensions = [".doc", ".docx", ".odt", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]
torrent_extensions = [".tpb"]

#Schimba numele daca este cazul
def makeUnique(dest, name):
    filename, extension = splitext(name)
    c = 1
    while exists(join(dest, name)):
        name = f"{filename}({str(c)}){extension}"
        c += 1
    return name

#Muta fisierele si afiseaza un mesaj informativ
def move_f(dest, entry, name):
    destination_path = join(dest, name)
    if exists(destination_path):
        unique_name = makeUnique(dest, name)
        destination_path = join(dest, unique_name)
    shutil_move(entry.path, destination_path)
    logging.info(f"Moved {entry.path} to {destination_path}")

def check_and_move(entry, name):
        if check_extension(name, audio_extensions):
            if entry.stat().st_size < 25000000 or "SFX" in name:
                move_f(dest_f_sfx, entry, name)
            else:
                move_f(dest_f_music, entry, name)
        elif check_extension(name, video_extensions):
            move_f(dest_f_video, entry, name)
        elif check_extension(name, image_extensions):
            move_f(dest_f_image, entry, name)
        elif check_extension(name, document_extensions):
            move_f(dest_f_documents, entry, name)
        elif check_extension(name, torrent_extensions):
            move_f(dest_f_torrents, entry, name)
        else : 
            move_f(dest_f_altele, entry, name)
    #Verificare daca fisierul se termina cu una dintre extensii
def check_extension(name, extensions):
        return any(name.lower().endswith(ext) for ext in extensions)
def organizare():
        if not source_f: 
            logging.warning("Nu a fost selectat niciun director sursă.")
            return
        with scandir(source_f) as entries:
            for entry in entries:
                if entry.is_file():
                    name = entry.name
                    check_and_move(entry, name)

def run_program():
    logging.info("Am inceput organizarea...")
    organizare()
    logging.info("Organizare efectuata !")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

window = Tk()
window.geometry("400x300")
window.title("Organizator fisiere")
window.config(background="grey")

folder_path = StringVar()

# Frame pentru a centra widgeturile
frame = Frame(window, bg="grey")
frame.pack(expand=True)

# Label
lbl1 = Label(master=frame, textvariable=folder_path, bg="grey")
lbl1.pack(pady=5)

# Browse Button
button2 = Button(frame, text="Browse", command=source_button)
button2.pack(pady=5)

# Run Button
run_button = Button(frame, text="Start", command=run_program)
run_button.pack(pady=5)
window.mainloop()
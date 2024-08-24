import os
from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move as shutil_move
from time import sleep
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

#definire fisiere
source_f = r"C:\Users\vasil\Downloads"
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

class MoveHandler(FileSystemEventHandler):
    #Este apelata cand este detectata o modificare si apeleaza metodele de mai jos
    def on_modified(self, event):
        with scandir(source_f) as entries:
            for entry in entries:
                if entry.is_file():
                    name = entry.name
                    self.check_and_move(entry, name)
                    
    def check_and_move(self, entry, name):
        if self.check_extension(name, audio_extensions):
            if entry.stat().st_size < 25000000 or "SFX" in name:
                move_f(dest_f_sfx, entry, name)
            else:
                move_f(dest_f_music, entry, name)
        elif self.check_extension(name, video_extensions):
            move_f(dest_f_video, entry, name)
        elif self.check_extension(name, image_extensions):
            move_f(dest_f_image, entry, name)
        elif self.check_extension(name, document_extensions):
            move_f(dest_f_documents, entry, name)
        elif self.check_extension(name, torrent_extensions):
            move_f(dest_f_torrents, entry, name)
        else : 
            move_f(dest_f_altele, entry, name)
    #Verificare daca fisierul se termina cu una dintre extensii
    def check_extension(self, name, extensions):
        return any(name.lower().endswith(ext) for ext in extensions)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_f
    event_handler = MoveHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
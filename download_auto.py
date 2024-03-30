import os
import sys
import time
import shutil
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# Do not forget to change the paths for this directories
# If you're on Windows change "\" to "\\"
source_dir = ""
dest_dir_sfx = ""
dest_dir_music = ""
dest_dir_video = ""
dest_dir_image = ""
dest_dir_documents = ""
dest_dir_programming = ""
dest_dir_other = ""

# Supported image types
image_exts = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".eps", 
             ".psd", ".raw", ".arw", ".cr2", ".nrw", ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".ai",
             ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ico"]
# Supported Video types
video_exts = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg", ".mp4", ".mp4v", 
             ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]
# Supported Audio types
audio_exts = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]
# Supported Document types
document_exts = [".doc", ".docx", ".odt", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx", ".pptm"]

programming_exts = [".cpp", ".java", ".txt", ".csv", ".py", ".exe", ".pl", ".v", ".tex", ".qsf"]




# Function to check the extensions
def endswith(s, suffix):
    """
    Check if string 's' ends with the specified suffix.

    Args:
    s (str): The string to check.
    suffix (str): The suffix to check against the end of the string.

    Returns:
    bool: True if 's' ends with the specified suffix, False otherwise.
    """
    return s[-len(suffix):] == suffix


# Function to avoid repetitive filenames
def make_unique(dest, name):
    filename, extension = os.path.splitext(name)
    counter = 1
    # * IF FILE EXISTS, ADDS NUMBER TO THE END OF THE FILENAME
    while os.path.exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name

# Function move the file to correspondent directory
def move_file(dest, entry, name):
    if os.path.exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        oldName = os.path.join(dest, name)
        newName = os.path.join(dest, unique_name)
        os.rename(oldName, newName)
    shutil.move(entry, dest)


class MainFunction(FileSystemEventHandler) :
    def on_modified(self, event) :
        if event.is_directory:
            return
        with os.scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                self.check_audio_files(entry, name)
                self.check_video_files(entry, name)
                self.check_document_files(entry, name)
                self.check_image_files(entry, name)
                self.check_programming_files(entry, name)
                # self.check_other_files(entry, name)
                

    def check_audio_files(self, entry, name):  # * Checks all Audio Files
        for audio_extension in audio_exts:
            if endswith(name, audio_extension) or endswith(name, audio_extension.upper()):
                if entry.stat().st_size < 10_000_000 or "SFX" in name:  # ? 10Megabytes
                    dest = dest_dir_sfx
                else:
                    dest = dest_dir_music
                move_file(dest, entry, name)
                logging.info(f"Moved audio file: {name}")
                

    def check_video_files(self, entry, name):  # * Checks all Video Files
        for video_extension in video_exts:
            if endswith(name, video_extension) or endswith(name, video_extension.upper()):
                dest = dest_dir_video
                move_file(dest, entry, name)
                logging.info(f"Moved video file: {name}")

    def check_document_files(self, entry, name):  # * Checks all Document Files
        for document_extension in document_exts:
            if endswith(name, document_extension) or endswith(name, document_extension.upper()):
                dest = dest_dir_documents
                move_file(dest, entry, name)
                logging.info(f"Moved document file: {name}")

    def check_image_files(self, entry, name):  # Checks all Image Files
        for image_extension in image_exts:
            if endswith(name, image_extension) or endswith(name, image_extension.upper()):
                dest = dest_dir_image
                move_file(dest, entry, name)
                logging.info(f"Moved image file: {name}")

    def check_programming_files(self, entry, name):  # Checks all Programming Files
        for prog_extension in programming_exts:
            if endswith(name, prog_extension) or endswith(name, prog_extension.upper()):
                dest = dest_dir_programming
                move_file(dest, entry, name)
                logging.info(f"Moved programming file: {name}")

    def check_other_files(self, entry, name):  # * Checks all Other Files
        dest = dest_dir_other
        move_file(dest, entry, name)
        logging.info(f"Moved other file: {name}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MainFunction()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()




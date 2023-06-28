import os
import tkinter as tk
from PIL import Image, ImageTk
import cv2

# Calea către dosarul cu imaginile și fișierele video
MEDIA_FOLDER = "calea/media"

class Slideshow:
    def __init__(self, root, media_folder):
        self.root = root
        self.root.attributes("-fullscreen", True)
        self.root.config(cursor="none")
        self.media_folder = media_folder
        self.media_files = []
        self.current_media_index = 0

        # Creează un cadru pentru a afișa imaginea sau fișierul video
        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        #demensiunele ecranului
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # Încarcă imaginile și fișierele video
        self.load_media_files()

        # Afiseaza prima imagine sau fișier video
        self.show_media()

        # Porneste slideshow-ul
        self.root.after(5000, self.next_media)

    def load_media_files(self):
        # Obține dimensiunile ecranului
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        for filename in os.listdir(self.media_folder):
            file_path = os.path.join(self.media_folder, filename)
            if filename.endswith(".jpg"):
                # Încarcă imaginea
                image = Image.open(file_path)
                resized_image = image.resize((screen_width, screen_height), Image.LANCZOS)
                self.media_files.append(ImageTk.PhotoImage(resized_image))
            elif filename.endswith(".mp4"):
                # Încarcă fișierul video
                video = cv2.VideoCapture(file_path)
                self.media_files.append(video)

    def show_media(self):
        # Afiseaza imaginea sau fișierul video curent in cadrul creat
        current_media = self.media_files[self.current_media_index]
        if isinstance(current_media, ImageTk.PhotoImage):
            label = tk.Label(self.frame, image=current_media)
            label.image = current_media
            label.pack(fill=tk.BOTH, expand=True)
        else:
            video = current_media
            _, frame = video.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (self.screen_width, self.screen_height))
            image = Image.fromarray(frame)
            current_media = ImageTk.PhotoImage(image)
            label = tk.Label(self.frame, image=current_media)
            label.image = current_media
            label.pack(fill=tk.BOTH, expand=True)

            # Porneste un loop pentru a citi continuu cadrul curent din video
            def update_video():
                _, frame = video.read()
                if frame is not None:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame = cv2.resize(frame, (self.screen_width, self.screen_height))
                    image = Image.fromarray(frame)
                    current_media.paste(image)
                    label.configure(image=current_media)
                    label.image = current_media
                    self.root.after(10, update_video)
            update_video()



    def next_media(self):
        # Incrementam indexul imaginii sau fișierului video curent
        self.current_media_index += 1
        if self.current_media_index == len(self.media_files):
            self.current_media_index = 0

        # Șterge imaginea sau fișierul video vechi
        for widget in self.frame.winfo_children():
            widget.destroy()

        # Afiseaza urmatoarea imagine sau fișier video
        self.show_media()

        # Porneste urmatoarea imagine sau fișier
        #self.root.after(50000, self.next_media)

# Crează obiectul Tkinter
root = tk.Tk()

# Crează slideshow-ul
slideshow = Slideshow(root, MEDIA_FOLDER)

# Rulează bucla evenimentelor Tkinter
root.mainloop()

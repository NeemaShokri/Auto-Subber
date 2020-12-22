import tkinter as tk
import tkinter.font as tkFont
import tkinter.filedialog as explorer
import moviepy.editor as mp
import json
from CloudService import Cloud
from tkinter.ttk import Combobox
import wave

#from os import path
from pydub import AudioSegment

class Application(tk.Frame):

    def __init__(self, master = None):
        super().__init__(master)
        self.file = None
        self.lang_in = None
        self.lang_out = None
        self.language = json.load(open('languages.json'))
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        fontStyle = tkFont.Font(family = "Lucida Grande", size = 20)

        #Label for app title
        header = tk.Label(master = self, text = "Auto-Subber", font = fontStyle, width = 20)
        header.pack(side = "top")

        #Frame for choosing .mp4 file
        file_frame = tk.Frame(master = self)

        file_label = tk.Label(master = file_frame, text = "Choose .MP4 File")
        file_label.pack(side = "left")
        
        self.file = tk.Label(master = file_frame, bg = "white", width = 20)
        self.file.pack(side = "left")

        fileBrowse = tk.Button(master = file_frame, text = "Browse", command = self.browse_files)
        fileBrowse.pack(side = "left")
        
        file_frame.pack(pady=10)
        
        #Frame for choosing language the video is in
        lang_in_frame = tk.Frame(master = self)

        lang_in_label = tk.Label(master = lang_in_frame, text = "Choose Language of .MP4")
        lang_in_label.pack(side = "left")

        languages = list (self.language.keys())
        #self.lang_in = tk.StringVar(master = lang_in_frame)
        #self.lang_in.set(languages[0])

        lang_in_menu = Combobox(master = lang_in_frame, values = languages)
        lang_in_menu.set(languages[0])
        lang_in_menu.pack()
        self.lang_in = lang_in_menu

        lang_in_frame.pack(pady=10)

        #Frame for choosing the language you want subtitles in
        lang_out_frame = tk.Frame(master = self)

        lang_out_label = tk.Label(master = lang_out_frame, text = "Choose Language of Subtitles")
        lang_out_label.pack(side = "left")

        #self.lang_out = tk.StringVar(master = lang_out_frame)
        #self.lang_out.set(languages[0])
        
        lang_out_menu = Combobox(master = lang_out_frame, values = languages)
        lang_out_menu.set(languages[0])
        lang_out_menu.pack()
        self.lang_out = lang_out_menu

        lang_out_frame.pack(pady=10)

        #Button to generate .SRT file
        gen_srt = tk.Button(master = self, text = "Generate .SRT", command = self.generte_srt)
        gen_srt.pack(side = "bottom", pady=10)

    def generte_srt(self):
        print("File Path: " + self.file["text"])
        print("Input Language: " + self.lang_in.get() + " Language Code: " + self.language[self.lang_in.get()])
        print("Output Language: " + self.lang_out.get() + " Language Code: " + self.language[self.lang_out.get()])

        #audio_file = self.video_to_mp3(self.file["text"])

        cloud = Cloud(self.language[self.lang_in.get()], self.language[self.lang_out.get()])
        cloud.audio_to_text("Audio.mp3")

    def browse_files(self):
        file_name = explorer.askopenfilename()
        self.file.configure(text = file_name)

    def video_to_mp3(self, video_file):
        video = mp.VideoFileClip(self.file["text"])
        audio_file = video.audio.write_audiofile(video_file)
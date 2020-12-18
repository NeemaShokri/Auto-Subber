import tkinter as tk
import tkinter.font as tkFont
import tkinter.filedialog as explorer
import moviepy.editor as mp
import json
from CloudService import Cloud

from os import path
from pydub import AudioSegment

class Application(tk.Frame):

    def __init__(self, master = None):
        super().__init__(master)
        self.file = None
        self.lang_in = None
        self.lang_out = None
        self.language = json.load(open('languages.json'))
        print(type(self.language))
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
        
        file_frame.pack()
        
        #Frame for choosing language the video is in
        lang_in_frame = tk.Frame(master = self)

        lang_in_label = tk.Label(master = lang_in_frame, text = "Choose Language of .MP4")
        lang_in_label.pack(side = "left")

        languages = list (self.language.keys())
        self.lang_in = tk.StringVar(master = lang_in_frame)
        self.lang_in.set(languages[0])

        lang_in_menu = tk.OptionMenu(lang_in_frame, self.lang_in, *languages)
        lang_in_menu.pack()

        lang_in_frame.pack()

        #Frame for choosing the language you want subtitles in
        lang_out_frame = tk.Frame(master = self)

        lang_out_label = tk.Label(master = lang_out_frame, text = "Choose Language of Subtitles")
        lang_out_label.pack(side = "left")

        self.lang_out = tk.StringVar(master = lang_out_frame)
        self.lang_out.set(languages[0])

        lang_out_menu = tk.OptionMenu(lang_out_frame, self.lang_out, *languages)
        lang_out_menu.pack()

        lang_out_frame.pack()

        #Button to generate .SRT file
        gen_srt = tk.Button(master = self, text = "Generate .SRT", command = self.generte_srt)
        gen_srt.pack(side = "bottom")

    def generte_srt(self):
        print("File Path: " + self.file["text"])
        print("Input Language: " + self.lang_in.get())
        print("Output Language: " + self.lang_out.get())

        #video = mp.VideoFileClip(self.file["text"])
        #audio_file = video.audio.write_audiofile("Audio.mp3")
        
        src = "Audio.mp3"
        dst = "Audio.wav"

        # convert wav to mp3
        AudioSegment.converter = R"C:\Users\Neema\AppData\Local\Programs\Python\Python39\Lib\site-packages\ffmpeg"                                          
        sound = AudioSegment.from_mp3(src)
        sound.export(dst, format="wav")

        #mp3 = AudioSegment.from_mp3("Audio.mp3")
        #mp3.export("Audio.wav", format="wav")

        #cloud = Cloud()
        #cloud.audio_to_text("Audio.mp3", self.language[self.lang_in.get()])

    def browse_files(self):
        file_name = explorer.askopenfilename()
        self.file.configure(text = file_name)
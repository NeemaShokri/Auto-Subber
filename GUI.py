import tkinter as tk
import tkinter.font as tkFont
import tkinter.filedialog as explorer
# import moviepy.editor as mp
import json
from CloudService import Cloud
from tkinter.ttk import Combobox
import wave

# from os import path
from pydub import AudioSegment


class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.file = None
        self.lang_in = None
        self.lang_out = None
        self.language = json.load(open('languages.json'))
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        fontStyle = tkFont.Font(family="Lucida Grande", size=20)

        # Label for app title
        header = tk.Label(master=self, text="Auto-Subber", font=fontStyle, width=20)
        header.pack(side="top")

        # Frame for choosing .mp4 file
        file_frame = tk.Frame(master=self)

        file_label = tk.Label(master=file_frame, text="Choose .MP4 File")
        file_label.pack(side="left")

        self.file = tk.Label(master=file_frame, bg="white", width=20)
        self.file.pack(side="left")

        fileBrowse = tk.Button(master=file_frame, text="Browse", command=self.browse_files)
        fileBrowse.pack(side="left")

        file_frame.pack(pady=10)

        # Frame for choosing language the video is in
        lang_in_frame = tk.Frame(master=self)

        languages = list (self.language.keys())
        #self.lang_in = tk.StringVar(master = lang_in_frame)
        #self.lang_in.set(languages[0])

        lang_in_menu = Combobox(master=lang_in_frame, values=languages)
        lang_in_menu.set(languages[0])
        lang_in_menu.pack()
        self.lang_in = lang_in_menu

        lang_in_frame.pack(pady=10)

        # Frame for choosing the language you want subtitles in
        lang_out_frame = tk.Frame(master=self)

        lang_out_label = tk.Label(master=lang_out_frame, text="Choose Language of Subtitles")
        lang_out_label.pack(side="left")

        #self.lang_out = tk.StringVar(master = lang_out_frame)
        #self.lang_out.set(languages[0])
        
        lang_out_menu = Combobox(master = lang_out_frame, values = languages)
        lang_out_menu.set(languages[0])
        lang_out_menu.pack()
        self.lang_out = lang_out_menu

        lang_out_frame.pack(pady=10)

        # Button to generate .SRT file
        gen_srt = tk.Button(master=self, text="Generate .SRT", command=self.generte_srt)
        gen_srt.pack(side="bottom", pady=10)

    def generte_srt(self):
        print("File Path: " + self.file["text"])
        print("Input Language: " + self.lang_in.get())
        print("Output Language: " + self.lang_out.get())

        # video = mp.VideoFileClip(self.file["text"])
        # audio_file = video.audio.write_audiofile("Audio.mp3")

        # convert wav to mp3

        # mp3 = AudioSegment.from_mp3("Audio.mp3")
        # mp3.export("Audio.wav", format="wav")
        # self.mp3_to_wav(r"Audio.mp3")
        cloud = Cloud("en-US", "en-US")
        cloud.audio_to_text("Audio.mp3")

    def browse_files(self):
        file_name = explorer.askopenfilename()
        self.file.configure(text=file_name)

    def mp3_to_wav(self, audio_file_name):
        if audio_file_name.split('.')[1] == 'mp3':
            a = AudioSegment()
            sound = AudioSegment.from_mp3(audio_file_name)
            audio_file_name = audio_file_name.split('.')[0] + '.wav'
            sound.export(audio_file_name, format="wav")

    def stereo_to_mono(self, audio_file_name):
        sound = AudioSegment.from_wav(audio_file_name)
        sound = sound.set_channels(1)
        sound.export(audio_file_name, format="wav")

    def frame_rate_channel(self, audio_file_name):
        with wave.open(audio_file_name, "rb") as wave_file:
            frame_rate = wave_file.getframerate()
            channels = wave_file.getnchannels()
            return frame_rate, channels
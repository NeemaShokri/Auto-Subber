import tkinter as tk
from GUI import Application
import json
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\nshok\Desktop\Code\Auto Anime Subber\Auto-Subber\stt_key.json"
print(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])

#TK
window = tk.Tk()
window.title("Auto-Subber")
window.resizable(False, False)

#Application
app = Application(master = window)
app.mainloop()
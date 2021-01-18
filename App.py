import tkinter as tk
from GUI import Application
import json
import os

authentication = json.load(open("authentication.json"))

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = authentication["Service Account Key Path"]
print(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])

#TK
window = tk.Tk()
window.title("Auto-Subber")
window.resizable(False, False)

#Application
app = Application(master = window)
window.geometry("400x220")
app.mainloop()
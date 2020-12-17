import tkinter as tk
from GUI import Application
import requests

#TK
window = tk.Tk()
window.title("Auto-Subber")
window.resizable(False, False)

#Application
app = Application(master = window)
app.mainloop()
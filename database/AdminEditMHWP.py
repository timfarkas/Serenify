import tkinter as tk
from tkinter import messagebox
from database import Database
from adminFunctions import MHWPSelectionApp, MHWPEditApp

root = tk.Tk()

app = MHWPSelectionApp(root)

root.mainloop()


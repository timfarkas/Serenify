import tkinter as tk
from tkinter import messagebox
from database import Database
from adminFunctions import PatientSelectionApp, PatientEditApp

root = tk.Tk()

app = PatientSelectionApp(root)

root.mainloop()



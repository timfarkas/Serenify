import sys
import os
import tkinter as tk
from tkinter import messagebox
# project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database'))
# sys.path.append(project_root)
# from database import Database
# from entities import UserError, RecordError, Admin, Patient, MHWP, PatientRecord, Allocation, JournalEntry, MoodEntry, Appointment
# from datetime import datetime
# import pandas as pd

##TO BE DEVELOPED
#expand exercises --> add their own section with embedded links
#"either point to the URLs of the results (audios or videos) or embed the results into your application for the user to play directly."

#search bar to  exercises (for now its looking for journal entries)


#as sessions etc dont work yet -- for now current user_id will be hardcoded
#that needs to be resolved and automater though
current_user_id = 3

class Patient:
    def __init__(self, root):
        self.root = root
        self.root.title("Exercises")
        self.root.geometry("700x700")

        # Title label
        self.title_label = tk.Label(root, text="Exercises", font=("Arial", 24, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=6, pady=10)


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = Patient(root)
    root.mainloop()
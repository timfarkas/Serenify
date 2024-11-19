# import sys
# import os
import tkinter as tk
# from tkinter import messagebox
import webbrowser
# project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database'))
# sys.path.append(project_root)
# from database import Database
# from entities import UserError, RecordError, Admin, Patient, MHWP, PatientRecord, Allocation, JournalEntry, MoodEntry, Appointment
# from datetime import datetime
# import pandas as pd

##TO BE DEVELOPED
#expand exercises --> add their own section with embedded links
#--> cant embed mp3 using only installed packages
#search bar to  exercises (for now its looking for journal entries)

##### Will need it later??????? #####
# def search():
#     query = search_entry.get()  # Get the search query from the entry
#     if query:
#         # For demonstration, we'll just show a message box with the search term
#         tk.messagebox.showinfo("Search", f"You searched for: {query}")
#     else:
#         tk.messagebox.showwarning("Warning", "Please enter a search term.")

######### Likely needed for the search bar to function: ###########
# def open_link():
#     print("Link clicked!")  # Replace this with opening a web link if desired

# link = tk.Label(root, text="Click here", fg="blue", cursor="hand2")
# link.bind("<Button-1>", lambda e: open_link())
# link.pack()



#as sessions etc dont work yet -- for now current user_id will be hardcoded
#that needs to be resolved and automater though
current_user_id = 3

class Exercises:
    def __init__(self, root):
        self.root = root
        self.root.title("Mental Health Exercises")
        self.root.geometry("700x700")

        # H1 equivalent
        h1_label = tk.Label(root, text="Mental Health Exercises", font=("Arial", 24, "bold"))
        h1_label.pack()

        # List of Google Drive links (replace with your actual links)
        self.exerciselinks = [
            "https://drive.google.com/file/d/1nzkNZ9r2SWWn86NTDykEkCj4HosAgfGb/view?usp=sharing",
            "https://drive.google.com/file/d/1eucLhrVRBT7FCTzdbpns7MCLb4PILK0t/view?usp=sharing",
            "https://drive.google.com/file/d/1bxolVImwO3UwauOwuyDOaNp4SRvM1pAn/view?usp=sharing",
            "https://drive.google.com/file/d/1hGEntCirailnpjSlX4ZgGVbmd-qAQHr8/view?usp=sharing",
            "https://drive.google.com/file/d/1F837yW9qSkmQCjoQYkHssgVNcVSOQIe7/view?usp=sharing"
        ]
        self.button_titles = [
            "3 minutes breathing",
            "5 minutes breathing",
            "6 minutes breath awareness",
            "10 minutes breathing",
            "10 minutes breath awareness"
        ]
        # Loop through the links and create a button for each
        for i, link in enumerate(self.exerciselinks):
            button = tk.Button(root, text=self.button_titles[i], command=lambda url=link: self.open_link(url))
            button.pack(pady=5)  # Adjust padding as needed

    def open_link(self, url):
        # Opens the  URL in web browser
        webbrowser.open(url)

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = Exercises(root)
    root.mainloop()
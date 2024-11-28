import tkinter as tk
import pandas as pd
import webbrowser
import subprocess
from tkinter import messagebox
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sessions import Session

class Exercises:
    def __init__(self, root):
        self.root = root
        self.root.title("Mental Health Exercises")
        self.root.geometry("1000x800")

        # Initialize the session instance 
        self.session = Session()
        self.session.open()
        self.current_user_id = self.session.getId()

        # Search Bar and Clear Button
        self.search_frame = tk.Frame(root)
        self.search_frame.grid(row=0, column=3, pady=10)
        self.search_var = tk.StringVar()  # For holding the search input
        self.search_entry = tk.Entry(self.search_frame, textvariable=self.search_var, font=('Arial', 14))
        self.search_entry.grid(row=0, column=0, pady=10)
        self.search_button = tk.Button(self.search_frame, text="Search", command=self.search_exercises) 
        self.search_button.grid(row=0, column=1, pady=5)

        #Back button
        self.back_button = tk.Button(root, text="Back to the main page", command=self.backButton)
        self.back_button.grid(row=0, column=0, pady=10)
        
        # H1 equivalent
        h1_label = tk.Label(root, text="Mental Health Exercises", font=("Arial", 24, "bold"), fg = "light pink")
        h1_label.grid(row=1, column=0, columnspan=4, pady=10)

        #Exercise Data
        self.exercises = {
            "Breathing": [
                ("Three minute breathing", "https://drive.google.com/file/d/1nzkNZ9r2SWWn86NTDykEkCj4HosAgfGb/view?usp=sharing"),
                ("Five minute breathing", "https://drive.google.com/file/d/1eucLhrVRBT7FCTzdbpns7MCLb4PILK0t/view?usp=sharing"),
                ("Ten minute breathing", "https://drive.google.com/file/d/1hGEntCirailnpjSlX4ZgGVbmd-qAQHr8/view?usp=sharing"),
                ("Ten minute breath awareness", "https://drive.google.com/file/d/1F837yW9qSkmQCjoQYkHssgVNcVSOQIe7/view?usp=sharing")
            ],
            "Mindfulness": [
                ("Brief mindfulness practice", "https://drive.google.com/file/d/19spOJz71lzbZiX5CDX7L-YNXrQutJPJX/view?usp=sharing"),
                ("The Breathing Space", "https://drive.google.com/file/d/19cCxG03o26RJB57g4xMUdyoDQlvaK8vS/view?usp=sharing"),
                ("The Tension Release Meditation", "https://drive.google.com/file/d/1dcsW9byG8G4Gyb1hFvtFS27LnrBdfvDA/view?usp=sharing"),
                ("Three minute mindfulness of sounds", "https://drive.google.com/file/d/1gYU6ayzOSzZZtEAlfGJ3BlFmFt73zb9m/view?usp=sharing")
            ],
            "Body Scan": [
                ("Four minute body scan", "https://drive.google.com/file/d/1JZ6NgU55LvekM5ZlZDc1nl8NGTxH8MtZ/view?usp=sharing"),
                ("Fifteen minute body scan", "https://drive.google.com/file/d/1H0oMBIwIDAg3X3elQwI_i2CIFAbcgPBJ/view?usp=sharing"),
                ("Twenty minute body scan", "https://drive.google.com/file/d/1oYF9nJdaWtKzWfbltDy_w9dHNbYVJZ8m/view?usp=sharing"),
                ("Forty-five minute body scan", "https://drive.google.com/file/d/1l2LFEQ8zBv5jvEc8eQQ0LmdJ4VJttvUg/view?usp=sharing")
            ],
             "Sitting Meditations": [
                ("Sitting meditation", "https://drive.google.com/file/d/1xUdzMOWfUPxvCmHpVXF2yAaYa0A8WlKw/view?usp=sharing"),
                ("Breath, sounds, body,\nthoughts, emotions",  "https://drive.google.com/file/d/1MQwdGV2lo0-hpca5FU5zILx14mWhVCxH/view?usp=sharing"),
                ("Ten minute wisdom meditation",  "https://drive.google.com/file/d/1VuklSoQ69h1jWmU2CKTJ72RR9HRmCucB/view?usp=sharing"),
                ("Compassionate Breath", "https://drive.google.com/file/d/1toFaicXEpAKaUoDxqWnpg1l3FT137ifw/view?usp=sharing")
            ],
            "Self Guided Mindfulness": [
                ("Five minutes just bells","https://drive.google.com/file/d/184pqYcLJONCJ1HebGPU-0cb7r1lNUryL/view?usp=sharing"),
                ("Ten minutes just bells", "https://drive.google.com/file/d/1uN6aqizXIqfikNqXgDVB_Q04vTcipfdX/view?usp=sharing"),
                ("Twenty minute bells\nwith 5 minute intervals", "https://drive.google.com/file/d/1udX_gljjbK8ObuWVYxl-ZC3x-1T3kCG4/view?usp=sharing"),
                ("Forty-five minute bells\nwith 5 minute intervals ", "https://drive.google.com/file/d/19xq9fYf4TVCIGEW1R1Yd-mEgQdPqdfYT/view?usp=sharing")
            ],
            "Additional Exercises":[
                ("Silent Meditation Timer", "https://www.freemindfulness.org/silent-meditation-timer"),
                ("Gratitude Journaling", "https://ggia.berkeley.edu/practice/gratitude_journal"),
                ("Journaling Prompts", "https://dayoneapp.com/blog/journal-prompts/"),
                ("Square Breathing for Anxiety","https://www.youtube.com/watch?v=bF_1ZiFta-E")
            ],
            "Additional Resources":[
                ("Mental Health Crisis", "https://www.nhs.uk/nhs-services/mental-health-services/where-to-get-urgent-help-for-mental-health/"),
                ("Twenty minute yoga practice", "https://www.youtube.com/watch?v=b1H3xO3x_Js"),
                ("Physical Activity and Mental Health","https://www.mentalhealth.org.uk/explore-mental-health/a-z-topics/physical-activity-and-mental-health"),
                ("How to go on a mindful walk?", "https://www.mindful.org/6-ways-to-get-the-benefits-of-mindful-walking/")
            ]
        }
        self.create_exercise_buttons()

    #Call 999 in an Emergency
        self.emergency_label = tk.Label(root, text="Call 999 in an Emergency", font=("Arial", 14), fg = "red")
        self.emergency_label.grid(row=17, column=0, pady=5)

    def create_exercise_buttons(self):
        row = 2
        col = 0
        # Create buttons for each category and its exercises
        for category, exercises in self.exercises.items():
            # Add category label
            label = tk.Label(self.root, text=category, font=("Arial", 18, "bold"), fg="light blue")
            label.grid(row=row, column=col, columnspan=4, pady=5)

            row += 1  # Move to next row

            for i, (title, link) in enumerate(exercises):
                button = tk.Button(self.root, text=title, command=lambda url=link: self.open_link(url), height=2)
                button.grid(row=row, column=col, pady=2, padx=5, sticky="ew")
                col += 1
                if col == 4:  # Move to next row after every 4 buttons
                    col = 0
                    row += 1


    def open_link(self, url):
        # Opens the  URL in web browser
        webbrowser.open(url)
    
    def backButton(self):
        subprocess.Popen(["python3", "patient/patientMain.py"])
        self.root.destroy()

    def search_exercises(self):
        search_term = self.search_var.get().lower()
        if search_term:
            matching_exercises = []
            for category, exercises in self.exercises.items():
                for exercise_title, link in exercises:
                    if search_term in exercise_title.lower():
                        matching_exercises.append(f"Exercise {exercise_title} : {link})")
            
            if matching_exercises:
                results_text = "\n\n".join(matching_exercises)
                messagebox.showinfo("Search Results", f"Found matching exercises:\n\n{results_text}")
            else:
                messagebox.showinfo("Search Results", "No matching exercises found.")
        else:
            messagebox.showwarning("Empty Search", "Please enter a term to search.")
        self.search_var.set("")  # Clear the search bar




# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = Exercises(root)
    root.mainloop()

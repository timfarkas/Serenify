import sys
import os
import tkinter as tk
from tkinter import messagebox
import subprocess # This allows us to open other files
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import Database
from database.entities import Patient, JournalEntry, MoodEntry
from database.initDBwithDummyData import initDummyDatabase
from datetime import datetime
import pandas as pd

### Initialize the database with dummy data and save it
# db = Database(overwrite=True)  ### this causes the database to be initialized from scratch and overwrites any changes
# initDummyDatabase(db)
# db.close()

#TO DO:
#SESSIONS
#functioning logout (have a session after logging in)
#see mood display
#error checks?

#as sessions etc dont work yet -- for now current user_id will be hardcoded
#that needs to be resolved and automater though
current_user_id = 3

class Patient:
    def __init__(self, root):
        self.root = root
        self.root.title("Patient")
        self.root.geometry("700x700")

        # Title label
        self.title_label = tk.Label(root, text="Welcome back", font=("Arial", 24, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=6, pady=10)

        #Mood of the day
        self.mood_label = tk.Label(root, text="How are you feeling today?", font=("Arial", 12))
        self.mood_label.grid(row=1, column=0, columnspan = 6, pady=10)

        # Create the mood selection options
        self.radio_var = tk.IntVar()
        self.radio_var.set("")  # Default to no selection

        self.radio1 = tk.Radiobutton(root, text="Amazing", variable=self.radio_var, value="6", fg="black")
        self.radio2 = tk.Radiobutton(root, text="Great", variable=self.radio_var, value="5", fg="black")
        self.radio3 = tk.Radiobutton(root, text="Good", variable=self.radio_var, value="4", fg="black")
        self.radio4 = tk.Radiobutton(root, text="Okay", variable=self.radio_var, value="3", fg="black")
        self.radio5 = tk.Radiobutton(root, text="Could be better", variable=self.radio_var, value="2", fg="black")
        self.radio6 = tk.Radiobutton(root, text="Terrible", variable=self.radio_var, value="1", fg="black")

        # Grid the radio buttons
        self.radio1.grid(row=2, column=0)
        self.radio2.grid(row=2, column=1)
        self.radio3.grid(row=2, column=2)
        self.radio4.grid(row=2, column=3)
        self.radio5.grid(row=2, column=4)
        self.radio6.grid(row=2, column=5)

        # Mood comment
        self.mood_comment_frame = tk.Frame(root)
        self.mood_comment_frame.grid(row=3, column=0, columnspan=6, pady=10)

        self.mood_comment_label = tk.Label(self.mood_comment_frame, text="(Optional) Mood comment:", font=("Arial", 12))
        self.mood_comment_label.grid(row=0, column=0, padx=10)

        self.mood_comment_text = tk.Text(self.mood_comment_frame, height=2, width=40)
        self.mood_comment_text.grid(row=1, column=0, padx=10, pady=5)

        # Create a submit button to process the selected mood
        self.submit_button = tk.Button(root, text="Submit Mood", command=self.submit_mood)
        self.submit_button.grid(row=4, column=0, columnspan=6, pady=10)

        # Frame for displaying exercises based on mood
        self.exercise_frame = tk.Frame(root)
        self.exercise_frame.grid(row=4, column=0, columnspan=6, pady=20)

        # Journaling section
        self.journal_frame = tk.Frame(root)
        self.journal_frame.grid(row=5, column=0, columnspan=6, pady=10)

        self.journal_label = tk.Label(self.journal_frame, text="Journal Entry:", font=("Arial", 12))
        self.journal_label.grid(row=0, column=0, padx=10)

        self.journal_text = tk.Text(self.journal_frame, height=5, width=40)
        self.journal_text.grid(row=1, column=0, padx=10, pady=5)

        self.save_button = tk.Button(self.journal_frame, text="Save Journal Entry", command=self.save_journal_entry)
        self.save_button.grid(row=2, column=0, pady=5)

        # Search functionality
        self.search_label = tk.Label(self.journal_frame, text="Search Journal Entries:", font=("Arial", 12))
        self.search_label.grid(row=0, column=1, padx=10)

        self.search_entry = tk.Entry(self.journal_frame, width=30)
        self.search_entry.grid(row=1, column=1, padx=10)

        self.search_button = tk.Button(self.journal_frame, text="Search", command=self.search_journal_entries)
        self.search_button.grid(row=2, column=1, pady=5)

         # View all journal entries button
        self.view_entries_button = tk.Button(self.journal_frame, text="View All Journal Entries", command=self.view_all_journal_entries)
        self.view_entries_button.grid(row=3, column=1, pady=5)

        # Buttons
        self.exercises_page = tk.Button(root, text="Exercises", command = self.exercises)
        self.edit_into = tk.Button(root, text="Edit personal info", command = self.edit_information)
        self.appointments = tk.Button(root, text="Book an appointment", command = self.book)
        self.cancel_appointement = tk.Button(root, text="Cancel your appointment", command = self.cancel) ####RESCHEDULE????
        self.exercises_page.grid(row=7, column=0, columnspan = 6, pady=5)
        self.edit_into.grid(row=8, column=0, columnspan = 6, pady=5)
        self.appointments.grid(row=9, column=0, columnspan=6, pady=5)
        self.cancel_appointement.grid(row=10, column=0, columnspan = 6, pady=5)

        ######Link to logging out action when connected to database#######
        self.logout_button = tk.Button(root, text="Logout")  # command=self.exitUser
        self.logout_button.grid(row=11, column=0, columnspan = 6, pady=5)

        self.apply_initial_colors()

    def apply_initial_colors(self):
        # Define color mapping based on mood values
        color_mapping = {
            6: "green",  # Amazing (Green)
            5: "light green",  # Great (Light Green)
            4: "yellow",  # Good (Yellow)
            3: "orange",  # Okay (Orange)
            2: "red",  # Could be better (Red)
            1: "dark red",  # Terrible (Dark Red)
        }

        # Apply color to all radio buttons initially
        self.radio1.config(bg=color_mapping[6])
        self.radio2.config(bg=color_mapping[5])
        self.radio3.config(bg=color_mapping[4])
        self.radio4.config(bg=color_mapping[3])
        self.radio5.config(bg=color_mapping[2])
        self.radio6.config(bg=color_mapping[1])

    def submit_mood(self):
        # Get the selected mood
        self.selected_mood = self.radio_var.get()
        # Get the comment
        mood_comment = self.mood_comment_text.get("1.0", "end-1c").strip()

        if not self.selected_mood:
            messagebox.showwarning("No Mood Selected", "Please select a mood before submitting.")
            return
        else:
            mood_entry = MoodEntry(moodentry_id = None, patient_id=current_user_id, moodscore=self.selected_mood, comment=mood_comment, timestamp=datetime.now())
            db = Database() # opens data system
            db. insert_mood_entry(mood_entry)
            db. close()
            self.mood_comment_text.delete("1.0", "end")

        # Ask the user if they want to proceed to exercises
        self.response = messagebox.askquestion(
            title="Proceed to Exercises",
            message="Thank you for submitting your mood.\nWould you like to view recommended exercises?"
        )

        # Handle the response
        if self.response == 'yes':
            self.show_recommended_exercises()

    def show_recommended_exercises(self):
        # Clear any existing exercise widgets
        for widget in self.exercise_frame.winfo_children():
            widget.destroy()

        # Based on the selected mood, show appropriate exercises
        if self.selected_mood in [6, 5]:
            exercise_text = "Recommended exercises for a positive mood:\n- Gratitude journaling\n- Mindful walk\n- You can also try some physical exercise and meditation!"
        elif self.selected_mood in [4, 3]:
            exercise_text = "Recommended exercises for moderate mood:\n- Meditation\n- Journaling\n- Breathing exercises\n- Calling a friend or a family member\n- Physical activity such as yoga or even just going on a walk"
        elif self.selected_mood in [2, 1]:
            exercise_text = "Recommended emergency exercises:\n- Calling emergency helpline\n- Scheduling a therapy session\n- If you would rather talk to someone you know, try calling a friend or a family member\n- Deep breathing and meditation\n- Physical activity and meditation can help as well!"
        else:
            exercise_text = "No exercises available."

        # Display the exercise recommendations in the exercise frame
        exercises_label = tk.Label(self.exercise_frame, text=exercise_text, font=("Arial", 12), justify="left")
        exercises_label.pack()

        # Add a button to go back to mood selection
        back_button = tk.Button(self.exercise_frame, text="Back to Mood Selection", command=self.back_to_mood)
        back_button.pack(pady=10)

    def back_to_mood(self):
        # Clear any exercise-related content and show the mood selection again
        for widget in self.exercise_frame.winfo_children():
            widget.destroy()

        self.title_label.config(text="Welcome back")
        self.submit_button.config(state=tk.NORMAL)

    def save_journal_entry(self):
        # Save the journal entry to the database
        journal_text = self.journal_text.get("1.0", "end-1c").strip()

        if journal_text:
            # self.journal_entries.append(journal_text)
            journal_entry = JournalEntry(entry_id = None, patient_id=current_user_id, text=journal_text, timestamp=datetime.now())
            db = Database() # opens data system
            db. insert_journal_entry(journal_entry)
            db. close()
            messagebox.showinfo("Journal Entry Saved", "Your journal entry has been saved.")
            self.journal_text.delete("1.0", "end")
        else:
            messagebox.showwarning("Empty Entry", "Please write something in the journal.")

    def search_journal_entries(self):
        # Get search term and search the journal entries
        search_term = self.search_entry.get().strip().lower()

        if search_term:
            # Fetch journal entries
            db = Database()
            journal_entries = db.getRelation("JournalEntry")
            filtered_rows = journal_entries.getRowsWhereEqual('patient_id', current_user_id)
            self.journal_df = pd.DataFrame(filtered_rows)

            # Search the DataFrame for the term
            matching_entries = self.journal_df[self.journal_df[2].str.contains(search_term, case=False, na=False)]

            if not matching_entries.empty:
                results_text = "\n\n".join([f"Entry on {entry[3]}: {entry[2]}" for _, entry in matching_entries.iterrows()])
                messagebox.showinfo("Search Results", f"Found matching entries:\n\n{results_text}")
            else:
                messagebox.showinfo("Search Results", "No matching entries found.")
        else:
            messagebox.showwarning("Empty Search", "Please enter a term to search.")

    def view_all_journal_entries(self):
        db = Database()
        journal_entries = db.getRelation("JournalEntry")
        filtered_rows = journal_entries.getRowsWhereEqual('patient_id', current_user_id)
        self.journal_df = pd.DataFrame(filtered_rows)

        if not self.journal_df.empty:
            entries_text = "\n\n".join([f"Entry on {entry[3]}: {entry[2]}" for _, entry in self.journal_df.iterrows()])
            messagebox.showinfo("All Journal Entries", f"Your journal entries:\n\n{entries_text}")
        else:
            messagebox.showinfo("No Entries", "You don't have any journal entries.")

    def edit_information(self):
        # Edit information
        subprocess.Popen(["python3", "editInfo.py"])
        self.root.destroy()

    def exercises(self):
        # Edit information
        subprocess.Popen(["python3", "exercises.py"])
        self.root.destroy()

    def book(self):
        # Book an appointement
        subprocess.Popen(["python3", "patient/booking.py"])
        self.root.destroy()

    def cancel(self):
        # Cancel appointement 
        subprocess.Popen(["python3", "patient/cancel.py"])
        self.root.destroy()


# logout_button = tk.Button(root, text="Logout", command=self.exitUser) 
# logout_button.pack()

#     def exitUser(self):
#         pass
        ######### Inputs #########
        # username = self.username_entry.get()
        # password = self.password_entry.get()
        # role = self.user_role.get()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = Patient(root)
    root.mainloop()
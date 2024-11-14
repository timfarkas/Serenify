#import patientNew  # Dont think ill need it here at all
import tkinter as tk
from tkinter import messagebox
import subprocess # This allows us to open other files

#TO DO
#Needs to be connected to the database still
#for now only storing journal entries in a list (for database store with current date and time)
#mood should be stored in the database in the form of numbers (1-6??)
#mood --> color coded; add comment option
#expand exercises --> add their own section with embedded links
#"either point to the URLs of the results (audios or videos) or embed the results into your application for the user to play directly."
#link the button to appointments page
#functioning logout (have a session after logging in)
#search bar to  exercises (for now its looking for journal entries)
#Who is too see mood display? both doctor and patient ?


####Dont need it########
# def open_patient_new():
#     root.destroy()  # Close the login window
#     patientNew.open_patient_window()  # Open patient window

##### Will need it later #####
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


class Patient:
    def __init__(self, root):
        self.root = root
        self.root.title("Patient")
        self.root.geometry("700x700")

        # Title label
        self.title_label = tk.Label(root, text="Welcome back", font=("Arial", 24, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=5, pady=10)

        #Mood of the day
        self.mood_label = tk.Label(root, text="How are you feeling today?", font=("Arial", 12))
        self.mood_label.grid(row=1, column=0, columnspan = 5, pady=10)

        # Create the mood selection options
        self.radio_var = tk.StringVar()
        self.radio_var.set("")  # Default to no selection

        self.radio1 = tk.Radiobutton(root, text="Great", variable=self.radio_var, value="Great")
        self.radio2 = tk.Radiobutton(root, text="Good", variable=self.radio_var, value="Good")
        self.radio3 = tk.Radiobutton(root, text="Okay", variable=self.radio_var, value="Okay")
        self.radio4 = tk.Radiobutton(root, text="Could be better", variable=self.radio_var, value="Could be better")
        self.radio5 = tk.Radiobutton(root, text="Terrible", variable=self.radio_var, value="Terrible")

        # Grid the radio buttons
        self.radio1.grid(row=2, column=0)
        self.radio2.grid(row=2, column=1)
        self.radio3.grid(row=2, column=2)
        self.radio4.grid(row=2, column=3)
        self.radio5.grid(row=2, column=4)

        # Create a submit button to process the selected mood
        self.submit_button = tk.Button(root, text="Submit Mood", command=self.submit_mood)
        self.submit_button.grid(row=3, column=0, columnspan=5, pady=10)

        # Frame for displaying exercises based on mood
        self.exercise_frame = tk.Frame(root)
        self.exercise_frame.grid(row=4, column=0, columnspan=5, pady=20)

        # Journaling section
        self.journal_frame = tk.Frame(root)
        self.journal_frame.grid(row=5, column=0, columnspan=5, pady=10)

        self.journal_label = tk.Label(self.journal_frame, text="Journal Entry:", font=("Arial", 12))
        self.journal_label.grid(row=0, column=0, padx=10)

        self.journal_text = tk.Text(self.journal_frame, height=5, width=40)
        self.journal_text.grid(row=1, column=0, padx=10, pady=5)

        self.save_button = tk.Button(self.journal_frame, text="Save Journal Entry", command=self.save_journal_entry)
        self.save_button.grid(row=2, column=0, pady=5)

        # List to store journal entries #NEEDS TO BE CHANGED OFC
        self.journal_entries = []

        # Search functionality SAME HERE
        self.search_label = tk.Label(self.journal_frame, text="Search Journal Entries:", font=("Arial", 12))
        self.search_label.grid(row=0, column=1, padx=10)

        self.search_entry = tk.Entry(self.journal_frame, width=30)
        self.search_entry.grid(row=1, column=1, padx=10)

        self.search_button = tk.Button(self.journal_frame, text="Search", command=self.search_journal_entries)
        self.search_button.grid(row=2, column=1, pady=5)

        h2_label = tk.Label(root, text="Personal info:", font=("Arial", 12, "bold"))
        h2_label.grid(row=6, column=0, columnspan = 5,  pady= 10)

        # Buttons
        self.edit_into = tk.Button(root, text="Edit personal info", command = self.edit_information)
        #####Link the button to appointments#########
        self.appointments = tk.Button(root, text="Book/Cancel appointment")
        self.edit_into.grid(row=7, column=0, columnspan = 5, pady=5)
        self.appointments.grid(row=8, column=0, columnspan=5, pady=5)

        ######Link to logging out action when connected to database#######
        self.logout_button = tk.Button(root, text="Logout")  # command=self.exitUser
        self.logout_button.grid(row=9, column=0, columnspan = 5, pady=5)

    def submit_mood(self):
        # Get the selected mood
        self.selected_mood = self.radio_var.get()

        if not self.selected_mood:
            messagebox.showwarning("No Mood Selected", "Please select a mood before submitting.")
            return

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
        if self.selected_mood in ["Great", "Good"]:
            exercise_text = "Recommended exercises for a positive mood:\n- Gratitude journaling\n- Mindful walk\n- You can also try some physical exercise and meditation!"
        elif self.selected_mood in ["Okay", "Could be better"]:
            exercise_text = "Recommended exercises for moderate mood:\n- Meditation\n- Journaling\n- Breathing exercises\n- Calling a friend or a family member\n- Physical activity such as yoga or even just going on a walk"
        elif self.selected_mood == "Terrible":
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
        # Save the journal entry to the list
        journal_text = self.journal_text.get("1.0", "end-1c").strip()

        if journal_text:
            self.journal_entries.append(journal_text)
            messagebox.showinfo("Journal Entry Saved", "Your journal entry has been saved.")
            self.journal_text.delete("1.0", "end")
        else:
            messagebox.showwarning("Empty Entry", "Please write something in the journal.")

    def search_journal_entries(self):
        # Get search term and search the journal entries
        search_term = self.search_entry.get().strip().lower()

        if search_term:
            matching_entries = [entry for entry in self.journal_entries if search_term in entry.lower()]

            if matching_entries:
                results_text = "\n\n".join(matching_entries)
                messagebox.showinfo("Search Results", f"Found matching entries:\n\n{results_text}")
            else:
                messagebox.showinfo("Search Results", "No matching entries found.")
        else:
            messagebox.showwarning("Empty Search", "Please enter a term to search.")

    def edit_information(self):
        # Edit information
        subprocess.Popen(["python3", "patient/editInfo.py"])


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



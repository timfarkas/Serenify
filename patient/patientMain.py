import sys
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.entities import Allocation,User,Patient, JournalEntry, MoodEntry,Notification
from addfeature.chatroom import startchatroom
from addfeature.forum import openforsum
from patient.exercises import Exercises
from database.database import Database
from patient.editInfo import EditInfo
from patient.booking import AppointmentBooking
from addfeature.notificationbox import opennotification
from patient.patient_dashboard import openpatientdashboard
from patient.mhwp_rating import openrating
from sessions import Session
from datetime import datetime
import pandas as pd
from addfeature.globaldb import global_db
db=global_db

# LOADING DUMMY DATA
# from database.initDummyData import initDummyDatabase
# ## Initialize the database with dummy data and save it
# db = Database(overwrite=True)  ### this causes the database to be initialized from scratch and overwrites any changes
# initDummyDatabase(db, printOut=True)
# db.close()


class Patient:
    def __init__(self,user_id=None):
        # Initialize the session instance
        self.session = Session()
        self.session.open()
        self.current_user_id = self.session.getId()
        self.root = tk.Tk()
        self.root.title("Patient")
        self.root.geometry("600x650")

        # db = Database()
        self.patientName = db.getRelation("User").getRowsWhereEqual("user_id",self.current_user_id)[0][4]

        # Title label
        self.title_label = tk.Label(self.root, text=f"Welcome back, {self.patientName}!", font=("Arial", 24, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=6, pady=10)
        self.main_frame = tk.Frame(self.root, width=200)  # Define width for main_frame
        self.main_frame.grid(row=1, column=0, padx=10, pady=10) 

        # MOOD FRAME
        self.mood_frame = tk.LabelFrame(self.main_frame, text="How are you feeling today?", labelanchor="n",font=("Arial", 12), padx=10, pady=10,width=500,height=200)
        self.mood_frame.grid(row=0, column=0, padx=10, pady=10)
        self.mood_frame.grid_propagate(False)

        usermoodlog = db.getRelation('MoodEntry').getRowsWhereEqual('patient_id', self.current_user_id)
        if len(usermoodlog) > 0:
            lastrecorddate = usermoodlog[-1][4].strftime("%Y-%m-%d")
            nowdate = datetime.now().strftime("%Y-%m-%d")
            if lastrecorddate == nowdate:
                self.printlastmood()
            else:
                self.showmoodselection(self.mood_frame)
        else:
            self.showmoodselection(self.mood_frame)

        ### MHWP INFO AND FUNCTIONS
        ## get allocations of current patient where mhwp id is not deleted 
        allocation = db.getRelation("Allocation").getWhereEqual("patient_id", self.current_user_id).getRowsWhereLarger('mhwp_id', 0)
        
        if not allocation:
            self.allocated = False
            self.mhwp_text = text="You are currently not allocated to any MHWP. Please contact an administrator."
        else:
            self.allocated = True
            mhwp_id = allocation[0][Allocation.MHWP_ID]  
            mhwp_info = db.getRelation("User").getRowsWhereEqual("user_id", mhwp_id)
            mhwp_name = f"{mhwp_info[0][User.FNAME]} {mhwp_info[0][User.LNAME]}"  
            self.mhwp_text = f"Your MHWP: {mhwp_name}"

        mhwp_frame = tk.LabelFrame(self.main_frame,text=self.mhwp_text,labelanchor="n",font=("Arial", 12), padx=10, pady=10)
        mhwp_frame.grid(row=1, column=0, padx=20, pady=20)
        
        self.ratemhwp = tk.Button(mhwp_frame, text="Rate", command=lambda: openrating(), padx=5, width=12)
        self.ratemhwp.grid(row=2, column=2)

        self.openchat = tk.Button(mhwp_frame, text="Chat", command=lambda:startchatroom(self.current_user_id), padx=5, width=12)
        self.openchat.grid(row=2, column=1)

        self.appointments = tk.Button(mhwp_frame, text="Appointments", command=self.book, padx=5, width=12)
        self.appointments.grid(row=2, column=0)


        

        ### PERSONAL FUNCTIONS
        self.personal_frame = tk.Frame(self.main_frame)
        self.personal_frame.grid(row=2, padx=20, pady=20)

        notificationdata = db.getRelation('Notification').getRowsWhereEqual('new', True)
        self.messagecounter = 0
        for i in notificationdata:
            if i[1] == self.current_user_id:
                self.messagecounter += 1

        self.opendashboard = tk.Button(self.personal_frame, text="My well-being stats", command=self.patientdashboard, width=20)
        self.opendashboard.grid(row=0, column=0, pady=5, sticky="w")

        self.journal_entry = tk.Button(self.personal_frame, text="My Journal", command=self.openjournal, width=20)
        self.journal_entry.grid(row=0, column=1, pady=5, sticky="w")

        self.exercises_page = tk.Button(self.personal_frame, text="Exercises", command=self.exercises, width=20)
        self.exercises_page.grid(row=1, column=0, pady=5, sticky="w")

        self.openforum = tk.Button(self.personal_frame, text="Forum", command=lambda:openforsum(), width=20)
        self.openforum.grid(row=1, column=1, pady=5, sticky="w")

        ### APP MESSAGES
        self.message_frame = tk.Frame(self.main_frame)
        self.message_frame.grid(row=3, column=0, columnspan=2, pady=5)

        self.messagenum = tk.Label(self.message_frame, text=f"You have {self.messagecounter} new messages", width=40)
        self.messagenum.grid(row=0, column=1, sticky="w")

        self.messagebox = tk.Button(self.message_frame, text="My messages", command=lambda:opennotification(), width=40)
        self.messagebox.grid(row=1, column=1, sticky="w")

        ### EDIT PERSONAL INFO AND LOGOUT
        self.editandlogout_frame = tk.Frame(self.main_frame)
        self.editandlogout_frame.grid(row=4, column=0, columnspan=2, pady=5)

        self.edit_into = tk.Button(self.editandlogout_frame, text="Edit personal info", command=self.edit_information, width=20)
        self.edit_into.grid(row=0, column=0, pady=5, sticky="w")

        self.logout_button = tk.Button(self.editandlogout_frame, text="Logout", command=self.exitUser)
        self.logout_button.grid(row=0, column=1, pady=5, sticky="w")

        # Turns off all widgets if user is disabled, turns off mhwp functions if user is not allocated
        self.disable_interactive_widgets()
        self.disable_mhwp_widgets()
    
        self.root.after(1000, self.refresh)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def showmoodselection(self,fieldset1):
        self.radio_var = tk.IntVar()
        self.radio_var.set("")  # Default to no selection
        # Create the mood selection options
        self.radio1 = tk.Radiobutton(self.mood_frame, text="Amazing", variable=self.radio_var, value="6", fg="black")
        self.radio2 = tk.Radiobutton(self.mood_frame, text="Great", variable=self.radio_var, value="5", fg="black")
        self.radio3 = tk.Radiobutton(self.mood_frame, text="Good", variable=self.radio_var, value="4", fg="black")
        self.radio4 = tk.Radiobutton(self.mood_frame, text="Okay", variable=self.radio_var, value="3", fg="black")
        self.radio5 = tk.Radiobutton(self.mood_frame, text="Bad", variable=self.radio_var, value="2",
                                     fg="black")
        self.radio6 = tk.Radiobutton(self.mood_frame, text="Terrible", variable=self.radio_var, value="1", fg="black")

        # Grid the radio buttons
        self.radio1.grid(row=2, column=0, padx = 7)
        self.radio2.grid(row=2, column=1, padx = 7)
        self.radio3.grid(row=2, column=2, padx = 7)
        self.radio4.grid(row=2, column=3, padx = 7)
        self.radio5.grid(row=2, column=4, padx = 7)
        self.radio6.grid(row=2, column=5, padx = 7)

        # Mood comment
        self.mood_comment_frame = tk.Frame(self.mood_frame)
        self.mood_comment_frame.grid(row=3, column=0, columnspan=6, pady=10)

        self.mood_comment_label = tk.Label(self.mood_frame, text="(Optional) Mood comment:", font=("Arial", 12))
        self.mood_comment_label.grid(row=4, column=0, padx=10, columnspan=6)

        self.mood_comment_text = tk.Text(self.mood_frame, height=2, width=40)
        self.mood_comment_text.grid(row=5, column=0, padx=10, pady=5, columnspan=6)

        # Create a submit button to process the selected mood
        self.submit_button = tk.Button(self.mood_frame, text="Submit Mood", command=self.submit_mood)
        self.submit_button.grid(row=6, column=0, columnspan=6, pady=10)

        self.apply_initial_colors()
        # Turn off widgets if user is disabled
        self.disable_mood()

    def cleanmoodwindow(self):
        for widget in self.mood_frame.winfo_children():
            widget.destroy()

    def resetmood(self):
        response = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete today's record?")
        if response:
            # db=Database()
            allmoods = db.getRelation('MoodEntry')
            usermood = allmoods.getRowsWhereEqual("patient_id", self.current_user_id)
            lastmoodindex = usermood[-1][0]
            print(lastmoodindex)
            allmoods.data.drop(allmoods.data[allmoods.data['moodentry_id'] == lastmoodindex].index, inplace=True)
            allmoods.data.reset_index(drop=True, inplace=True)
            messagebox.showinfo("Success", f"Mood record deleted successfully.")
            print(db.getRelation('MoodEntry'))
            # db.close()
            self.cleanmoodwindow()
            self.showmoodselection(self.mood_frame)


    def moodlevelcheck(self):
        # db = Database()
        allmoods = db.getRelation('MoodEntry')
        usermood = allmoods.getRowsWhereEqual("patient_id", self.current_user_id)
        moodsum=0
        print("checkmood")
        if len(usermood)>=3:
            print("have three")
            for i in range(-1,-4,-1):
                moodsum+=usermood[i][2]
                print(moodsum)
            if (moodsum/3)<=2:
                print("bad mood found")
                matchingmhwp=db.getRelation('Allocation').getRowsWhereEqual('patient_id',self.current_user_id)
                mhwp_id=matchingmhwp[0][3]
                newnotify = Notification(
                    user_id=mhwp_id,
                    notifycontent="MoodAlert",
                    source_id=self.current_user_id,
                    new=True,
                    timestamp=datetime.now(),
                )
                db.insert_notification(newnotify)
                print("message sent")
                
    def printlastmood(self):
        self.mood_frame.grid_rowconfigure(0, weight=1)  # Ensure row expands
        self.mood_frame.grid_columnconfigure(0, weight=1)
        # db = Database()
        usermoodlog = db.getRelation('MoodEntry').getRowsWhereEqual('patient_id', self.current_user_id)
        self.lastmood = usermoodlog[-1][2]
        self.lastcomment = usermoodlog[-1][3]
        self.update_title = tk.Label(self.mood_frame, text=f"Congratulations! You have recorded your mood today",
                                    font=("Arial", 18, "bold"), anchor="n")
        self.update_text = tk.Label(self.mood_frame, text=f"You mood score: {self.lastmood}\n"
                                                         f"You Comment: {self.lastcomment}\n",

                                    font=("Arial", 14,))
        self.update_button = tk.Button(self.mood_frame, text="Delete and Redo", command=lambda: self.resetmood())
        self.update_title.grid(row=0, column=0, stick="nsew")
        self.update_text.grid(row=1, column=0, stick="nsew")
        self.update_button.grid(row=2, column=0, pady=5)

    def disable_interactive_widgets(self):
        #Remove some functionalities for disabled users
        try:
            user_info = db.getRelation("User")
            user_info = user_info.getRowsWhereEqual('user_id', self.current_user_id)
            user_info = pd.DataFrame(user_info)
            if not user_info.empty:
                #Accessing the is_disabled column using the numeric index - 10 (True/False)
                is_disabled = user_info.iloc[0][10]
            else: 
                is_disabled = False
                
            if is_disabled:
        
                # Disable buttons
                self.appointments.config(state=tk.DISABLED)
                self.journal_entry.config(state=tk.DISABLED)
                self.exercises_page.config(state=tk.DISABLED)
                self.edit_into.config(state=tk.DISABLED)
                self.ratemhwp.config(state=tk.DISABLED)
                self.openchat.config(state=tk.DISABLED)
                self.openforum.config(state=tk.DISABLED)
                self.messagebox.config(state=tk.DISABLED)
                # self.opendashboard.config(state=tk.DISABLED) #disabled user can see statistics dashnoard

                # Show message that the user is disabled
                messagebox.showinfo("Access Restricted", "Your account is disabled. You cannot make changes or submit new information.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while disabling widgets: {e}")

    def disable_mhwp_widgets(self):
        ###disable mhwp functions if user is not allocated yet
        if not self.allocated:
            self.ratemhwp.config(state=tk.DISABLED)
            self.openchat.config(state=tk.DISABLED)
            self.appointments.config(state=tk.DISABLED)
            
    def disable_mood(self):
        #Remove some functionalities for disabled users
        try:
            user_info = db.getRelation("User")
            user_info = user_info.getRowsWhereEqual('user_id', self.current_user_id)
            user_info = pd.DataFrame(user_info)
            if not user_info.empty:
                #Accessing the is_disabled column using the numeric index - 10 (True/False)
                is_disabled = user_info.iloc[0][10]
            else: 
                is_disabled = False
                
            if is_disabled:
                # Disable mood submission
                self.radio1.config(state=tk.DISABLED)
                self.radio2.config(state=tk.DISABLED)
                self.radio3.config(state=tk.DISABLED)
                self.radio4.config(state=tk.DISABLED)
                self.radio5.config(state=tk.DISABLED)
                self.radio6.config(state=tk.DISABLED)
                self.mood_comment_text.config(state=tk.DISABLED)
                self.submit_button.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while disabling widgets: {e}")

    def exitUser(self):
        db.close()
        subprocess.Popen(["python3", "main.py"])
        self.root.destroy()

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
            mood_entry = MoodEntry(
                moodentry_id=None,
                patient_id=self.current_user_id,
                moodscore=self.selected_mood,
                comment=mood_comment,
                timestamp=datetime.now()
            )
            db.insert_mood_entry(mood_entry)
            self.mood_comment_text.delete("1.0", "end")
            self.moodlevelcheck()

        # Ask the user if they want to proceed to exercises
        self.response = messagebox.askquestion(
            title="Proceed to Exercises",
            message="Thank you for submitting your mood.\nWould you like to view recommended exercises?"
        )

        # Handle the response
        if self.response == 'yes':
            self.show_recommended_exercises()

        # Clear the content of `fieldset1` but keep the size
        self.cleanmoodwindow()
        self.printlastmood()

    def show_recommended_exercises(self):
        # Clear any existing exercise widgets
        # for widget in self.exercise_frame.winfo_children():
        #     widget.destroy()
        self.root2= tk.Tk()
        self.root2.title("Exercise Recommendations")
        self.exercise_frame = tk.Frame(self.root2)
        self.exercise_frame.grid(row=0, column=0, columnspan=6, pady=20)

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
        exercises_label = tk.Label(self.exercise_frame, text=exercise_text, font=("Arial", 16), justify="left")
        exercises_label.pack()
        back_button = tk.Button(self.exercise_frame, text="Go to Exercises", command=self.exercises,width=20)
        back_button.pack(pady=10)
        # Add a button to go back to mood selection
        back_button = tk.Button(self.exercise_frame, text="Back to Mood Selection", command=self.back_to_mood,width=20)
        back_button.pack(pady=10)

    def back_to_mood(self):
        self.root2.destroy()
        # Clear any exercise-related content and show the mood selection again
        # for widget in self.exercise_frame.winfo_children():
        #     widget.destroy()
        #
        # self.title_label.config(text="Welcome back")
        # self.submit_button.config(state=tk.NORMAL)

    def openjournal(self):
        # Create a new Toplevel window for the journal
        root3 = tk.Toplevel(self.root)
        root3.title("Journal")  # Set the title of the journal window
        root3.geometry("650x500")  # Set a fixed size for the window

        # Journaling Section Frame
        self.journal_frame = tk.Frame(root3, padx=10, pady=10)
        self.journal_frame.grid(row=0, column=0, columnspan=6, pady=(10, 0), padx=10, sticky="nsew")

        # Journal Entry Label
        self.journal_label = tk.Label(
            self.journal_frame, text="Journal Entry:", font=("Arial", 12)
        )
        self.journal_label.grid(row=0, column=0, padx=10, pady=(0, 5), sticky="w")

        # Journal Entry Textbox
        self.journal_text = tk.Text(self.journal_frame, height=5, width=40)
        self.journal_text.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Save Button
        self.save_button = tk.Button(
            self.journal_frame, text="Save Journal Entry", command=self.save_journal_entry
        )
        self.save_button.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        # Search Functionality
        self.search_label = tk.Label(
            self.journal_frame, text="Search Journal Entries:", font=("Arial", 12)
        )
        self.search_label.grid(row=0, column=1, padx=10, pady=(0, 5), sticky="w")

        self.search_entry = tk.Entry(self.journal_frame, width=30)
        self.search_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.search_button = tk.Button(
            self.journal_frame, text="Search", command=self.search_journal_entries
        )
        self.search_button.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Treeview Section Frame
        self.tree_frame = tk.Frame(root3, padx=10, pady=10)
        self.tree_frame.grid(row=1, column=0, columnspan=6, padx=10, pady=10, sticky="nsew")

        # Treeview Widget
        self.journal_tree = ttk.Treeview(
            self.tree_frame, columns=("Text", "Time"), show="headings", height=10
        )
        self.journal_tree.pack(fill="both", expand=True)

        # Define Treeview Headings
        self.journal_tree.heading("Text", text="Text")
        self.journal_tree.heading("Time", text="Time")

        # Define Treeview Columns
        self.journal_tree.column("Text", anchor="w", width=400)
        self.journal_tree.column("Time", anchor="center", width=150)

        # Treeview Scrollbar
        scrollbar = tk.Scrollbar(
            self.tree_frame, orient="vertical", command=self.journal_tree.yview
        )
        scrollbar.pack(side="right", fill="y")
        self.journal_tree.configure(yscrollcommand=scrollbar.set)

        # Bind click event to the Treeview
        self.journal_tree.bind("<Double-1>", self.show_full_entry)

        # Load Journal Entries into Treeview
        self.load_journal_entries()

    def refresh_treeview(self):
        """Clear and reload the Treeview with updated journal entries."""
        # Clear all existing items in the Treeview
        for item in self.journal_tree.get_children():
            self.journal_tree.delete(item)

        # Reload the data into the Treeview
        self.load_journal_entries()

    def load_journal_entries(self):
        """Load all journal entries into the Treeview."""
        # Clear the Treeview
        for item in self.journal_tree.get_children():
            self.journal_tree.delete(item)

        # Fetch journal entries from the database
        journal_entries = db.getRelation("JournalEntry").getRowsWhereEqual("patient_id", self.current_user_id)

        # Insert all entries into the Treeview
        for entry in journal_entries:
            self.journal_tree.insert("", "end", values=(entry[2][:50], entry[3].strftime("%Y-%m-%d %H:%M")))

    def show_full_entry(self, event):
        """Display the full content of a journal entry."""
        # Get selected item
        selected_item = self.journal_tree.selection()
        if selected_item:
            item_values = self.journal_tree.item(selected_item, "values")

            # Show full text in a popup
            full_text = item_values[0]  # Extract full text
            timestamp = item_values[1]  # Extract timestamp

            popup = tk.Toplevel(self.root)
            popup.title("Journal Entry")
            popup.geometry("400x300")

            # Display text
            text_label = tk.Label(popup, text="Full Entry:", font=("Arial", 12, "bold"))
            text_label.pack(pady=10)

            text_box = tk.Text(popup, wrap="word", height=10, width=40)
            text_box.pack(pady=10, padx=10)
            text_box.insert("1.0", full_text)
            text_box.config(state="disabled")  # Make it read-only

            # Display timestamp
            timestamp_label = tk.Label(popup, text=f"Date: {timestamp}", font=("Arial", 10, "italic"))
            timestamp_label.pack(pady=5)

            close_button = tk.Button(popup, text="Close", command=popup.destroy)
            close_button.pack(pady=10)

    def exitUser(self):
        db.close()
        subprocess.Popen(["python3", "-m" "login.login"])
        self.root.destroy()

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
            mood_entry = MoodEntry(
                moodentry_id=None,
                patient_id=self.current_user_id,
                moodscore=self.selected_mood,
                comment=mood_comment,
                timestamp=datetime.now()
            )
            db.insert_mood_entry(mood_entry)
            self.mood_comment_text.delete("1.0", "end")
            self.moodlevelcheck()

        # Ask the user if they want to proceed to exercises
        self.response = messagebox.askquestion(
            title="Proceed to Exercises",
            message="Thank you for submitting your mood.\nWould you like to view recommended exercises?"
        )

        # Handle the response
        if self.response == 'yes':
            self.show_recommended_exercises()

        # Clear the content of `fieldset1` but keep the size
        self.cleanmoodwindow()
        self.printlastmood()

    def show_recommended_exercises(self):
        self.root2= tk.Tk()
        self.root2.title("Exercise Recommendations")
        self.exercise_frame = tk.Frame(self.root2)
        self.exercise_frame.grid(row=0, column=0, columnspan=6, pady=20)

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
        self.root2.destroy()

    def save_journal_entry(self):
        """Save the journal entry to the database and refresh"""
        # Get the journal text
        journal_text = self.journal_text.get("1.0", "end-1c").strip()

        # Check if the entry is empty
        if not journal_text:
            messagebox.showwarning("Empty Entry", "Please write something in the journal.")
            return

        # Save the journal entry to the database
        journal_entry = JournalEntry(
            entry_id=None,
            patient_id=self.current_user_id,
            text=journal_text,
            timestamp=datetime.now()
        )
        db.insert_journal_entry(journal_entry)

        # Clear the Text widget
        self.journal_text.delete("1.0", "end")

        # Show a success message
        messagebox.showinfo("Journal Entry Saved", "Your journal entry has been saved.")

        # Refresh the Treeview
        self.refresh_treeview()

    def search_journal_entries(self):
        """Search for journal entries and display matching results in the Treeview."""
        search_term = self.search_entry.get().strip().lower()

        # Clear the Treeview
        for item in self.journal_tree.get_children():
            self.journal_tree.delete(item)

        if search_term:
          
            # Fetch all journal entries
            journal_entries = db.getRelation("JournalEntry").getRowsWhereEqual("patient_id", self.current_user_id)
            # journal_entries = db.getRelation("JournalEntry")
            filtered_rows = journal_entries
            self.journal_df = pd.DataFrame(filtered_rows)

            # Filter entries that match the search term
            matching_entries = [
                entry for entry in journal_entries if search_term in entry[2].lower()
            ]

            # Reload the Treeview with matching entries
            for entry in matching_entries:
                self.journal_tree.insert("", "end", values=(entry[2][:50], entry[3].strftime("%Y-%m-%d %H:%M")))
        else:
            # If no search term, reload all entries
            self.load_journal_entries()

    def view_all_journal_entries(self):
        journal_entries = db.getRelation("JournalEntry")
        filtered_rows = journal_entries.getRowsWhereEqual('patient_id', self.current_user_id)
        self.journal_df = pd.DataFrame(filtered_rows)

        if not self.journal_df.empty:
            entries_text = "\n\n".join([f"Entry on {entry[3]}: {entry[2]}" for _, entry in self.journal_df.iterrows()])
            messagebox.showinfo("All Journal Entries", f"Your journal entries:\n\n{entries_text}")
        else:
            messagebox.showinfo("No Entries", "You don't have any journal entries.")

    def edit_information(self):
        # Edit information
        db.close()
        self.root.destroy()
        EditInfo()

    def exercises(self):
        # Edit information
        db.close()
        self.root.destroy()
        try:
            self.root2.destroy()
        except:
            pass
        Exercises()

    def book(self):
        # Book an appointement
        db.close()
        self.root.destroy()
        AppointmentBooking()

    def patientdashboard(self):
        # Edit information
        openpatientdashboard()

    def refresh(self):
        print("Refreshing")
        notifications = db.getRelation('Notification').getRowsWhereEqual('new', True)
        self.message_counter = sum(1 for n in notifications if n[1] == self.current_user_id)
        self.messagenum.config(text=f"You have {self.message_counter} new messages")
        self.root.after(1000, self.refresh)

    def on_close(self):
        db.close()
        self.root.destroy()

if __name__ == "__main__":
    Patient()


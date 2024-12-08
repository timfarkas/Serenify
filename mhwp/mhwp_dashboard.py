import tkinter as tk
from tkinter import ttk
from tkinter import *
import subprocess


import os
import sys
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sessions import Session
from database.database import Database
from database.entities import User
from addfeature.notificationbox import opennotification
from addfeature.forum import openforsum
from addfeature.patientMoodDisplay import displaymood
from addfeature.globaldb import global_db
from mhwp.booking import MHWPAppointmentManager
from mhwp.patientInfo import PatientRecords
from addfeature.globaldb import global_db
global global_db
db=global_db

def open_review():
    sess = Session()
    sess.open()
    userID = sess.getId()
    identity = sess.getRole()
    root = tk.Tk()
    root.title("My Patient Review")
    root.geometry("600x200")

    tree = ttk.Treeview(root, columns=("Time", "Review", "Rate"), show="headings")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    tree.heading("Time", text="Time")
    tree.heading("Review", text="Review")
    tree.heading("Rate", text="Rate")

    tree.column("Time", width=100, anchor="center")
    tree.column("Review", width=200, anchor="w")
    tree.column("Rate", width=50, anchor="center")

    reviews = db.getRelation('MHWPReview').getRowsWhereEqual('mhwp_id',userID)

    for row in reviews:
        tree.insert("", "end", values=(row[5].strftime("%Y-%m-%d"),row[4],row[3]))

    scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

    root.mainloop()

class MHWPDashboard:
    def __init__(self):
        self.db=db
        self.sess = Session()
        self.sess.open()
        self.userID = self.sess.getId()
        self.root = tk.Tk()
        self.root.title("MHWP Dashboard")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.patient_data = []
        self.message_counter = 0
        self.my_rating_score = "NA"
        self.fetch_data()

        self.create_widgets()

        self.root.after(1000, self.refresh)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def fetch_data(self):
        patient_list = self.db.getRelation('Allocation').getRowsWhereEqual('mhwp_id', self.userID)
        patient_ids = [i[2] for i in patient_list]

        for i in patient_ids:
            userdata = self.db.getRelation('User').getRowsWhereEqual('user_id', i)
            Moodrecord = self.db.getRelation('MoodEntry')
            user_mood = Moodrecord.getRowsWhereEqual('patient_id', i)
            recent_mood = "-" if not user_mood else user_mood[-1][2]
            recent_update = "-" if not user_mood else user_mood[-1][4].strftime("%b %d")
            self.patient_data.append(
                [userdata[0][0], f"{userdata[0][4]} {userdata[0][5]}", userdata[0][2], recent_mood, recent_update]
            )

        all_reviews = self.db.getRelation('MHWPReview').getRowsWhereEqual('mhwp_id', self.userID)
        review_list = [i[3] for i in all_reviews]
        if review_list:
            self.my_rating_score = sum(review_list) / len(review_list)

        notifications = self.db.getRelation('Notification').getRowsWhereEqual('new', True)
        self.message_counter = sum(1 for n in notifications if n[1] == self.userID)

    def create_widgets(self):
        title_frame = tk.Frame(self.root, width=600)
        title_frame.grid(row=0, column=0, sticky="nsew")
        self.user = self.db.getRelation("User").getRowsWhereEqual("user_id", self.userID)[0]
        self.name = f"{self.user[User.FNAME]}. {self.user[User.LNAME]}" if self.user[User.FNAME] == "Dr" else f"{self.user[User.FNAME]} {self.user[User.LNAME]}"
        tk.Label(title_frame, text=f"Welcome Back, {self.name}!", font=("Arial", 24, "bold")).pack(pady=10)

        main_frame = tk.Frame(self.root, width=600)
        main_frame.grid(row=1, column=0, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=0, uniform="group")
        main_frame.grid_columnconfigure(1, weight=0, uniform="group")

        def openappointment():
            db.close()
            self.root.destroy()
            MHWPAppointmentManager()
        def openpatientedit():
            db.close()
            self.root.destroy()
            PatientRecords()

        # Left fieldset
        fieldset1 = tk.LabelFrame(main_frame, text="MHWP Functions", padx=10, pady=10)
        fieldset1.grid(row=0, column=0, padx=10, pady=10)
        Button(fieldset1, text="Patient Records", command=openpatientedit, width=15).grid(row=1, column=0, sticky="w")
        Button(fieldset1, text="Appointments", command=openappointment, width=15).grid(row=2, column=0, sticky="w")
        Button(fieldset1, text="Patient Forum", command=openforsum, width=15).grid(row=3, column=0, sticky="w")
        Button(fieldset1, text="My Messages", command=opennotification, width=15).grid(row=4, column=0, sticky="w")
        self.label3 = tk.Label(fieldset1, text=f"You have {self.message_counter} new messages")
        self.label3.grid(row=5, column=0, sticky="w")


        # Right fieldset
        fieldset2 = tk.LabelFrame(main_frame, text="Your Statistics", padx=10, pady=10)
        fieldset2.grid(row=0, column=1, padx=10, pady=10)
        tk.Label(fieldset2, text=f"Allocated Patients: {len(self.patient_data)}").grid(row=0, column=0, sticky="w")
        appointments = self.db.getRelation('Appointment').getRowsWhereEqual('mhwp_id', self.userID)
        appcount=0
        for i in appointments:
            if (i[5] == "Confirmed") and (i[3]>datetime.now()):
                appcount += 1
        tk.Label(fieldset2, text=f"Upcoming Appointments: {appcount}").grid(row=1, column=0, sticky="w")
        tk.Label(fieldset2, text=f"My Rating: {self.my_rating_score}").grid(row=2, column=0, sticky="w")
        Button(fieldset2, text="View Reviews", command=open_review, width=15).grid(row=3, column=0, sticky="w")

        # Treeview for patient list
        tree_frame = tk.LabelFrame(main_frame, text="My Patients", padx=10, pady=10)
        tree_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        self.tree = ttk.Treeview(tree_frame, columns=("#1", "#2", "#3", "#4", "#5"), show="headings", height=10)
        self.tree.pack(fill="x", padx=10, pady=10)
        self.tree.heading("#1", text="ID")
        self.tree.heading("#2", text="Name")
        self.tree.heading("#3", text="Email")
        self.tree.heading("#4", text="Current Mood")
        self.tree.heading("#5", text="Update date")
        self.tree.column("#1", width=50, anchor="center")
        self.tree.column("#2", width=150, anchor="center")
        self.tree.column("#3", width=200, anchor="center")
        self.tree.column("#4", width=100, anchor="center")
        self.tree.column("#5", width=100, anchor="center")

        for item in self.patient_data:
            self.tree.insert("", tk.END, values=item)
        self.tree.bind("<Double-1>", self.on_row_selected)

        note = Label(tree_frame, text="Note: Double click to show mood tracker", anchor="e")
        note.pack(side=LEFT)
        
        
        logout_button = tk.Button(self.root, text="Logout", command=self.logout, width=15)
        logout_button.grid(row=2, column=0, pady=10)  
    def on_row_selected(self, event):
        """Handle double-click on a row in the treeview."""
        selected_item = self.tree.selection()[0]
        item_values = self.tree.item(selected_item, "values")
        display_id = int(item_values[0])
        displaymood(display_id)

    def logout(self):
        self.db.close()
        self.sess.close()
        self.root.destroy()
        subprocess.Popen(["python3", "login/login.py"])

    def refresh(self):
        # print("Refreshing")
        notifications = self.db.getRelation('Notification').getRowsWhereEqual('new', True)
        self.message_counter = sum(1 for n in notifications if n[1] == self.userID)
        self.label3.config(text=f"You have {self.message_counter} new messages")
        self.root.after(1000, self.refresh)

    def on_close(self):
        self.db.close()
        self.root.destroy()


if __name__ == "__main__":
    MHWPDashboard()

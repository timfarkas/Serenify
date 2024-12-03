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
from addfeature.notificationbox import opennotification
from addfeature.forum import openforsum
from addfeature.patientMoodDisplay import displaymood
from addfeature.globaldb import global_db
from mhwp.booking import MHWPAppointmentManager
from mhwp.patientInfo import PatientRecords
from addfeature.globaldb import global_db

def open_review():
    global global_db
    db = global_db
    # Create the main application window
    sess = Session()
    sess.open()
    userID = sess.getId()
    identity = sess.getRole()
    root = tk.Tk()
    root.title("My Patient Review")
    root.geometry("600x200")  # Set window size (optional)

    # Create a Treeview widget
    tree = ttk.Treeview(root, columns=("Time", "Review", "Rate"), show="headings")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    # Define column headings
    tree.heading("Time", text="Time")
    tree.heading("Review", text="Review")
    tree.heading("Rate", text="Rate")

    # Define column widths
    tree.column("Time", width=100, anchor="center")
    tree.column("Review", width=200, anchor="w")
    tree.column("Rate", width=50, anchor="center")

    reviews = db.getRelation('MHWPReview').getRowsWhereEqual('mhwp_id',userID)

    for row in reviews:
        tree.insert("", "end", values=(row[5].strftime("%Y-%m-%d"),row[4],row[3]))

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

    # Run the main Tkinter event loop
    root.mainloop()

def openmhwpdashboard():
    global global_db
    db = global_db
    sess = Session()
    sess.open()
    userID = sess.getId()
    #Can change this input for test
    # userdata = db.getRelation('Allocations').getAllRows()
    # print(userdata)
    patientlist = db.getRelation('Allocation').getRowsWhereEqual('mhwp_id',userID)
    # print(patientlist)
    patientids=[i[2] for i in patientlist]

    patientdata=[]
    for i in patientids:
        userdata=db.getRelation('User').getRowsWhereEqual('user_id',i)
        Moodrecord= db.getRelation('MoodEntry')
        usermood = Moodrecord.getRowsWhereEqual('patient_id', i)
        recentmood="-"
        recentupdate="-"
        if len(usermood)>0:
            recentmood=usermood[-1][2]
            recentupdate=usermood[-1][4].strftime("%b %d")
        patientdata.append([userdata[0][0], str(userdata[0][4]) + " " + str(userdata[0][5]), userdata[0][2],recentmood,recentupdate])
    allreview = db.getRelation('MHWPReview').getRowsWhereEqual('mhwp_id',userID)
    reviewlist=[]
    for i in allreview:
        reviewlist.append(i[3])
    if len(reviewlist)>=1:
        myratingscore=sum(reviewlist)/len(reviewlist)
    else:
        myratingscore="NA"

    notificationdata = db.getRelation('Notification').getRowsWhereEqual('new',True)
    messagecounter=0
    for i in notificationdata:
        if i[1]==userID:
            messagecounter+=1

    def clickbutton():
        # label3.config(text="You have 0 new massage",fg="black")
        opennotification()



    # root1 = tk.Tk()
    #
    # fieldset = tk.LabelFrame(root1, text="MHWP Information", padx=10, pady=10)
    # fieldset.pack(padx=10, pady=10)
    #
    # nam_label = tk.Label(fieldset, text="Name: ", width=25)
    # nam_label.grid(row=0, column=0)
    # spe_label = tk.Label(fieldset, text="Specialization: ")
    # spe_label.grid(row=1, column=0)
    # ema_label = tk.Label(fieldset, text="Email: ")
    # ema_label.grid(row=2, column=0)

    root = tk.Tk()
    root.title("MHWP Dashboard")

    # Configure main grid
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Create main frame
    # Main frame configuration
    main_frame = tk.Frame(root, width=600)  # Define width for main_frame
    main_frame.grid(row=0, column=0, sticky="nsew")
    main_frame.grid_columnconfigure(0, weight=0, uniform="group")  # Left fieldset
    main_frame.grid_columnconfigure(1, weight=0, uniform="group")  # Right fieldset
    # Left fieldset
    fieldset1 = tk.LabelFrame(main_frame, text="MHWP Key Feature", padx=10, pady=10)
    fieldset1.grid(row=0, column=0, padx=10, pady=10)
    btn = Button(fieldset1, text="Manage Patiennt", command=lambda: PatientRecords(),width=15)
    btn.grid(row=1, column=0, sticky="w")
    btn = Button(fieldset1, text="Review Booking", command=lambda: MHWPAppointmentManager(), width=15)
    btn.grid(row=2, column=0, sticky="w")
    btn = Button(fieldset1, text="Enter Forum", command=lambda: openforsum(),width=15)
    btn.grid(row=3, column=0, sticky="w")
    btn = Button(fieldset1, text="Open Message", command=lambda: clickbutton(),width=15)
    btn.grid(row=4, column=0, sticky="w")
    label3 = tk.Label(fieldset1, text=f"You have {messagecounter} new massages")
    label3.grid(row=5, column=0, sticky="w")
    # Right fieldset
    fieldset2 = tk.LabelFrame(main_frame, text="MHWP Data", padx=10, pady=10)
    fieldset2.grid(row=0, column=1, padx=10, pady=10)
    label4 = tk.Label(fieldset2, text=f"Total Patients: {len(patientids)}")
    label4.grid(row=0, column=0, sticky="w")
    appointments = db.getRelation('Appointment').getRowsWhereEqual('mhwp_id', userID)
    label5 = tk.Label(fieldset2, text=f"Appointments: {len(appointments)}")
    label5.grid(row=1, column=0, sticky="w")
    label6 = tk.Label(fieldset2, text=f"My Rating: {myratingscore}")
    label6.grid(row=2, column=0, sticky="w")
    btn = Button(fieldset2, text="View my review", command=lambda: open_review(),width=15)
    btn.grid(row=3, column=0, sticky="w")

    # Treeview within its own frame
    tree_frame = tk.Frame(main_frame)
    tree_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

    tree = ttk.Treeview(tree_frame, columns=("#1", "#2", "#3", "#4", "#5"), show="headings", height=10)
    tree.pack(fill="x", padx=10, pady=10)

    tree.heading("#1", text="ID")
    tree.heading("#2", text="Name")
    tree.heading("#3", text="Email")
    tree.heading("#4", text="Current Mood")
    tree.heading("#5", text="Update date")

    tree.column("#1", width=50, anchor="center")
    tree.column("#2", width=150, anchor="center")
    tree.column("#3", width=200, anchor="center")
    tree.column("#4", width=100, anchor="center")
    tree.column("#5", width=100, anchor="center")

    for item in patientdata:
        tree.insert("", tk.END, values=item)
    tree.grid(padx=10, pady=10)

    def on_row_selected(event):
        selected_item = tree.selection()[0]
        item_values = tree.item(selected_item, "values")
        displayid = int(item_values[0])
        displaymood(displayid,"MHWP")

    tree.bind("<Double-1>", on_row_selected)

    w2 = Label(root, text="  Note: Double click to show mood tracker", anchor="e")
    w2.grid()

    # def openappointment():
    #     # db.close()
    #     # root.destroy()
    #     MHWPAppointmentManager()



    # Run the Tkinter event loop
    def on_close():
        db.close()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()



if __name__ == "__main__":
    openmhwpdashboard()
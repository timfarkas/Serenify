import tkinter as tk
from tkinter import ttk
from tkinter import *
from addfeature.patientMoodDisplay import displaymood
import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database'))
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath((__file__))))
sys.path.append(project_root)
from addfeature.notificationbox import opennotification
from .globalvariables import db


def openmhwpdashboard(MHWPID):
    #Can change this input for test
    # userdata = db.getRelation('Allocations').getAllRows()
    # print(userdata)
    patientlist = db.getRelation('Allocation').getRowsWhereEqual('mhwp_id',MHWPID)
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

    allreview = db.getRelation('MHWPReview').getRowsWhereEqual('mhwp_id',MHWPID)
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
        if i[1]==MHWPID:
            messagecounter+=1

    def clickbutton(MHWPID):
        w3.config(text="You have 0 new massage",fg="black")
        opennotification(MHWPID)



    root = tk.Tk()
    root.title("Patient Dashboard")

    root.grid_rowconfigure(1, weight=10)
    root.grid_columnconfigure(0, weight=1)

    frame = Frame(root, borderwidth=0, relief="solid", width=400)
    frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)

    w1 = Label(frame, text=f"Total Patients: {len(patientids)}")
    w1.grid(row=0, column=0, sticky="W")
    myratingscore=f"{myratingscore:.1f}"
    w2 = Label(frame, text=f"My Rating: {myratingscore}", anchor="w")
    w2.grid(row=1, column=0, sticky="W")

    w3 = Label(frame, text=f"You have {messagecounter} new massages", anchor="e",fg="red" if messagecounter>0 else None)
    w3.grid(row=0, column=1, sticky="E")

    btn = Button(frame, text="Messages", command=lambda: clickbutton(MHWPID))
    btn.grid(row=1, column=1, sticky="E")

    tree = ttk.Treeview(root, columns=("#1", "#2", "#3", "#4", "#5"), show="headings")
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

    tree.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

    def on_row_selected(event):
        selected_item = tree.selection()[0]
        item_values = tree.item(selected_item, "values")
        userid = int(item_values[0])
        displaymood(userid, "m")

    tree.bind("<Double-1>", on_row_selected)

    w2 = Label(root, text="  Note: Double click to show mood tracker", anchor="e")
    w2.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

    # Run the Tkinter event loop
    def on_close():
        # db.close()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
if __name__ == "__main__":
    MHWPID = 5
    openmhwpdashboard(MHWPID)
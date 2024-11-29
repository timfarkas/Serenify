import tkinter as tk
from tkinter import ttk
from tkinter import *
from addfeature.patientMoodDisplay import displaymood
import os
import sys
from datetime import datetime
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database'))
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath((__file__))))
sys.path.append(project_root)
from .notificationbox import opennotification
from .globalvariables import db,userID
from mhwp.booking import MHWPAppointmentManager
from .forum import openforsum
from .chatroom import startchatroom
import datetime

def openpatientdashboard(userID):
    #Can change this input for test
    # # userdata = db.getRelation('Allocations').getAllRows()
    # # print(userdata)
    # patientlist = db.getRelation('Allocation').getRowsWhereEqual('patient_id',userID)
    # # print(patientlist)
    # patientids=[i[2] for i in patientlist]
    #
    # patientdata=[]
    # for i in patientids:
    #     userdata=db.getRelation('User').getRowsWhereEqual('user_id',i)
    #     Moodrecord= db.getRelation('MoodEntry')
    #     usermood = Moodrecord.getRowsWhereEqual('patient_id', i)
    #     recentmood="-"
    #     recentupdate="-"
    #     if len(usermood)>0:
    #         recentmood=usermood[-1][2]
    #         recentupdate=usermood[-1][4].strftime("%b %d")
    #     patientdata.append([userdata[0][0], str(userdata[0][4]) + " " + str(userdata[0][5]), userdata[0][2],recentmood,recentupdate])
    # allreview = db.getRelation('MHWPReview').getRowsWhereEqual('mhwp_id',MHWPID)
    # reviewlist=[]
    # for i in allreview:
    #     reviewlist.append(i[3])
    # if len(reviewlist)>=1:
    #     myratingscore=sum(reviewlist)/len(reviewlist)
    # else:
    #     myratingscore="NA"
    #
    notificationdata = db.getRelation('Notification').getRowsWhereEqual('new',True)
    messagecounter=0
    for i in notificationdata:
        if i[1]==userID:
            messagecounter+=1

    def clickbutton(MHWPID):
        label3.config(text="You have 0 new massage",fg="black")
        opennotification(MHWPID)



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
    root.title("Patient Dashboard")

    # Configure main grid

    winwidth = 500
    winheight = 300

    # Set window size to match the canvas width
    root.geometry(f"{winwidth+50}x{winheight+200}")  # Add extra height and width for padding

    # Create main frame
    # Main frame configuration
    main_frame = tk.Frame(root)
    main_frame.grid(row=0, column=0, sticky="nsew")
    main_frame.grid_columnconfigure(0, weight=1)  # Left fieldset
    main_frame.grid_columnconfigure(1, weight=1)

    # Left fieldset
    fieldset1 = tk.LabelFrame(main_frame, text="Patient Key Feature", padx=10, pady=10)
    fieldset1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    btn = Button(fieldset1, text="Chat with MHWP", command=lambda:startchatroom(userID,"p"), width=15)
    btn.grid(row=1, column=0, sticky="w")
    btn = Button(fieldset1, text="Enter Forum", command=lambda: openforsum(userID), width=15)
    btn.grid(row=2, column=0, sticky="w")
    btn = Button(fieldset1, text="Open Message", command=lambda: clickbutton(userID), width=15)
    btn.grid(row=3, column=0, sticky="w")
    label3 = tk.Label(fieldset1, text=f"You have {messagecounter} new messages")
    label3.grid(row=4, column=0, sticky="w")


    exerrecords = db.getRelation('ExerRecord').getRowsWhereEqual('user_id',userID)
    exercount=0
    nowtime=datetime.datetime.now()
    thirty_days_ago = nowtime - datetime.timedelta(days=30)
    for i in exerrecords:
        if i[3]>thirty_days_ago:
            print(i)
            exercount+=1

    userdata = db.getRelation('User').getRowsWhereEqual('user_id', userID)
    userName = str(userdata[0][4]) + ' ' + str(userdata[0][5])
    Moodrecord = db.getRelation('MoodEntry')
    usermood = Moodrecord.getRowsWhereEqual('patient_id', userID)
    usermood.sort(key=lambda i:i[4])

    print(usermood)
    pastscore=[]
    seven_days_ago = nowtime - datetime.timedelta(days=7)
    for i in usermood:
        if i[4] > seven_days_ago:
            print(i[4])
            pastscore.append(i[2])

    averagescore=sum(pastscore)/len(pastscore)


    fieldset2 = tk.LabelFrame(main_frame, text="Patient Data", padx=10, pady=10)
    fieldset2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    label1 = tk.Label(fieldset2, text=f"Exercises in 30 days: {exercount}")
    label1.grid(row=0, column=0, sticky="w")
    label2 = tk.Label(fieldset2, text=f"Average mood in 7 days: {averagescore}")
    label2.grid(row=1, column=0, sticky="w")
    appointments = db.getRelation('Appointment').getRowsWhereEqual('patient_id', userID)
    label3 = tk.Label(fieldset2, text=f"Appointments: {len(appointments)}")
    label3.grid(row=2, column=0, sticky="w")
    # label3 = tk.Label(fieldset2, text=f"My Rating: {myratingscore}")
    # label3.grid(row=2, column=0, sticky="w")
    # btn = Button(fieldset2, text="View my review", command=lambda: create_treeview_window(),width=15)
    # btn.grid(row=3, column=0, sticky="w")

    # Treeview within its own frame



    tree_frame = tk.Frame(main_frame)
    tree_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)


    length = len(usermood)
    dotdata = []
    interval = winwidth // (len(usermood) + 1)
    radius = 5
    cord = interval

    for i in usermood:
        dotdata.append([cord, winheight - 40 - i[2] * 30])  # Adjust height for mood visualization
        cord += interval

    canv = Canvas(main_frame, width=winwidth, height=winheight, bg="white")
    if len(dotdata) > 0:
        for i in dotdata:
            canv.create_oval(i[0] - radius, i[1] - radius, i[0] + radius, i[1] + radius, outline="pink", fill="pink")
        for i in range(len(dotdata)):
            if i >= 1:
                canv.create_line(dotdata[i][0], dotdata[i][1], dotdata[i - 1][0], dotdata[i - 1][1], width=2,
                                 fill="pink")
            canv.create_text(dotdata[i][0], winheight - 20, text=usermood[i][4].strftime("%b %d"), fill="gray",
                             font=("Arial", 10))
            canv.create_text(dotdata[i][0], dotdata[i][1] - 20, text=usermood[i][2], fill="gray", font=("Arial", 10))
        canv.create_rectangle(15, 40, winwidth - 15, winheight - 15, outline="gray")
        canv.create_text(120, 20, text=f"Name: {userName}", fill="dark blue", font=("Arial", 14, "bold"))
    else:
        canv.create_text(winwidth / 2, winheight / 2, text="No Record", fill="Gray", font=("Arial", 20, "bold"))
    canv.grid(row=1, column=0, columnspan=2, pady=10)

    def on_close():
        root.destroy()


    root.mainloop()



if __name__ == "__main__":
    MHWPID = 5
    openmhwpdashboard(MHWPID)
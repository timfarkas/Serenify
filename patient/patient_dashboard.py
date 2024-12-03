import tkinter as tk
from tkinter import *
import os
import sys
from datetime import datetime
import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sessions import Session
from database.database import Database
from addfeature.notificationbox import opennotification
from addfeature.forum import openforsum
from addfeature.chatroom import startchatroom
from patient.mhwp_rating import openrating
from addfeature.globaldb import global_db
global global_db
db=global_db

def openpatientdashboard():
    sess = Session()
    sess.open()
    userID = sess.getId()
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
    fieldset1 = tk.LabelFrame(main_frame, text="My exercises", padx=10, pady=10,labelanchor="n")
    fieldset1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    # btn = Button(fieldset1, text="Rate my MHWP", command=lambda:openrating(), width=15)
    # btn.grid(row=1, column=0, sticky="w")
    # btn = Button(fieldset1, text="Chat with MHWP", command=lambda:startchatroom(userID,"Patient"), width=15)
    # btn.grid(row=2, column=0, sticky="w")
    # btn = Button(fieldset1, text="Enter Forum", command=lambda: openforsum(), width=15)
    # btn.grid(row=3, column=0, sticky="w")
    # btn = Button(fieldset1, text="Open Message", command=lambda: clickbutton(), width=15)
    # btn.grid(row=4, column=0, sticky="w")
    # label3 = tk.Label(fieldset1, text=f"You have {messagecounter} new messages")
    # label3.grid(row=5, column=0, sticky="w")

    userexerdata = db.getRelation('ExerRecord').getRowsWhereEqual("user_id", userID)
    exercisedata = []
    exerdict=dict()
    colorset=["red", "blue", "green", "yellow"]

    for i in userexerdata:
        if i[2] in exerdict:
            exerdict[i[2]]+=1
        else:
            exerdict[i[2]] =1
        exercisedata.append(i[2])
    canwidth=250
    canheight=120
    execanv = Canvas(fieldset1, width=canwidth, height=canheight, bg="white")
    exercisedata = list(exerdict.values())[::-1]
    labels = list(exerdict.keys())[::-1]
    colors = ["Lemonchiffon","Coral", "Turquoise", "Lawngreen","yellow","violet","RoyalBlue"]

    x = canwidth/2-60
    y = canheight/2
    radius = canheight/2*0.8
    total = sum(exercisedata)
    start_angle = 0

    for i, value in enumerate(exercisedata):
        # Calculate the extent of the slice
        extent = (value / total) * 360
        # Draw the slice
        execanv.create_arc(x-radius, y - radius, x + radius, y + radius,start=start_angle, extent=extent,fill=colors[i], outline="black")
        start_angle += extent
    execanv.pack()

    box_size = 10  # Size of the color box
    padding = 5  # Spacing between items
    legendx=canwidth-130
    legendy=20
    for i, (label, color) in enumerate(zip(labels, colors)):
        execanv.create_rectangle(
            legendx, legendy + i * (box_size + padding),
               legendx + box_size, legendy + i * (box_size + padding) + box_size,
            fill=color, outline="black"
        )
        execanv.create_text(
            legendx + box_size + 10, legendy + i * (box_size + padding) + box_size // 2,
            text=label, anchor="w", font=("Arial", 10)
        )
    execanv.pack()

    exerrecords = db.getRelation('ExerRecord').getRowsWhereEqual('user_id',userID)
    exercount=0
    nowtime=datetime.datetime.now()
    thirty_days_ago = nowtime - datetime.timedelta(days=30)
    for i in exerrecords:
        if i[3]>thirty_days_ago:
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
            pastscore.append(i[2])

    averagescore=(round((sum(pastscore)/len(pastscore)),1) if len(pastscore)>0 else "")


    fieldset2 = tk.LabelFrame(main_frame, text="Key Statistics", padx=10, pady=10, labelanchor="n")
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
        canv.create_text(80, 20, text=f"Name: {userName}", fill="Lightseagreen", font=("Arial", 14, "bold"))
    else:
        canv.create_text(winwidth / 2, winheight / 2, text="No Record", fill="Gray", font=("Arial", 20, "bold"))
    canv.grid(row=1, column=0, columnspan=2, pady=10)

    def on_close():
        # db.close()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()


# if __name__ == "__main__":
#     openpatientdashboard()
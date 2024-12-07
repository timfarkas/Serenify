import tkinter as tk
from tkinter import ttk
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

    notificationdata = db.getRelation('Notification').getRowsWhereEqual('new',True)
    messagecounter=0
    for i in notificationdata:
        if i[1]==userID:
            messagecounter+=1

    def clickbutton():
        # label3.config(text="You have 0 new massage",fg="black")
        opennotification()



    root = tk.Tk()
    root.title("Patient Dashboard")

    # Configure main grid

    winwidth = 500
    winheight = 300

    # Set window size to match the canvas width
    root.geometry(f"{winwidth+50}x{winheight+600}")  # Add extra height and width for padding

    # Create main frame
    # Main frame configuration
    main_frame = tk.Frame(root)
    main_frame.grid(row=0, column=0, sticky="nsew")
    main_frame.grid_columnconfigure(0, weight=1)  # Left fieldset
    # main_frame.grid_columnconfigure(1, weight=1)

    # Left fieldset
    fieldset1 = tk.LabelFrame(main_frame, text="My exercises", padx=10, pady=10,labelanchor="n")
    fieldset1.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    userexerdata = db.getRelation('ExerRecord').getRowsWhereEqual("user_id", userID)
    exercisedata = []
    exerdict=dict()

    for i in userexerdata:
        if i[2] in exerdict:
            exerdict[i[2]]+=1
        else:
            exerdict[i[2]] =1
        exercisedata.append(i[2])
    canwidth=250
    canheight=150
    execanv = Canvas(fieldset1, width=canwidth, height=canheight, bg="white")
    exercisedata = list(exerdict.values())[::-1]
    labels = list(exerdict.keys())[::-1]
    colors = ["Lemonchiffon","Coral", "Turquoise", "Lawngreen","yellow","violet","RoyalBlue"]

    x = canwidth/2-60
    y = canheight/2
    radius = canheight/2*0.6
    total = sum(exercisedata)
    start_angle = 0

    for i, value in enumerate(exercisedata):
        # Calculate the extent of the slice
        extent = (value / total) * 360
        # Draw the slice
        execanv.create_arc(x-radius, y - radius, x + radius, y + radius,start=start_angle, extent=extent,fill=colors[i], outline="black")
        start_angle += extent
    execanv.grid(row=0,column=0)

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
    fieldset2.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    label1 = tk.Label(fieldset2, text=f"Exercises in 30 days: {exercount}")
    label1.grid(row=1, column=0, sticky="w")
    label2 = tk.Label(fieldset2, text=f"Average mood in 7 days: {averagescore}")
    label2.grid(row=0, column=0, sticky="w")
    appointments = db.getRelation('Appointment').getRowsWhereEqual('patient_id', userID)
    appcount=0
    for i in appointments:
        if (i[5]=="Confirmed") and(i[3]>datetime.datetime.now()):
            appcount+=1
    label3 = tk.Label(fieldset2, text=f"Upcoming appointments: {appcount}")
    label3.grid(row=2, column=0, sticky="w")
    # label3 = tk.Label(fieldset2, text=f"My Rating: {myratingscore}")
    # label3.grid(row=2, column=0, sticky="w")
    # btn = Button(fieldset2, text="View my review", command=lambda: create_treeview_window(),width=15)
    # btn.grid(row=3, column=0, sticky="w")

    # Treeview within its own frame



    # tree_frame = tk.Frame(main_frame)
    # tree_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
    tree_frame = tk.LabelFrame(main_frame, text="Mood Tracker", padx=10, pady=10, labelanchor="n")
    tree_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    usermood.sort(key=lambda x:x[4])

    maxdots = 10
    showmood = usermood[-min(maxdots,len(usermood)):]
    print(showmood)
    length = len(showmood)
    dotdata=[]
    winwidth=500
    winhight=300
    interval=winwidth//(length+1)
    radius=5
    cord=interval
    for i in showmood:
        dotdata.append([cord, 260-i[2]*30])
        cord+=interval
    canv = Canvas(tree_frame, width=winwidth, height=winheight, bg="white")
    canv.grid(row=0, column=0, sticky="nsew")

    if len(dotdata) > 0:
        for i in dotdata:
            canv.create_oval(i[0] - radius, i[1] - radius, i[0] + radius, i[1] + radius, outline="pink", fill="pink")
        for i in range(len(dotdata)):
            if i >= 1:
                canv.create_line(dotdata[i][0], dotdata[i][1], dotdata[i - 1][0], dotdata[i - 1][1], width=2,
                                 fill="pink")
            canv.create_text(dotdata[i][0], winheight - 40, text=showmood[i][4].strftime("%b %d"), fill="gray",
                             font=("Arial", 10))
            canv.create_text(dotdata[i][0], dotdata[i][1] - 20, text=showmood[i][2], fill="gray", font=("Arial", 10))
        canv.create_rectangle(15, 40, winwidth - 15, winheight - 15, outline="gray")
        canv.create_text(20, 20, text=f"Name: {userName}", fill="Lightseagreen", font=("Arial", 20, "bold"),anchor="w")
    else:
        canv.create_text(winwidth / 2, winheight / 2, text="No Record", fill="Gray", font=("Arial", 20, "bold"))
    mood_btn = Button(tree_frame, text="View Full Mood Records", command=lambda: open_mood_records_window(userID))
    mood_btn.grid(row=1)

    def open_mood_records_window(userID):
        mood_window = Toplevel()
        mood_window.title("Mood Records")
        mood_window.geometry("600x400")

        tree = ttk.Treeview(mood_window, columns=("Date", "Score", "Comments"), show="headings")
        tree.heading("Date", text="Date")
        tree.heading("Score", text="Score")
        tree.heading("Comments", text="Comments")
        tree.column("Date", width=150, anchor="center")
        tree.column("Score", width=100, anchor="center")
        tree.column("Comments", width=300, anchor="w")

        Moodrecord = db.getRelation('MoodEntry')
        usermood = Moodrecord.getRowsWhereEqual('patient_id', userID)

        for mood in usermood:
            date = mood[4].strftime("%Y-%m-%d")
            score = mood[2]
            comments = mood[3]
            tree.insert("", "end", values=(date, score, comments))

        tree.pack(fill="both", expand=True)

        close_btn = Button(mood_window, text="Close", command=mood_window.destroy)
        close_btn.pack(pady=10)

    allexer = db.getRelation('ExerRecord').getRowsWhereEqual('user_id', userID)
    exerrecords = dict()
    for i in allexer:
        if i[3].strftime("%Y-%m-%d") in exerrecords:
            exerrecords[i[3].strftime("%Y-%m-%d")] += 1
        else:
            exerrecords[i[3].strftime("%Y-%m-%d")] = 1
    # print(exerrecords)
    # userdata=room1.getRowsWhereEqual("user_id",3)
    sorted_list = sorted(exerrecords.items(), key=lambda x:x[0])
    # print(sorted_list)
    displaynum = 7
    if len(sorted_list) > displaynum:
        sorted_list = sorted_list[-displaynum:]

    dates = []
    values = []
    num_bars = len(sorted_list)
    for i in sorted_list:
        dates.append(i[0])
        values.append(i[1])

    # Create a Canvas to draw the chart

    barcanv = Canvas(fieldset1, width=250, height=150, bg="white")
    barcanv.grid(row=0, column=1, columnspan=2, pady=10)
    # Draw the bar chart
    def draw_bar_chart():
        # Dimensions
        chart_width = 200
        chart_height = 90
        padding = 30
        bar_width = 20
        max_value = max(values)

        # Calculate scaling factor
        scale = chart_height / max_value if max_value > 0 else 1

        # Draw X-axis and Y-axis


        # Draw bars and labels
        for i in range(num_bars):
            x0 = padding + i * (bar_width + 10)
            y0 = chart_height + padding - (values[i] * scale)
            x1 = x0 + bar_width
            y1 = chart_height + padding

            # Draw the bar
            barcanv.create_rectangle(x0, y0, x1, y1, fill="lightblue", outline="lightblue")

            # Add text labels (value)
            barcanv.create_text(
                (x0 + x1) / 2, y0 - 10, text=str(values[i]), anchor="s", font=("Arial", 8)
            )

            # Add text labels (date)
            barcanv.create_text(
                (x0 + x1) / 2, chart_height + padding + 15, text=dates[i], anchor="n", font=("Arial", 5)
            )
        barcanv.create_line(
            padding, chart_height + padding, chart_width + padding, chart_height + padding, width=1
        )
        # barcanv.create_line(
        #     padding, padding, padding, chart_height + padding, width=1
        # )

    draw_bar_chart()

    def on_close():
        # db.close()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()


# if __name__ == "__main__":
#     openpatientdashboard()
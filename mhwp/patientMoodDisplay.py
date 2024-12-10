from tkinter import *
from tkinter import ttk
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sessions import Session

from database.database import Database
from addfeature.chatroom import startchatroom

sess = Session()
sess.open()
userID = sess.getId()
from addfeature.globaldb import global_db
global global_db
db=global_db

def startchat():

    startchatroom()

def displaymood(patientID):
    sess.open()
    identity= sess.getRole()
    # print(identity)
    userdata = db.getRelation('User').getRowsWhereEqual('user_id', patientID)
    userName = str(userdata[0][4]) + ' ' + str(userdata[0][5])
    Moodrecord = db.getRelation('MoodEntry')
    usermood = Moodrecord.getRowsWhereEqual('patient_id', patientID)
    usermood.sort(key=lambda x: x[4])
    maxdots = 10
    showmood = usermood[-maxdots:]
    length = len(showmood)
    dotdata = []
    winwidth = 500
    winhight = 300
    interval = winwidth // (length + 1)
    radius = 5
    cord = interval
    for i in showmood:
        dotdata.append([cord, 260 - i[2] * 30])
        cord += interval
    root = Tk()
    root.title("Patient Info")
    fieldset2 = LabelFrame(root, text="Patient Info", padx=5, pady=5, labelanchor="n",width=winwidth,height=winhight)
    fieldset2.pack_propagate(False)
    fieldset2.pack(fill="x")
    patientinfo = db.getRelation('User').getRowsWhereEqual('user_id',patientID)
    label1 = Label(fieldset2, text=f"User Name: {patientinfo[0][4]} {patientinfo[0][5]} ")
    label1.grid(row=0, column=0, sticky="w")
    label2 = Label(fieldset2, text=f"Email: {patientinfo[0][2]}")
    label2.grid(row=1, column=0, sticky="w")
    label3 = Label(fieldset2, text=f"Emergency Contact: {patientinfo[0][8]}")
    label3.grid(row=2, column=0, sticky="w")
    label4 = Label(fieldset2, text=f"Emergency Contact Email: {patientinfo[0][7]}")
    label4.grid(row=3, column=0, sticky="w")

    # Draw the chart
    canv = Canvas(root, width=winwidth, height=winhight, bg="white")
    if len(dotdata)>0:
        for i in dotdata:
            canv.create_oval(i[0]-radius,i[1]-radius,i[0]+radius,i[1]+radius, outline="pink",fill="pink")

        for i in range(len(dotdata)):
            if i>=1:
                canv.create_line((dotdata[i][0],dotdata[i][1]), (dotdata[i-1][0],dotdata[i-1][1]), width=2, fill="pink")
            canv.create_text(dotdata[i][0], winhight-40, text=showmood[i][4].strftime("%b %d"), fill="gray", font=("Arial", 12))
            canv.create_text(dotdata[i][0], dotdata[i][1]-20, text=showmood[i][2], fill="gray", font=("Arial", 12))
        canv.create_rectangle(15, 40, winwidth-15, winhight-15, outline="gray")
        canv.create_text(20, 20, text=f"Name: {userName}", fill="Lightseagreen", font=("Arial", 20, "bold"),anchor="w")

    else:
        canv.create_text(winwidth/2,winhight/2, text="No Record", fill="Gray", font=("Arial", 20, "bold"))
    canv.pack()

    mood_btn = Button(root, text="Full Mood Records", command=lambda: open_mood_records_window(patientID),width=20)
    mood_btn.pack(pady=3)

    if identity=="MHWP":
        # print("before start",userId,"m")
        btn = Button(root, text="Start Chat",  command=lambda: startchatroom(patientID),width=20)
        btn.pack(pady=5)

    def open_mood_records_window(patientID):
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
        usermood = Moodrecord.getRowsWhereEqual('patient_id', patientID)

        for mood in usermood:
            date = mood[4].strftime("%b %d, %Y")
            score = mood[2]
            comments = mood[3]
            tree.insert("", "end", values=(date, score, comments))

        tree.pack(fill="both", expand=True)

        close_btn = Button(mood_window, text="Close", command=mood_window.destroy)
        close_btn.pack(pady=10)

    def on_close():
        # db.close()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
#
if __name__ == "__main__":
    displaymood()
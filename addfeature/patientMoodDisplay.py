from tkinter import *
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sessions import Session

from database.database import Database
from .chatroom import startchatroom

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
    length = len(usermood)
    dotdata=[]

    winwidth=500
    winhight=300
    interval=winwidth//(length+1)
    radius=5
    cord=interval
    for i in usermood:
        dotdata.append([cord, 260-i[2]*30])
        cord+=interval

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
            canv.create_text(dotdata[i][0], winhight-40, text=usermood[i][4].strftime("%b %d"), fill="gray", font=("Arial", 12))
            canv.create_text(dotdata[i][0], dotdata[i][1]-20, text=usermood[i][2], fill="gray", font=("Arial", 12))
        canv.create_rectangle(15, 40, winwidth-15, winhight-15, outline="gray")
        canv.create_text(20, 20, text=f"Name: {userName}", fill="Lightseagreen", font=("Arial", 20, "bold"),anchor="w")

    else:
        canv.create_text(winwidth/2,winhight/2, text="No Record", fill="Gray", font=("Arial", 20, "bold"))
    canv.pack()
    if identity=="MHWP":
        # print("before start",userId,"m")
        btn = Button(root, text="Start Chat",  command=lambda: startchatroom(patientID))
        btn.pack(pady=10)
    def on_close():
        # db.close()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
#
if __name__ == "__main__":
    displaymood()
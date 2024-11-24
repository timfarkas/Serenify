from tkinter import *
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database'))
sys.path.append(project_root)

from .chatroom import startchatroom
from .globalvariables import  db




##### DB QUERIES


def startchat(userID):
    startchatroom(userID)
    """This function is triggered by the button."""


def displaymood(userId,identity):

    userdata = db.getRelation('User').getRowsWhereEqual('user_id', userId)
    userName = str(userdata[0][4]) + ' ' + str(userdata[0][5])
    Moodrecord = db.getRelation('MoodEntry')
    usermood = Moodrecord.getRowsWhereEqual('patient_id', userId)
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
    root.title("My mood score")
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
        canv.create_text(120, 20, text=f"Name: {userName}", fill="dark blue", font=("Arial", 20, "bold"))
    else:
        canv.create_text(winwidth/2,winhight/2, text="No Record", fill="Gray", font=("Arial", 20, "bold"))
    canv.pack()
    if identity=="m":
        # print("before start",userId,"m")
        btn = Button(root, text="Start Chat",  command=lambda: startchatroom(userId,"m"))
        btn.pack(pady=10)
    def on_close():
        # db.close()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
#
if __name__ == "__main__":
    userId = 2
    identity="m"
    displaymood(userId,identity)
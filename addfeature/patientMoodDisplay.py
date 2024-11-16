from tkinter import *
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database'))
sys.path.append(project_root)
from database.database import Database
from database.initDBwithDummyData_FeatureTest import initDummyDatabase

db = Database(overwrite = True)
initDummyDatabase(db)
db.close()
db = Database()

##### DB QUERIES
# userId = 2
def displaymood(userId):
    userdata = db.getRelation('User').getRowsWhereEqual('user_id', userId)
    userName = str(userdata[0][4]) + ' ' + str(userdata[0][5])
    Moodrecord = db.getRelation('MoodEntry')
    usermood = Moodrecord.getRowsWhereEqual('patient_id', userId)
    print(usermood)
    if len(usermood) > 0:
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

        for i in dotdata:
            canv.create_oval(i[0]-radius,i[1]-radius,i[0]+radius,i[1]+radius, outline="pink",fill="pink")

        for i in range(len(dotdata)):
            if i>=1:
                canv.create_line((dotdata[i][0],dotdata[i][1]), (dotdata[i-1][0],dotdata[i-1][1]), width=2, fill="pink")
            canv.create_text(dotdata[i][0], winhight-40, text=usermood[i][4].strftime("%b %d"), fill="gray", font=("Arial", 12))
            canv.create_text(dotdata[i][0], dotdata[i][1]-20, text=usermood[i][2], fill="gray", font=("Arial", 12))
        canv.create_rectangle(15, 40, winwidth-15, winhight-15, outline="gray")
        canv.create_text(120, 20, text=f"Name: {userName}", fill="dark blue", font=("Arial", 20, "bold"))
        canv.pack()
        root.mainloop()
    else:
        print("no match")
#
# displaymood(2)
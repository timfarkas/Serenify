import tkinter as tk
from tkinter import ttk
from tkinter import *
from addfeature.patientMoodDisplay import displaymood
import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database'))
sys.path.append(project_root)
from database.database import Database
from database.initDBwithDummyData_FeatureTest import initDummyDatabase

db = Database(overwrite = True)
initDummyDatabase(db)
db.close()
db = Database()
WHMPID=6 #Can change this input for test
# userdata = db.getRelation('Allocations').getAllRows()
# print(userdata)
patientlist = db.getRelation('Allocation').getRowsWhereEqual('mhwp_id',WHMPID)
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

allreview = db.getRelation('MHWPReview').getRowsWhereEqual('mhwp_id',WHMPID)
reviewlist=[]
for i in allreview:
    reviewlist.append(i[3])
if len(reviewlist)>=1:
    myratingscore=sum(reviewlist)/len(reviewlist)
else:
    myratingscore="NA"


root = tk.Tk()
root.title("Patient Dashboard")

w1 = Label(root, text = f"Total Patients: {len(patientids)}", anchor="se")
w1.grid(row=1, column=0,sticky="W")
w2 = Label(root, text = f"My Rating: {myratingscore}")
w2.grid(row=2, column=0,sticky="W")

# w1.pack()
# Create the Treeview widget
columns = ("#1", "#2", "#3","#4","#5")
tree = ttk.Treeview(root, columns=columns, show="headings")
# Define the column headers
tree.heading("#1", text="ID")
tree.heading("#2", text="Name")
tree.heading("#3", text="Email")
tree.heading("#4", text="Current Mood")
tree.heading("#5", text="Update date")

# Define the column widths
tree.column("#1", width=50, anchor="center")
tree.column("#2", width=150, anchor="center")
tree.column("#3", width=200, anchor="center")
tree.column("#4", width=100, anchor="center")
tree.column("#5", width=100, anchor="center")
for item in patientdata:
    tree.insert("", tk.END, values=item)
# Place the Treeview widget in the window

def on_row_selected(event):
    # Get the selected item
    selected_item = tree.selection()[0]  # Get the first selected item
    item_values = tree.item(selected_item, "values")  # Get the values of the selected item
    userid=int(item_values[0])
    displaymood(userid)

    # Display the selected item details

tree.bind("<Double-1>", on_row_selected)


tree.grid(row=3, column=0)

w2 = Label(root, text = "  Note: Double click to show mood tracker", anchor="se")
w2.grid(row=4, column=0,sticky="W")
# tree.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()

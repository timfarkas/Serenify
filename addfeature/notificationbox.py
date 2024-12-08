from tkinter import Tk, ttk
import tkinter as tk
from datetime import datetime
from tkinter import scrolledtext
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sessions import Session
from .chatroom import startchatroom
from mhwp.booking import MHWPAppointmentManager
from patient.booking import AppointmentBooking
from addfeature.patientMoodDisplay import displaymood
from database.database import Database
from tkinter import messagebox
from addfeature.globaldb import global_db
global global_db
db=global_db

def opennotification():
    # db=Database()
    sess = Session()
    sess.open()
    userID = sess.getId()
    identity = sess.getRole()

    def refresh_treeview():
        for item in tree.get_children():
            tree.delete(item)

        usernotification = allnotification.getRowsWhereEqual('user_id', userID)
        # print("all noti",usernotification)
        usernotification.sort(key=lambda x: x[-1], reverse=True)
        # print("allnoti",usernotification)
        counter = 0
        for i in usernotification:
            if counter == 30:
                break
            sourceuser = db.getRelation('User').getRowsWhereEqual('user_id', i[3])
            if i[2] == "Newchat":
                tree.insert(
                    "",
                    "end",
                    values=("You have a new message!",
                            f"{sourceuser[0][4]} {sourceuser[0][5]}",
                            i[5].strftime("%Y-%m-%d %H:%M:%S"),
                            i[3],
                            i[0]),
                    tags=("new" if i[4] else "old")
                )
            elif i[2] == "Newappointment":
                tree.insert(
                    "",
                    "end",
                    values=("You have a new appointment request!",
                            "System",
                            i[5].strftime("%Y-%m-%d %H:%M:%S"),
                            i[3],
                            i[0]),
                    tags=("new" if i[4] else "old")
                )
            elif i[2] == "Newreview":
                tree.insert(
                    "",
                    "end",
                    values=("You have a new patient review!",
                            "System",
                            i[5].strftime("%Y-%m-%d %H:%M:%S"),
                            i[3],
                            i[0]),
                    tags=("new" if i[4] else "old")
                )
            elif i[2] == "MoodAlert":
                tree.insert(
                    "",
                    "end",
                    values=("Your patient has logged a low mood score!",
                            f"{sourceuser[0][4]} {sourceuser[0][5]}",
                            i[5].strftime("%Y-%m-%d %H:%M:%S"),
                            i[3],
                            i[0]),
                    tags=("new" if i[4] else "old")
                )
            elif i[2] == "AppointmentUpdated":
                tree.insert(
                    "",
                    "end",
                    values=("Your appointment has been updated!",
                            f"System",
                            i[5].strftime("%Y-%m-%d %H:%M:%S"),
                            i[3],
                            i[0]),
                    tags=("new" if i[4] else "old")
                )
            elif i[2] == "AppointmentConfirmed":
                tree.insert(
                    "",
                    "end",
                    values=("Your appointment has been confirmed!",
                            f"System",
                            i[5].strftime("%Y-%m-%d %H:%M:%S"),
                            i[3],
                            i[0]),
                    tags=("new" if i[4] else "old")
                )
            elif i[2] == "AppointmentDeclined":
                tree.insert(
                    "",
                    "end",
                    values=("Your appointment has been declined!",
                            f"System",
                            i[5].strftime("%Y-%m-%d %H:%M:%S"),
                            i[3],
                            i[0]),
                    tags=("new" if i[4] else "old")
                )

            counter += 1
    root = Tk()
    root.title("My message box")

    tree = ttk.Treeview(root, columns=("Message", "From", "Time", "UserID", "MessageID"), show="headings")

    tree.heading("Message", text="Message")
    tree.heading("From", text="From")
    tree.heading("Time", text="Time")
    tree.heading("UserID", text="User ID")  # Hidden column
    tree.heading("MessageID", text="Message ID")  # Hidden column

    tree.column("Message", width=250)
    tree.column("From", width=100)
    tree.column("Time", width=200)
    tree.column("UserID", width=0, stretch=False)  # Hide UserID
    tree.column("MessageID", width=0, stretch=False)  # Hide MessageID

    allnotification = db.getRelation('Notification')
    refresh_treeview()

    def on_row_selected(event):
        selected_item = tree.selection()[0]
        item_values = tree.item(selected_item, "values")  # Get the values of the selected item
        # print("Selected item values:", item_values)
        messageID = int(item_values[4])
        # print(f"Updating Message ID: {messageID}")
        allnotification.editFieldInRow(messageID, 'new', False)

        refresh_treeview()
        # print(identity)
        if identity == "MHWP":
            patientID = item_values[3]
        elif identity == "Patient":
            patientID = userID
        # print("p", patientID, "iden", identity)
        if item_values[0] == "You have a new message!":
            startchatroom(int(patientID))
        elif item_values[0] == "You have a new appointment request!":
            messagebox.showinfo("Notification", "Please return to the dashboard to view the appointment.")
        elif item_values[0] == "Your patient has logged a low mood score!":
            displaymood(int(patientID), "MHWP")
        elif item_values[0] == "You have a new patient review!":
            messagebox.showinfo("Notification", "Please return to the dashboard to view the review.")
        elif item_values[0] in ["Your appointment has been updated!", "Your appointment has been declined!", "Your appointment has been confirmed!"]:
            messagebox.showinfo("Notification", "Please return to the dashboard to view the appointment.")

    tree.tag_configure("old", foreground="gray")
    tree.tag_configure("new", foreground="green")

    tree.bind("<Double-1>", on_row_selected)
    tree.pack(fill="both", expand=True)

    def on_close():
        # db.close()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

if __name__ == "__main__":
    opennotification()
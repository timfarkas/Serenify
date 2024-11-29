from tkinter import Tk, ttk
from datetime import datetime
from tkinter import scrolledtext
import os
import sys

import numpy as np

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database'))
# project_root=(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)
from .chatroom import startchatroom
from .globalvariables import db
from mhwp.booking import MHWPAppointmentManager
# from .mhwp_dashboard import open_review

# def sendnotifiation(senderID,recieverID,Content):
#     newnotify = Notification(
#                     user_id=recieverID,
#                     source_id=senderID,
#                     notifycontent=Content,
#                     new=True,
#                     timestamp=datetime.now(),
#                 )
#                 db.insert_notification(newnotify)

def opennotification(userID):
    def refresh_treeview():
        """Clears and refreshes the Treeview with updated data."""
        # Clear existing rows in the Treeview
        for item in tree.get_children():
            tree.delete(item)

        # Fetch notifications and re-populate
        usernotification = allnotification.getRowsWhereEqual('user_id', userID)
        usernotification.sort(key=lambda x: x[-1], reverse=True)

        # Add rows to Treeview
        counter = 0
        for i in usernotification:
            print(i)
            if counter == 30:
                break

            if i[2] == "Newchat":
                sourceuser = db.getRelation('User').getRowsWhereEqual('user_id', i[3])
                tree.insert(
                    "",
                    "end",
                    values=("You have a new chat",
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
                    values=("You have a new appointment",
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
                    values=("You have a new patient review",
                            "System",
                            i[5].strftime("%Y-%m-%d %H:%M:%S"),
                            i[3],
                            i[0]),
                    tags=("new" if i[4] else "old")
                )
            counter += 1
    # Create the main application window
    root = Tk()
    root.title("My message box")

    # Create a Treeview widget
    tree = ttk.Treeview(root, columns=("Message", "From", "Time", "UserID", "MessageID"), show="headings")

    # Define column headings
    tree.heading("Message", text="Message")
    tree.heading("From", text="From")
    tree.heading("Time", text="Time")
    tree.heading("UserID", text="User ID")  # Hidden column
    tree.heading("MessageID", text="Message ID")  # Hidden column

    # Set column widths
    tree.column("Message", width=200)
    tree.column("From", width=100)
    tree.column("Time", width=200)
    tree.column("UserID", width=0, stretch=False)  # Hide UserID
    tree.column("MessageID", width=0, stretch=False)  # Hide MessageID

    # Fetch notifications
    allnotification = db.getRelation('Notification')
    refresh_treeview()  # Populate the Treeview initially

    def on_row_selected(event):
        """Handles the double-click event on a Treeview row."""
        # Get the selected item

        selected_item = tree.selection()[0]
        item_values = tree.item(selected_item, "values")  # Get the values of the selected item
        print("Selected item values:", item_values)
        messageID = int(item_values[4])  # Extract MessageID
        print(f"Updating Message ID: {messageID}")
        allnotification.editFieldInRow(messageID, 'new', False)

        # Refresh the Treeview after the update
        refresh_treeview()
        if item_values[0]=="You have a new chat":
            if userID > int(item_values[3]):
                patientID = item_values[3]
                identity = "m"
            elif userID < int(item_values[3]):
                patientID = userID
                identity = "p"
            startchatroom(int(patientID), identity)
        elif item_values[0] == "You have a new appointment":
            MHWPAppointmentManager(userID)
        elif item_values[0] == "You have a new patient review":
            pass
            # opeen(userID)
            # Update the 'new' field in the Notification relation


        # Start the chatroom


    # Configure tag styles
    tree.tag_configure("old", foreground="gray")
    tree.tag_configure("new", foreground="green")

    # Bind row selection event
    tree.bind("<Double-1>", on_row_selected)

    # Pack the Treeview widget
    tree.pack(fill="both", expand=True)

    def on_close():
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

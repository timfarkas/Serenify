import time
from datetime import datetime
import tkinter as tk
from tkinter import scrolledtext
import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database'))
sys.path.append(project_root)
from database.initDBwithDummyData_FeatureTest import initDummyDatabase
from database.database import Database
from database.database import ChatContent

db = Database(overwrite = True)
initDummyDatabase(db)
db.close()
db = Database()

userID=5 #can try different user

room1 = db.getRelation('Allocation').getRowsWhereEqual('patient_id',userID)
room2 = db.getRelation('Allocation').getRowsWhereEqual('mhwp_id',userID)
if room1:
    roomnumber=room1[0][0]
elif room2:
    roomnumber =room2[0][0]
roominfo=db.getRelation('Allocation').getRowsWhereEqual('allocation_id',roomnumber)
user1=userID
if roominfo[0][2]==user1:
    user2=roominfo[0][3]
else:
    user2=roominfo[0][2]
# print(user2)
user2info=db.getRelation("User").getRowsWhereEqual('user_id',user2)
user2name=str(user2info[0][4]) + ' ' + str(user2info[0][5])
chat_history=db.getRelation('ChatContent').getRowsWhereEqual('allocation_id',roomnumber)
# print(chat_history)

def send_message(event=None,user_message=None):
    # Get the message from the entry box
    event=0
    if user_message is None:
        message = entry.get()
        showtime=datetime.now()
        inputuser=userID
        newchat= ChatContent(
            allocation_id=roomnumber,
            user_id=userID,
            text=message,
            timestamp=showtime,
        )
        db.insert_chatcontent(newchat)
    else:
        message = user_message[3]
        inputuser=user_message[2]
        showtime=user_message[4]
        # If there's a message, display it in the chat display area
    if message:
        if userID==inputuser:
            chat_display.config(state="normal")  # Enable editing of chat display
            chat_display.insert(tk.END, str(showtime.strftime("%Y-%m-%d %H:%M:%S")) + "\n", "system")
            chat_display.insert(tk.END, "You: " + message + "\n", "me")
            chat_display.config(state="disabled")  # Disable editing of chat display
            entry.delete(0, tk.END)  # Clear the entry box
        else:
            chat_display.config(state="normal",)  # Enable editing of chat display
            chat_display.insert(tk.END, str(showtime.strftime("%Y-%m-%d %H:%M:%S"))+ "\n","system")
            chat_display.insert(tk.END, str(user2name)+": " + message + "\n","other")
            chat_display.config(state="disabled")  # Disable editing of chat display
            entry.delete(0, tk.END)  # Clear the entry box
        chat_display.yview(tk.END)
    if user_message is None:
        entry.delete(0, tk.END)


# Initialize the main window
root = tk.Tk()
root.title("ChatRoom")

# Create a scrollable text widget for the chat display area
chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, state="disabled", width=70, height=20)
chat_display.pack(padx=10, pady=10)
chat_display.tag_config("me", foreground="green")
chat_display.tag_config("other", foreground="blue")
chat_display.tag_config("system", foreground="black")

# Create an entry widget for typing messages
entry = tk.Entry(root, width=40, font=('Arial', 12))
entry.pack(padx=10, pady=(0, 10), side=tk.LEFT)

# Create a button to send messages

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(padx=(0, 10), pady=(0, 10), side=tk.RIGHT)

root.bind('<Return>', send_message)

for message in chat_history:
    send_message(user_message=message)  # Call send_message with predefined messages

root.mainloop()


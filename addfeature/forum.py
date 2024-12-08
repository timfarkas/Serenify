import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sessions import Session
from database.database import Database, Forum
from addfeature.globaldb import global_db
global global_db
db=global_db

def openforsum():
    sess = Session()
    sess.open()
    userID = sess.getId()
    root = tk.Tk()
    forumdata= db.getRelation('Forum')
    parent_threads=forumdata.getRowsWhereEqual('thread_id',0)
    class NewForum:
        def __init__(self, root):
            self.root = root
            self.root.title("The Garden")
            # self.root.geometry("800x900")

            self.tree = ttk.Treeview(root, columns=("Author", "Content","Post Date"), height=8)
            self.tree.heading("#0", text="Topic")
            self.tree.column("#0", width=200)
            self.tree.heading("Author", text="Author")
            self.tree.heading("Post Date", text="Post Date")
            self.tree.column("Author", width=50, anchor="center")
            self.tree.column("Content", width=0, stretch=False)
            self.tree.column("Post Date", width=50, anchor="center")
            self.tree.pack(fill="both", expand=True, pady=(10, 0))

            self.text_frame = tk.Frame(root)
            self.text_frame.pack(fill="both", expand=False, pady=10)

            self.text_label = tk.Label(self.text_frame, text="Thread Content:")
            self.text_label.pack(anchor="w", padx=5)

            self.text_box = tk.Text(self.text_frame, wrap="word", height=8)
            self.text_box.pack(fill="both", expand=True, padx=5, pady=5)


            self.input_frame1 = tk.Frame(root)
            self.input_frame1.pack(fill="x", pady=5)
            self.input_label = tk.Label(self.input_frame1, text="Enter Topic:",width=10)
            self.input_label.pack(side="left", padx=5)
            self.topic_entry = tk.Entry(self.input_frame1, width=46)
            self.topic_entry.pack(side="left", padx=5)

            self.input_frame2 = tk.Frame(root)
            self.input_frame2.pack(fill="x", pady=5)
            self.input_label_content = tk.Label(self.input_frame2, text="Enter Content:",width=10, anchor="w")
            self.input_label_content.pack(side="left", padx=5)
            self.content_entry = tk.Text(self.input_frame2, width=60,height=5)
            self.content_entry.pack(side="left", padx=5)

            self.input_frame3 = tk.Frame(root)
            self.input_frame3.pack(fill="x", pady=5)
            self.button_frame = tk.Frame(self.input_frame3)
            self.button_frame.pack(side="right", padx=5)
            self.add_thread_btn = tk.Button(self.button_frame, text="New Thread", command=self.add_thread,width=10)
            self.add_thread_btn.pack(side="right", pady=2)
            self.reply_btn = tk.Button(self.button_frame, text="Reply", command=self.add_reply,width=10)
            self.reply_btn.pack(side="right", pady=2)

            self.populate_forum()
            self.tree.tag_configure("me", foreground="green")
            self.tree.tag_configure("other", foreground="black")
            self.tree.bind("<<TreeviewSelect>>", self.display_selected_content)

        def populate_forum(self):
            forumdata = db.getRelation('Forum')
            parent_threads = forumdata.getRowsWhereEqual('parent_id', 0)
            parent_threads.sort(key = lambda x:x[5],reverse=True)
            for i in range(len(parent_threads)):
                user_id = parent_threads[i][4]
                userdata = db.getRelation('User').getRowsWhereEqual('user_id', user_id)
                userName = str(userdata[0][1])
                thread=self.tree.insert("", "end",text=parent_threads[i][2], values=(("You" if user_id==userID else userName), parent_threads[i][3], parent_threads[i][5].strftime("%Y-%m-%d %H:%M"),parent_threads[i][0]),tags=("me" if user_id==userID else "other"))
                # print(parent_threads[i][2])
                curparent_id = parent_threads[i][0]
                child_threads = forumdata.getRowsWhereEqual('parent_id', curparent_id)
                for j in range(len(child_threads)):
                    user_id=child_threads[j][4]
                    userdata = db.getRelation('User').getRowsWhereEqual('user_id', user_id)
                    userName = str(userdata[0][1])
                    # print(userName)
                    self.tree.insert(thread, "end", text=child_threads[j][2],values=(("You" if user_id==userID else userName), child_threads[j][3], child_threads[j][5].strftime("%Y-%m-%d %H:%M"),parent_threads[i][0]),tags=("me" if user_id==userID else "other"))

        def add_thread(self):
            topic = self.topic_entry.get().strip()
            content = self.content_entry.get("1.0","end").strip()
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if topic and content:
                self.topic_entry.delete(0, tk.END)
                self.content_entry.delete("1.0", tk.END)
                new_forum_entry = Forum(
                    parent_id=0,
                    topic=topic,
                    content=content,
                    user_id=userID,
                    timestamp=datetime.now(),
                )
                db.insert_forum(new_forum_entry)
                newforumdata = db.getRelation('Forum')
                newentry = newforumdata.getAllRows()[-1]
                # print(newentry[0])
                self.tree.insert("", "end", text=topic, values=("You", content, time,newentry[0]),tags="me")
            else:
                messagebox.showwarning("Empty Input", "Please enter both a topic and content.")

        def add_reply(self):
            selected_item = self.tree.selection()
            time = datetime.now().strftime("%Y-%m-%d %H:%M")
            if not selected_item:
                messagebox.showwarning("No Selection", "Please select a thread or post to reply to.")
                return

            upper_id = self.tree.parent(selected_item[0])  # Get the parent of the selected item
            if upper_id:
                directreply=False
                while upper_id:
                    parent_thread=upper_id
                    upper_id=self.tree.parent(upper_id)
            else:
                directreply = True
                parent_thread = selected_item[0]
            parent_id = self.tree.item(parent_thread, "values")[3]

            # Add the reply to the parent thread
            author = self.tree.item(selected_item[0], "values")[0]
            replytopic = self.topic_entry.get().strip()
            replycontent = self.content_entry.get("1.0","end").strip()
            if replytopic:
                self.tree.insert(parent_thread, "end", text=replytopic if directreply else "RE "+author+": "+replytopic, values=("You", replycontent,time,),tags="me")
                self.topic_entry.delete(0, tk.END)
                self.content_entry.delete("1.0", tk.END)
                new_forum_entry = Forum(
                    parent_id=int(parent_id),
                    topic=str(replytopic),
                    content=str(replycontent),
                    user_id=int(userID),
                    timestamp=datetime.now()
                )
                db.insert_forum(new_forum_entry)
            else:
                messagebox.showwarning("Empty Input", "Please enter a reply.")

        def display_selected_content(self, event):
            selected_item = self.tree.selection()
            if not selected_item:
                return
            title = self.tree.item(selected_item[0])["text"]
            content = self.tree.item(selected_item[0], "values")[1]
            author = self.tree.item(selected_item[0], "values")[0]
            time = self.tree.item(selected_item[0], "values")[2]

            self.text_box.delete("1.0", tk.END)  # Clear the text box
            self.text_box.insert(tk.END, f"[Title] {title}\n")
            self.text_box.insert(tk.END, f"[Author] {author}   {time} \n{content}")

    app = NewForum(root)
    def on_close():
        # db.close()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
# if __name__ == "__main__":
#     openforsum()

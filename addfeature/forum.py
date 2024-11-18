import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

class ForumApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Forum Layout with User Icons")

        # Load user icon (replace 'user_icon.png' with your icon path)
        # self.user_icon = tk.PhotoImage(file="pics/Picture 1.png")  # Ensure it's a small image, e.g., 16x16 pixels

        # Create a Treeview widget to display forum threads
        self.tree = ttk.Treeview(root, columns=("Author", "Message"), show="tree headings", height=15)
        self.tree.heading("#0", text="Thread")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Message", text="Message")
        self.tree.column("Author", width=100, anchor="center")
        self.tree.column("Message", width=300)

        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        # Sample data (initial forum thread)
        self.thread_id = self.tree.insert("", tk.END, text="General Discussion", values=("Admin", "Welcome to the forum!"))

        # Reply Section
        self.reply_label = tk.Label(root, text="Write a reply:")
        self.reply_label.pack(padx=10, pady=(5, 0), anchor="w")

        self.reply_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=4, width=50)
        self.reply_text.pack(padx=10, pady=(0, 10))

        self.author_label = tk.Label(root, text="Author:")
        self.author_label.pack(padx=10, pady=(0, 0), anchor="w")

        self.author_entry = tk.Entry(root, width=20)
        self.author_entry.pack(padx=10, pady=(0, 10), anchor="w")

        self.reply_button = tk.Button(root, text="Reply", command=self.add_reply)
        self.reply_button.pack(pady=(0, 10))

    def add_reply(self):
        # Get the reply text and author
        reply_text = self.reply_text.get("1.0", tk.END).strip()
        author = self.author_entry.get().strip()

        if reply_text and author:
            # Insert reply under the selected thread or as a sub-comment to the selected message
            selected_item = self.tree.selection()
            if selected_item:
                self.tree.insert(selected_item[0], tk.END, text="Reply", values=(author, reply_text), image=self.user_icon)
            else:
                self.tree.insert(self.thread_id, tk.END, text="Reply", values=(author, reply_text), image=self.user_icon)

            # Clear input fields
            self.reply_text.delete("1.0", tk.END)
            self.author_entry.delete(0, tk.END)

# Run the application
root = tk.Tk()
app = ForumApp(root)
root.mainloop()

import tkinter as tk
import 

# Create the main window
root = tk.Tk()
root.title("Logout")

h1_label = tk.Label(root, text="Logout successful!", font=("Arial", 24, "bold"))
h1_label.pack()

# Login button
login_button = tk.Button(root, text="Log back in", command=root.login.py)
login_button.pack()

root.mainloop()
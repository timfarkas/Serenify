import tkinter as tk

root = tk.Tk()
root.title("Appointment")

# H1 equivalent
h1_label = tk.Label(root, text="Book an appointment with you practioner here", font=("Arial", 24, "bold"))
h1_label.pack()

# Create a menubar
menubar = tk.Menu(root)

# Create a file menu
file_menu = tk.Menu(menubar, tearoff=0)

# Add commands to the file menu
file_menu.add_command(label="Select a date over the next 7 days", command=lambda: print("Date selection triggered"))
file_menu.add_command(label="Open", command=lambda: print("Open file triggered"))
file_menu.add_command(label="Save", command=lambda: print("Save file triggered"))
file_menu.add_separator()  # Adds a separator line
file_menu.add_command(label="Exit", command=root.quit)

# Add the file menu to the menubar
menubar.add_cascade(label="File", menu=file_menu)

# Configure the root window to use the menubar
root.config(menu=menubar)

check_var = tk.BooleanVar()
check1 = tk.Checkbutton(root, text="Time1", variable=check_var)
check2 = tk.Checkbutton(root, text="Time2", variable=check_var)
check3 = tk.Checkbutton(root, text="Time2", variable=check_var)
check4 = tk.Checkbutton(root, text="Time4", variable=check_var)
check1.pack()
check2.pack()
check3.pack()
check4.pack()

# submit appointment
button = tk.Button(root, text="Request")
button.pack()

    # Back button
    self.back_button = tk.Button(root, text="Back", command=self.backButton)
    self.back_button.pack()

    def backButton(self):
        subprocess.Popen(["python3", "patient/patientMain.py"])
        self.root.destroy()

root.mainloop()
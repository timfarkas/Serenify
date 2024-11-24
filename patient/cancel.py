import tkinter as tk

root = tk.Tk()
root.title("Cancellation")

# H1 equivalent
h1_label = tk.Label(root, text="Cancel an up-and-coming appointment", font=("Arial", 24, "bold"))
h1_label.pack()

# Radio buttons to describe user and hyperlink them to appropriate main page
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
button = tk.Button(root, text="Cancel")
button.pack()

    # Back button
    self.back_button = tk.Button(root, text="Back", command=self.backButton)
    self.back_button.pack()

    def backButton(self):
        subprocess.Popen(["python3", "patient/patientMain.py"])
        self.root.destroy()
    
root.mainloop()
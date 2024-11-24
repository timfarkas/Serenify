import tkinter as tk

root = tk.Tk()
root.title("Appointment request")

# H1 equivalent
h1_label = tk.Label(root, text="Appointment requested from:", font=("Arial", 24, "bold"))
h1_label.pack()

fieldset = tk.LabelFrame(root, text="Personal Information", padx=10, pady=10)
fieldset.pack(padx=10, pady=10)

name_label = tk.Label(fieldset, text="Name:")
name_label.grid(row=0, column=0)
name_entry = tk.Entry(fieldset)
name_entry.grid(row=0, column=1)

age_label = tk.Label(fieldset, text="Age:")
age_label.grid(row=1, column=0)
age_entry = tk.Entry(fieldset)
age_entry.grid(row=1, column=1)

age_label = tk.Label(fieldset, text="Diagnosis:")
age_label.grid(row=2, column=0)
age_entry = tk.Entry(fieldset)
age_entry.grid(row=2, column=1)

age_label = tk.Label(fieldset, text="Date:")
age_label.grid(row=3, column=0)
age_entry = tk.Entry(fieldset)
age_entry.grid(row=3, column=1)

age_label = tk.Label(fieldset, text="Time:")
age_label.grid(row=4, column=0)
age_entry = tk.Entry(fieldset)
age_entry.grid(row=4, column=1)

    # Buttons
accept_button = tk.Button(root, text="Accept")
accept_button.pack()
decline_button = tk.Button(root, text="Decline")
decline_button.pack()

    ####### Back button - needs completing #######
    # self.back_button = tk.Button(root, text="Login", command=self.backButton)
    # self.back_button.pack()

    # def backButton(self):
    #     subprocess.Popen(["python3", "mhwpMain.py"])
    #     self.root.destroy()

root.mainloop()
import tkinter as tk
# import patientNew

# Make sure you OOP throughout - Good marks!

# def open_patient_new():
#     root.destroy()  # Close the login window
#     patientNew.open_patient_window()  # Call the function from patientNew.py

# Create the main window
root = tk.Tk()
root.title("Login")

# H1 equivalent
h1_label = tk.Label(root, text="Sign up", font=("Arial", 24, "bold"))
h1_label.pack()

# radio buttons to signify who user is so can be directed to correct page
radio_var = tk.StringVar()
radio1 = tk.Radiobutton(root, text="Admin", variable=radio_var, value="A") # When this is clicked, take user to adminMain
radio2 = tk.Radiobutton(root, text="MHWP", variable=radio_var, value="B") # When this is clicked, take user to mhwpMain
radio3 = tk.Radiobutton(root, text="Patient", variable=radio_var, value="C") # When this is clicked, take user to patientMain
radio4 = tk.Radiobutton(root, text="New Patient", variable=radio_var, value="D") # When this is clicked, take user to newPatient
radio1.pack()
radio2.pack()
radio3.pack()
radio4.pack()

fieldset = tk.LabelFrame(root, text="Login", padx=10, pady=10)
fieldset.pack(padx=10, pady=10)
 
# Username field
name_label = tk.Label(fieldset, text="Username:")
name_label.grid(row=0, column=0)
name_entry = tk.Entry(fieldset)
name_entry.grid(row=0, column=1)
# Password field
password_label = tk.Label(fieldset, text="Password:")
password_label.grid(row=1, column=0)
password_entry = tk.Entry(fieldset, show="*")
password_entry.grid(row=1, column=1)

# Login button to open patientNew.py
login_button = tk.Button(root, text="Login")
login_button.pack()

class findMainPage():
    def __init__(self, name_entry, password_entry):
        self.name_entry = name_entry
        self.password_entry = password_entry

    def adminDirect(self):
        if name_entry == name_entry logged in pandas:
    if password_entry == password_entry in pandas:
        print('Login successful!')
        Need to link this to the radio buttons
    def patientDirect(self):
        if name_entry == name_entry logged in pandas:
    if password_entry == password_entry in pandas:
        print('Login successful!')
        Need to link this to the radio buttons
    def newPatientDirect(self):
        if name_entry == name_entry logged in pandas:
    if password_entry == password_entry in pandas:
        print('Login successful!')
        Need to link this to the radio buttons
    def mhwpDirect(self):
        if name_entry == name_entry logged in pandas:
    if password_entry == password_entry in pandas:
        print('Login successful!')
        Need to link this to the radio buttons
    

# Run the application
root.mainloop()
import tkinter as tk
import patientNew

def open_patient_new():
    root.destroy()  # Close the login window
    patientNew.open_patient_window()  # Call the function from patientNew.py

# Create the main window
root = tk.Tk()
root.title("Login")
-
# H1 equivalent
h1_label = tk.Label(root, text="Sign up", font=("Arial", 24, "bold"))
h1_label.pack()

radio_var = tk.StringVar()

radio1 = tk.Radiobutton(root, text="Option A", variable=radio_var, value="A")
radio2 = tk.Radiobutton(root, text="Option B", variable=radio_var, value="B")
radio3 = tk.Radiobutton(root, text="Option C", variable=radio_var, value="C")
radio4 = tk.Radiobutton(root, text="Option D", variable=radio_var, value="D")
radio1.pack()
radio2.pack()
radio3.pack()
radio4.pack()

fieldset = tk.LabelFrame(root, text="Login", padx=10, pady=10)
fieldset.pack(padx=10, pady=10)
 
name_label = tk.Label(fieldset, text="Username:")
name_label.grid(row=0, column=0)
name_entry = tk.Entry(fieldset)
name_entry.grid(row=0, column=1)

password_label = tk.Label(fieldset, text="Password:")
password_label.grid(row=1, column=0)
password_entry = tk.Entry(fieldset, show="*")
password_entry.grid(row=1, column=1)

# Login button to open patientNew.py
login_button = tk.Button(root, text="Login", command=open_patient_new)
login_button.pack()

# Run the application
root.mainloop()
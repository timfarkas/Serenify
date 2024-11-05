import tkinter as tk

root = tk.Tk()
root.title("Disable Patients")

# H1 equivalent
h1_label = tk.Label(root, text="Welcome back admin", font=("Arial", 24, "bold"))
h1_label.pack()


docToPatient = tk.Label(root, text="Choose the patient(s) to disable:", font=("Arial", 12, "bold"))
docToPatient.pack()

check_var = tk.BooleanVar()
check1 = tk.Checkbutton(root, text="Patient1", variable=check_var)
check2 = tk.Checkbutton(root, text="Patient2", variable=check_var)
check3 = tk.Checkbutton(root, text="Patient3", variable=check_var)
check4 = tk.Checkbutton(root, text="Patient4", variable=check_var)
check1.pack()
check2.pack()
check3.pack()
check4.pack()

#Button 
delete_button = tk.Button(root, text="Disable")  
delete_button.pack()

# Run the application
root.mainloop()
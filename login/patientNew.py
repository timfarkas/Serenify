import tkinter as tk

def open_patient_window():
    patient_root = tk.Toplevel()  # Toplevel for the patient window
    patient_root.title("New Patient Submission")

    # H1 equivalent
    h1_label = tk.Label(patient_root, text="Sign up", font=("Arial", 24, "bold"))
    h1_label.pack()

    h2_label = tk.Label(patient_root, text="Welcome! Please fill out the below:", font=("Arial", 18, "bold"))
    h2_label.pack()

    fieldset = tk.LabelFrame(patient_root, text="Personal Information", padx=10, pady=10)
    fieldset.pack(padx=10, pady=10)

    name_label = tk.Label(fieldset, text="Name:")
    name_label.grid(row=0, column=0)
    name_entry = tk.Entry(fieldset)
    name_entry.grid(row=0, column=1)

    age_label = tk.Label(fieldset, text="Age:")
    age_label.grid(row=1, column=0)
    age_entry = tk.Entry(fieldset)
    age_entry.grid(row=1, column=1)

    age_label = tk.Label(fieldset, text="Home address:")
    age_label.grid(row=2, column=0)
    age_entry = tk.Entry(fieldset)
    age_entry.grid(row=2, column=1)

    age_label = tk.Label(fieldset, text="Diagnosis:")
    age_label.grid(row=3, column=0)
    age_entry = tk.Entry(fieldset)
    age_entry.grid(row=3, column=1)

    age_label = tk.Label(fieldset, text="Email:")
    age_label.grid(row=4, column=0)
    age_entry = tk.Entry(fieldset)
    age_entry.grid(row=4, column=1)

    age_label = tk.Label(fieldset, text="Mobile:")
    age_label.grid(row=5, column=0)
    age_entry = tk.Entry(fieldset)
    age_entry.grid(row=5, column=1)

    age_label = tk.Label(fieldset, text="ICE name and mobile:")
    age_label.grid(row=6, column=0)
    age_entry = tk.Entry(fieldset)
    age_entry.grid(row=6, column=1)

    # Add a button to the patient info window
    button = tk.Button(patient_root, text="Submit", command=patient_root.destroy)
    button.pack()

    button = tk.Button(patient_root, text="Submit", command=patient_root.destroy)
    button.pack()

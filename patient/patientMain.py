import tkinter as tk
import patientNew  # Import patientNew module

def open_patient_new():
    root.destroy()  # Close the login window
    patientNew.open_patient_window()  # Open patient window

def search():
    query = search_entry.get()  # Get the search query from the entry
    if query:
        # For demonstration, we'll just show a message box with the search term
        tk.messagebox.showinfo("Search", f"You searched for: {query}")
    else:
        tk.messagebox.showwarning("Warning", "Please enter a search term.")

######### Likely needed for the search bar to function: ###########
# def open_link():
#     print("Link clicked!")  # Replace this with opening a web link if desired

# link = tk.Label(root, text="Click here", fg="blue", cursor="hand2")
# link.bind("<Button-1>", lambda e: open_link())
# link.pack()

root = tk.Tk()
root.title("Patient")

# H1 equivalent
h1_label = tk.Label(root, text="Welcome back", font=("Arial", 24, "bold"))
h1_label.pack()

# Search bar section
search_label = tk.Label(root, text="Search:")
search_label.pack(pady=5)

search_entry = tk.Entry(root, width=30)  # Create the search entry widget
search_entry.pack(pady=5)

search_button = tk.Button(root, text="Search", command=search)  # Create the search button
search_button.pack(pady=10)

# Mood of the day
radio_var = tk.StringVar()
radio1 = tk.Radiobutton(root, text="Great", variable=radio_var, value="Great")
radio2 = tk.Radiobutton(root, text="Good", variable=radio_var, value="Good")
radio3 = tk.Radiobutton(root, text="Okay", variable=radio_var, value="Okay")
radio4 = tk.Radiobutton(root, text="Could be better", variable=radio_var, value="Could be better")
radio5 = tk.Radiobutton(root, text="Terrible", variable=radio_var, value="Terrible")
radio1.pack()
radio2.pack()
radio3.pack()
radio4.pack()
radio5.pack()

# Fieldset for journalling 
fieldset = tk.LabelFrame(root, text="Journal", padx=10, pady=10)
fieldset.pack(padx=10, pady=10)

name_label = tk.Label(fieldset, text="How are we doing today?")
name_label.grid(row=0, column=0)
name_entry = tk.Entry(fieldset)
name_entry.grid(row=0, column=1)

h2_label = tk.Label(root, text="Personal info:", font=("Arial", 12, "bold"))
h2_label.pack()

#Buttons
login_button1 = tk.Button(root, text="Edit personal info", command=open_patient_new) 
login_button2 = tk.Button(root, text="Book/Cancel appointment", command=open_patient_new)  
login_button1.pack()
login_button2.pack()

# Run the application
root.mainloop()
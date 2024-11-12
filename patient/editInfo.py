import tkinter as tk
from tkinter import messagebox
#Once we have real database there should be a better way to edit information rather than having to retype each item
#first we need to see that that input exists within existing_records
def match_in_database(name, emergency_contact, emergency_contact_phone, email):
    existing_records = {} #once we have the real database
    return (name, emergency_contact, emergency_contact_phone, email) in existing_records #if match is found in our database
def update_info ():
    name = name_entry.get()
    emergency_contact = emergency_contact_entry.get()
    emergency_contact_phone = emergency_contact_phone_entry.get()
    email = email_entry.get()

    if not emergency_contact_phone.isdigit(): #checking if emergency contact phone number is a valid number, not including any letters
        messagebox.showerror("Invalid Input, Please enter only digits")
        return

    if  match_in_database(name, emergency_contact, emergency_contact_phone, email):
        messagebox.showinfo("Information Updated", f"Name: {name}\nEmergency Contact: {emergency_contact}\nEmail: {email}")

    else: #error
        messagebox.showerror("Update Failed, Information not found")

root = tk.Tk()
root.title("Personal information")

# H1 equivalent
h1_label = tk.Label(root, text="Edit your personal information here", font=("Arial", 24, "bold"))
h1_label.pack()

fieldset = tk.LabelFrame(root, text="Personal Information", padx=10, pady=10)
fieldset.pack(padx=10, pady=10)

name_label = tk.Label(fieldset, text="Full Name:")
name_label.grid(row=0, column=0)
name_entry = tk.Entry(fieldset)
name_entry.grid(row=0, column=1)


emergency_contact_label = tk.Label(fieldset, text="Emergency Contact:")
emergency_contact_label.grid(row=1, column=0)
emergency_contact_entry = tk.Entry(fieldset)
emergency_contact_entry.grid(row=1, column=1)

emergency_contact_phone_label = tk.Label(fieldset, text="Emergency Contact Phone:")
emergency_contact_phone_label.grid(row=2, column=0)
emergency_contact_phone_entry = tk.Entry(fieldset)
emergency_contact_phone_entry.grid(row=2, column=1)


email_label = tk.Label(fieldset, text="Email:")
email_label.grid(row=3, column=0)
email_entry = tk.Entry(fieldset)
email_entry.grid(row=3, column=1)

update_button = tk.Button(root,text = "Update", command=update_info)
update_button.pack(pady=5)



root.mainloop()
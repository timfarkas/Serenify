import tkinter as tk
from tkinter import messagebox
from database import Database


class PatientSelectionApp:
    def __init__(self, root):
        self.db = Database()
        self.root = root
        self.selected_patient_id = tk.IntVar(value=-1)
        self.users = self.db.getRelation('Users').getRowsWhereEqual("type", "Patient")
        self.create_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_ui(self):
        self.root.title("Select Patient")

        # H1 equivalent
        h1_label = tk.Label(self.root, text="Welcome back admin", font=("Arial", 24, "bold"))
        h1_label.pack()
        
        # instruction label
        docToPatient = tk.Label(self.root, text="Choose the patient to edit:", font=("Arial", 12, "bold"))
        docToPatient.pack()

        # creating checkbox for each patient
        for user in self.users:
            patient_name = f"{user[4]} {user[5]}"
            radio_button = tk.Radiobutton(self.root, text=patient_name, variable=self.selected_patient_id, value=user[0])
            radio_button.pack(anchor="w")

        # select Button 
        select_button = tk.Button(self.root, text="Select patient", command=self.edit_patient)  
        select_button.pack()

    def edit_patient(self):
        selected_patient_id = self.selected_patient_id.get()
        if selected_patient_id != -1:
            self.root.withdraw()
            edit_window = tk.Toplevel(self.root)
            app = PatientEditApp(edit_window, selected_patient_id)
        else:
            messagebox.showinfo("No Patient Selected", "Please select a patient to continue.")

    def on_close(self):
        self.db.close()
        self.root.destroy()


class PatientEditApp:
    def __init__(self, root, user_id):
        self.db = Database()
        self.root = root
        self.user_id = user_id 
        self.original_data = {}
        self.create_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_ui(self):
        self.root.title("Edit User Information")

        # H1 equivalent
        h1_label = tk.Label(self.root, text="Edit Patient Information", font=("Arial", 24, "bold"))
        h1_label.pack()

        user = self.fetch_user_details(self.user_id)
        self.original_data = user

        # Create labels and entry fields
        user_frame = tk.Frame(self.root)
        user_frame.pack(fill='x', padx=10, pady=5)

        tk.Label(user_frame, text=f"User ID: {user['user_id']}", width=15).grid(row=0, column=0)
        tk.Label(user_frame, text="Username:").grid(row=1, column=0)
        self.username_entry = tk.Entry(user_frame)
        self.username_entry.insert(0, user['username'] if user['username'] else '')
        self.username_entry.config(state='disabled')
        self.username_entry.grid(row=1, column=1)

        tk.Label(user_frame, text="Email:").grid(row=2, column=0)
        self.email_entry = tk.Entry(user_frame)
        self.email_entry.insert(0, user['email'] if user['email'] else '')
        self.email_entry.config(state='disabled')
        self.email_entry.grid(row=2, column=1)

        tk.Label(user_frame, text="Password:").grid(row=3, column=0)
        self.password_entry = tk.Entry(user_frame, show="*")
        self.password_entry.insert(0, user['password'] if user['password'] else '')
        self.password_entry.config(state='disabled')
        self.password_entry.grid(row=3, column=1)

        tk.Label(user_frame, text="First Name:").grid(row=4, column=0)
        self.fName_entry = tk.Entry(user_frame)
        self.fName_entry.insert(0, user['fName'] if user['fName'] else '')
        self.fName_entry.config(state='disabled')
        self.fName_entry.grid(row=4, column=1)

        tk.Label(user_frame, text="Last Name:").grid(row=5, column=0)
        self.lName_entry = tk.Entry(user_frame)
        self.lName_entry.insert(0, user['lName'] if user['lName'] else '')
        self.lName_entry.config(state='disabled')
        self.lName_entry.grid(row=5, column=1)

        tk.Label(user_frame, text="Emergency Contact Email:").grid(row=6, column=0)
        self.emergency_email_entry = tk.Entry(user_frame)
        self.emergency_email_entry.insert(0, user['emergency_contact_email'] if user['emergency_contact_email'] else '')
        self.emergency_email_entry.config(state='disabled')
        self.emergency_email_entry.grid(row=6, column=1)

        tk.Label(user_frame, text="Mood:").grid(row=7, column=0)
        self.mood_entry = tk.Entry(user_frame)
        self.mood_entry.insert(0, user['mood'] if user['mood'] else '')
        self.mood_entry.config(state='disabled')
        self.mood_entry.grid(row=7, column=1)

        tk.Label(user_frame, text="Mood Comment:").grid(row=8, column=0)
        self.mood_comment_entry = tk.Entry(user_frame)
        self.mood_comment_entry.insert(0, user['mood_comment'] if user['mood_comment'] else '')
        self.mood_comment_entry.config(state='disabled')
        self.mood_comment_entry.grid(row=8, column=1)

        tk.Label(user_frame, text="Disabled:").grid(row=10, column=0)
        self.is_disabled_var = tk.BooleanVar(value=user['is_disabled'])
        self.is_disabled_check = tk.Checkbutton(user_frame, variable=self.is_disabled_var)
        self.is_disabled_check.config(state='disabled')
        self.is_disabled_check.grid(row=10, column=1)

        # Toggle Edit/Save Button
        self.toggle_button = tk.Button(self.root, text="Edit", command=self.toggle_edit_save)
        self.toggle_button.pack(pady=0)

        # Delete Button
        self.delete_button = tk.Button(self.root, text="Delete Patient", command=self.delete_patient)
        self.delete_button.pack(pady=0)

        # Back Button
        self.back_button = tk.Button(self.root, text="Back", command=self.go_back)
        self.back_button.pack(pady=0)

    def fetch_user_details(self, user_id):
        user_relation = self.db.getRelation('Users')
        user = user_relation.getRowsWhereEqual('user_id', user_id)

        if user:
            user_data = user[0]
            return {
                'user_id': user_data[0],
                'username': user_data[1],
                'email': user_data[2],
                'password': user_data[3],
                'fName': user_data[4],
                'lName': user_data[5],
                'emergency_contact_email': user_data[7],
                'mood': user_data[8],
                'mood_comment': user_data[9],
                'is_disabled': user_data[11]
            }
        else:
            messagebox.showerror("Error", "User not found!")
            return {}

    def toggle_edit_save(self):
        if self.username_entry.cget('state') == 'disabled':
            # Enable all the entry fields for editing
            self.username_entry.config(state='normal')
            self.email_entry.config(state='normal')
            self.password_entry.config(state='normal')
            self.fName_entry.config(state='normal')
            self.lName_entry.config(state='normal')
            self.emergency_email_entry.config(state='normal')
            self.mood_entry.config(state='normal')
            self.mood_comment_entry.config(state='normal')
            self.is_disabled_check.config(state='normal')

            self.toggle_button.config(text="Save Changes")  
        
        else:
            self.save_changes_to_db()
            
            updated_data = {
                'username': self.username_entry.get(),
                'email': self.email_entry.get(),
                'password': self.password_entry.get(),
                'fName': self.fName_entry.get(),
                'lName': self.lName_entry.get(),
                'emergency_contact_email': self.emergency_email_entry.get(),
                'mood': self.mood_entry.get(),
                'mood_comment': self.mood_comment_entry.get(),
                'is_disabled': self.is_disabled_var.get()
            }

            self.toggle_button.config(text="Edit")

            # disable fields again after saving
            self.username_entry.config(state='disabled')
            self.email_entry.config(state='disabled')
            self.password_entry.config(state='disabled')
            self.fName_entry.config(state='disabled')
            self.lName_entry.config(state='disabled')
            self.emergency_email_entry.config(state='disabled')
            self.mood_entry.config(state='disabled')
            self.mood_comment_entry.config(state='disabled')
            self.is_disabled_check.config(state='disabled')
    
    def save_changes_to_db(self):
        user_relation = self.db.getRelation('Users')
        updated_data = {
            'username': self.username_entry.get(),
            'email': self.email_entry.get(),
            'password': self.password_entry.get(),
            'fName': self.fName_entry.get(),
            'lName': self.lName_entry.get(),
            'emergency_contact_email': self.emergency_email_entry.get(),
            'mood': self.mood_entry.get(),
            'mood_comment': self.mood_comment_entry.get(),
            'is_disabled': self.is_disabled_var.get()
        }
        
        for field, new_value in updated_data.items():
            if self.original_data[field] != new_value:
                user_relation.editFieldInRow(self.user_id, field, new_value)
        
        messagebox.showinfo("Success", "Patient information updated successfully.")

    def delete_patient(self):
        user_relation = self.db.getRelation('Users')
        response = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this patient?")

        if response:
            user_relation.dropRows(id=self.user_id)
            messagebox.showinfo("Success", "Patient deleted successfully.")
            self.on_close()

    def go_back(self):
        self.root.destroy()

        root = tk.Tk()
        app = PatientSelectionApp(root)
        root.mainloop()

    def on_close(self):
        self.db.close()
        self.root.destroy()


class MHWPSelectionApp:
    def __init__(self, root):
        self.db = Database()
        self.root = root
        self.selected_MHWP_id = tk.IntVar(value=-1)
        self.users = self.db.getRelation('Users').getRowsWhereEqual("type", "MHWP")
        self.create_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_ui(self):
        self.root.title("Select MHWP")

        # H1 equivalent
        h1_label = tk.Label(self.root, text="Welcome back admin", font=("Arial", 24, "bold"))
        h1_label.pack()
        
        # instruction label
        docToMHWP = tk.Label(self.root, text="Choose the MHWP to edit:", font=("Arial", 12, "bold"))
        docToMHWP.pack()

        # creating checkbox for each MHWP
        for user in self.users:
            MHWP_name = f"{user[4]} {user[5]}"
            radio_button = tk.Radiobutton(self.root, text=MHWP_name, variable=self.selected_MHWP_id, value=user[0])
            radio_button.pack(anchor="w")

        # select Button 
        select_button = tk.Button(self.root, text="Select MHWP", command=self.edit_MHWP)  
        select_button.pack()

    def edit_MHWP(self):
        selected_MHWP_id = self.selected_MHWP_id.get()
        if selected_MHWP_id != -1:
            self.root.withdraw()
            edit_window = tk.Toplevel(self.root)
            app = MHWPEditApp(edit_window, selected_MHWP_id)
        else:
            messagebox.showinfo("No MHWP Selected", "Please select a MHWP to continue.")

    def on_close(self):
        self.db.close()
        self.root.destroy()


class MHWPEditApp:
    def __init__(self, root, user_id):
        self.db = Database()
        self.root = root
        self.user_id = user_id 
        self.original_data = {}
        self.create_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_ui(self):
        self.root.title("Edit User Information")

        # H1 equivalent
        h1_label = tk.Label(self.root, text="Edit MHWP Information", font=("Arial", 24, "bold"))
        h1_label.pack()

        user = self.fetch_user_details(self.user_id)
        self.original_data = user

        # Create labels and entry fields
        user_frame = tk.Frame(self.root)
        user_frame.pack(fill='x', padx=10, pady=5)

        tk.Label(user_frame, text=f"User ID: {user['user_id']}", width=15).grid(row=0, column=0)
        tk.Label(user_frame, text="Username:").grid(row=1, column=0)
        self.username_entry = tk.Entry(user_frame)
        self.username_entry.insert(0, user['username'] if user['username'] else '')
        self.username_entry.config(state='disabled')
        self.username_entry.grid(row=1, column=1)

        tk.Label(user_frame, text="Email:").grid(row=2, column=0)
        self.email_entry = tk.Entry(user_frame)
        self.email_entry.insert(0, user['email'] if user['email'] else '')
        self.email_entry.config(state='disabled')
        self.email_entry.grid(row=2, column=1)

        tk.Label(user_frame, text="Password:").grid(row=3, column=0)
        self.password_entry = tk.Entry(user_frame, show="*")
        self.password_entry.insert(0, user['password'] if user['password'] else '')
        self.password_entry.config(state='disabled')
        self.password_entry.grid(row=3, column=1)

        tk.Label(user_frame, text="First Name:").grid(row=4, column=0)
        self.fName_entry = tk.Entry(user_frame)
        self.fName_entry.insert(0, user['fName'] if user['fName'] else '')
        self.fName_entry.config(state='disabled')
        self.fName_entry.grid(row=4, column=1)

        tk.Label(user_frame, text="Last Name:").grid(row=5, column=0)
        self.lName_entry = tk.Entry(user_frame)
        self.lName_entry.insert(0, user['lName'] if user['lName'] else '')
        self.lName_entry.config(state='disabled')
        self.lName_entry.grid(row=5, column=1)

        tk.Label(user_frame, text="Emergency Contact Email:").grid(row=6, column=0)
        self.emergency_email_entry = tk.Entry(user_frame)
        self.emergency_email_entry.insert(0, user['emergency_contact_email'] if user['emergency_contact_email'] else '')
        self.emergency_email_entry.config(state='disabled')
        self.emergency_email_entry.grid(row=6, column=1)

        tk.Label(user_frame, text="Disabled:").grid(row=10, column=0)
        self.is_disabled_var = tk.BooleanVar(value=user['is_disabled'])
        self.is_disabled_check = tk.Checkbutton(user_frame, variable=self.is_disabled_var)
        self.is_disabled_check.config(state='disabled')
        self.is_disabled_check.grid(row=10, column=1)

        # Toggle Edit/Save Button
        self.toggle_button = tk.Button(self.root, text="Edit", command=self.toggle_edit_save)
        self.toggle_button.pack(pady=0)

        # Delete Button
        self.delete_button = tk.Button(self.root, text="Delete MHWP", command=self.delete_MHWP)
        self.delete_button.pack(pady=0)

        # Back Button
        self.back_button = tk.Button(self.root, text="Back", command=self.go_back)
        self.back_button.pack(pady=0)

    def fetch_user_details(self, user_id):
        user_relation = self.db.getRelation('Users')
        user = user_relation.getRowsWhereEqual('user_id', user_id)

        if user:
            user_data = user[0]
            return {
                'user_id': user_data[0],
                'username': user_data[1],
                'email': user_data[2],
                'password': user_data[3],
                'fName': user_data[4],
                'lName': user_data[5],
                'emergency_contact_email': user_data[7],
                'is_disabled': user_data[11]
            }
        else:
            messagebox.showerror("Error", "User not found!")
            return {}

    def toggle_edit_save(self):
        if self.username_entry.cget('state') == 'disabled':
            # Enable all the entry fields for editing
            self.username_entry.config(state='normal')
            self.email_entry.config(state='normal')
            self.password_entry.config(state='normal')
            self.fName_entry.config(state='normal')
            self.lName_entry.config(state='normal')
            self.emergency_email_entry.config(state='normal')
            self.is_disabled_check.config(state='normal')

            self.toggle_button.config(text="Save Changes")  
        
        else:
            self.save_changes_to_db()
            
            updated_data = {
                'username': self.username_entry.get(),
                'email': self.email_entry.get(),
                'password': self.password_entry.get(),
                'fName': self.fName_entry.get(),
                'lName': self.lName_entry.get(),
                'emergency_contact_email': self.emergency_email_entry.get(),
                'is_disabled': self.is_disabled_var.get()
            }

            self.toggle_button.config(text="Edit")

            # disable fields again after saving
            self.username_entry.config(state='disabled')
            self.email_entry.config(state='disabled')
            self.password_entry.config(state='disabled')
            self.fName_entry.config(state='disabled')
            self.lName_entry.config(state='disabled')
            self.emergency_email_entry.config(state='disabled')
            self.is_disabled_check.config(state='disabled')
    
    def save_changes_to_db(self):
        user_relation = self.db.getRelation('Users')
        updated_data = {
            'username': self.username_entry.get(),
            'email': self.email_entry.get(),
            'password': self.password_entry.get(),
            'fName': self.fName_entry.get(),
            'lName': self.lName_entry.get(),
            'emergency_contact_email': self.emergency_email_entry.get(),
            'is_disabled': self.is_disabled_var.get()
        }
        
        for field, new_value in updated_data.items():
            if self.original_data[field] != new_value:
                user_relation.editFieldInRow(self.user_id, field, new_value)
        
        messagebox.showinfo("Success", "MHWP information updated successfully.")

    def delete_MHWP(self):
        user_relation = self.db.getRelation('Users')
        response = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this MHWP?")

        if response:
            user_relation.dropRows(id=self.user_id)
            messagebox.showinfo("Success", "MHWP deleted successfully.")
            self.on_close()

    def go_back(self):
        self.root.destroy()

        root = tk.Tk()
        app = MHWPSelectionApp(root)
        root.mainloop()

    def on_close(self):
        self.db.close()
        self.root.destroy()
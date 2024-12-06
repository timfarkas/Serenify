import tkinter as tk
from tkinter import messagebox, ttk
import math

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database import Database
from database.entities import Admin, Patient, MHWP, PatientRecord, Allocation, JournalEntry, Appointment

from sessions import Session

# on a temporary basis might need to run the adminSessionTest.py file first to initialise the sessions.

class AllocationEdit(tk.Toplevel):
    def __init__(self, patient_id, parent, db):
        super().__init__()
        self.db = db
        self.patient_id = patient_id
        self.parent = parent
        self.create_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_ui(self):
        self.title("Edit MHWP Assignment")

        # H1 equivalent
        h1_label = tk.Label(self, text="Assign MHWP to Patient", font=("Arial", 24, "bold"))
        h1_label.pack()
        
        # Fetch current MHWP assigned to the patient
        patient = self.db.getRelation('Allocation').getRowsWhereEqual("patient_id", self.patient_id)
        if not patient:
            messagebox.showerror("Error", "No patient found with the provided ID.")
            return
        assigned_mhwp_id = patient[0][3]
        
        self.allocation_id = patient[0][0]
        
        assigned_mhwp = self.db.getRelation('User').getRowsWhereEqual("user_id", assigned_mhwp_id)
        assigned_mhwp_name = f"{assigned_mhwp[0][4]} {assigned_mhwp[0][5]}"

        # Fetch list of MHWPs
        mhwps = self.db.getRelation('User').getRowsWhereEqual("type", "MHWP")
        self.mhwp_dict = {f"{mhwp[4]} {mhwp[5]}": mhwp[0] for mhwp in mhwps}
        mhwp_names = list(self.mhwp_dict.keys())

        # Create label and dropdown for MHWP selection
        tk.Label(self, text="Select New MHWP:").pack(pady=10)
        self.mhwp_var = tk.StringVar(value=assigned_mhwp_name)
        self.mhwp_dropdown = tk.OptionMenu(self, self.mhwp_var, *mhwp_names)
        self.mhwp_dropdown.pack(pady=10)

        # Save Button
        save_button = tk.Button(self, text="Save", command=self.save_mhwp)
        save_button.pack(pady=0)

        # Back Button
        self.back_button = tk.Button(self, text="Back", command=self.go_back)
        self.back_button.pack(pady=0)

    def save_mhwp(self):
        # Get the new MHWP selection
        new_mhwp_name = self.mhwp_var.get()
        new_mhwp_id = self.mhwp_dict.get(new_mhwp_name)

        try:
            # Update the patient's MHWP in the database
            userRelation = self.db.getRelation('Allocation')
            userRelation.editFieldInRow(self.allocation_id, 'mhwp_id', new_mhwp_id)

            messagebox.showinfo("Success", "MHWP updated successfully.")
        
        except Exception as e:
            messagebox.showerror("Error", str(e)) 

    def go_back(self):
        self.destroy()
        self.parent.refresh_treeview()
        self.parent.deiconify()

    def on_close(self):
        self.destroy()

class PatientEditApp(tk.Toplevel):
    def __init__(self, user_id, parent, db):
        super(PatientEditApp, self).__init__()
        self.db = db
        self.parent = parent
        self.user_id = user_id
        self.user_type = self.db.getRelation('User').getRowsWhereEqual("user_id", user_id)[0][6]
        self.original_data = {}
        self.create_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_ui(self):
        self.title("Edit User Information")

        # H1 equivalent
        h1_label = tk.Label(self, text=f"Edit {self.user_type} Information", font=("Arial", 24, "bold"))
        h1_label.pack()

        user = self.fetch_user_details(self.user_id)
        self.original_data = user

        # Create labels and entry fields
        user_frame = tk.Frame(self)
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

        tk.Label(user_frame, text="Emergency Contact Name:").grid(row=7, column=0)
        self.emergency_name_entry = tk.Entry(user_frame)
        self.emergency_name_entry.insert(0, user['emergency_contact_name'] if user['emergency_contact_name'] else '')
        self.emergency_name_entry.config(state='disabled')
        self.emergency_name_entry.grid(row=7, column=1)

        tk.Label(user_frame, text="Disable User:").grid(row=10, column=0)
        self.is_disabled_var = tk.BooleanVar(value=bool(user['is_disabled']))
        self.is_disabled_check = tk.Checkbutton(user_frame, variable=self.is_disabled_var)
        self.is_disabled_check.config(state='disabled')
        self.is_disabled_check.grid(row=10, column=1)

        # Toggle Edit/Save Button
        self.toggle_button = tk.Button(self, text="Edit", command=self.toggle_edit_save)
        self.toggle_button.pack(pady=0)

        # Delete Button
        self.delete_button = tk.Button(self, text=f"Delete {self.user_type}", command=self.delete_user)
        self.delete_button.pack(pady=0)

        # Back Button
        self.back_button = tk.Button(self, text="Back", command=self.go_back)
        self.back_button.pack(pady=0)

    def fetch_user_details(self, user_id):
        user_relation = self.db.getRelation('User')
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
                'emergency_contact_name': user_data[8],
                'is_disabled': user_data[10]
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
            self.emergency_name_entry.config(state='normal')
            self.is_disabled_check.config(state='normal')

            self.toggle_button.config(text="Save Changes")  
        
        else:
            success = self.save_changes_to_db()
            
            if success:
                self.toggle_button.config(text="Edit")
                
                # disable fields again after saving
                self.username_entry.config(state='disabled')
                self.email_entry.config(state='disabled')
                self.password_entry.config(state='disabled')
                self.fName_entry.config(state='disabled')
                self.lName_entry.config(state='disabled')
                self.emergency_email_entry.config(state='disabled')
                self.emergency_name_entry.config(state='disabled')
                self.is_disabled_check.config(state='disabled')
            else:
                pass

            updated_data = {
                'username': self.username_entry.get(),
                'email': self.email_entry.get(),
                'password': self.password_entry.get(),
                'fName': self.fName_entry.get(),
                'lName': self.lName_entry.get(),
                'emergency_contact_email': self.emergency_email_entry.get(),
                'emergency_contact_name': self.emergency_name_entry.get(),
                'is_disabled': self.is_disabled_var.get()
            }
    
    def save_changes_to_db(self):
        user_relation = self.db.getRelation('User')
        updated_data = {
            'username': self.username_entry.get(),
            'email': self.email_entry.get(),
            'password': self.password_entry.get(),
            'fName': self.fName_entry.get(),
            'lName': self.lName_entry.get(),
            'emergency_contact_email': self.emergency_email_entry.get(),
            'emergency_contact_name': self.emergency_name_entry.get(),
            'is_disabled': self.is_disabled_var.get()
        }
        
        try:
            for field, new_value in updated_data.items():
                if self.original_data[field] != new_value:
                    user_relation.editFieldInRow(self.user_id, field, new_value)

            messagebox.showinfo("Success", f"{self.user_type} information updated successfully.")
            return True
        
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False
        
        

    def delete_user(self):
        user_relation = self.db.getRelation('User')
        response = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete this {self.user_type}?")

        if response:
            self.db.delete_patient(patientId=self.user_id)
            messagebox.showinfo("Success", f"{self.user_type} deleted successfully.")
            
            self.parent.refresh_treeview()
            self.destroy()
            self.parent.deiconify()

    def go_back(self):
        self.parent.refresh_treeview()
        self.destroy()
        self.parent.deiconify()
        
    def on_close(self):
        self.db.close()
        self.destroy()

class MHWPEditApp(PatientEditApp):
    def __init__(self, user_id, parent, db):
        super().__init__(user_id, parent, db)

    def create_ui(self):
        self.title("Edit User Information")

        # H1 equivalent
        h1_label = tk.Label(self, text=f"Edit {self.user_type} Information", font=("Arial", 24, "bold"))
        h1_label.pack()

        user = self.fetch_user_details(self.user_id)
        self.original_data = user

        # Create labels and entry fields
        user_frame = tk.Frame(self)
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

        tk.Label(user_frame, text="Emergency Contact Name:").grid(row=7, column=0)
        self.emergency_name_entry = tk.Entry(user_frame)
        self.emergency_name_entry.insert(0, user['emergency_contact_name'] if user['emergency_contact_name'] else '')
        self.emergency_name_entry.config(state='disabled')
        self.emergency_name_entry.grid(row=7, column=1)

        # to speak to Tim about the hypenated ones which were causing an error.
        specialization_options = [
            "Psychology",
            "Psychiatry",
            "Counseling",
            "Substance Abuse Counseling",
            "Clinical Psychology",
            "Child and Adolescent Psychology",
            "Geriatric Psychology",
            "Neuropsychology",
            "Health Psychology",
            "Rehabilitation Counseling",
            "Art Therapy",
            "Music Therapy",
            "Behavioral Therapy",
            "Cognitive Behavioral Therapy",
            "Dialectical Behavior Therapy",
            "Play Therapy",
            "Hypnotherapy",
            "Psychodynamic Therapy",
            "Existential Therapy",
            "Humanistic Therapy",
            "Integrative Therapy",
            "Narrative Therapy",
            "Gestalt Therapy",
            "Acceptance and Commitment Therapy",
            "Eye Movement Desensitization and Reprocessing"
        ]
        tk.Label(user_frame, text="Specialization:").grid(row=8, column=0)
        self.specialization_var = tk.StringVar(value=user['specialization'] if user['specialization'] else specialization_options[0])
        self.specialization_combobox = ttk.Combobox(user_frame, textvariable=self.specialization_var, values=specialization_options, state='disabled')
        self.specialization_combobox.grid(row=8, column=1)

        tk.Label(user_frame, text="Disable User:").grid(row=10, column=0)
        self.is_disabled_var = tk.BooleanVar(value=bool(user['is_disabled']))
        self.is_disabled_check = tk.Checkbutton(user_frame, variable=self.is_disabled_var)
        self.is_disabled_check.config(state='disabled')
        self.is_disabled_check.grid(row=10, column=1)

        # Toggle Edit/Save Button
        self.toggle_button = tk.Button(self, text="Edit", command=self.toggle_edit_save)
        self.toggle_button.pack(pady=0)

        # Delete Button
        self.delete_button = tk.Button(self, text=f"Delete {self.user_type}", command=self.delete_MHWP)
        self.delete_button.pack(pady=0)

        # Back Button
        self.back_button = tk.Button(self, text="Back", command=self.go_back)
        self.back_button.pack(pady=0)

    def fetch_user_details(self, user_id):
        user_relation = self.db.getRelation('User')
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
                'emergency_contact_name': user_data[8],
                'specialization': user_data[9],
                'is_disabled': user_data[10]
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
            self.emergency_name_entry.config(state='normal')
            self.specialization_combobox.config(state='readonly')
            self.is_disabled_check.config(state='normal')

            self.toggle_button.config(text="Save Changes")  
        
        else:
            success = self.save_changes_to_db()
            if success:
                self.toggle_button.config(text="Edit")

                # disable fields again after saving
                self.username_entry.config(state='disabled')
                self.email_entry.config(state='disabled')
                self.password_entry.config(state='disabled')
                self.fName_entry.config(state='disabled')
                self.lName_entry.config(state='disabled')
                self.emergency_email_entry.config(state='disabled')
                self.emergency_name_entry.config(state='disabled')
                self.specialization_combobox.config(state='disabled')
                self.is_disabled_check.config(state='disabled')
            else:
                pass

            updated_data = {
                'username': self.username_entry.get(),
                'email': self.email_entry.get(),
                'password': self.password_entry.get(),
                'fName': self.fName_entry.get(),
                'lName': self.lName_entry.get(),
                'emergency_contact_email': self.emergency_email_entry.get(),
                'emergency_contact_name': self.emergency_name_entry.get(),
                'specialization': self.specialization_var.get(),
                'is_disabled': self.is_disabled_var.get()
            }

    def save_changes_to_db(self):
        user_relation = self.db.getRelation('User')
        updated_data = {
            'username': self.username_entry.get(),
            'email': self.email_entry.get(),
            'password': self.password_entry.get(),
            'fName': self.fName_entry.get(),
            'lName': self.lName_entry.get(),
            'emergency_contact_email': self.emergency_email_entry.get(),
            'emergency_contact_name': self.emergency_name_entry.get(),
            'specialization': self.specialization_var.get(),
            'is_disabled': self.is_disabled_var.get()
        }
        
        try:
            for field, new_value in updated_data.items():
                if self.original_data[field] != new_value:
                    user_relation.editFieldInRow(self.user_id, field, new_value)
        
            messagebox.showinfo("Success", f"{self.user_type} information updated successfully.")
            return True
        
        except Exception as e:
            messagebox.showerror("Error", str(e)) 
            return False
    
    def delete_MHWP(self):
        user_relation = self.db.getRelation('User')
        response = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete this MHWP?")

        if response:
            user_relation.deleteRow(self.user_id, self.db)
            messagebox.showinfo("Success", "MWHP deleted successfully.")
            
            self.parent.refresh_treeview()
            self.destroy()
            self.parent.deiconify()

class UserSelectionApp(tk.Toplevel):
    def __init__(self, user_type, parent):
        super().__init__()
        self.db = Database()
        self.geometry("400x350")
        self.resizable(True, False)
        self.user_type = user_type
        self.parent = parent
        self.selected_user_id = None
        self.users = self.db.getRelation('User').getRowsWhereEqual("type", user_type)
        self.create_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_ui(self):
        self.title(f"Select {self.user_type}")

        # H1 equivalent
        h1_label = tk.Label(self, text=f"Edit {self.user_type}", font=("Arial", 22, "bold"))
        h1_label.pack()
        
        # instruction label
        doc_to_user = tk.Label(self, text=f"Choose the {self.user_type} to edit:", font=("Arial", 12, "bold"))
        doc_to_user.pack()

        # treeview frame
        tree_frame = tk.Frame(self)
        tree_frame.pack(pady=10, fill="both", expand=True)

        # create a scrollbar for the tree view
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")

        # create a treeview widget for displaying users
        self.tree = ttk.Treeview(tree_frame, yscrollcommand=scrollbar.set, selectmode="browse")
        self.tree.pack(fill="both", expand=True)

        # connect the scrollbar to the tree view
        scrollbar.config(command=self.tree.yview)

        # define the columns for the tree view
        self.tree["columns"] = ("ID", "First Name", "Last Name")

        # define the width and alignment for each column
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("ID", anchor=tk.CENTER, width=50)
        self.tree.column("First Name", anchor=tk.CENTER, width=150)
        self.tree.column("Last Name", anchor=tk.CENTER, width=150)

        # set the heading for each column
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("ID", text="ID", anchor=tk.W)
        self.tree.heading("First Name", text="First Name", anchor=tk.W)
        self.tree.heading("Last Name", text="Last Name", anchor=tk.W)

        # creating checkbox for each patient
        for user in self.users:
            self.tree.insert("", "end", values=(user[0], user[4], user[5]))

        # select button 
        select_button = tk.Button(self, text=f"Select {self.user_type}", command=self.edit_user)  
        select_button.pack(pady=0)

        # back button
        self.back_button = tk.Button(self, text="Back", command=self.go_back)
        self.back_button.pack(pady=0)

    def refresh_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.users = self.db.getRelation('User').getRowsWhereEqual('type', self.user_type)

        for user in self.users:
            self.tree.insert("", "end", values=(user[0], user[4], user[5]))

    def edit_user(self):
        selected_item = self.tree.selection()
        if selected_item:
            self.selected_user_id = int(self.tree.item(selected_item, "values")[0])
            self.withdraw()
            if self.user_type == "Patient":
                app = PatientEditApp(self.selected_user_id, self, db=self.db)
            else:
                app = MHWPEditApp(self.selected_user_id, self, db=self.db)
        else:
            messagebox.showinfo(f"No {self.user_type} Selected", f"Please select a {self.user_type} to continue.")

    def go_back(self): 
        self.db.close()
        self.destroy()
        self.parent.deiconify()

    def on_close(self):
        self.db.close()
        self.destroy()

class AllocationSelection(UserSelectionApp):
    def __init__(self, user_type, parent):
        super().__init__(user_type, parent)

    def refresh_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.users = self.db.getRelation('User').getRowsWhereEqual('type', self.user_type)

        for user in self.users:
            patient_id = user[0]
            patient_name = f"{user[4]} {user[5]}"

            mhwp_allocation = self.db.getRelation('Allocation').getRowsWhereEqual("patient_id", patient_id)
            mhwp_allocation_id = mhwp_allocation[0][3] if mhwp_allocation else None

            if mhwp_allocation_id:
                assigned_mhwp = self.db.getRelation('User').getRowsWhereEqual("user_id", mhwp_allocation_id)
                assigned_mhwp_name = f"{assigned_mhwp[0][4]} {assigned_mhwp[0][5]}"
                print(assigned_mhwp_name)
            else:
                assigned_mhwp_name = "Unassigned"

            self.tree.insert("", "end", values=(user[0], patient_name, assigned_mhwp_name))

    def edit_user(self):
        selected_item = self.tree.selection()
        if selected_item:
            self.selected_user_id = int(self.tree.item(selected_item, "values")[0])
            self.withdraw()
            app = AllocationEdit(self.selected_user_id, self, db=self.db)
        else:
            messagebox.showinfo("No Patient Selected", "Please select a patient to continue.")

    def create_ui(self):
        self.title(f"Select {self.user_type}")

        # H1 equivalent
        h1_label = tk.Label(self, text="Patient Allocations", font=("Arial", 22, "bold"))
        h1_label.pack()
        
        # instruction label
        doc_to_user = tk.Label(self, text=f"Choose the Patient to edit:", font=("Arial", 12, "bold"))
        doc_to_user.pack()

        # treeview frame
        tree_frame = tk.Frame(self)
        tree_frame.pack(pady=10, fill="both", expand=True)

        # create a scrollbar for tree view
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")

        # create a treeview widget for displaying users
        self.tree = ttk.Treeview(tree_frame, yscrollcommand=scrollbar.set, selectmode="browse")
        self.tree.pack(fill="both", expand=True)

        # connect the scrollbar to the tree view
        scrollbar.config(command=self.tree.yview)

        # define the column for the tree view
        self.tree["columns"] = ("ID", "Patient Name", "Assigned MHWP")

        # define the width and alignment for each column
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("ID", anchor=tk.CENTER, width=50)
        self.tree.column("Patient Name", anchor=tk.CENTER, width=150)
        self.tree.column("Assigned MHWP", anchor=tk.CENTER, width=200)

        # set the heading for each column
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("ID", text="ID", anchor=tk.W)
        self.tree.heading("Patient Name", text="Patient Name", anchor=tk.W)
        self.tree.heading("Assigned MHWP", text="Assigned MHWP", anchor=tk.W)

        # creating checkbox for each patient
        for user in self.users:
            patient_id = user[0]
            patient_name = f"{user[4]} {user[5]}"

            mhwp_allocation = self.db.getRelation('Allocation').getRowsWhereEqual("patient_id", patient_id)
            if mhwp_allocation and len(mhwp_allocation) > 0:
                mhwp_allocation_id = mhwp_allocation[0][3]
            else:
                mhwp_allocation_id = None

            if mhwp_allocation_id:
                assigned_mhwp = self.db.getRelation('User').getRowsWhereEqual("user_id", mhwp_allocation_id)
                assigned_mhwp_name = f"{assigned_mhwp[0][4]} {assigned_mhwp[0][5]}"
            else:
                assigned_mhwp_name = "Unassigned"

            # insert user and their assigned MHWP into treeview
            self.tree.insert("", "end", values=(user[0], patient_name, assigned_mhwp_name))

        # select button 
        select_button = tk.Button(self, text=f"Select {self.user_type}", command=self.edit_user)  
        select_button.pack()

        # back button
        self.back_button = tk.Button(self, text="Back", command=self.go_back)
        self.back_button.pack(pady=0)

class KeyStatistics(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.db = Database()
        self.parent = parent
        self.mhwps = self.db.getRelation('User').getRowsWhereEqual('type', 'MHWP')
        self.total_appointments = {}
        self.calculations()
        self.create_ui()

    def calculations(self):
        self.total_appointments = {}
        for row in self.mhwps:
            user_id = row[0]
            mhwp_appointments = self.db.getRelation('Appointment').getRowsWhereEqual('mhwp_id', user_id)
            
            mhwp_user = self.db.getRelation('User').getRowsWhereEqual("user_id", user_id)
            mhwp_name = f"{mhwp_user[0][4]} {mhwp_user[0][5]}"

            self.total_appointments.update({mhwp_name : mhwp_appointments})

        # calculate allocation counts per MHWP
        mhwp_counts = {}
        allocations = self.db.getRelation('Allocation').getAllRows() 
        for alloc in allocations:
            mhwp_id = alloc.getField('mhwp_id')
            if mhwp_id and mhwp_id != "":
                # Get MHWP name
                mhwp_user = self.db.getRelation('User').getRowsWhereEqual("user_id", mhwp_id)
                if mhwp_user:
                    mhwp_name = f"{mhwp_user[0][4]} {mhwp_user[0][5]}"
                    mhwp_counts[mhwp_name] = mhwp_counts.get(mhwp_name, 0) + 1

        self.allocation_counts = mhwp_counts
    
    def create_ui(self):
        
        self.title("Bar Chart with Tkinter Canvas")

        # Create a Canvas widget
        canvas = tk.Canvas(self, width=1050, height=550)
        canvas.pack()

        # Graph title
        canvas.create_text(300, 22, text="Total Appointments per MHWP", font=("Arial", 16, "bold"))

        # Data for the bar chart (categories and values)
        categories = list(self.total_appointments)
        no_items = len(categories)

        values = []
        for elements in categories:
            length = len(self.total_appointments[elements])
            values.append(length)

        # Dimensions for the bar chart
        bar_width = (600/no_items) - (no_items * 30)
        bar_spacing = 20
        max_value = max(values)

        x_position = 60

        # Draw X and Y axes
        canvas.create_line(50, 350, 570, 350, width=1)
        canvas.create_line(50, 50, 50, 350, width=1)

        # Add Y-axis numbers
        for i in range(0, max_value + 1, max(1, max_value // 5)):
            y_position = 350 - (i / max_value) * 300
            canvas.create_text(40, y_position, text=str(i), anchor="e")
            
        # Loop through the data and draw bars
        for i, value in enumerate(values):
            bar_height = (value / max_value) * 300  # scale to a height of 300
            # Drawing the bars of the graph
            canvas.create_rectangle(x_position, 350 - bar_height, x_position + bar_width, 350, fill="skyblue")
            # Adding the category name below the bar
            canvas.create_text(x_position + bar_width / 2, 360, text=categories[i])
            # Update the X position for the next item
            x_position += bar_width + bar_spacing

        canvas.create_text(20, 190, text="Number of Appointments", angle=90, font=("Arial", 14))
        canvas.create_text(300, 380, text="MHWP", font=("Arial", 14))
        
        # calculating the number of patients
        patients = self.db.getRelation('User').getRowsWhereEqual('type', 'Patient')
        patient_row_count = len(patients)

        # calculating the number of MHWPs
        mhwps = self.db.getRelation('User').getRowsWhereEqual('type', 'MHWP')
        mhwp_row_count = len(mhwps)

        # calculating the number of patients per MHWPs
        patient_per_MHWP = round((patient_row_count / mhwp_row_count), 1)

        # calculating the number of disabled accounts
        disabled_accounts = self.db.getRelation('User').getRowsWhereEqual('is_disabled', True)
        disabled_accounts_row_count = len(disabled_accounts)

        # calculating the number of unalocated patients
        unalocated_patients = self.db.getRelation('Allocation').getRowsWhereEqual('mhwp_id', "")
        unalocated_patients_row_count = len(unalocated_patients)

        # calculating the number of journal entries
        journal_entries = self.db.getRelation('JournalEntry')
        no_journal_entries = len(journal_entries)

        # calculating the number of patient records
        patient_records = self.db.getRelation('PatientRecord')
        no_patient_records = len(patient_records)

        # calculating the number of active appointments
        active_appointments = self.db.getRelation('Appointment').getRowsWhereEqual('status', 'active')
        no_active_appointments = len(active_appointments)

        # calculating the number of confirmed appointments
        confirmed_appointments = self.db.getRelation('Appointment').getRowsWhereEqual('status', 'Confirmed')
        no_confirmed_appointments = len(confirmed_appointments)

        # calculating the number of declined appointments
        declined_appointments = self.db.getRelation('Appointment').getRowsWhereEqual('status', 'Declined')
        no_declined_appointments = len(declined_appointments)

        key_stats_x_position = 427
        key_stats_gap = 22

        # Create the summary of key statistics on the canvas
        canvas.create_text(527, (key_stats_x_position - 10), text="Key Statistics", font=("Arial", 16, "bold"))
        canvas.create_text(402, (key_stats_x_position + key_stats_gap * 1), text=f"No. Patients: {patient_row_count}", font=("Arial", 14))
        canvas.create_text(402, (key_stats_x_position + key_stats_gap * 2), text=f"No. MHWP: {mhwp_row_count}", font=("Arial", 14))
        canvas.create_text(402, (key_stats_x_position + key_stats_gap * 3), text=f"Patients Per MHWP: {patient_per_MHWP}", font=("Arial", 14))
        canvas.create_text(402, (key_stats_x_position + key_stats_gap * 4), text=f"Disabled Accounts: {disabled_accounts_row_count}", font=("Arial", 14))
        canvas.create_text(402, (key_stats_x_position + key_stats_gap * 5), text=f"Unallocated Patients: {unalocated_patients_row_count}", font=("Arial", 14))
        canvas.create_text(652, (key_stats_x_position + key_stats_gap * 1), text=f"No. Journal Entries: {no_journal_entries}", font=("Arial", 14))
        canvas.create_text(652, (key_stats_x_position + key_stats_gap * 2), text=f"No. Patient Records: {no_patient_records}", font=("Arial", 14))
        canvas.create_text(652, (key_stats_x_position + key_stats_gap * 3), text=f"Active Appointments: {no_active_appointments}", font=("Arial", 14))
        canvas.create_text(652, (key_stats_x_position + key_stats_gap * 4), text=f"Confirmed Appointments: {no_confirmed_appointments}", font=("Arial", 14))
        canvas.create_text(652, (key_stats_x_position + key_stats_gap * 5), text=f"Declined Appointments: {no_declined_appointments}", font=("Arial", 14))

        # draw the pie chart
        self.draw_pie_chart(canvas, x_center=780, y_center=205, radius=100)

        # Back button
        back_button = tk.Button(self, text="Back", command=self.go_back)
        back_button.pack(pady=5)

    def draw_pie_chart(self, canvas, x_center, y_center, radius):

        canvas.create_text(x_center + 55, y_center - radius - 85, text="Patients per MHWP", font=("Arial", 16, "bold"))

        colors = ["lightgreen", "lavender", "mistyrose", "palegreen", "lightpink", "lightblue", "peachpuff", "thistle", "honeydew", "powderblue", "mintcream", "lemonchiffon", "cornsilk", "skyblue", "plum1"]
        color_index = 0

        start_angle = 0

        data = self.allocation_counts
        total = sum(data.values()) if data else 1
        
        legend_x = x_center + radius + 50  # Position of the legend
        legend_y = y_center - radius  # Top position of the legend

        for mhwp_name, count in data.items():
            # Calculate the angle of each slice
            extent_angle = (count / total) * 360

            # Draw the arc
            fill_color = colors[color_index % len(colors)]
            canvas.create_arc(
                x_center - radius, y_center - radius, 
                x_center + radius, y_center + radius,
                start=start_angle, extent=extent_angle, 
                fill=fill_color)

            # Update start angle for next slice
            start_angle += extent_angle
            color_index += 1

        # Draw Legend
        color_index = 0
        for mhwp_name, count in data.items():
            fill_color = colors[color_index % len(colors)]

            # Draw legend color box
            canvas.create_rectangle(
                legend_x, legend_y + (color_index * 20),
                legend_x + 20, legend_y + (color_index * 20) + 15,
                fill=fill_color
            )

            # Add text for the legend
            canvas.create_text(
                legend_x + 30, legend_y + (color_index * 20) + 7,
                text=f"{mhwp_name} ({count})",
                font=("Arial", 10),
                anchor="w"
            )
            color_index += 1

        # If no data, draw a message
        if not data:
            canvas.create_text(x_center, y_center, text="No Allocations Found", font=("Arial", 12))


    def go_back(self): 
        self.destroy()
        self.parent.deiconify()

class AdminMainPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.title("Admin Dashboard")
        self.geometry("310x300")
        self.create_ui()

    def create_ui(self):
        
        # H1 equivalent
        h1_label = tk.Label(text="Admin Dashboard", font=("Arial", 24, "bold"))
        h1_label.pack(pady=10)

        # Quick Actions Section
        quick_actions_label = tk.Label(text="Actions", font=("Arial", 14, "bold"))
        quick_actions_label.pack(pady=10)

        tk.Button(text="Patients Allocations", command=self.patient_allocations, width=20
        ).pack(pady=5)

        tk.Button(text="Edit Patients", command=self.edit_patient_info, width=20
        ).pack(pady=5)

        tk.Button(text="Edit MHWPs", command=self.edit_MHWP_info, width=20
        ).pack(pady=5)

        tk.Button(text="Key Statistics", command=self.key_stats, width=20
        ).pack(pady=5)

        tk.Button(text="Log Out", command=self.log_out, width=20
        ).pack(pady=5)

    def patient_allocations(self):
        self.withdraw()
        app = AllocationSelection("Patient", self)

    def edit_patient_info(self):
        self.withdraw()
        app = UserSelectionApp("Patient", self)

    def edit_MHWP_info(self):
        self.withdraw()
        app = UserSelectionApp("MHWP", self)

    def key_stats(self):
        self.withdraw()
        app = KeyStatistics(self)

    def log_out(self):
        from main import App
        self.destroy()
        app = App()

if __name__ == "__main__":
    
    ## open session
    sess = Session()
    sess.open()

    ## get id and role from session
    userId = sess.getId()
    userRole = sess.getRole()

    ## get any other details
    isDisabled = sess.get("isDisabled")

    if userRole == "Admin" and isDisabled == False:
        app = AdminMainPage()
        app.mainloop()
    else:
        root = tk.Tk()
        app = LoginPage(root)
        root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sessions import Session
from database.database import Database
from database.entities import User, Admin, Patient, MHWP, Allocation, Appointment

from addfeature.globaldb import global_db
db = global_db

class AllocationEdit(tk.Toplevel):
    """
    Window for changing the allocated MWHP assigned to the patient. 
    """

    def __init__(self, patient_id, parent, db):
        super().__init__()
        self.db = db
        self.patient_id = patient_id
        self.parent = parent

        # Open session and get admin ID
        self.sess = Session()
        self.sess.open()
        self.adminID = self.sess.getId()

        self.create_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_ui(self):
        self.title("Edit MHWP Assignment")

        h1_label = tk.Label(self, text="Assign MHWP to Patient", font=("Arial", 24, "bold"))
        h1_label.pack()

        # Fetch the current MHWP assigned to the patient
        patient_allocation = self.db.getRelation('Allocation').getRowsWhereEqual("patient_id", self.patient_id)
        if not patient_allocation:
            newPatient = self.db.getRelation('User').getRowsWhereEqual("user_id", self.patient_id)
            if not newPatient:
                messagebox.showerror("Error", "No patient found with the provided ID.")
            else:
                self.patientIsNewlyCreated = True
        else:
            self.patientIsNewlyCreated = False

        # Retrieve the MHWPs name assigned to the patient
        if not self.patientIsNewlyCreated:
            assigned_mhwp_id = patient_allocation[0][Allocation.MHWP_ID]
            self.allocation_id = patient_allocation[0][Allocation.ALLOCATION_ID]
            assigned_mhwp = self.db.getRelation('User').getRowsWhereEqual("user_id", assigned_mhwp_id)
            assigned_mhwp_name = f"{assigned_mhwp[0][User.FNAME]} {assigned_mhwp[0][User.LNAME]}"
        else:
            assigned_mhwp_name = "No MHWP assigned yet."
            self.new_user_id = newPatient[0][User.USER_ID]

        # Fetch list of all MHWPs
        mhwps = self.db.getRelation('User').getRowsWhereEqual("type", "MHWP")
        self.mhwp_dict = {f"{mhwp[User.FNAME]} {mhwp[User.LNAME]}": mhwp[0] for mhwp in mhwps}
        mhwp_names = list(self.mhwp_dict.keys())

        tk.Label(self, text="Select New MHWP:").pack(pady=10)
        self.mhwp_var = tk.StringVar(value=assigned_mhwp_name)
        self.mhwp_dropdown = tk.OptionMenu(self, self.mhwp_var, *mhwp_names)
        self.mhwp_dropdown.pack(pady=10)

        save_button = tk.Button(self, text="Save", command=self.save_mhwp)
        save_button.pack(pady=0)
        self.back_button = tk.Button(self, text="Back", command=self.go_back)
        self.back_button.pack(pady=0)

    # Update MHWP allocated to the patient or if there is no assignment create a new allocation
    def save_mhwp(self):
        new_mhwp_name = self.mhwp_var.get()
        new_mhwp_id = self.mhwp_dict.get(new_mhwp_name)

        try:
            if not self.patientIsNewlyCreated:
                userRelation = self.db.getRelation('Allocation')
                userRelation.editFieldInRow(self.allocation_id, 'mhwp_id', new_mhwp_id)
                messagebox.showinfo("Success", "MHWP updated successfully.")
            else:
                allocation = Allocation(
                    admin_id=self.adminID,
                    patient_id=self.new_user_id,
                    mhwp_id=new_mhwp_id,
                    start_date=datetime.now(),
                    end_date=datetime.now().replace(year=datetime.now().year + 1)
                )
                self.db.insert_allocation(allocation)
                messagebox.showinfo("Success", "MHWP allocated successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def go_back(self):
        self.destroy()
        self.parent.refresh_treeview()
        self.parent.deiconify()

    def on_close(self):
        self.destroy()
        
class PatientEditApp(tk.Toplevel):
    """
    Window for allowing the admin to edit, delete or disable a patient.
    """
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

        h1_label = tk.Label(self, text=f"Edit {self.user_type} Information", font=("Arial", 24, "bold"))
        h1_label.pack()

        user = self.fetch_user_details(self.user_id)
        self.original_data = user

        user_frame = tk.Frame(self)
        user_frame.pack(fill='x', padx=10, pady=5)

        # A number of data integrity have been included by the database including: 
        # only allowing email addresses in the correct format to be entered, limiting the characters which can entered into the name field
        # and requiring a minimum length of password.
        # The section below creates entry fields for each of the user's details.

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
        self.is_disabled_var = tk.BooleanVar(value=bool(user['is_disabled']))  # BooleanVar for checkbox state
        self.is_disabled_check = tk.Checkbutton(user_frame, variable=self.is_disabled_var)
        self.is_disabled_check.config(state='disabled')
        self.is_disabled_check.grid(row=10, column=1)

        self.toggle_button = tk.Button(self, text="Edit", command=self.toggle_edit_save)
        self.toggle_button.pack(pady=0)

        self.delete_button = tk.Button(self, text=f"Delete {self.user_type}", command=self.delete_user)
        self.delete_button.pack(pady=0)

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
                self.username_entry.config(state='disabled')
                self.email_entry.config(state='disabled')
                self.password_entry.config(state='disabled')
                self.fName_entry.config(state='disabled')
                self.lName_entry.config(state='disabled')
                self.emergency_email_entry.config(state='disabled')
                self.emergency_name_entry.config(state='disabled')
                self.is_disabled_check.config(state='disabled')

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

        # Update fields in database where the admin has made changes to the user's details
        # Return an exception if there is an error
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

        # Propogation of deletes have been included by the database so when a patient is removed all of their associated data is also 
        # removed including their appointment bookings.

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

# This class inherits from the PatientEditApp and is very similar
# except with a couple of custom fields specifically for the MHWP including 'specialization'.
class MHWPEditApp(PatientEditApp):
    """
    Window for allowing the admin to edit, disable or delete the MHWP. 
    """
    def __init__(self, user_id, parent, db):
        super().__init__(user_id, parent, db)

    def create_ui(self):

        self.title("Edit User Information")

        h1_label = tk.Label(self, text=f"Edit {self.user_type} Information", font=("Arial", 24, "bold"))
        h1_label.pack()

        user = self.fetch_user_details(self.user_id)
        self.original_data = user

        user_frame = tk.Frame(self)
        user_frame.pack(fill='x', padx=10, pady=5)

        # A number of data integrity have been included by the database including: 
        # only allowing email addresses in the correct format to be entered, limiting the characters which can entered into the name field
        # and requiring a minimum length of password.
        # The section below creates entry fields for each of the user's details.
        
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

        specialization_options = [
            "Psychology", "Psychiatry", "Counseling", "Substance Abuse Counseling",
            "Clinical Psychology", "Child and Adolescent Psychology", "Geriatric Psychology",
            "Neuropsychology", "Health Psychology", "Rehabilitation Counseling",
            "Art Therapy", "Music Therapy", "Behavioral Therapy", "Cognitive Behavioral Therapy",
            "Dialectical Behavior Therapy", "Play Therapy", "Hypnotherapy",
            "Psychodynamic Therapy", "Existential Therapy", "Humanistic Therapy",
            "Integrative Therapy", "Narrative Therapy", "Gestalt Therapy",
            "Acceptance and Commitment Therapy", "Eye Movement Desensitization and Reprocessing"
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

        self.toggle_button = tk.Button(self, text="Edit", command=self.toggle_edit_save)
        self.toggle_button.pack(pady=0)

        self.delete_button = tk.Button(self, text=f"Delete {self.user_type}", command=self.delete_MHWP)
        self.delete_button.pack(pady=0)

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
            # If save has been successful revert fields to view-only
            success = self.save_changes_to_db()
            if success:
                self.toggle_button.config(text="Edit")
                self.username_entry.config(state='disabled')
                self.email_entry.config(state='disabled')
                self.password_entry.config(state='disabled')
                self.fName_entry.config(state='disabled')
                self.lName_entry.config(state='disabled')
                self.emergency_email_entry.config(state='disabled')
                self.emergency_name_entry.config(state='disabled')
                self.specialization_combobox.config(state='disabled')
                self.is_disabled_check.config(state='disabled')

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
            # Update only changed fields to the database
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
    """
    Window for allowing the admin to select a user to edit.
    """
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

        h1_label = tk.Label(self, text=f"Edit {self.user_type}", font=("Arial", 22, "bold"))
        h1_label.pack()

        doc_to_user = tk.Label(self, text=f"Choose the {self.user_type} to edit:", font=("Arial", 12, "bold"))
        doc_to_user.pack()

        tree_frame = tk.Frame(self)
        tree_frame.pack(pady=10, fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")

        self.tree = ttk.Treeview(tree_frame, yscrollcommand=scrollbar.set, selectmode="browse")
        self.tree.pack(fill="both", expand=True)

        scrollbar.config(command=self.tree.yview)

        self.tree["columns"] = ("ID", "First Name", "Last Name")
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("ID", anchor=tk.CENTER, width=50)
        self.tree.column("First Name", anchor=tk.CENTER, width=150)
        self.tree.column("Last Name", anchor=tk.CENTER, width=150)

        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("ID", text="ID", anchor=tk.W)
        self.tree.heading("First Name", text="First Name", anchor=tk.W)
        self.tree.heading("Last Name", text="Last Name", anchor=tk.W)

        # Populate the tree view with users from the database
        for user in self.users:
            self.tree.insert("", "end", values=(user[0], user[4], user[5]))

        select_button = tk.Button(self, text=f"Select {self.user_type}", command=self.edit_user)
        select_button.pack(pady=0)

        self.back_button = tk.Button(self, text="Back", command=self.go_back)
        self.back_button.pack(pady=0)

    # Clear the tree view and reload users, this allows the tree view to update when you press back from the edit window
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
            # direct the admin to the correct edit window depending on the user type i.e Patient or MHWP.
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
    """
    Window allowing the admin to select a patient to edit their allocated MHWP.
    """
    def __init__(self, user_type, parent):
        super().__init__(user_type, parent)

    # Clear the tree view and reload users, this allows the tree view to update when you press back from the edit allocation window
    def refresh_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.users = self.db.getRelation('User').getRowsWhereEqual('type', self.user_type)

        for user in self.users:
            patient_id = user[0]
            patient_name = f"{user[4]} {user[5]}"  

            # Retrieve the patient's MHWP assignment
            mhwp_allocation = self.db.getRelation('Allocation').getRowsWhereEqual("patient_id", patient_id)
            mhwp_allocation_id = mhwp_allocation[0][3] if mhwp_allocation else None

            # Fetch the assigned MHWP's name from the database, else label them as unassigned.
            if mhwp_allocation_id:
                assigned_mhwp = self.db.getRelation('User').getRowsWhereEqual("user_id", mhwp_allocation_id)
                assigned_mhwp_name = f"{assigned_mhwp[0][4]} {assigned_mhwp[0][5]}"
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

        h1_label = tk.Label(self, text="Patient Allocations", font=("Arial", 22, "bold"))
        h1_label.pack()

        doc_to_user = tk.Label(self, text=f"Choose the Patient to edit:", font=("Arial", 12, "bold"))
        doc_to_user.pack()

        tree_frame = tk.Frame(self)
        tree_frame.pack(pady=10, fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")

        self.tree = ttk.Treeview(tree_frame, yscrollcommand=scrollbar.set, selectmode="browse")
        self.tree.pack(fill="both", expand=True)

        scrollbar.config(command=self.tree.yview)

        self.tree["columns"] = ("ID", "Patient Name", "Assigned MHWP")
        self.tree.column("#0", width=0, stretch=tk.NO)  # Hide the default column
        self.tree.column("ID", anchor=tk.CENTER, width=50)
        self.tree.column("Patient Name", anchor=tk.CENTER, width=150)
        self.tree.column("Assigned MHWP", anchor=tk.CENTER, width=200)

        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("ID", text="ID", anchor=tk.W)
        self.tree.heading("Patient Name", text="Patient Name", anchor=tk.W)
        self.tree.heading("Assigned MHWP", text="Assigned MHWP", anchor=tk.W)

        # Populate the tree view with patients name and the name of their assigned MHWP
        for user in self.users:
            patient_id = user[0]
            patient_name = f"{user[4]} {user[5]}"

            # Retrieve the MHWP assignment for the patient from the 'Allocation' table
            mhwp_allocation = self.db.getRelation('Allocation').getRowsWhereEqual("patient_id", patient_id)
            if mhwp_allocation and len(mhwp_allocation) > 0:
                mhwp_allocation_id = mhwp_allocation[0][3]
            else:
                mhwp_allocation_id = None

            # Fetch the assigned MHWP's name from the 'User' table
            if mhwp_allocation_id:
                assigned_mhwp = self.db.getRelation('User').getRowsWhereEqual("user_id", mhwp_allocation_id)
                assigned_mhwp_name = f"{assigned_mhwp[0][4]} {assigned_mhwp[0][5]}"
            else:
                assigned_mhwp_name = "Unassigned"  

            # Insert details into the tree view
            self.tree.insert("", "end", values=(user[0], patient_name, assigned_mhwp_name))

        select_button = tk.Button(self, text=f"Select {self.user_type}", command=self.edit_user)
        select_button.pack()

        self.back_button = tk.Button(self, text="Back", command=self.go_back)
        self.back_button.pack(pady=0)

class KeyStatistics(tk.Toplevel):
    """
    Window showing an overview of useful key statistics for the admin user.
    """
    def __init__(self, parent):
        super().__init__()
        self.db = Database()  
        self.parent = parent  
        self.mhwps = self.db.getRelation('User').getRowsWhereEqual('type', 'MHWP')  
        self.total_appointments = {}  
        self.calculations()  
        self.create_ui()  

    def calculations(self):
        
        # Calculate total appointments per MHWP
        self.total_appointments = {}
        for row in self.mhwps:
            user_id = row[0]
            mhwp_appointments = self.db.getRelation('Appointment').getRowsWhereEqual('mhwp_id', user_id)
            
            mhwp_user = self.db.getRelation('User').getRowsWhereEqual("user_id", user_id)
            mhwp_name = f"{mhwp_user[0][4]} {mhwp_user[0][5]}"  # Get MHWP name

            self.total_appointments.update({mhwp_name: mhwp_appointments})

        # Calculate number of allocations per MHWP
        mhwp_counts = {}
        allocations = self.db.getRelation('Allocation').getAllRows()
        for alloc in allocations:
            mhwp_id = alloc.getField('mhwp_id')
            if mhwp_id and mhwp_id != "":
                mhwp_user = self.db.getRelation('User').getRowsWhereEqual("user_id", mhwp_id)
                if mhwp_user:
                    mhwp_name = f"{mhwp_user[0][4]} {mhwp_user[0][5]}"
                    mhwp_counts[mhwp_name] = mhwp_counts.get(mhwp_name, 0) + 1

        self.allocation_counts = mhwp_counts  

    def create_ui(self):
        self.title("Admin Key Statistics")

        canvas = tk.Canvas(self, width=1050, height=550)
        canvas.pack()

        canvas.create_text(300, 22, text="Total Appointments per MHWP", font=("Arial", 16, "bold"))

        categories = list(self.total_appointments)
        values = [len(self.total_appointments[cat]) for cat in categories]
        max_value = max(values) if values else 1 

        # Set the dimensions and layout of the bar chart
        canvas_width = 520
        bar_spacing = 20
        bar_width = max(10, (canvas_width - bar_spacing * (len(categories) - 1)) / len(categories))  
        x_position = 60  # Set the initial X position for the bar chart

        # Bar chart axis
        canvas.create_line(50, 350, 570, 350, width=1)  
        canvas.create_line(50, 50, 50, 350, width=1) 

        # Y-axis labels
        for i in range(0, max_value + 1, max(1, max_value // 5)):
            y_position = 350 - (i / max_value) * 300
            canvas.create_text(40, y_position, text=str(i), anchor="e")

        # Drawing the bars
        for i, value in enumerate(values):
            bar_height = (value / max_value) * 300  
            canvas.create_rectangle(
                x_position, 350 - bar_height, x_position + bar_width, 350, fill="skyblue"
            )
            canvas.create_text(x_position + bar_width / 2, 360, text=categories[i], anchor="center")
            # Increment position for next bar
            x_position += bar_width + bar_spacing  

        canvas.create_text(20, 190, text="Number of Appointments", angle=90, font=("Arial", 14))
        canvas.create_text(300, 380, text="MHWP", font=("Arial", 14))

        # Displaying key statistics retrieved from the database
        patients = len(self.db.getRelation('User').getRowsWhereEqual('type', 'Patient'))
        mhwps = len(self.db.getRelation('User').getRowsWhereEqual('type', 'MHWP'))
        patients_per_mhwp = round(patients / mhwps, 1) if mhwps > 0 else 0  
        stats = [
            f"No. Patients: {patients}",
            f"No. MHWP: {mhwps}",
            f"Patients Per MHWP: {patients_per_mhwp}",
            f"Disabled Accounts: {len(self.db.getRelation('User').getRowsWhereEqual('is_disabled', True))}",
            f"Unallocated Patients: {len(self.db.getRelation('Allocation').getRowsWhereEqual('mhwp_id', ''))}",
            f"No. Journal Entries: {len(self.db.getRelation('JournalEntry'))}",
            f"No. Patient Records: {len(self.db.getRelation('PatientRecord'))}",
            f"Pending Appointments: {len(self.db.getRelation('Appointment').getRowsWhereEqual('status', 'Pending'))}",
            f"Confirmed Appointments: {len(self.db.getRelation('Appointment').getRowsWhereEqual('status', 'Confirmed'))}",
            f"Cancelled Appointments: {len(self.db.getRelation('Appointment').getRowsWhereEqual('status', 'Cancelled'))}"
        ]

        key_stats_gap = 22
        for i, stat in enumerate(stats[:5]):
            canvas.create_text(402, 427 + key_stats_gap * i, text=stat, font=("Arial", 14))
        for i, stat in enumerate(stats[5:]):
            canvas.create_text(652, 427 + key_stats_gap * i, text=stat, font=("Arial", 14))

        # Draw a pie chart for patient allocation distribution
        self.draw_pie_chart(canvas, x_center=780, y_center=205, radius=100)

        back_button = tk.Button(self, text="Back", command=self.go_back)
        back_button.pack(pady=5)

    # Create a pie chart for patient allocations per MHWP
    def draw_pie_chart(self, canvas, x_center, y_center, radius):
        canvas.create_text(x_center + 55, y_center - radius - 85, text="Patients per MHWP", font=("Arial", 16, "bold"))

        colors = ["lightgreen", "lavender", "mistyrose", "palegreen", "lightpink", "lightblue", "peachpuff"]
        total = sum(self.allocation_counts.values()) if self.allocation_counts else 1  

        # Drawing the arcs of the pie chart
        start_angle = 0
        for i, (mhwp_name, count) in enumerate(self.allocation_counts.items()):
            extent_angle = (count / total) * 360
            fill_color = colors[i % len(colors)]
            canvas.create_arc(
                x_center - radius, y_center - radius, x_center + radius, y_center + radius,
                start=start_angle, extent=extent_angle, fill=fill_color
            )
            start_angle += extent_angle

        # Pie chart legend
        legend_x, legend_y = x_center + radius + 50, y_center - radius
        for i, (mhwp_name, count) in enumerate(self.allocation_counts.items()):
            canvas.create_rectangle(legend_x, legend_y + i * 20, legend_x + 20, legend_y + i * 20 + 15, fill=colors[i % len(colors)])
            canvas.create_text(legend_x + 30, legend_y + i * 20 + 7, text=f"{mhwp_name} ({count})", anchor="w", font=("Arial", 10))

        if not self.allocation_counts:
            canvas.create_text(x_center, y_center, text="No Allocations Found", font=("Arial", 12))

    def go_back(self):
        self.destroy()
        self.parent.deiconify()

class AdminMainPage(tk.Tk):
    """
    Main page for the admin allowing them to navigate to their key functionalities.
    """
    def __init__(self):
        super().__init__()
        self.db = Database()  
        self.title("Admin Dashboard") 
        self.geometry("310x300") 
        self.create_ui()  

    def create_ui(self):
        h1_label = tk.Label(text="Admin Dashboard", font=("Arial", 24, "bold"))
        h1_label.pack(pady=10)

        quick_actions_label = tk.Label(text="Actions", font=("Arial", 14, "bold"))
        quick_actions_label.pack(pady=10)

        tk.Button(text="Patients Allocations", command=self.patient_allocations, width=20).pack(pady=5)
        tk.Button(text="Edit Patients", command=self.edit_patient_info, width=20).pack(pady=5)
        tk.Button(text="Edit MHWPs", command=self.edit_MHWP_info, width=20).pack(pady=5)
        tk.Button(text="Key Statistics", command=self.key_stats, width=20).pack(pady=5)
        tk.Button(text="Log Out", command=self.log_out, width=20).pack(pady=5)

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
        from main import App
        app = App()


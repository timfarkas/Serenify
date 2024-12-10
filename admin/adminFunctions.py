import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os
import sys

# Adjust system path to access parent directory modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sessions import Session
from database.database import Database
from database.entities import User, Admin, Patient, MHWP, Allocation, Appointment

# Global database connection
from addfeature.globaldb import global_db
db = global_db

class AllocationEdit(tk.Toplevel):
    """
    Window for editing MHWP assignment to a patient.
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
        """Set up the UI for MHWP assignment."""
        self.title("Edit MHWP Assignment")

        # Header label
        h1_label = tk.Label(self, text="Assign MHWP to Patient", font=("Arial", 24, "bold"))
        h1_label.pack()

        # Fetch current MHWP allocation for the patient
        patient_allocation = self.db.getRelation('Allocation').getRowsWhereEqual("patient_id", self.patient_id)
        if not patient_allocation:
            newPatient = self.db.getRelation('User').getRowsWhereEqual("user_id", self.patient_id)
            if not newPatient:
                messagebox.showerror("Error", "No patient found with the provided ID.")
            else:
                self.patientIsNewlyCreated = True
        else:
            self.patientIsNewlyCreated = False

        # Set up the current assigned MHWP name
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

        # MHWP dropdown
        tk.Label(self, text="Select New MHWP:").pack(pady=10)
        self.mhwp_var = tk.StringVar(value=assigned_mhwp_name)
        self.mhwp_dropdown = tk.OptionMenu(self, self.mhwp_var, *mhwp_names)
        self.mhwp_dropdown.pack(pady=10)

        # Save and Back buttons
        save_button = tk.Button(self, text="Save", command=self.save_mhwp)
        save_button.pack(pady=0)
        self.back_button = tk.Button(self, text="Back", command=self.go_back)
        self.back_button.pack(pady=0)

    def save_mhwp(self):
        """Save the MHWP assignment to the database."""
        new_mhwp_name = self.mhwp_var.get()
        new_mhwp_id = self.mhwp_dict.get(new_mhwp_name)

        try:
            if not self.patientIsNewlyCreated:
                # Update existing MHWP allocation
                userRelation = self.db.getRelation('Allocation')
                userRelation.editFieldInRow(self.allocation_id, 'mhwp_id', new_mhwp_id)
                messagebox.showinfo("Success", "MHWP updated successfully.")
            else:
                # Create new allocation for the patient
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
        """Close the window and refresh parent view."""
        self.destroy()
        self.parent.refresh_treeview()
        self.parent.deiconify()

    def on_close(self):
        """Handle the window close event."""
        self.destroy()
        
class PatientEditApp(tk.Toplevel):
    def __init__(self, user_id, parent, db):
        # Initialize the Toplevel window and set attributes
        super(PatientEditApp, self).__init__()
        self.db = db  # Database instance
        self.parent = parent  # Parent window reference
        self.user_id = user_id  # ID of the user being edited
        self.user_type = self.db.getRelation('User').getRowsWhereEqual("user_id", user_id)[0][6]  # User type
        self.original_data = {}  # Store original user data for comparison
        self.create_ui()  # Create the user interface
        self.protocol("WM_DELETE_WINDOW", self.on_close)  # Handle window close event

    def create_ui(self):
        # Set up the window title
        self.title("Edit User Information")

        # Add a header label displaying the user type
        h1_label = tk.Label(self, text=f"Edit {self.user_type} Information", font=("Arial", 24, "bold"))
        h1_label.pack()

        # Fetch user details and save for later comparison
        user = self.fetch_user_details(self.user_id)
        self.original_data = user

        # Create a frame to organize the form layout
        user_frame = tk.Frame(self)
        user_frame.pack(fill='x', padx=10, pady=5)

        # Create entry fields for user details
        tk.Label(user_frame, text=f"User ID: {user['user_id']}", width=15).grid(row=0, column=0)
        tk.Label(user_frame, text="Username:").grid(row=1, column=0)
        self.username_entry = tk.Entry(user_frame)
        self.username_entry.insert(0, user['username'] if user['username'] else '')
        self.username_entry.config(state='disabled')  # Initially disabled
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

        # Button to toggle edit mode
        self.toggle_button = tk.Button(self, text="Edit", command=self.toggle_edit_save)
        self.toggle_button.pack(pady=0)

        # Button to delete the user
        self.delete_button = tk.Button(self, text=f"Delete {self.user_type}", command=self.delete_user)
        self.delete_button.pack(pady=0)

        # Button to return to the parent view
        self.back_button = tk.Button(self, text="Back", command=self.go_back)
        self.back_button.pack(pady=0)

    def fetch_user_details(self, user_id):
        # Fetch user details from the database
        user_relation = self.db.getRelation('User')
        user = user_relation.getRowsWhereEqual('user_id', user_id)

        if user:
            user_data = user[0]  # Extract the first matching record
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
        # Toggle between editing and saving user details
        if self.username_entry.cget('state') == 'disabled':  # Enable fields for editing
            self.username_entry.config(state='normal')
            self.email_entry.config(state='normal')
            self.password_entry.config(state='normal')
            self.fName_entry.config(state='normal')
            self.lName_entry.config(state='normal')
            self.emergency_email_entry.config(state='normal')
            self.emergency_name_entry.config(state='normal')
            self.is_disabled_check.config(state='normal')
            self.toggle_button.config(text="Save Changes")  # Change button text
        else:
            # Save changes to the database
            success = self.save_changes_to_db()
            if success:
                self.toggle_button.config(text="Edit")  # Change button text
                # Disable fields after saving
                self.username_entry.config(state='disabled')
                self.email_entry.config(state='disabled')
                self.password_entry.config(state='disabled')
                self.fName_entry.config(state='disabled')
                self.lName_entry.config(state='disabled')
                self.emergency_email_entry.config(state='disabled')
                self.emergency_name_entry.config(state='disabled')
                self.is_disabled_check.config(state='disabled')

    def save_changes_to_db(self):
        # Save updated user details to the database
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
            # Update fields where changes have been made
            for field, new_value in updated_data.items():
                if self.original_data[field] != new_value:
                    user_relation.editFieldInRow(self.user_id, field, new_value)

            messagebox.showinfo("Success", f"{self.user_type} information updated successfully.")
            return True
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False

    def delete_user(self):
        # Delete the user from the database
        user_relation = self.db.getRelation('User')
        response = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete this {self.user_type}?")

        if response:  # Proceed if user confirms
            self.db.delete_patient(patientId=self.user_id)
            messagebox.showinfo("Success", f"{self.user_type} deleted successfully.")
            self.parent.refresh_treeview()
            self.destroy()
            self.parent.deiconify()

    def go_back(self):
        # Return to the parent view
        self.parent.refresh_treeview()
        self.destroy()
        self.parent.deiconify()

    def on_close(self):
        # Handle window close event
        self.db.close()
        self.destroy()

class MHWPEditApp(PatientEditApp):
    def __init__(self, user_id, parent, db):
        # Initialize by inheriting attributes and methods from PatientEditApp
        super().__init__(user_id, parent, db)

    def create_ui(self):
        # Set window title
        self.title("Edit User Information")

        # Add a header label indicating the type of user being edited
        h1_label = tk.Label(self, text=f"Edit {self.user_type} Information", font=("Arial", 24, "bold"))
        h1_label.pack()

        # Fetch user details and store them for comparison
        user = self.fetch_user_details(self.user_id)
        self.original_data = user

        # Frame to organize user details form
        user_frame = tk.Frame(self)
        user_frame.pack(fill='x', padx=10, pady=5)

        # Create entry fields for user details (disabled by default)
        tk.Label(user_frame, text=f"User ID: {user['user_id']}", width=15).grid(row=0, column=0)
        tk.Label(user_frame, text="Username:").grid(row=1, column=0)
        self.username_entry = tk.Entry(user_frame)
        self.username_entry.insert(0, user['username'] if user['username'] else '')
        self.username_entry.config(state='disabled')  # Disabled for view-only mode
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

        # Dropdown for specialization options (disabled by default)
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

        # Buttons for editing, deleting, and going back
        self.toggle_button = tk.Button(self, text="Edit", command=self.toggle_edit_save)
        self.toggle_button.pack(pady=0)

        self.delete_button = tk.Button(self, text=f"Delete {self.user_type}", command=self.delete_MHWP)
        self.delete_button.pack(pady=0)

        self.back_button = tk.Button(self, text="Back", command=self.go_back)
        self.back_button.pack(pady=0)

    def fetch_user_details(self, user_id):
        # Fetch user details from the database
        user_relation = self.db.getRelation('User')
        user = user_relation.getRowsWhereEqual('user_id', user_id)

        if user:
            # Return user data as a dictionary
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
        # Toggle between editing and saving changes to user details
        if self.username_entry.cget('state') == 'disabled':
            # Enable fields for editing
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
            # Save changes and revert fields to view-only mode
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
        # Save changes to the database and handle errors
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
            # Update only changed fields
            for field, new_value in updated_data.items():
                if self.original_data[field] != new_value:
                    user_relation.editFieldInRow(self.user_id, field, new_value)

            messagebox.showinfo("Success", f"{self.user_type} information updated successfully.")
            return True
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False

    def delete_MHWP(self):
        # Delete the MHWP from the database
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
        # Initialize Toplevel window and attributes
        super().__init__()
        self.db = Database()  # Create a new database connection
        self.geometry("400x350")  # Set window size
        self.resizable(True, False)  # Make window resizable only horizontally
        self.user_type = user_type  # Type of user to display (e.g., Patient or MHWP)
        self.parent = parent  # Reference to parent window
        self.selected_user_id = None  # Track selected user ID
        self.users = self.db.getRelation('User').getRowsWhereEqual("type", user_type)  # Fetch users of the given type
        self.create_ui()  # Build the UI
        self.protocol("WM_DELETE_WINDOW", self.on_close)  # Handle window close event

    def create_ui(self):
        # Set window title
        self.title(f"Select {self.user_type}")

        # Header label
        h1_label = tk.Label(self, text=f"Edit {self.user_type}", font=("Arial", 22, "bold"))
        h1_label.pack()

        # Instruction label
        doc_to_user = tk.Label(self, text=f"Choose the {self.user_type} to edit:", font=("Arial", 12, "bold"))
        doc_to_user.pack()

        # Create a frame for the tree view and scrollbar
        tree_frame = tk.Frame(self)
        tree_frame.pack(pady=10, fill="both", expand=True)

        # Add scrollbar for the tree view
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")

        # Create a treeview widget to display users
        self.tree = ttk.Treeview(tree_frame, yscrollcommand=scrollbar.set, selectmode="browse")
        self.tree.pack(fill="both", expand=True)

        # Link scrollbar to the tree view
        scrollbar.config(command=self.tree.yview)

        # Define columns for the tree view
        self.tree["columns"] = ("ID", "First Name", "Last Name")
        self.tree.column("#0", width=0, stretch=tk.NO)  # Hide default column
        self.tree.column("ID", anchor=tk.CENTER, width=50)
        self.tree.column("First Name", anchor=tk.CENTER, width=150)
        self.tree.column("Last Name", anchor=tk.CENTER, width=150)

        # Set column headers
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("ID", text="ID", anchor=tk.W)
        self.tree.heading("First Name", text="First Name", anchor=tk.W)
        self.tree.heading("Last Name", text="Last Name", anchor=tk.W)

        # Populate the tree view with users
        for user in self.users:
            self.tree.insert("", "end", values=(user[0], user[4], user[5]))

        # Add a button to select a user
        select_button = tk.Button(self, text=f"Select {self.user_type}", command=self.edit_user)
        select_button.pack(pady=0)

        # Add a back button to return to the parent window
        self.back_button = tk.Button(self, text="Back", command=self.go_back)
        self.back_button.pack(pady=0)

    def refresh_treeview(self):
        # Clear the tree view and reload users
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.users = self.db.getRelation('User').getRowsWhereEqual('type', self.user_type)
        for user in self.users:
            self.tree.insert("", "end", values=(user[0], user[4], user[5]))

    def edit_user(self):
        # Open the appropriate edit window for the selected user
        selected_item = self.tree.selection()
        if selected_item:
            self.selected_user_id = int(self.tree.item(selected_item, "values")[0])  # Get selected user ID
            self.withdraw()  # Hide current window
            if self.user_type == "Patient":
                app = PatientEditApp(self.selected_user_id, self, db=self.db)  # Open Patient editor
            else:
                app = MHWPEditApp(self.selected_user_id, self, db=self.db)  # Open MHWP editor
        else:
            # Notify the user if no selection was made
            messagebox.showinfo(f"No {self.user_type} Selected", f"Please select a {self.user_type} to continue.")

    def go_back(self):
        # Close the database connection and return to the parent window
        self.db.close()
        self.destroy()
        self.parent.deiconify()

    def on_close(self):
        # Handle window close event by closing the database and destroying the window
        self.db.close()
        self.destroy()

class AllocationSelection(UserSelectionApp):
    def __init__(self, user_type, parent):
        # Initialize by inheriting from UserSelectionApp
        super().__init__(user_type, parent)

    def refresh_treeview(self):
        # Clear existing entries in the tree view
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fetch users of the specified type
        self.users = self.db.getRelation('User').getRowsWhereEqual('type', self.user_type)

        # Populate the tree view with patient and MHWP assignment details
        for user in self.users:
            patient_id = user[0]
            patient_name = f"{user[4]} {user[5]}"  # Construct patient name

            # Retrieve the patient's MHWP assignment
            mhwp_allocation = self.db.getRelation('Allocation').getRowsWhereEqual("patient_id", patient_id)
            mhwp_allocation_id = mhwp_allocation[0][3] if mhwp_allocation else None

            if mhwp_allocation_id:
                # Fetch the assigned MHWP's name
                assigned_mhwp = self.db.getRelation('User').getRowsWhereEqual("user_id", mhwp_allocation_id)
                assigned_mhwp_name = f"{assigned_mhwp[0][4]} {assigned_mhwp[0][5]}"
            else:
                assigned_mhwp_name = "Unassigned"  # Default for unassigned patients

            # Insert patient details and assigned MHWP into the tree view
            self.tree.insert("", "end", values=(user[0], patient_name, assigned_mhwp_name))

    def edit_user(self):
        # Open the allocation editor for the selected patient
        selected_item = self.tree.selection()
        if selected_item:
            self.selected_user_id = int(self.tree.item(selected_item, "values")[0]) 
            self.withdraw()  
            app = AllocationEdit(self.selected_user_id, self, db=self.db) 
        else:
            # Notify the user if no patient is selected
            messagebox.showinfo("No Patient Selected", "Please select a patient to continue.")

    def create_ui(self):
        # Set the window title
        self.title(f"Select {self.user_type}")

        # Add a header label for the allocation selection window
        h1_label = tk.Label(self, text="Patient Allocations", font=("Arial", 22, "bold"))
        h1_label.pack()

        # Instruction label for user guidance
        doc_to_user = tk.Label(self, text=f"Choose the Patient to edit:", font=("Arial", 12, "bold"))
        doc_to_user.pack()

        # Create a frame for the tree view and its scrollbar
        tree_frame = tk.Frame(self)
        tree_frame.pack(pady=10, fill="both", expand=True)

        # Add scrollbar for the tree view
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")

        # Create a treeview widget to display patients and their MHWP assignments
        self.tree = ttk.Treeview(tree_frame, yscrollcommand=scrollbar.set, selectmode="browse")
        self.tree.pack(fill="both", expand=True)

        # Link the scrollbar to the tree view
        scrollbar.config(command=self.tree.yview)

        # Define the columns for the tree view
        self.tree["columns"] = ("ID", "Patient Name", "Assigned MHWP")
        self.tree.column("#0", width=0, stretch=tk.NO)  # Hide the default column
        self.tree.column("ID", anchor=tk.CENTER, width=50)
        self.tree.column("Patient Name", anchor=tk.CENTER, width=150)
        self.tree.column("Assigned MHWP", anchor=tk.CENTER, width=200)

        # Set the column headers
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("ID", text="ID", anchor=tk.W)
        self.tree.heading("Patient Name", text="Patient Name", anchor=tk.W)
        self.tree.heading("Assigned MHWP", text="Assigned MHWP", anchor=tk.W)

        # Populate the tree view with user data and their MHWP assignments
        for user in self.users:
            patient_id = user[0]
            patient_name = f"{user[4]} {user[5]}"

            # Retrieve the MHWP assignment for the patient
            mhwp_allocation = self.db.getRelation('Allocation').getRowsWhereEqual("patient_id", patient_id)
            if mhwp_allocation and len(mhwp_allocation) > 0:
                mhwp_allocation_id = mhwp_allocation[0][3]
            else:
                mhwp_allocation_id = None

            if mhwp_allocation_id:
                # Fetch the assigned MHWP's name
                assigned_mhwp = self.db.getRelation('User').getRowsWhereEqual("user_id", mhwp_allocation_id)
                assigned_mhwp_name = f"{assigned_mhwp[0][4]} {assigned_mhwp[0][5]}"
            else:
                assigned_mhwp_name = "Unassigned"  

            # Insert patient and MHWP assignment details into the tree view
            self.tree.insert("", "end", values=(user[0], patient_name, assigned_mhwp_name))

        # Add a button to select a patient
        select_button = tk.Button(self, text=f"Select {self.user_type}", command=self.edit_user)
        select_button.pack()

        # Add a back button to return to the parent window
        self.back_button = tk.Button(self, text="Back", command=self.go_back)
        self.back_button.pack(pady=0)

class KeyStatistics(tk.Toplevel):
    def __init__(self, parent):
        # Initialize the Toplevel window for displaying key statistics
        super().__init__()
        self.db = Database()  # Create a database connection
        self.parent = parent  # Reference to the parent window
        self.mhwps = self.db.getRelation('User').getRowsWhereEqual('type', 'MHWP')  # Fetch MHWPs from the database
        self.total_appointments = {}  # Initialize appointment data storage
        self.calculations()  # Perform necessary calculations
        self.create_ui()  # Build the UI for the window

    def calculations(self):
        # Calculate total appointments per MHWP
        self.total_appointments = {}
        for row in self.mhwps:
            user_id = row[0]
            mhwp_appointments = self.db.getRelation('Appointment').getRowsWhereEqual('mhwp_id', user_id)
            
            mhwp_user = self.db.getRelation('User').getRowsWhereEqual("user_id", user_id)
            mhwp_name = f"{mhwp_user[0][4]} {mhwp_user[0][5]}"  # Get MHWP name

            self.total_appointments.update({mhwp_name: mhwp_appointments})

        # Calculate allocation counts per MHWP
        mhwp_counts = {}
        allocations = self.db.getRelation('Allocation').getAllRows()
        for alloc in allocations:
            mhwp_id = alloc.getField('mhwp_id')
            if mhwp_id and mhwp_id != "":
                mhwp_user = self.db.getRelation('User').getRowsWhereEqual("user_id", mhwp_id)
                if mhwp_user:
                    mhwp_name = f"{mhwp_user[0][4]} {mhwp_user[0][5]}"
                    mhwp_counts[mhwp_name] = mhwp_counts.get(mhwp_name, 0) + 1

        self.allocation_counts = mhwp_counts  # Store MHWP allocation counts

    def create_ui(self):
        # Create UI components to display key statistics
        self.title("Bar Chart with Tkinter Canvas")

        # Create a Canvas widget for visualization
        canvas = tk.Canvas(self, width=1050, height=550)
        canvas.pack()

        # Add a title to the graph
        canvas.create_text(300, 22, text="Total Appointments per MHWP", font=("Arial", 16, "bold"))

        # Prepare data for bar chart
        categories = list(self.total_appointments)
        values = [len(self.total_appointments[cat]) for cat in categories]
        max_value = max(values) if values else 1  # Avoid division by zero

        # Set bar chart dimensions and layout
        canvas_width = 520
        bar_spacing = 20
        bar_width = max(10, (canvas_width - bar_spacing * (len(categories) - 1)) / len(categories))  # Minimum bar width
        x_position = 60  # Initial X position for bars

        # Draw axes for the bar chart
        canvas.create_line(50, 350, 570, 350, width=1)  # X-axis
        canvas.create_line(50, 50, 50, 350, width=1)  # Y-axis

        # Add Y-axis labels
        for i in range(0, max_value + 1, max(1, max_value // 5)):
            y_position = 350 - (i / max_value) * 300
            canvas.create_text(40, y_position, text=str(i), anchor="e")

        # Draw bars on the chart
        for i, value in enumerate(values):
            bar_height = (value / max_value) * 300  # Scale bar height
            canvas.create_rectangle(
                x_position, 350 - bar_height, x_position + bar_width, 350, fill="skyblue"
            )
            canvas.create_text(x_position + bar_width / 2, 360, text=categories[i], anchor="center")
            x_position += bar_width + bar_spacing  # Increment position for next bar

        # Add axis labels
        canvas.create_text(20, 190, text="Number of Appointments", angle=90, font=("Arial", 14))
        canvas.create_text(300, 380, text="MHWP", font=("Arial", 14))

        # Calculate and display key statistics
        patients = len(self.db.getRelation('User').getRowsWhereEqual('type', 'Patient'))
        mhwps = len(self.db.getRelation('User').getRowsWhereEqual('type', 'MHWP'))
        patients_per_mhwp = round(patients / mhwps, 1) if mhwps > 0 else 0  # Avoid division by zero
        stats = [
            f"No. Patients: {patients}",
            f"No. MHWP: {mhwps}",
            f"Patients Per MHWP: {patients_per_mhwp}",
            f"Disabled Accounts: {len(self.db.getRelation('User').getRowsWhereEqual('is_disabled', True))}",
            f"Unallocated Patients: {len(self.db.getRelation('Allocation').getRowsWhereEqual('mhwp_id', ''))}",
            f"No. Journal Entries: {len(self.db.getRelation('JournalEntry'))}",
            f"No. Patient Records: {len(self.db.getRelation('PatientRecord'))}",
            f"Active Appointments: {len(self.db.getRelation('Appointment').getRowsWhereEqual('status', 'active'))}",
            f"Confirmed Appointments: {len(self.db.getRelation('Appointment').getRowsWhereEqual('status', 'Confirmed'))}",
            f"Declined Appointments: {len(self.db.getRelation('Appointment').getRowsWhereEqual('status', 'Declined'))}"
        ]

        key_stats_gap = 22
        for i, stat in enumerate(stats[:5]):
            canvas.create_text(402, 427 + key_stats_gap * i, text=stat, font=("Arial", 14))
        for i, stat in enumerate(stats[5:]):
            canvas.create_text(652, 427 + key_stats_gap * i, text=stat, font=("Arial", 14))

        # Draw a pie chart for allocation distribution
        self.draw_pie_chart(canvas, x_center=780, y_center=205, radius=100)

        # Add a back button to return to the parent window
        back_button = tk.Button(self, text="Back", command=self.go_back)
        back_button.pack(pady=5)

    def draw_pie_chart(self, canvas, x_center, y_center, radius):
        # Create a pie chart for MHWP allocations
        canvas.create_text(x_center + 55, y_center - radius - 85, text="Patients per MHWP", font=("Arial", 16, "bold"))

        colors = ["lightgreen", "lavender", "mistyrose", "palegreen", "lightpink", "lightblue", "peachpuff"]
        total = sum(self.allocation_counts.values()) if self.allocation_counts else 1  # Avoid division by zero

        start_angle = 0
        for i, (mhwp_name, count) in enumerate(self.allocation_counts.items()):
            extent_angle = (count / total) * 360
            fill_color = colors[i % len(colors)]
            canvas.create_arc(
                x_center - radius, y_center - radius, x_center + radius, y_center + radius,
                start=start_angle, extent=extent_angle, fill=fill_color
            )
            start_angle += extent_angle

        # Add a legend for the pie chart
        legend_x, legend_y = x_center + radius + 50, y_center - radius
        for i, (mhwp_name, count) in enumerate(self.allocation_counts.items()):
            canvas.create_rectangle(legend_x, legend_y + i * 20, legend_x + 20, legend_y + i * 20 + 15, fill=colors[i % len(colors)])
            canvas.create_text(legend_x + 30, legend_y + i * 20 + 7, text=f"{mhwp_name} ({count})", anchor="w", font=("Arial", 10))

        # If no data is available, display a message
        if not self.allocation_counts:
            canvas.create_text(x_center, y_center, text="No Allocations Found", font=("Arial", 12))

    def go_back(self):
        # Close the current window and return to the parent
        self.destroy()
        self.parent.deiconify()

class AdminMainPage(tk.Tk):
    def __init__(self):
        # Initialize the Admin Dashboard window
        super().__init__()
        self.db = Database()  # Establish a database connection
        self.title("Admin Dashboard")  # Set the window title
        self.geometry("310x300")  # Set the window size
        self.create_ui()  # Create the user interface

    def create_ui(self):
        # Add a header label for the dashboard
        h1_label = tk.Label(text="Admin Dashboard", font=("Arial", 24, "bold"))
        h1_label.pack(pady=10)

        # Add a section label for quick actions
        quick_actions_label = tk.Label(text="Actions", font=("Arial", 14, "bold"))
        quick_actions_label.pack(pady=10)

        # Add buttons for various admin actions
        tk.Button(text="Patients Allocations", command=self.patient_allocations, width=20).pack(pady=5)
        tk.Button(text="Edit Patients", command=self.edit_patient_info, width=20).pack(pady=5)
        tk.Button(text="Edit MHWPs", command=self.edit_MHWP_info, width=20).pack(pady=5)
        tk.Button(text="Key Statistics", command=self.key_stats, width=20).pack(pady=5)
        tk.Button(text="Log Out", command=self.log_out, width=20).pack(pady=5)

    def patient_allocations(self):
        # Open the Patient Allocations management window
        self.withdraw() 
        app = AllocationSelection("Patient", self) 

    def edit_patient_info(self):
        # Open the Patient Info editing window
        self.withdraw()  
        app = UserSelectionApp("Patient", self) 

    def edit_MHWP_info(self):
        # Open the MHWP Info editing window
        self.withdraw() 
        app = UserSelectionApp("MHWP", self)  

    def key_stats(self):
        # Open the Key Statistics window
        self.withdraw() 
        app = KeyStatistics(self) 

    def log_out(self):
        # Log out and return to the main application
        from main import App  # Import the main application
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


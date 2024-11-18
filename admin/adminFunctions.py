import tkinter as tk
from tkinter import messagebox
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database'))
sys.path.append(project_root)
from database import Database
from entities import UserError, RecordError, Admin, Patient, MHWP, PatientRecord, Allocation, JournalEntry, Appointment


class AllocationEdit:
    def __init__(self, root, patient_id, parent_window):
        self.db = Database()
        self.root = root
        self.patient_id = patient_id
        self.parent_window = parent_window
        self.create_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_ui(self):
        self.root.title("Edit MHWP Assignment")

        # H1 equivalent
        h1_label = tk.Label(self.root, text="Assign MHWP to Patient", font=("Arial", 24, "bold"))
        h1_label.pack()
        
        # Fetch current MHWP assigned to the patient
        patient = self.db.getRelation('Allocation').getRowsWhereEqual("patient_id", self.patient_id)
        assigned_mhwp_id = patient[0][3]
        
        self.allocation_id = patient[0][0]
        
        assigned_mhwp = self.db.getRelation('User').getRowsWhereEqual("user_id", assigned_mhwp_id)
        assigned_mhwp_name = f"{assigned_mhwp[0][4]} {assigned_mhwp[0][5]}"

        # Fetch list of MHWPs
        mhwps = self.db.getRelation('User').getRowsWhereEqual("type", "MHWP")
        self.mhwp_dict = {f"{mhwp[4]} {mhwp[5]}": mhwp[0] for mhwp in mhwps}
        mhwp_names = list(self.mhwp_dict.keys())

        # Create label and dropdown for MHWP selection
        tk.Label(self.root, text="Select New MHWP:").pack(pady=10)
        self.mhwp_var = tk.StringVar(value=assigned_mhwp_name)
        self.mhwp_dropdown = tk.OptionMenu(self.root, self.mhwp_var, *mhwp_names)
        self.mhwp_dropdown.pack(pady=10)

        # Save Button
        save_button = tk.Button(self.root, text="Save", command=self.save_mhwp)
        save_button.pack(pady=0)

        # Back Button
        self.back_button = tk.Button(self.root, text="Back", command=self.go_back)
        self.back_button.pack(pady=0)

    def save_mhwp(self):
        # Get the new MHWP selection
        new_mhwp_name = self.mhwp_var.get()
        new_mhwp_id = self.mhwp_dict.get(new_mhwp_name)

        # Update the patient's MHWP in the database
        print(type(self.allocation_id))
        print(type(new_mhwp_id))
        userRelation = self.db.getRelation('Allocation')
        userRelation.editFieldInRow(self.allocation_id, 'mhwp_id', new_mhwp_id)

        messagebox.showinfo("Success", "MHWP updated successfully.")
        self.root.destroy()  # Close the edit window

    def go_back(self):
        self.root.destroy()
        self.parent_window.deiconify()

    def on_close(self):
        self.db.close()
        self.root.destroy()

class UserEditApp:
    def __init__(self, root, user_id, parent_window):
        self.db = Database()
        self.root = root
        self.parent_window = parent_window
        self.user_id = user_id
        self.user_type = self.db.getRelation('User').getRowsWhereEqual("user_id", user_id)[0][6]
        self.original_data = {}
        self.create_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_ui(self):
        self.root.title("Edit User Information")

        # H1 equivalent
        h1_label = tk.Label(self.root, text=f"Edit {self.user_type} Information", font=("Arial", 24, "bold"))
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

        tk.Label(user_frame, text="Specialization:").grid(row=8, column=0)
        self.specialization_entry = tk.Entry(user_frame)
        self.specialization_entry.insert(0, user['specialization'] if user['specialization'] else '')
        self.specialization_entry.config(state='disabled')
        self.specialization_entry.grid(row=8, column=1)

        tk.Label(user_frame, text="Disabled:").grid(row=10, column=0)
        self.is_disabled_var = tk.BooleanVar(value=user['is_disabled'])
        self.is_disabled_check = tk.Checkbutton(user_frame, variable=self.is_disabled_var)
        self.is_disabled_check.config(state='disabled')
        self.is_disabled_check.grid(row=10, column=1)

        # Toggle Edit/Save Button
        self.toggle_button = tk.Button(self.root, text="Edit", command=self.toggle_edit_save)
        self.toggle_button.pack(pady=0)

        # Delete Button
        self.delete_button = tk.Button(self.root, text=f"Delete {self.user_type}", command=self.delete_user)
        self.delete_button.pack(pady=0)

        # Back Button
        self.back_button = tk.Button(self.root, text="Back", command=self.go_back)
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
                'specialization': user_data[8],
                'is_disabled': user_data[9]
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
            self.specialization_entry.config(state='normal')
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
                'specialization': self.specialization.get(),
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
            self.specialization_entry.config(state='disabled')
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
            'specialization': self.specialization_entry.get(),
            'is_disabled': self.is_disabled_var.get()
        }
        
        for field, new_value in updated_data.items():
            if self.original_data[field] != new_value:
                user_relation.editFieldInRow(self.user_id, field, new_value)
        
        messagebox.showinfo("Success", f"{self.user_type} information updated successfully.")

    def delete_user(self):
        user_relation = self.db.getRelation('User')
        response = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete this {self.user_type}?")

        if response:
            user_relation.dropRows(id=self.user_id)
            messagebox.showinfo("Success", f"{self.user_type} deleted successfully.")
            
            self.parent_window.destroy()
            self.on_close()

            root = tk.Tk()
            new_user_selection_app = UserSelectionApp(root, self.user_type)
            root.mainloop()

    def go_back(self):
        self.root.destroy()
        self.parent_window.deiconify()

    def on_close(self):
        self.db.close()
        self.root.destroy()

class UserSelectionApp:
    def __init__(self, root, user_type):
        self.db = Database()
        self.root = root
        self.user_type = user_type
        self.selected_user_id = tk.IntVar(value=-1)
        self.users = self.db.getRelation('User').getRowsWhereEqual("type", user_type)
        self.create_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_ui(self):
        self.root.title(f"Select {self.user_type}")

        # H1 equivalent
        h1_label = tk.Label(self.root, text="Welcome back admin", font=("Arial", 24, "bold"))
        h1_label.pack()
        
        # instruction label
        docToUser = tk.Label(self.root, text=f"Choose the {self.user_type}s to edit:", font=("Arial", 12, "bold"))
        docToUser.pack()

        # creating checkbox for each patient
        for user in self.users:
            user_name = f"{user[4]} {user[5]}"
            radio_button = tk.Radiobutton(self.root, text=user_name, variable=self.selected_user_id, value=user[0])
            radio_button.pack(anchor="w")

        # select button 
        select_button = tk.Button(self.root, text=f"Select {self.user_type}", command=self.edit_user)  
        select_button.pack()

        # back button
        self.back_button = tk.Button(self.root, text="Back", command=self.go_back)
        self.back_button.pack(pady=0)

    def edit_user(self):
        selected_user_id = self.selected_user_id.get()
        if selected_user_id != -1:
            self.root.withdraw()
            edit_window = tk.Toplevel(self.root)
            app = UserEditApp(edit_window, selected_user_id, self.root)
        else:
            messagebox.showinfo("No {self.user_type} Selected", f"Please select a {self.user_type} to continue.")

    def go_back(self):
        self.root.destroy()

        root = tk.Tk()
        app = AdminMainPage(root)
        root.mainloop()

    def on_close(self):
        self.db.close()
        self.root.destroy()

class AllocationSelection(UserSelectionApp):
    def __init__(self, root, user_type):
        super().__init__(root, user_type)

    def edit_user(self):
        selected_user_id = self.selected_user_id.get()
        if selected_user_id != -1:
            self.root.withdraw()
            edit_window = tk.Toplevel(self.root)
            app = AllocationEdit(edit_window, selected_user_id, self.root)
        else:
            messagebox.showinfo("No Patient Selected", "Please select a patient to continue.")

class AdminMainPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Dashboard")
        self.root.geometry("600x500")

        # H1 equivalent
        h1_label = tk.Label(root, text="Admin Dashboard", font=("Arial", 24, "bold"))
        h1_label.pack(pady=10)

        # Quick Actions Section
        quick_actions_label = tk.Label(root, text="Actions", font=("Arial", 14, "bold"))
        quick_actions_label.pack(pady=10)

        tk.Button(
            root, text="Allocate Patients", command=self.allocate_patients, width=20
        ).pack(pady=5)

        tk.Button(
            root, text="Edit Patients", command=self.edit_patient_info, width=20
        ).pack(pady=5)

        tk.Button(
            root, text="Edit MHWPs", command=self.edit_MHWP_info, width=20
        ).pack(pady=5)

        tk.Button(
            root, text="Key Statistics", command=self.key_stats, width=20
        ).pack(pady=5)

        # Improved Summary Section
        self.summary_frame = tk.Frame(root, bd=2, relief="groove")
        self.summary_frame.pack(padx=20, pady=20, fill="both", expand=True)

        summary_label = tk.Label(
            self.summary_frame, text="User Summary", font=("Arial", 16, "bold"), anchor="w", padx=10
        )
        summary_label.grid(row=0, column=0, sticky="w", pady=5)

        # Summary content in a grid for better organization
        self.summary_text = tk.Text(self.summary_frame, height=10, width=50, wrap="word", bd=0, font=("Arial", 12))
        self.summary_text.grid(row=1, column=0, padx=10, pady=10)
        self.summary_text.insert(
            tk.END,
            "Active Patients: 10\n"
            "Active MHWPs: 5\n"
            "Disabled Accounts: 2\n"
            "Unallocated Patients: 3\n",
        )
        self.summary_text.config(state="disabled")  # Make the summary read-only

        # Add a horizontal separator for a neat layout
        separator = tk.Frame(self.summary_frame, height=2, bd=1, relief="sunken", bg="gray")
        separator.grid(row=2, column=0, pady=10, sticky="ew")

        # Add an extra summary option with visual indicators (e.g., Patient Health Trends)
        patient_trends_label = tk.Label(self.summary_frame, text="Patient Health Trends", font=("Arial", 12, "bold"), anchor="w", padx=10)
        patient_trends_label.grid(row=3, column=0, sticky="w", pady=5)

        trends_text = tk.Label(self.summary_frame, text="Improving: 4\nStable: 3\nDeclining: 3", font=("Arial", 12), anchor="w", padx=10)
        trends_text.grid(row=4, column=0, sticky="w", padx=10)

        # Logout Button
        tk.Button(
            root, text="Logout", command=self.logout, bg="red", fg="white", width=10
        ).pack(pady=20)

    def allocate_patients(self):
        self.root.withdraw()
        select_window = tk.Toplevel(self.root)
        app = AllocationSelection(select_window, "Patient")
        select_window.protocol("WM_DELETE_WINDOW", self.on_select_window_close)

    def edit_patient_info(self):
        self.root.withdraw()
        select_window = tk.Toplevel(self.root)
        app = UserSelectionApp(select_window, "Patient")
        select_window.protocol("WM_DELETE_WINDOW", self.on_select_window_close)

    def edit_MHWP_info(self):
        self.root.withdraw()
        select_window = tk.Toplevel(self.root)
        app = UserSelectionApp(select_window, "MHWP")
        select_window.protocol("WM_DELETE_WINDOW", self.on_select_window_close)

    def key_stats(self):
        # Placeholder logic for Disable User
        messagebox.showinfo("Disable User", "This feature is under development.")
    
    def on_select_window_close(self):
        self.root.deiconify()

    def logout(self):
        # Confirm logout and navigate back to the login page
        if messagebox.askyesno("Logout", "Are you sure you want to log out?"):
            self.root.destroy()


root = tk.Tk()

app = AdminMainPage(root)

root.mainloop()
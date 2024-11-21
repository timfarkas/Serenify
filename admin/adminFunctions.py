import tkinter as tk
from tkinter import messagebox
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database'))
sys.path.append(project_root)
from database import Database
from entities import UserError, RecordError, Admin, Patient, MHWP, PatientRecord, Allocation, JournalEntry, Appointment


class AllocationEdit(tk.Toplevel):
    def __init__(self, patient_id, parent):
        super().__init__()
        self.db = Database()
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

        # Update the patient's MHWP in the database
        userRelation = self.db.getRelation('Allocation')
        userRelation.editFieldInRow(self.allocation_id, 'mhwp_id', new_mhwp_id)

        self.db.close()
        messagebox.showinfo("Success", "MHWP updated successfully.")

    def go_back(self):
        self.db.close()
        self.destroy()
        self.parent.deiconify()

    def on_close(self):
        self.db.close()
        self.destroy()

class UserEditApp(tk.Toplevel):
    def __init__(self, user_id, parent):
        super(UserEditApp, self).__init__()
        self.db = Database()
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

        tk.Label(user_frame, text="Specialization:").grid(row=8, column=0)
        self.specialization_entry = tk.Entry(user_frame)
        self.specialization_entry.insert(0, user['specialization'] if user['specialization'] else '')
        self.specialization_entry.config(state='disabled')
        self.specialization_entry.grid(row=8, column=1)

        #tk.Label(user_frame, text="Disabled:").grid(row=10, column=0)
        #self.is_disabled_var = tk.BooleanVar(value=user['is_disabled'])
        #self.is_disabled_check = tk.Checkbutton(user_frame, variable=self.is_disabled_var)
        #self.is_disabled_check.config(state='disabled')
        #self.is_disabled_check.grid(row=10, column=1)

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
                'specialization': user_data[8],
                #'is_disabled': user_data[9]
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
            #self.is_disabled_check.config(state='normal')

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
                'specialization': self.specialization_entry.get(),
                #'is_disabled': self.is_disabled_var.get()
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
            #self.is_disabled_check.config(state='disabled')
    
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
            #'is_disabled': self.is_disabled_var.get()
        }
        
        for field, new_value in updated_data.items():
            if self.original_data[field] != new_value:
                user_relation.editFieldInRow(self.user_id, field, new_value)
        
        self.db.close()
        messagebox.showinfo("Success", f"{self.user_type} information updated successfully.")

    def delete_user(self):
        user_relation = self.db.getRelation('User')
        response = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete this {self.user_type}?")

        if response:
            user_relation.dropRows(id=self.user_id)
            messagebox.showinfo("Success", f"{self.user_type} deleted successfully.")
            
            self.db.close()
            self.destroy()
            self.parent.deiconify()

    def go_back(self):
        self.destroy()
        self.parent.deiconify()
        
    def on_close(self):
        self.db.close()
        self.destroy()

class UserSelectionApp(tk.Toplevel):
    def __init__(self, user_type, parent):
        super().__init__()
        self.db = Database()
        self.geometry("280x165")
        self.resizable(True, False)
        self.user_type = user_type
        self.parent = parent
        self.selected_user_id = tk.IntVar(value=-1)
        self.users = self.db.getRelation('User').getRowsWhereEqual("type", user_type)
        self.create_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_ui(self):
        self.title(f"Select {self.user_type}")

        # H1 equivalent
        h1_label = tk.Label(self, text=f"Edit {self.user_type}", font=("Arial", 22, "bold"))
        h1_label.pack()
        
        # instruction label
        docToUser = tk.Label(self, text=f"Choose the {self.user_type} to edit:", font=("Arial", 12, "bold"))
        docToUser.pack()

        # creating checkbox for each patient
        for user in self.users:
            user_name = f"{user[4]} {user[5]}"
            radio_button = tk.Radiobutton(self, text=user_name, variable=self.selected_user_id, value=user[0])
            radio_button.pack(padx=60, anchor="w")

        # select button 
        select_button = tk.Button(self, text=f"Select {self.user_type}", command=self.edit_user)  
        select_button.pack()

        # back button
        self.back_button = tk.Button(self, text="Back", command=self.go_back)
        self.back_button.pack(pady=0)

    def edit_user(self):
        selected_user_id = self.selected_user_id.get()
        if selected_user_id != -1:
            self.withdraw()
            app = UserEditApp(selected_user_id, self)
        else:
            messagebox.showinfo("No {self.user_type} Selected", f"Please select a {self.user_type} to continue.")

    def go_back(self): 
        self.destroy()
        self.parent.deiconify()

    def on_close(self):
        self.db.close()
        self.destroy()

class AllocationSelection(UserSelectionApp):
    def __init__(self, user_type, parent):
        super().__init__(user_type, parent)

    def edit_user(self):
        selected_user_id = self.selected_user_id.get()
        if selected_user_id != -1:
            self.withdraw()
            app = AllocationEdit(selected_user_id, self)
        else:
            messagebox.showinfo("No Patient Selected", "Please select a patient to continue.")

    def create_ui(self):
        self.title(f"Select {self.user_type}")

        # H1 equivalent
        h1_label = tk.Label(self, text="Patient Allocations", font=("Arial", 22, "bold"))
        h1_label.pack()
        
        # instruction label
        docToUser = tk.Label(self, text=f"Choose the Patient to edit:", font=("Arial", 12, "bold"))
        docToUser.pack()

        # Fetch current MHWP assigned to the patient
        

        # creating checkbox for each patient
        for user in self.users:
            patient_id = user[0]
            patient = self.db.getRelation('Allocation').getRowsWhereEqual("patient_id", patient_id)
            assigned_mhwp_id = patient[0][3]
            self.allocation_id = patient[0][0]

            if assigned_mhwp_id:
                assigned_mhwp = self.db.getRelation('User').getRowsWhereEqual("user_id", assigned_mhwp_id)
                assigned_mhwp_name = f"{assigned_mhwp[0][4]} {assigned_mhwp[0][5]}"
            else:
                assigned_mhwp_name = "Unassigned"

            user_name = f"{user[4]} {user[5]} - {assigned_mhwp_name}"
            radio_button = tk.Radiobutton(self, text=user_name, variable=self.selected_user_id, value=user[0])
            radio_button.pack(padx=10, anchor="w")

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

        print(self.total_appointments)
    
    def create_ui(self):
        
        self.title("Bar Chart with Tkinter Canvas")

        # Create a Canvas widget
        canvas = tk.Canvas(self, width=600, height=582)
        canvas.pack()

        # Graph title
        canvas.create_text(300, 22, text="Total Appointments per MHWP", font=("Arial", 16, "bold"))

        # Data for the bar chart (categories and values)
        categories = list(self.total_appointments)
        print(categories)
        no_items = len(categories)
        print(no_items)

        values = []
        for elements in categories:
            length = len(self.total_appointments[elements])
            values.append(length)
        print(values)

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

        # doesn't seem to be working - TO SPEAK TO TIM
        # calculating the number of disabled accounts
        disabled_accounts = self.db.getRelation('User').getWhereEqual('is_disabled', True)
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

        key_stats_x_position = 427
        key_stats_gap = 22

        # Create the summary of key statistics on the canvas
        canvas.create_text(300, (key_stats_x_position - 10), text="Key Statistics", font=("Arial", 16, "bold"))
        canvas.create_text(300, (key_stats_x_position + key_stats_gap * 1), text=f"No. Patients: {patient_row_count}", font=("Arial", 14))
        canvas.create_text(300, (key_stats_x_position + key_stats_gap * 2), text=f"No. MHWP: {mhwp_row_count}", font=("Arial", 14))
        canvas.create_text(300, (key_stats_x_position + key_stats_gap * 3), text=f"No. Disabled Accounts: {disabled_accounts_row_count}", font=("Arial", 14))
        canvas.create_text(300, (key_stats_x_position + key_stats_gap * 4), text=f"No. Unallocated Patients: {unalocated_patients_row_count}", font=("Arial", 14))
        canvas.create_text(300, (key_stats_x_position + key_stats_gap * 5 + 10), text=f"No. Journal Entries: {no_journal_entries}", font=("Arial", 14))
        canvas.create_text(300, (key_stats_x_position + key_stats_gap * 6 + 10), text=f"No. of Patient Records: {no_patient_records}", font=("Arial", 14))

        # Back button
        back_button = tk.Button(self, text="Back", command=self.go_back)
        back_button.pack(pady=5)

    def go_back(self): 
        self.destroy()
        self.parent.deiconify()

class AdminMainPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.title("Admin Dashboard")
        self.geometry("310x280")
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


app = AdminMainPage()
app.mainloop()
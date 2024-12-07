import sys
import os
import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.entities import PatientRecord
from database import Database
from sessions import Session
import pandas as pd

class PatientRecords:
    def __init__(self, user_id=None):

        # Initialize the session instance
        self.session = Session()
        self.session.open()
        self.current_user_id = self.session.getId()
        self.db = Database()
        self.root =  tk.Tk()
        self.root.title("Patient Records")
        self.root.geometry("700x700")

        self.title_label = tk.Label(self.root, text=f"Patient Records", font=("Arial", 24, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=5)

        #Back button
        self.back_button = tk.Button(self.root, text="Back", command= self.backButton,width=10)
        self.back_button.grid(row=3, column=1, padx=2, pady=5,sticky="se")

        # Load conditions from conditions.txt
        self.conditions_list = self.load_conditions("conditions.txt")

       # Search Patient Section
        self.patient_list_frame = tk.LabelFrame(self.root, text="Search Patient", padx=2, pady=5)
        self.patient_list_frame.grid(row=1, column=0, padx=2, pady=5, sticky="n")

        self.patient_listbox = tk.Listbox(self.patient_list_frame, height=10, width=25)
        self.patient_listbox.pack(side=tk.LEFT, padx=2, pady=5)
        self.patient_listbox.bind('<<ListboxSelect>>', self.load_patient_records)

        self.scrollbar = tk.Scrollbar(self.patient_list_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.patient_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.patient_listbox.yview)

        # Populate List with Patients
        self.patients = self.db.getRelation("User")
        self.patients = self.patients.getRowsWhereEqual('type', 'Patient')
        self.patients = pd.DataFrame(self.patients)
        for _, row in self.patients.iterrows():
            user_id = row[0]
            first_name = row[4]
            last_name = row[5]
            full_name = f"{user_id} {first_name} {last_name}"
            self.patient_listbox.insert(tk.END, full_name)

        # Patient Records Section
        self.record_frame = tk.LabelFrame(self.root, text="Records", padx=2, pady=5)
        self.record_frame.grid(row=1, column=1, padx=2, pady=5, sticky="n")

        self.record_text = tk.Text(self.record_frame, height=15, width=50)
        self.record_text.pack(padx=5, pady=5)
        self.record_text.config(state=tk.DISABLED)

        # Notes Section
        self.note_frame = tk.LabelFrame(self.root, text="Add Notes and Diagnosis", padx=2, pady=5)
        self.note_frame.grid(row=2, column=0, columnspan=2, padx=2, pady=5)

        # Notes Entry
        tk.Label(self.note_frame, text="Notes:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.notes_entry = tk.Text(self.note_frame, width=50, height=5)
        self.notes_entry.grid(row=0, column=1, padx=5, pady=5)

        # Diagnosis Dropdown
        tk.Label(self.note_frame, text="Diagnosis:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.diagnosis_var = tk.StringVar()
        self.diagnosis_dropdown = ttk.Combobox(self.note_frame, textvariable=self.diagnosis_var, width=47)
        self.diagnosis_dropdown['values'] = self.conditions_list
        self.diagnosis_dropdown.grid(row=1, column=1, padx=5, pady=5)

        self.save_button = tk.Button(self.note_frame, text="Save", command=self.save_diagnosis_and_notes)
        self.save_button.grid(row=2, column=1, pady=10, sticky="e")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def load_conditions(self, filename):
        """Loads mental health conditions from a text file."""
        try:
            with open(filename, 'r') as file:
                conditions = [line.strip() for line in file.readlines() if line.strip()]
                return conditions
        except FileNotFoundError:
            messagebox.showerror("Error", f"File '{filename}' not found.")
            return []

    def load_patient_records(self, event=None):
        """Loads selected patient's most recent diagnosis and all non-empty notes."""
        selected_index = self.patient_listbox.curselection()
        if not selected_index:
            return

        selected_patient = self.patients.iloc[selected_index[0]]
        patient_id = selected_patient[0]

        #Loading patient data
        self.record = self.db.getRelation("PatientRecord")
        self.record = self.record.getRowsWhereEqual('patient_id', patient_id)
        self.record = pd.DataFrame(self.record)

        # Check if the record is not empty
        if not self.record.empty:
            # Sort records by the first column (record_id)
            self.record.sort_values(by=self.record.columns[0], ascending=False, inplace=True) 
            most_recent_record = self.record.iloc[0]  # Get the most recent record

            # Extract the most recent diagnosis
            most_recent_diagnosis = most_recent_record[4] 

            # Filter and collect non-empty notes 
            non_empty_notes = self.record[self.record[3].str.strip() != ''][3] 

            # Display the data
            self.record_text.config(state=tk.NORMAL)
            self.record_text.delete("1.0", tk.END)

            # Show most recent diagnosis
            self.record_text.insert(tk.END, f"Most Recent Diagnosis: {', '.join(most_recent_diagnosis) if most_recent_diagnosis else 'None'}\n\n")

            # Show all non-empty notes
            if not non_empty_notes.empty:
                self.record_text.insert(tk.END, "Notes:\n")
                for note in non_empty_notes:
                    self.record_text.insert(tk.END, f"- {note}\n")
            else:
                self.record_text.insert(tk.END, "No notes available.\n")


            self.record_text.config(state=tk.DISABLED)
        else:
            # If no records are found
            # Show empty diagnosis
            self.record_text.config(state=tk.NORMAL)
            self.record_text.delete("1.0", tk.END)
            self.record_text.insert(tk.END, f"Most Recent Diagnosis: None \n\n")
            # Show lack of notes
            self.record_text.insert(tk.END, "No notes available.\n")
            self.record_text.config(state=tk.DISABLED)

    def save_note(self):
        """Saves the notes for the selected patient."""
        # Get selected patient index and validate selection
        selected_index = self.patient_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("No Patient Selected", "Please select a patient to save notes.")
            return
        # Extract patient ID and new note text
        patient_id = int(self.patients.iloc[selected_index[0]][0])
        new_note = self.notes_entry.get()
        if not new_note:
            messagebox.showwarning("Incomplete Data", "Please provide notes.")
            return

        try:
            # Connect to database and get existing records
            records_relation = self.db.getRelation("PatientRecord")
            existing_records = records_relation.getRowsWhereEqual('patient_id', patient_id)

            #Initialise variables for existing data
            existing_notes = ""
            conditions = []
            if existing_records:
                existing_notes = existing_records[0][3]
                conditions = existing_records[0][4]

            # Combine existing notes with new note
            combined_notes = f"{existing_notes}\nDiagnosis: ['Depression']\n\nNotes: {new_note}" if existing_notes else new_note

            # Create and save new patient record
            new_record = PatientRecord(
                patient_id=patient_id,
                mhwp_id=3,
                notes=combined_notes,
                conditions=conditions if conditions else []
            )
            print("Before save:", self.record)
            self.db.insert_patient_record(new_record)
            print("After save:", self.db.getRelation("PatientRecord").getRowsWhereEqual('patient_id', patient_id))

            # Cleanup and refresh display
            self.load_patient_records(None)
            self.notes_entry.delete(0, tk.END)
            messagebox.showinfo("Success", "Notes saved successfully")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save notes: {str(e)}")


    def save_diagnosis_and_notes(self):
        """Save combined notes and diagnosis for the selected patient."""
        selected_index = self.patient_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("No Patient Selected", "Please select a patient.")
            return

        patient_id = int(self.patients.iloc[selected_index[0]][0])
        new_notes = self.notes_entry.get("1.0", tk.END).strip()
        new_diagnosis = self.diagnosis_var.get().strip()

        if not new_notes and not new_diagnosis:
            messagebox.showwarning("Incomplete Data", "Please provide notes or select a diagnosis.")
            return

        try:
            # Connect to database and get existing records
            records_relation = self.db.getRelation("PatientRecord")
            existing_records = records_relation.getRowsWhereEqual('patient_id', patient_id)

            # Handle existing conditions
            conditions = []
            if existing_records:
                latest_record = existing_records[-1]
                conditions = latest_record[4] if latest_record[4] else []
            if new_diagnosis:
                if new_diagnosis not in conditions:
                    # Ask the user whether to replace or add
                    response = messagebox.askyesno(
                        "Update Diagnosis",
                        "Would you like to add the diagnosis to the list of conditions? If you click no we will replace the old diagnosis with the new one."
                    )
                    if response:  # Add
                        conditions.append(new_diagnosis)
                    else:  # Replace
                        conditions = [new_diagnosis]
                else:
                    messagebox.showinfo("Information", "The selected diagnosis already exists.")
                    
            # Create and save new patient record
            new_record = PatientRecord(
                patient_id=patient_id,
                mhwp_id=3,
                notes=new_notes,
                conditions=conditions
            )

            # Save record and refresh display
            self.db.insert_patient_record(new_record)

            # Refresh display
            self.load_patient_records(None)
            self.notes_entry.delete("1.0", tk.END)
            self.diagnosis_var.set("")
            messagebox.showinfo("Success", "Notes and diagnosis saved successfully.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save notes and diagnosis: {str(e)}")

    def on_close(self):
        self.db.close()
        self.root.destroy()
        import subprocess
        subprocess.Popen(["python3", "mhwp/mhwp_dashboard.py"])

    def backButton(self):
        import subprocess
        subprocess.Popen(["python3", "mhwp/mhwp_dashboard.py"])
        self.db.close()
        self.root.destroy()


if __name__ == "__main__":
    app = PatientRecords()
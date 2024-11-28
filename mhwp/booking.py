import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import smtplib
from email.mime.text import MIMEText


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import Database
from database.entities import Appointment
from database.dataStructs import Row




class MHWPAppointmentManager:
   def __init__(self, root, mhwp_id):
       self.root = root
       self.root.title("MHWP Appointment Management")
       self.mhwp_id = mhwp_id



       # Initialise database connection
       try:
           self.db = Database()
           # Verify database connection by trying to access Appointments relation
           self.db.getRelation("Appointment")
       except Exception as e:
           messagebox.showerror("Database Error", f"Failed to connect to database: {str(e)}")
           self.root.destroy()
           return

############# Not sure if this is correct so only commented it out
#     # Back button
#     self.back_button = tk.Button(root, text="Back", command=self.backButton)
#     self.back_button.pack()

#     def backButton(self):
#         subprocess.Popen(["python3", "mhwpMain.py"])
#         self.root.destroy()

       self.setup_ui()
       self.root.protocol("WM_DELETE_WINDOW", self.on_closing)


   def setup_ui(self):
       # Title
       h1_label = ttk.Label(
           self.root,
           text="Appointment Requests",
           font=("Arial", 24, "bold")
       )
       h1_label.pack(pady=10)


       # Create notebook for different appointment views
       self.notebook = ttk.Notebook(self.root)
       self.notebook.pack(padx=10, pady=5, fill="both", expand=True)


       # Create tabs for different appointment statuses
       self.pending_frame = ttk.Frame(self.notebook)
       self.confirmed_frame = ttk.Frame(self.notebook)
       self.declined_frame = ttk.Frame(self.notebook)
       self.cancelled_frame = ttk.Frame(self.notebook)


       self.notebook.add(self.pending_frame, text="Pending Requests")
       self.notebook.add(self.confirmed_frame, text="Confirmed Appointments")
       self.notebook.add(self.declined_frame, text="Declined Requests")
       self.notebook.add(self.cancelled_frame, text="Cancelled Appointments")


       # Create appointment lists for each tab
       self.setup_appointment_list(self.pending_frame, "Pending")
       self.setup_appointment_list(self.confirmed_frame, "Confirmed")
       self.setup_appointment_list(self.declined_frame, "Declined")
       self.setup_appointment_list(self.cancelled_frame, "Cancelled")


       # Button Frame
       button_frame = ttk.Frame(self.root)
       button_frame.pack(pady=10)


       ttk.Button(
           button_frame,
           text="Accept Selected",
           command=lambda: self.update_appointment_status("Confirmed")
       ).pack(side='left', padx=5)


       ttk.Button(
           button_frame,
           text="Decline Selected",
           command=lambda: self.update_appointment_status("Declined")
       ).pack(side='left', padx=5)


       ttk.Button(
           button_frame,
           text="Refresh",
           command=self.refresh_lists
       ).pack(side='left', padx=5)


       ttk.Button(
           button_frame,
           text="Back to Dashboard",
           command=self.back_to_dashboard
       ).pack(side='left', padx=5)


   def setup_appointment_list(self, parent, status):
       frame = ttk.Frame(parent)
       frame.pack(fill="both", expand=True)


       # Create Treeview
       tree = ttk.Treeview(
           frame,
           columns=("ID", "Patient", "Date", "Time", "Status"),
           show="headings"
       )


       # Configure columns
       tree.heading("ID", text="ID")
       tree.heading("Patient", text="Patient Name")
       tree.heading("Date", text="Date")
       tree.heading("Time", text="Time")
       tree.heading("Status", text="Status")


       # Configure column widths
       tree.column("ID", width=50)
       tree.column("Patient", width=150)
       tree.column("Date", width=100)
       tree.column("Time", width=100)
       tree.column("Status", width=100)


       # Add scrollbar
       scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
       tree.configure(yscrollcommand=scrollbar.set)


       # Pack elements
       tree.pack(side="left", fill="both", expand=True)
       scrollbar.pack(side="right", fill="y")


       # Store reference to tree
       setattr(self, f"{status.lower()}_tree", tree)


       # Load appointments
       self.load_appointments(tree, status)


   def get_appointments_from_db(self):
       """Safely get appointments from database"""
       try:
           appointments_relation = self.db.getRelation("Appointment")
           if appointments_relation is None:
               print("Warning: Appointments relation is None")
               return []


           rows = appointments_relation.getRowsWhereEqual("mhwp_id", self.mhwp_id)
           if rows is None:
               print(f"Warning: No appointments found for MHWP ID {self.mhwp_id}")
               return []


           return rows
       except Exception as e:
           print(f"Error getting appointments: {str(e)}")
           return []


   def get_patient_name(self, patient_id):
       """Safely get patient name from database"""
       try:
           users_relation = self.db.getRelation("Users")
           if users_relation is None:
               return "Unknown"


           patient_rows = users_relation.getRowsWhereEqual("user_id", patient_id)
           if not patient_rows:
               return "Unknown"


           return patient_rows[0][1]  # Assuming name is in second column
       except Exception as e:
           print(f"Error getting patient name: {str(e)}")
           return "Unknown"

   def load_appointments(self, tree, status):
       """Load appointments with specified status"""
       # Clear existing items
       tree.delete(*tree.get_children())

       try:
           appointments_relation = self.db.getRelation("Appointment")
           if appointments_relation is None:
               raise Exception("Could not access Appointments relation")

           # Get all appointments for this MHWP
           appointments = appointments_relation.getRowsWhereEqual("mhwp_id", self.mhwp_id)

           for row in appointments:
               #print(f" Debugging Loading appointment: ID={row[0]}, Status={row[5]}, Looking for status={status}")

               # Create Appointment object from row
               apt = Appointment(
                   appointment_id=row[0],
                   patient_id=row[1],
                   mhwp_id=row[2],
                   date=row[3],
                   status=row[5],
                   room_name=row[4]
               )

               # Only process appointments matching requested status
               if apt.status == status:
                   # Get patient name
                   users_relation = self.db.getRelation("User")
                   patient_rows = users_relation.getRowsWhereEqual("user_id", apt.patient_id)
                   patient_name = patient_rows[0][1] if patient_rows else "Unknown"

                   # Format date and time
                   date_str = apt.date.strftime('%Y-%m-%d')
                   time_str = apt.date.strftime('%H:%M')

                   # Add to tree
                   tree.insert(
                       "",
                       "end",
                       values=(apt.appointment_id, patient_name, date_str, time_str, apt.status)
                   )

       except Exception as e:
           print(f"Error loading appointments: {str(e)}")
           tree.insert("", "end", values=("", "Error loading appointments", "", "", ""))

   def update_appointment_status(self, new_status):
       current_tree = \
       self.notebook.children[self.notebook.select().split('.')[-1]].winfo_children()[0].winfo_children()[0]
       selected_item = current_tree.selection()

       if not selected_item:
           messagebox.showerror("Error", "Please select an appointment")
           return

       try:
           appointment_id = current_tree.item(selected_item)['values'][0]
           appointments_relation = self.db.getRelation("Appointment")

           if new_status == "Confirmed":
               # Get the appointment details
               apt_row = appointments_relation.getRowsWhereEqual("appointment_id", appointment_id)[0]
               apt_date = apt_row[3]
               room = apt_row[4]
               patient_id = apt_row[1]

               # Check for conflicts
               existing_appointments = appointments_relation.getRowsWhereEqual("patient_id", patient_id)
               for row in existing_appointments:
                   if row[0] != appointment_id and row[5] == "Confirmed":  # Skip same appointment and non-confirmed
                       existing_date = row[3]
                       if isinstance(existing_date, datetime):
                           if (existing_date.date() == apt_date.date() and
                                   existing_date.hour == apt_date.hour):
                               messagebox.showerror("Error", "Patient already has an appointment at this time")
                               return

               # Check room availability
               room_appointments = appointments_relation.getRowsWhereEqual("mhwp_id", self.mhwp_id)
               for row in room_appointments:
                   if row[0] != appointment_id and row[5] == "Confirmed":
                       existing_date = row[3]
                       if isinstance(existing_date, datetime):
                           if (existing_date.date() == apt_date.date() and
                                   existing_date.hour == apt_date.hour and
                                   row[4] == room):
                               messagebox.showerror("Error", f"{room} is already booked for this time")
                               return

           appointments_relation.validityChecking = False
           appointments_relation.editFieldInRow(appointment_id, "status", new_status)
           appointments_relation.validityChecking = True

           self.refresh_lists()
           messagebox.showinfo("Success", f"Appointment {new_status.lower()} successfully")

           if new_status in ["Confirmed", "Declined"]:
               row = appointments_relation.getRowsWhereEqual("appointment_id", appointment_id)[0]
               self.send_email_notification(
                   'accept' if new_status == "Confirmed" else 'decline',
                   appointment_id,
                   row[1]
               )

       except Exception as e:
           messagebox.showerror("Error", f"Failed to update appointment: {str(e)}")
           print(f"Detailed error: {str(e)}")

   def send_email_notification(self, notification_type, appointment_id, patient_id):
       """Send email notifications for appointments using Gmail"""
       try:
           # Get appointment and user details
           appointments_relation = self.db.getRelation("Appointment")
           appointment_row = appointments_relation.getRowsWhereEqual("appointment_id", appointment_id)[0]

           users_relation = self.db.getRelation("User")
           patient = users_relation.getRowsWhereEqual("user_id", patient_id)[0]
           mhwp = users_relation.getRowsWhereEqual("user_id", self.mhwp_id)[0]

           # Gmail configuration
           smtp_server = "smtp.gmail.com"
           smtp_port = 587
           sender_email = "serenify.project@gmail.com"
           app_password = "zyis yvtr soop tmoe"
           sender_name = "Serenify App"

           # Get appointment date for the message
           appointment_date = appointment_row[3].strftime('%Y-%m-%d %H:%M')

           if notification_type == 'accept':
               subject = "Appointment Confirmed"
               message = f"The appointment request for {appointment_date} has been confirmed. Please check your dashboard for more details."
           elif notification_type == 'decline':
               subject = "Appointment Declined"
               message = f"The appointment request for {appointment_date} has been declined. Please check your dashboard for more details."
           else:
               subject = "Appointment Update"
               message = f"The appointment status for {appointment_date} has been updated. Please check your dashboard for more details."

           # Send emails using SMTP
           with smtplib.SMTP(smtp_server, smtp_port) as server:
               server.starttls()  # Enable TLS
               server.login(sender_email, app_password)

               # Email to patient
               patient_msg = MIMEText(message)
               patient_msg['Subject'] = subject
               patient_msg['From'] = f"{sender_name} <{sender_email}>"
               patient_msg['To'] = patient[2]
               server.send_message(patient_msg)

               # Email to MHWP
               mhwp_msg = MIMEText(message)
               mhwp_msg['Subject'] = subject
               mhwp_msg['From'] = f"{sender_name} <{sender_email}>"
               mhwp_msg['To'] = mhwp[2]
               server.send_message(mhwp_msg)

       except smtplib.SMTPAuthenticationError:
           print("Failed to authenticate with Gmail. Please check credentials.")
       except smtplib.SMTPException as e:
           print(f"SMTP error occurred: {str(e)}")
       except Exception as e:
           print(f"Failed to send email notifications: {str(e)}")

       except smtplib.SMTPAuthenticationError:
           print("Failed to authenticate with Gmail. Please check credentials.")
       except smtplib.SMTPException as e:
           print(f"SMTP error occurred: {str(e)}")
       except Exception as e:
           print(f"Failed to send email notifications: {str(e)}")


   def refresh_lists(self):
       """Refresh all appointment lists"""
       self.load_appointments(self.pending_tree, "Pending")
       self.load_appointments(self.confirmed_tree, "Confirmed")
       self.load_appointments(self.declined_tree, "Declined")
       self.load_appointments(self.cancelled_tree, "Cancelled")



   def back_to_dashboard(self):
       """Return to main MHWP dashboard"""
       import subprocess
       subprocess.Popen(["python3", "mhwpMain.py"])
       self.root.destroy()


   def on_closing(self):
       """Handle window closing"""
       try:
           if hasattr(self, 'db'):
               self.db.close()
       except Exception as e:
           print(f"Error closing database: {str(e)}")
       self.root.destroy()




if __name__ == "__main__":
   root = tk.Tk()
   # For testing purposes - in production this would come from login
   app = MHWPAppointmentManager(root, mhwp_id=5)
   root.mainloop()
"""Appointment management script for mhwps"""
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from patient.custom_calendar import Calendar
from database.database import Database, Notification

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import Database
from database.entities import Appointment
from sessions import Session



class MHWPAppointmentManager():
   """Initialise the appointment manager for mhwps"""
   def __init__(self):
       sess = Session()
       sess.open()
       mhwp_id = sess.getId()
       self.root = tk.Tk()
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

       self.setup_ui()
       self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
       self.root.mainloop()

   def setup_ui(self):
       """Create and configure the graphical user interface components for the mhwp."""
       # Title
       h1_label = ttk.Label(
           self.root,
           text="Appointment Requests",
           font=("Arial", 24, "bold")
       )
       h1_label.pack(pady=10)

       # Calendar Frame
       calendar_frame = ttk.Frame(self.root)
       calendar_frame.pack(pady=10, padx=10)

       min_date = datetime.now()
       max_date = min_date + timedelta(days=30)
       self.calendar = Calendar(
           calendar_frame,
           mindate=min_date,
           maxdate=max_date,
           date_pattern='yyyy-mm-dd'
       )
       self.calendar.pack()
       self.calendar.bind('<<CalendarSelected>>', lambda e: self.show_day_appointments())

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

       # Setup appointment lists
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
           text="Cancel Selected",
           command=lambda: self.cancel_confirmed_appointment()
       ).pack(side='left', padx=5)

       ttk.Button(
           button_frame,
           text="Show all",
           command=self.refresh_lists
       ).pack(side='left', padx=5)

       ttk.Button(
           button_frame,
           text="Back to Dashboard",
           command=self.back_to_dashboard
       ).pack(side='left', padx=5)

   def show_day_appointments(self):
       """Display appointments for the selected day in the calendar"""
       selected_date = self.calendar.get_date()
       try:
           appointments_relation = self.db.getRelation("Appointment")
           day_appointments = appointments_relation.getRowsWhereEqual("mhwp_id", self.mhwp_id)

           # Clear all trees
           for status in ["Pending", "Confirmed", "Declined", "Cancelled"]:
               tree = getattr(self, f"{status.lower()}_tree")
               tree.delete(*tree.get_children())

           # Process appointments for selected date
           for row in day_appointments:
               apt_date = row[3]
               if isinstance(apt_date, datetime):
                   if apt_date.strftime('%Y-%m-%d') == selected_date:
                       apt = Appointment(
                           appointment_id=row[0],
                           patient_id=row[1],
                           mhwp_id=row[2],
                           date=row[3],
                           status=row[5],
                           room_name=row[4]
                       )

                       # Get patient name
                       users_relation = self.db.getRelation("User")
                       patient_rows = users_relation.getRowsWhereEqual("user_id", apt.patient_id)
                       patient_name = patient_rows[0][1] if patient_rows else "Unknown"

                       # Format date and time
                       date_str = apt.date.strftime('%Y-%m-%d')
                       time_str = apt.date.strftime('%H:%M')

                       # Add to appropriate tree based on status
                       tree = getattr(self, f"{apt.status.lower()}_tree")
                       tree.insert(
                           "",
                           "end",
                           values=(apt.appointment_id, patient_name, date_str, time_str, apt.status)
                       )

       except Exception as e:
           print(f"Error loading appointments: {str(e)}")

   def get_day_appointments(self, date_str):
       """Retrieve all appointments for specified day"""
       appointments = []
       try:
           appointments_relation = self.db.getRelation("Appointment")
           all_appointments = appointments_relation.getRowsWhereEqual("mhwp_id", self.mhwp_id)

           for row in all_appointments:
               apt_date = row[3]
               if isinstance(apt_date, datetime):
                   if apt_date.strftime('%Y-%m-%d') == date_str:
                       appointments.append(row)
       except Exception as e:
           print(f"Error getting appointments: {str(e)}")
       return appointments

   def setup_appointment_list(self, parent, status):
       """Set up the appointment list interface, including a Treeview for displaying appointments"""
       main_frame = ttk.Frame(parent)
       main_frame.pack(fill="both", expand=True)

       list_frame = ttk.Frame(main_frame)
       list_frame.pack(side="right", fill="both", expand=True)

       tree = ttk.Treeview(
           list_frame,
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
       scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=tree.yview)
       tree.configure(yscrollcommand=scrollbar.set)

       # Pack elements
       tree.pack(side="left", fill="both", expand=True)
       scrollbar.pack(side="right", fill="y")

       # Store reference to tree
       setattr(self, f"{status.lower()}_tree", tree)

       # Load appointments initially
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
       """Updates the status of a specific appointment in the database"""
       current_tab = self.notebook.select()
       status = "pending" if new_status in ["Confirmed", "Declined"] else new_status.lower()
       current_tree = getattr(self, f"{status}_tree")
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
                   if row[0] != appointment_id and row[5] in ["Pending",
                                                              "Confirmed"]:  # Check both pending and confirmed
                       existing_date = row[3]
                       if isinstance(existing_date, datetime):
                           if (existing_date.date() == apt_date.date() and
                                   existing_date.hour == apt_date.hour):
                               messagebox.showerror("Error", "Patient already has an appointment at this time")
                               return

               # Check room availability
               room_appointments = appointments_relation.getRowsWhereEqual("mhwp_id", self.mhwp_id)
               for row in room_appointments:
                   if row[0] != appointment_id and row[5] in ["Pending", "Confirmed"]:
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

   def cancel_confirmed_appointment(self):
       selected_item = self.confirmed_tree.selection()
       if not selected_item:
           messagebox.showerror("Error", "Please select a confirmed appointment")
           return
       try:
           appointment_id = self.confirmed_tree.item(selected_item)['values'][0]

           # Update the status in the database
           appointments_relation = self.db.getRelation("Appointment")
           appointments_relation.validityChecking = False
           appointments_relation.editFieldInRow(appointment_id, "status", "Cancelled")
           appointments_relation.validityChecking = True
           self.selected_patient = self.db.getRelation("Appointment").getRowsWhereEqual('appointment_id',appointment_id)[0][1]
           # Refresh the appointment lists
           self.refresh_lists()
           messagebox.showinfo("Success", "Confirmed appointment canceled successfully")
           newnotify = Notification(
               user_id=self.selected_patient,
               notifycontent="AppointmentCanceled",
               source_id=0,
               new=True,
               timestamp=datetime.now(),
           )
           self.db.insert_notification(newnotify)
           # Optionally send an email notification about the cancellation
           row = appointments_relation.getRowsWhereEqual("appointment_id", appointment_id)[0]
           self.send_email_notification('cancel', appointment_id, row[Appointment.PATIENT_ID])

       except Exception as e:
           messagebox.showerror("Error", f"Failed to cancel appointment: {str(e)}")
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
               notifyinfo = "AppointmentConfirmed"
               message = f"The appointment request for {appointment_date} has been confirmed. Please check your dashboard for more details."
               newnotify = Notification(
                   user_id=patient_id,
                   notifycontent=notifyinfo,
                   source_id=0,
                   new=True,
                   timestamp=datetime.now(),
               )
               self.db.insert_notification(newnotify)
           elif notification_type == 'decline':
               subject = "Appointment Declined"
               notifyinfo = "AppointmentDeclined"
               message = f"The appointment request for {appointment_date} has been declined. Please check your dashboard for more details."
               newnotify = Notification(
                   user_id=patient_id,
                   notifycontent=notifyinfo,
                   source_id=0,
                   new=True,
                   timestamp=datetime.now(),
               )
               self.db.insert_notification(newnotify)
           elif notification_type == 'cancel':
                subject = "Appointment Cancelled"
                notifyinfo = "AppointmentCancelled"
                message = f"The appointment request for {appointment_date} has been cancelled. Please check your dashboard for more details."
                newnotify = Notification(
                    user_id=patient_id,
                    notifycontent=notifyinfo,
                    source_id=0,
                    new=True,
                    timestamp=datetime.now(),
                )
                self.db.insert_notification(newnotify)
           else:
               subject = "Appointment Update"
               notifyinfo = "Appointment Upated"
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



   def refresh_lists(self):
       """Refresh all appointment lists"""
       self.load_appointments(self.pending_tree, "Pending")
       self.load_appointments(self.confirmed_tree, "Confirmed")
       self.load_appointments(self.declined_tree, "Declined")
       self.load_appointments(self.cancelled_tree, "Cancelled")



   def back_to_dashboard(self):
       """Return to main MHWP dashboard"""
       self.db.close()
       self.root.destroy()
       import subprocess
       subprocess.Popen(["python3", "mhwp/mhwp_dashboard.py"])


   def on_closing(self):
       """Handle window closing"""
       try:
           if hasattr(self, 'db'):
               self.db.close()
       except Exception as e:
           print(f"Error closing database: {str(e)}")
       self.root.destroy()
       import subprocess
       subprocess.Popen(["python3", "mhwp/mhwp_dashboard.py"])



if __name__ == "__main__":

   # For testing purposes - in production this would come from login
   app = MHWPAppointmentManager()

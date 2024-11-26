import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
from patient.custom_calendar import Calendar
from datetime import datetime, timedelta
import traceback
import smtplib
from email.mime.text import MIMEText




# Fixed import path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database'))
sys.path.append(project_root)


from database.database import Database
from database.entities import Appointment
from database.dataStructs import Row





class AppointmentBooking:
   def __init__(self, root, patient_id, mhwp_id):
       self.root = root
       self.root.title("Appointment Booking System")
       self.patient_id = patient_id
       self.mhwp_id = mhwp_id

############# Not sure if this is correct so only commented it out
#     # Back button
#     self.back_button = tk.Button(root, text="Back", command=self.backButton)
#     self.back_button.pack()

#     def backButton(self):
#         subprocess.Popen(["python3", "patient/patientMain.py"])
#         self.root.destroy()


       # Initialise database connection
       try:
           self.db = Database()
           self.db.printAll()
       except Exception as e:


           messagebox.showerror("Database Error", f"Failed to connect to database: {str(e)} {str(traceback.format_exception(e))}")
           self.root.destroy()
           return

       # Available rooms list
       self.available_rooms = ["Room A", "Room B", "Room C"]  # You can modify this list as needed
       self.room_var = tk.StringVar()
       self.room_var.set(self.available_rooms[0])  # Set default room


       self.setup_ui()


       # Ensure database is closed when window is closed
       self.root.protocol("WM_DELETE_WINDOW", self.on_closing)


   def setup_ui(self):
       # Title
       h1_label = ttk.Label(
           self.root,
           text="Book an appointment with your practitioner",
           font=("Arial", 24, "bold")
       )
       h1_label.pack(pady=10)


       # Calendar Frame
       calendar_frame = ttk.Frame(self.root)
       calendar_frame.pack(pady=10, padx=10)


       # Create calendar with date range restriction
       min_date = datetime.now()
       max_date = min_date + timedelta(days=30)
       self.calendar = Calendar(
           calendar_frame,
           mindate=min_date,
           maxdate=max_date,
           date_pattern='yyyy-mm-dd'
       )
       self.calendar.pack()


       # Time Slots Frame
       time_frame = ttk.LabelFrame(self.root, text="Available Time Slots")
       time_frame.pack(pady=10, padx=10, fill="x")

       # Add Room Selection Frame
       room_frame = ttk.LabelFrame(self.root, text="Select Room")
       room_frame.pack(pady=10, padx=10, fill="x")

       # Add room selection radio buttons
       for room in self.available_rooms:
           ttk.Radiobutton(
               room_frame,
               text=room,
               value=room,
               variable=self.room_var
           ).pack(anchor='w', padx=5)


       # Time slots (9 AM to 5 PM, hourly slots)
       self.time_var = tk.StringVar()
       self.update_available_times()  # New method to show only available times


       # Buttons Frame
       button_frame = ttk.Frame(self.root)
       button_frame.pack(pady=10)


       ttk.Button(
           button_frame,
           text="Request Appointment",
           command=self.request_appointment
       ).pack(side='left', padx=5)


       ttk.Button(
           button_frame,
           text="Cancel Appointment",
           command=self.cancel_appointment
       ).pack(side='left', padx=5)


       ttk.Button(
           button_frame,
           text="Back",
           command=self.back_to_main
       ).pack(side='left', padx=5)


       # Appointments List
       list_frame = ttk.LabelFrame(self.root, text="Your Appointments")
       list_frame.pack(pady=10, padx=10, fill="both", expand=True)


       self.appointments_list = ttk.Treeview(
           list_frame,
           columns=("DateTime", "Room", "Status"),
           show="headings"
       )
       self.appointments_list.heading("DateTime", text="Date/Time")
       self.appointments_list.heading("Room", text="Room")
       self.appointments_list.heading("Status", text="Status")
       self.appointments_list.pack(fill="both", expand=True)


       # Bind calendar selection to update available times
       self.calendar.bind('<<CalendarSelected>>', lambda e: self.update_available_times())


       self.load_appointments()


   def update_available_times(self):
       """Update available time slots based on existing appointments"""
       selected_date = self.calendar.get_date()
       all_times = [f"{hour:02d}:00" for hour in range(9, 17)]


       # Clear existing time slots
       for widget in self.root.nametowidget(self.root.winfo_children()[2]).winfo_children():
           if isinstance(widget, ttk.Radiobutton):
               widget.destroy()


       # Get booked times for selected date
       booked_times = self.get_booked_times(selected_date)


       # Create new time slots, excluding booked times
       for time in all_times:
           if time not in booked_times:
               ttk.Radiobutton(
                   self.root.nametowidget(self.root.winfo_children()[2]),
                   text=time,
                   value=time,
                   variable=self.time_var
               ).pack(anchor='w', padx=5)

   def get_booked_times(self, date_str):
       """Get list of booked times for a specific date"""
       booked_times = set()
       try:
           appointments_relation = self.db.getRelation("Appointment")
           # Get appointments for this patient instead of MHWP
           existing_appointments = appointments_relation.getRowsWhereEqual("patient_id", self.patient_id)

           for row in existing_appointments:
               apt_date = row[3]
               if isinstance(apt_date, datetime):
                   if apt_date.strftime('%Y-%m-%d') == date_str and row[5] != 'Cancelled':
                       booked_times.add(apt_date.strftime('%H:%M'))
       except Exception as e:
           print(f"Error getting booked times: {str(e)}")

       return booked_times


   def is_timeslot_available(self, date_time):
       """Check if a timeslot is available"""
       appointments_relation = self.db.getRelation("Appointment")
       existing_appointments = appointments_relation.getRowsWhereEqual("mhwp_id", self.mhwp_id)


       for row in existing_appointments:
           apt_date = row[3]
           if isinstance(apt_date, datetime):
               # Check for same day and hour
               if (apt_date.date() == date_time.date() and
                       apt_date.hour == date_time.hour):
                   return False
       return True

   def request_appointment(self):
       date_str = self.calendar.get_date()
       time_str = self.time_var.get()
       room = self.room_var.get()

       if not time_str:
           messagebox.showerror("Error", "Please select a time slot")
           return

       try:
           date_time = datetime.strptime(f"{date_str} {time_str}", '%Y-%m-%d %H:%M')
           appointments_relation = self.db.getRelation("Appointment")
           patient_appointments = appointments_relation.getRowsWhereEqual("patient_id", self.patient_id)

           # Check for existing appointments at same time
           for row in patient_appointments:
               apt_date = row[3]
               if isinstance(apt_date, datetime):
                   if (apt_date.date() == date_time.date() and
                           apt_date.hour == date_time.hour and
                           row[5] != 'Cancelled'):
                       messagebox.showerror("Error", "You already have an appointment at this time")
                       return

           # Check if room is available at this time
           existing_appointments = appointments_relation.getRowsWhereEqual("mhwp_id", self.mhwp_id)
           for row in existing_appointments:
               apt_date = row[3]
               if isinstance(apt_date, datetime):
                   if (apt_date.date() == date_time.date() and
                           apt_date.hour == date_time.hour and
                           row[4] == room and
                           row[5] != 'Cancelled'):
                       messagebox.showerror("Error", f"{room} is already booked for this time")
                       return

           new_appointment = Appointment(
               patient_id=self.patient_id,
               mhwp_id=self.mhwp_id,
               date=date_time,
               status="Pending",
               room_name=room
           )

           self.db.insert_appointment(new_appointment)
           self.load_appointments()
           messagebox.showinfo("Success", "Appointment requested successfully")
           self.send_email_notification('request')

       except Exception as e:
           messagebox.showerror("Error", f"Failed to create appointment: {str(e)}")


   def load_appointments(self):
       """Load and display appointments in the treeview"""
       self.db.printAll()
       appointments_relation = self.db.getRelation('Appointment')
       appointments = appointments_relation.getRowsWhereEqual('patient_id', self.patient_id)
       print("this is new appts", appointments)


       # Clear existing items
       for item in self.appointments_list.get_children():
           self.appointments_list.delete(item)


       # Add appointments to treeview
       for row in appointments:
           apt_date = row[3]
           room_name = row[4]
           status = row[5]


           if isinstance(apt_date, datetime):
               formatted_date = apt_date.strftime('%Y-%m-%d %H:%M')
               self.appointments_list.insert('', 'end', values=(formatted_date, room_name, status))

   def cancel_appointment(self):
       selected_item = self.appointments_list.selection()
       if not selected_item:
           messagebox.showerror("Error", "Please select an appointment to cancel")
           return

       values = self.appointments_list.item(selected_item)['values']
       date_str = values[0]

       confirm = messagebox.askyesno(
           "Confirm Cancellation",
           "Are you sure you want to cancel this appointment?"
       )

       if not confirm:
           return

       try:
           appointments_relation = self.db.getRelation("Appointment")
           appointments = appointments_relation.getRowsWhereEqual("patient_id", self.patient_id)

           for row in appointments:
               apt_date = row[3]
               if isinstance(apt_date, datetime):
                   if apt_date.to_pydatetime().strftime('%Y-%m-%d %H:%M') == date_str:
                       self.update_appointment_status(row[0], "Cancelled")
                       break

           self.load_appointments()
           self.update_available_times()
           self.send_email_notification('cancel')
           messagebox.showinfo("Success", "Appointment cancelled successfully")

       except Exception as e:
           messagebox.showerror("Error", f"Failed to cancel appointment: {str(e)}")
           print(f"Detailed error: {str(e)}")

   def update_appointment_status(self, appointment_id, new_status):
       try:
           appointments_relation = self.db.getRelation("Appointment")
           current_apt = appointments_relation.getRowsWhereEqual("appointment_id", appointment_id)[0]

           appointments_relation.validityChecking = False
           appointments_relation.editFieldInRow(appointment_id, "status", new_status)
           appointments_relation.validityChecking = True

           self.load_appointments()
           self.update_available_times()
           self.send_email_notification('cancel')


       except Exception as e:
           messagebox.showerror("Error", f"Failed to cancel appointment: {str(e)}")
           print(f"Detailed error: {str(e)}")

   def send_email_notification(self, notification_type):
       try:
           users_relation = self.db.getRelation("User")
           patient = users_relation.getRowsWhereEqual("user_id", self.patient_id)[0]

           # Get MHWP ID directly from allocations
           allocations_relation = self.db.getRelation("Allocation")
           allocation = allocations_relation.getRowsWhereEqual("patient_id", self.patient_id)[0]
           mhwp_id = allocation[3]  # Get mhwp_id from allocation
           mhwp = users_relation.getRowsWhereEqual("user_id", mhwp_id)[0]


           # Gmail configuration
           smtp_server = "smtp.gmail.com"
           smtp_port = 587
           sender_email = "serenify.project@gmail.com"
           app_password = "zyis yvtr soop tmoe"
           sender_name = "Serenify App"

           appointment_datetime = f"{self.calendar.get_date()} {self.time_var.get()}"

           if notification_type == 'request':
               subject = "New Appointment Request"
               message = f"An appointment has been requested for {appointment_datetime}. Please check your dashboard for more details."
           elif notification_type == 'cancel':
               subject = "Appointment Cancelled"
               message = f"The appointment scheduled for {appointment_datetime} has been cancelled."
           else:
               subject = "Appointment Update"
               message = "Your appointment status has been updated."

           # Debug prints
           print(f"Attempting to send email...")
           print(f"From: {sender_email}")
           print(f"To (Patient): {patient[2]}")
           print(f"To (MHWP): {mhwp[2]}")
           print(f"Subject: {subject}")

           # Send emails using SMTP with explicit error handling
           server = smtplib.SMTP(smtp_server, smtp_port)
           server.set_debuglevel(1)  # Add debug information

           # Establish secure connection
           try:
               server.ehlo()
               server.starttls()
               server.ehlo()
               print("TLS connection established")
           except Exception as e:
               print(f"TLS connection failed: {str(e)}")
               raise

           # Login
           try:
               server.login(sender_email, app_password)
               print("Login successful")
           except Exception as e:
               print(f"Login failed: {str(e)}")
               raise

           # Send emails
           try:
               # Email to MHWP
               mhwp_msg = MIMEText(message)
               mhwp_msg['Subject'] = subject
               mhwp_msg['From'] = f"{sender_name} <{sender_email}>"
               mhwp_msg['To'] = mhwp[2]
               server.send_message(mhwp_msg)
               print("MHWP email sent successfully")

               # Email to patient
               patient_msg = MIMEText(message)
               patient_msg['Subject'] = subject
               patient_msg['From'] = f"{sender_name} <{sender_email}>"
               patient_msg['To'] = patient[2]
               server.send_message(patient_msg)
               print("Patient email sent successfully")

           except Exception as e:
               print(f"Failed to send message: {str(e)}")
               raise
           finally:
               server.quit()

       except smtplib.SMTPAuthenticationError as e:
           print(f"Authentication failed: {str(e)}")
       except smtplib.SMTPException as e:
           print(f"SMTP error occurred: {str(e)}")
       except Exception as e:
           print(f"Failed to send email notifications. Error: {str(e)}")
           print(f"Error type: {type(e)}")
           import traceback
           print(f"Traceback: {traceback.format_exc()}")

   def back_to_main(self):
       """Return to main patient screen"""
       import subprocess
       subprocess.Popen(["python3", "patientMain.py"])
       self.root.destroy()


   def on_closing(self):
       """Handle window closing"""
       self.db.close()
       root.destroy()
       # try:
       #     if hasattr(self, 'db'):
       #         self.db.close()
       # # except Exception as e:
       #     print(f"Error closing database: {str(e)}")
       # self.root.destroy()




if __name__ == "__main__":
   root = tk.Tk()
   db = Database()
   allocation = db.getRelation("Allocation").getRowsWhereEqual("patient_id", 4)[0]
   app = AppointmentBooking(root, patient_id=4, mhwp_id=allocation[3])
   root.mainloop()
   
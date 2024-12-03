
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.initDBwithDummyData_FeatureTest import initDummyDatabase
from sessions import Session
from database.database import Database
import tkinter as tk
from mhwp.mhwp_dashboard import openmhwpdashboard
# from addfeature.chatroom import startchatroom
# from addfeature.notificationbox import opennotification
from patient.patient_dashboard import openpatientdashboard
# from addfeature.forum import openforsum
# from patient.exercises import Exercises
from patient.patientMain import Patient

db=Database()
sess = Session()
sess._initialize()
sess.open()
sess.setId(3)
sess.setRole(db.getRelation('User').getRowsWhereEqual("user_id",sess.getId())[0][6])
sess.close()
db.close()

# subprocess.Popen(["python3", "mhwp/mhwp_dashboard.py"])

# root = tk.Tk()
# app = Patient(root)
# root.mainloop()
exec(open("patient/patientMain.py").read())
# openmhwpdashboard()
# openpatientdashboard()
# openrating()
# opennotification()
# openforsum()
# Exercises()
# startchatroom(userID,"Patient")
# MHWPAppointmentManager(root,userID)

# db.close()



# print("program finished")
# userID= 5
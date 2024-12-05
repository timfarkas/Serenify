
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.initDBwithDummyData_FeatureTest import initDummyDatabase
from sessions import Session
from database.database import Database
import tkinter as tk
from mhwp.mhwp_dashboard import MHWPDashboard
# from addfeature.chatroom import startch
# atroom
# from addfeature.notificationbox import opennotification
from patient.patient_dashboard import openpatientdashboard
from patient.patientMain import Patient
from addfeature.forum import openforsum
from patient.exercises import Exercises

db=Database()
sess = Session()
sess._initialize()
sess.open()
sess.setId(9)
sess.setRole(db.getRelation('User').getRowsWhereEqual("user_id",sess.getId())[0][6])
sess.close()
db.close()
#
exec(open("patient/patientMain.py").read())
# MHWPDashboard()
# Exercises()
# subprocess.Popen(["python3", "mhwp/mhwp_dashboard.py"])


# Patient()

# exec(open("patient/patientMain.py").read())

# openpatientdashboard()
# openrating()
# opennotification()
# openforsum()
#
# startchatroom(userID,"Patient")
# MHWPAppointmentManager(root,userID)

# db.close()



# print("program finished")
# userID= 5
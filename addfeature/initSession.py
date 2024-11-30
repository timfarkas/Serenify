import os
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.initDBwithDummyData_FeatureTest import initDummyDatabase
from sessions import Session
from database.database import Database

from mhwp.mhwp_dashboard import openmhwpdashboard
from addfeature.chatroom import startchatroom
from addfeature.notificationbox import opennotification
from patient.patient_dashboard import openpatientdashboard
from addfeature.forum import openforsum
from patient.exercises import Exercises

db=Database()

sess = Session()
sess._initialize()
sess.open()
sess.setId(3)
sess.setRole("Patient")
sess.close()


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
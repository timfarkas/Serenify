import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database'))
sys.path.append(project_root)

from .globalvariables import db,userID
from .notificationbox import opennotification
from .chatroom import startchatroom
from .mhwp_dashboard import openmhwpdashboard
from .forum import openforsum
from .mhwp_rating import openrating
from mhwp.booking import MHWPAppointmentManager
from patient.exercises import Exercises
from .patient_dashboard import openpatientdashboard

global db
userID=5
openmhwpdashboard(userID)

# openpatientdashboard(userID)
# openrating(userID)
# opennotification(userID)
# # openforsum(userID)
# Exercises(userID)
#

# root = tk.Tk()
# MHWPAppointmentManager(root,userID)



# root.mainloop()
db.close()




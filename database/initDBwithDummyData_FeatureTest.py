"""
This class is deprecated and will be deleted soon.
"""

import os
import sys

# Get the absolute path of the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the project root to sys.path if it's not already there
if project_root not in sys.path:
    sys.path.append(project_root)

# Now absolute imports will work
from .database import Database
from .entities import Admin, Patient, MHWP, PatientRecord, Allocation, JournalEntry, Appointment,MoodEntry,MHWPReview,ChatContent,Forum,Notification,ExerRecord
import datetime
import database.initDummyData

import logging

"""
This class is deprecated and will be deleted soon.
"""

# Test functions
def initDummyDatabase(db: Database):
    logging.warning("\n\nWARNING, this way of calling initDummyDatabase is deprecated, please use initDummyData.initDummyDatabase (instead of initDBwithDummyData_FeatureTest.initDummyDatabase, changed for brevity).\n\n")
    database.initDummyData.initDummyDatabase(db, printOut=True)
    logging.warning("\n\n WARNING, this way of calling initDummyDatabase is deprecated, please use initDummyData.initDummyDatabase (instead of initDBwithDummyData_FeatureTest.initDummyDatabase, changed for brevity).\n\n initDummyDatabase merges dummy data of initDBwithDummyData_FeatureTest and initDBwithDummyData into one.")



if __name__ == "__main__":
    db = Database(overwrite=True)
    initDummyDatabase(db)
    db.close()

"""
This class is deprecated and will be deleted soon.
"""
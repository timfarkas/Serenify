import sys
import os
import datetime
from .database import Database
from .entities import UserError, RecordError, Admin, Patient, MHWP, PatientRecord, Allocation, JournalEntry, Appointment

from .initDBwithDummyData import initDummyDatabase

##### DB INIT FOR TESTING
### Initialize the database with dummy data and save it
db = Database(overwrite=True)  ### this causes the database to be initialized from scratch and overwrites any changes
initDummyDatabase(db)
db.close()

##### DB OPENING
### reopen database
db = Database()

##### DB QUERIES
### get User relation (table) via db.getRelation(entityName)
print("Getting and printing relation 'User':")
userRelation = db.getRelation('User')
print(userRelation)

### GET the rows WHERE username == 'patient2' and
### count number of results
##### using anyRelation.getWhereEqual(attributeName, value)
##### and len(anyRelation)
user = userRelation.getWhereEqual('username', 'patient1')
print(f"Found {len(user)} user with username patient1.")

### get the IDs where username == 'patient2'
userIDs = userRelation.getIDsWhereEqual('username', 'patient1')
print(f"List of ids found: {userIDs}")
userId = userIDs[0]  ### get first element of userIDs (we are assuming there is only one user with any given username)

### get PatientRecord relation
recordsRelation = db.getRelation('PatientRecord')

db.printAll()
## filter for patient records corresponding to userId
userRecords = recordsRelation.getWhereEqual('patient_id', userId)
print(f"\n\nFound {len(userRecords)} record entries for user")
print(userRecords)

## filter for patient records corresponding to mhwp id with condition
mhwpId = 3  ### you can get this from session or database, hardcoded for demo

#### chaining together queries
filteredRecords = recordsRelation.getWhereEqual('mhwp_id', mhwpId).getWhereEqual('conditions', ['Anxiety'])
print(f"\n\nFound {len(filteredRecords)} record entries for that MHWP and Anxiety")
print(filteredRecords)

#### INSERTING

## prepare a JournalEntry object
patId = 3  ### you can get this from session, hardcoded for demo
entry = JournalEntry(
    entry_id=None,  # id will get chosen automatically upon insertion
    patient_id=patId,
    text="Today I had a really weird dream... The whole world was ...",
    timestamp=datetime.datetime.now()
)

db.insert_journal_entry(entry)

db.close()  ## exit db, saving state

### load database again and print journal entries to confirm that entry was saved between sessions

db = Database()
print("Get Journal:")
print(db.getRelation('JournalEntry'))

# EDITING ROWS OR SINGLE FIELDS

userRelation = db.getRelation('User')

# Update the entire row for the user with id=1
userRelation.editRow(primaryKey=1, newValues=['patient1',
                                              'password1',
                                              'John',
                                              'Doe',
                                              'john.doe@example.com',
                                                None, None, None, False])

# edit a single field in a row
# update the email of the user with id=1
userRelation.editFieldInRow(1, targetAttribute='email', value='john.doe@newdomain.com')

# Print the updated relation to verify changes
print("Updated User Relation:")
print(userRelation)

#### DELETING ROWS
appointmentsRelation = db.getRelation('Appointment')
print(appointmentsRelation)

### gets last schedule appointment by getting row with maximum primary key
lastScheduledAppointment = appointmentsRelation.getAttributeMaxRow(appointmentsRelation.primaryKeyName)
lastScheduleAppointmentId = lastScheduledAppointment[0]  ## index 0 is always primary key

## get relation
appointmentsRelation = db.getRelation('Appointment')

## deletes one row using its primary key (appointmentId)
appointmentsRelation.dropRows(id=lastScheduleAppointmentId)

print("")
print(appointmentsRelation)

### delete multiple rows using multiple keys
userRelation = db.getRelation('User')
rowIDs = userRelation.getAllRowIDs()  ## get all keys
userRelation.dropRows(ids=rowIDs)

print("User relation after deleting all rows:")  ## of course, this also works for any subset of rows
print(userRelation.getAllRowIDs())

db.close()  # Close database at the end of session to ensure changes are saved between sessions

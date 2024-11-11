import sys
import os
import datetime
import entities

from database import Database
from initDBwithDummyData import initDummyDatabase

##### DB INIT FOR TESTING
### Initialize the database with dummy data and save it
db = Database(overwrite = True) ### this causes the database to be initialized from scratch and overwrites any changes
initDummyDatabase(db)
db.close()

##### DB OPENING
### reopen database
db = Database()

##### DB QUERIES
### get Users relation (table) via db.getRelation(entityName)
print("Getting and printing relation 'Users':")
userRelation = db.getRelation('Users')
print(userRelation)

### GET the rows WHERE username == 'patient2' and 
### count number of results 
##### using anyRelation.getWhereEqual(attributeName, value)
##### and len(anyRelation)
user = userRelation.getWhereEqual('username','patient2')
print(f"Found {len(user)} user with username patient2.")

### get the IDs where username == 'patient2' 
userIds = userRelation.getIdsWhereEqual('username','patient2')
print(f"List of ids found: {userIds}")
userId = userIds[0]    ### get first element of userIds (we are assuming there is only one user with any given username)


### get patient records relation
recordsRelation = db.getRelation('PatientRecords')

## filter for patient records corresponding to userId
userRecords=recordsRelation.getWhereEqual('patient_id',userId)
print(f"\n\nFound {len(userRecords)} record entries for user")
print(userRecords)

## filter for patient records corresponding to mhwp id with condition
mhwpId = 3 ### you can get this from session or database, hardcoded for demo

#### chaining together queries
filteredRecords = recordsRelation.getWhereEqual('mhwp_id',mhwpId).getWhereEqual('conditions',['Anxiety'])
print(f"\n\nFound {len(filteredRecords)} record entries for that MHWP and Anxiety")
print(filteredRecords)

#### INSERTING

## prepare a JournalEntry object
patId = 3 ### you can get this from session, hardcoded for demo
entry = entities.JournalEntry(
                entry_id=None, # id will get chosen automatically upon insertion
                patient_id=patId,
                text="Today I had a really weird dream... The whole world was ...",
                timestamp=datetime.datetime.now()
            )

db.insert_journal_entry(entry)

db.close() ## exit db, saving state

### load database again and print journal entries to confirm that entry was saved between sessions
db = Database()
print(db.getRelation('JournalEntries'))
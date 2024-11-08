# Serenify Project Notes

[Todd's diagram of overall structure](https://lucid.app/lucidspark/0daace95-f237-4da9-b69d-43f0215e82d1/edit?invitationId=inv_7aa9b477-44f2-47d7-93aa-e2f762b3ea6f&page=0_0#)

[Aleksandra's task allocation plan](task_allocation.pdf)

# Set-up
## Front End
<!-- tkinter is a standalone library within Python so does not require terminal commands -->
### Please check out the 2 comments on watch_tkinter.py, you may need to make slight changes depending on what you're working on


<!-- Download watchdog so that you have an automatically live preview to show you how your work looks for the user on the frontend. -->

### Do:
<p>pip install watchdog</p>

### If that doesnt work:
<p>pip3 install watchdog</p> 

## Back End
Entity relationship diagram
![ER diagram](database/ERdiagram/serenify_erd.png)

#### General code whenever dealing with data storage

```python
from database.database import Database
db = Database() ## opens database (loading all previously stored info automatically)

### INSERT CODE FOR STORING/RETRIEVING DATA HERE

db.close() ## Saves the database state to storage and closes it (IMPORTANT, CHANGES WON'T BE SAVED OTHERWISE)
```

#### Example of how you can init a patient
```python
from database.database import Database, Patient
db = Database() ## opens database
### insert logic on getting user details from user
patient1 = Patient(user_id, username, password, name, email, emergency_contact_email, mood, mood_comment, is_disabled)
db.insert_patient(patient1)
db.close() # Save the database state and closes it 

 
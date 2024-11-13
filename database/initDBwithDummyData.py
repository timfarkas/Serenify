import os
import sys

# Get the absolute path of the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the project root to sys.path if it's not already there
if project_root not in sys.path:
    sys.path.append(project_root)

# Now absolute imports will work
from database import Database
from entities import UserError, RecordError, Admin, Patient, MHWP, PatientRecord, Allocation, JournalEntry, Appointment
import datetime


# Test functions
def initDummyDatabase(db: Database):
    
    try:
        # Create User objects
        admin_user = Admin(user_id=1, username='admin1', password='pass123')
        patient_user = Patient(
            user_id=2,
            username='patient1',
            password='pass123',
            fName='John',
            lName='Doe',
            email='johndoe@example.com'
        )
        mhwp_user = MHWP(
            user_id=3,
            username='mhwp1',
            password='pass123',
            fName='Dr. Martin',
            lName='Smith',
            email='drsmith@example.com',
            specialization='Psychology'
        )

        # Insert Admin, Patient & User
        db.insert_admin(admin_user)
        db.insert_patient(patient_user)
        db.insert_mhwp(mhwp_user)

        # Allocate mhwp to patient and insert allocation into database
        allocation = Allocation(
            allocation_id=1,
            admin_id=admin_user.user_id,
            patient_id=patient_user.user_id,
            mhwp_id=mhwp_user.user_id,
            start_date=datetime.datetime.now(),
            end_date=datetime.datetime.now()
            #start_date=datetime('2024-01-01'),
            #end_date='2025-12-31'
        )

        db.insert_allocation(allocation)

        # Create JournalEntry object and insert
        journal_entry = JournalEntry(
            entry_id=1,
            patient_id=patient_user.user_id,
            text='Feeling bad now.',
            score=1,
            timestamp=datetime.datetime(year=2024, month=9, day=23, hour=15, minute=30, second=0)#'2024-11-07 14:26:00'
        )
        db.insert_journal_entry(journal_entry)
        journal_entry3 = JournalEntry(
            entry_id=3,
            patient_id=patient_user.user_id,
            text='Get better.',
            score=2,
            timestamp=datetime.datetime(year=2024, month=9, day=28, hour=12, minute=0, second=0)
        )
        db.insert_journal_entry(journal_entry3)
        journal_entry4 = JournalEntry(
            entry_id=4,
            patient_id=patient_user.user_id,
            text='Much better now.',
            score=3,
            timestamp=datetime.datetime(year=2024, month=10, day=2, hour=15, minute=0, second=0)
        )
        db.insert_journal_entry(journal_entry4)

        journal_entry5 = JournalEntry(
            entry_id=5,
            patient_id=patient_user.user_id,
            text='About the same.',
            score=3,
            timestamp=datetime.datetime(year=2024, month=10, day=4, hour=8, minute=0, second=0)
        )
        db.insert_journal_entry(journal_entry5)

        journal_entry6 = JournalEntry(
            entry_id=6,
            patient_id=patient_user.user_id,
            text='Get worse a little.',
            score=2,
            timestamp=datetime.datetime(year=2024, month=10, day=10, hour=20, minute=0, second=0)
        )
        db.insert_journal_entry(journal_entry6)

        journal_entry7 = JournalEntry(
            entry_id=7,
            patient_id=patient_user.user_id,
            text='Feel pretty good today.',
            score=4,
            timestamp=datetime.datetime(year=2024, month=10, day=15, hour=18, minute=0, second=0)
        )
        db.insert_journal_entry(journal_entry7)

        journal_entry8 = JournalEntry(
            entry_id=8,
            patient_id=patient_user.user_id,
            text='Still feel good.',
            score=4,
            timestamp=datetime.datetime(year=2024, month=10, day=20, hour=18, minute=0, second=0)
        )
        db.insert_journal_entry(journal_entry8)

        journal_entry9 = JournalEntry(
            entry_id=9,
            patient_id=patient_user.user_id,
            text='I am very happy.',
            score=5,
            timestamp=datetime.datetime(year=2024, month=10, day=25, hour=10, minute=0, second=0)
        )
        db.insert_journal_entry(journal_entry9)

        journal_entry10 = JournalEntry(
            entry_id=10,
            patient_id=patient_user.user_id,
            text='Just amazing!.',
            score=6,
            timestamp=datetime.datetime(year=2024, month=10, day=30, hour=14, minute=0, second=0)
        )
        db.insert_journal_entry(journal_entry10)

        journal_entry11 = JournalEntry(
            entry_id=11,
            patient_id=patient_user.user_id,
            text='OK, get back to normal.',
            score=4,
            timestamp=datetime.datetime(year=2024, month=11, day=5, hour=12, minute=0, second=0)
        )
        db.insert_journal_entry(journal_entry11)

        # Create PatientRecord object and insert
        patient_record = PatientRecord(
            record_id=1,
            patient_id=patient_user.user_id,
            mhwp_id=mhwp_user.user_id,
            notes='Initial assessment notes.',
            conditions=['Anxiety']
        )

        db.insert_patient_record(patient_record)

        # Additional data
        # Create another Patient and MHWP
        patient_user2 = Patient(
            user_id=4,
            username='patient2',
            password='pass456',
            fName='Jane',
            lName='Smith',
            email='janesmith@example.com'
        )
        mhwp_user2 = MHWP(
            user_id=5,
            username='mhwp2',
            password='pass456',
            fName='Dr.',
            lName='Brown',
            email='drbrown@example.com',
            specialization='Counseling'
        )

        # Insert additional Patient & MHWP
        db.insert_patient(patient_user2)
        db.insert_mhwp(mhwp_user2)

        # Allocate new mhwp to new patient and insert allocation into database
        allocation2 = Allocation(
            allocation_id=2,
            admin_id=admin_user.user_id,
            patient_id=patient_user2.user_id,
            mhwp_id=mhwp_user2.user_id,
            start_date=datetime.datetime.now(),#'2024-02-01',
            end_date=datetime.datetime.now()#'2025-11-30'
        )

        db.insert_allocation(allocation2)

        # Create another JournalEntry object and insert
        journal_entry2 = JournalEntry(
            entry_id=2,
            patient_id=patient_user2.user_id,
            text='Had a productive session today.',
            timestamp=datetime.datetime.now()#'2024-11-08 10:00:00'
        )


        db.insert_journal_entry(journal_entry2)

        # Create another PatientRecord object and insert
        patient_record2 = PatientRecord(
            record_id=2,
            patient_id=patient_user2.user_id,
            mhwp_id=mhwp_user2.user_id,
            notes='Follow-up assessment notes.',
            conditions=['Depression']
        )

        patient_record3 = PatientRecord(
            record_id=2,
            patient_id=patient_user2.user_id,
            mhwp_id=mhwp_user.user_id,
            notes='Second round of follow-up assessment notes.',
            conditions=['Depression']
        )


        db.insert_patient_record(patient_record2)
        db.insert_patient_record(patient_record3)

        # Create Appointment objects and insert them into the database
        appointment1 = Appointment(
            appointment_id=1,
            patient_id=patient_user2.user_id,
            mhwp_id=mhwp_user2.user_id,
            date=datetime.datetime.now(),
            status='active'
        )

        appointment2 = Appointment(
            appointment_id=2,
            patient_id=patient_user2.user_id,
            mhwp_id=mhwp_user2.user_id,
            date=datetime.datetime.now(),
            status='active'
        )

        # Insert appointments into the database
        db.insert_appointment(appointment1)
        db.insert_appointment(appointment2)

    except (UserError, RecordError) as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    db = Database(overwrite = True)
    initDummyDatabase(db)
    db.close()

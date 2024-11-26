import os
import sys

from .database import Database
from .entities import Admin, Patient, MHWP, PatientRecord, Allocation, JournalEntry, Appointment
import datetime
import traceback

# Test functions
def initDummyDatabase(db: Database):
    try:
        # Create User objects
        admin_user = Admin(user_id=1, username='admin1', password='pass1234567')
        patient_user = Patient(
            user_id=2,
            username='patient1',
            password='pass1234567',
            fName='John',
            lName='Doe',
            email='johndoe@example.com'
        )
        mhwp_user = MHWP(
            user_id=3,
            username='mhwp1',
            password='pass1234567',
            fName='DrMartin',
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
            admin_id=admin_user.user_id,  ## example admin id
            patient_id=patient_user.user_id,  ## example patient id
            mhwp_id=mhwp_user.user_id,  ## example mhwp id
            start_date=datetime.datetime.now(),
            end_date=datetime.datetime.now()
        )

        db.insert_allocation(allocation)

        print(db.getRelation("Allocation"))

        # Create JournalEntry object and insert
        journal_entry = JournalEntry(
            entry_id=1,
            patient_id=patient_user.user_id,
            text='Feeling bad now.',
            timestamp=datetime.datetime(year=2024, month=9, day=23, hour=15, minute=30, second=0)
        )
        db.insert_journal_entry(journal_entry)

        journal_entry3 = JournalEntry(
            entry_id=3,
            patient_id=patient_user.user_id,
            text='Get better.',
            timestamp=datetime.datetime(year=2024, month=9, day=28, hour=12, minute=0, second=0)
        )
        db.insert_journal_entry(journal_entry3)
        journal_entry4 = JournalEntry(
            entry_id=4,
            patient_id=patient_user.user_id,
            text='Much better now.',
            timestamp=datetime.datetime(year=2024, month=10, day=2, hour=15, minute=0, second=0)
        )
        db.insert_journal_entry(journal_entry4)

        journal_entry5 = JournalEntry(
            entry_id=5,
            patient_id=patient_user.user_id,
            text='About the same.',
            timestamp=datetime.datetime(year=2024, month=10, day=4, hour=8, minute=0, second=0)
        )
        db.insert_journal_entry(journal_entry5)

        journal_entry6 = JournalEntry(
            entry_id=6,
            patient_id=patient_user.user_id,
            text='Get worse a little.',
            timestamp=datetime.datetime(year=2024, month=10, day=10, hour=20, minute=0, second=0)
        )
        db.insert_journal_entry(journal_entry6)

        journal_entry7 = JournalEntry(
            entry_id=7,
            patient_id=patient_user.user_id,
            text='Feel pretty good today.',
            timestamp=datetime.datetime(year=2024, month=10, day=15, hour=18, minute=0, second=0)
        )
        db.insert_journal_entry(journal_entry7)

        journal_entry8 = JournalEntry(
            entry_id=8,
            patient_id=patient_user.user_id,
            text='Still feel good.',
            timestamp=datetime.datetime(year=2024, month=10, day=20, hour=18, minute=0, second=0)
        )
        db.insert_journal_entry(journal_entry8)

        journal_entry9 = JournalEntry(
            entry_id=9,
            patient_id=patient_user.user_id,
            text='I am very happy.',
            timestamp=datetime.datetime(year=2024, month=10, day=25, hour=10, minute=0, second=0)
        )
        db.insert_journal_entry(journal_entry9)

        journal_entry10 = JournalEntry(
            entry_id=10,
            patient_id=patient_user.user_id,
            text='Just amazing!.',
            timestamp=datetime.datetime(year=2024, month=10, day=30, hour=14, minute=0, second=0)
        )
        db.insert_journal_entry(journal_entry10)

        journal_entry11 = JournalEntry(
            entry_id=11,
            patient_id=patient_user.user_id,
            text='OK, get back to normal.',
            timestamp=datetime.datetime(year=2024, month=11, day=5, hour=12, minute=0, second=0)
        )
        db.insert_journal_entry(journal_entry11)

        # Create PatientRecord object and insert
        patient_record = PatientRecord(
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
            password='pass456789',
            fName='Jane',
            lName='Smith',
            email='janesmith@example.com'
        )
        mhwp_user2 = MHWP(
            user_id=5,
            username='mhwp2',
            password='pass456789',
            fName='Dr',
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
            start_date=datetime.datetime.now(),
            end_date=datetime.datetime.now()
        )

        db.insert_allocation(allocation2)

        # Create another JournalEntry object and insert
        journal_entry2 = JournalEntry(
            entry_id=2,
            patient_id=patient_user2.user_id,
            text='Had a productive session today.',
            timestamp=datetime.datetime.now()
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
            room_name='Room A',
            status='active'
        )

        appointment2 = Appointment(
            appointment_id=2,
            patient_id=patient_user2.user_id,
            mhwp_id=mhwp_user2.user_id,
            date=datetime.datetime.now(),
            room_name='Room B',
            status='active'
        )

        # Insert appointments into the database
        db.insert_appointment(appointment1)
        db.insert_appointment(appointment2)

        db.printAll()

        print(db.getRelation("Appointment"))
        print(db.getRelation("PatientRecord"))
        ## ...
        db.close()


    except (Exception) as e:
        print("An error occurred:")
        traceback.print_exc()


if __name__ == "__main__":
    db = Database(overwrite=True)
    initDummyDatabase(db)
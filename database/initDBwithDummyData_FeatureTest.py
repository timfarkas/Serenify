import os
import sys

# Get the absolute path of the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the project root to sys.path if it's not already there
if project_root not in sys.path:
    sys.path.append(project_root)

# Now absolute imports will work
from .database import Database
from .entities import Admin, Patient, MHWP, PatientRecord, Allocation, JournalEntry, Appointment,MoodEntry,MHWPReview,ChatContent,Forum,Notification
import datetime


# Test functions
def initDummyDatabase(db: Database):
        # Create User objects
        admin_user1 = Admin(user_id=1, username='admin1', password='pass123456')
        patient_user1 = Patient(
            username='Sunflower',
            password='pass123456',
            fName='John',
            lName='Doe',
            email='johndoe@example.com',
            emergency_contact_name='some',
            is_disabled=False,
        )
        patient_user2 = Patient(
            username='Lavender',
            password='pass456789',
            fName='Jane',
            lName='Smith',
            email='janesmith@example.com',
            emergency_contact_name = 'some',
            is_disabled=False,
        )
        patient_user3 = Patient(
            username='Orchid',
            password='pass456789',
            fName='Tony',
            lName='Wills',
            email='tonywills@example.com',
            emergency_contact_name = 'some',
            is_disabled=False,
        )
        mhwp_user1 = MHWP(
            username='Elephant',
            password='pass456789',
            fName='DrMartin',
            lName='Smith',
            email='drsmith@example.com',
            specialization='Psychology'
        )
        mhwp_user2 = MHWP(
            username='Whale',
            password='pass456789',
            fName='Dr',
            lName='Brown',
            email='drbrown@example.com',
            specialization='Counseling'
        )

        # Insert Admin, Patient & User
        db.insert_admin(admin_user1)
        db.insert_patient(patient_user1)
        db.insert_patient(patient_user2)
        db.insert_patient(patient_user3)
        db.insert_mhwp(mhwp_user1)
        db.insert_mhwp(mhwp_user2)

        # Allocate mhwp to patient and insert allocation into database
        allocation1 = Allocation(
            admin_id=1,
            patient_id=2,
            mhwp_id=5,
            start_date=datetime.datetime.now(),
            end_date=datetime.datetime.now()
            # start_date=datetime('2024-01-01'),
            # end_date='2025-12-31'
        )
        allocation2 = Allocation(
            admin_id=1,
            patient_id=3,
            mhwp_id=5,
            start_date=datetime.datetime.now(),
            end_date=datetime.datetime.now()
            # start_date=datetime('2024-01-01'),
            # end_date='2025-12-31'
        )
        allocation3 = Allocation(
            admin_id=1,
            patient_id=4,
            mhwp_id=6,
            start_date=datetime.datetime.now(),  # '2024-02-01',
            end_date=datetime.datetime.now()  # '2025-11-30'
        )
        db.insert_allocation(allocation1)
        db.insert_allocation(allocation2)
        db.insert_allocation(allocation3)

        chat1 = ChatContent(
            allocation_id=1,
            user_id=2,
            text="Hello, I'm a patient",
            timestamp=datetime.datetime.now(),
        )
        chat2 = ChatContent(
            allocation_id=1,
            user_id=5,
            text="Hello, I'm a doctor. How do you feel?",
            timestamp=datetime.datetime.now(),
        )
        chat3 = ChatContent(
            allocation_id=1,
            user_id=2,
            text="I feel alright. Thanks.",
            timestamp=datetime.datetime.now(),
        )
        db.insert_chatcontent(chat1)
        db.insert_chatcontent(chat2)
        db.insert_chatcontent(chat3)
        # Create JournalEntry object and insert
        mood_entry1 = MoodEntry(
            patient_id=2,
            moodscore=1,
            comment='Feeling bad now.',
            timestamp=datetime.datetime(year=2024, month=9, day=23, hour=15, minute=30, second=0)
        )

        mood_entry2 = MoodEntry(
            patient_id=2,
            moodscore=5,
            comment='Had a productive session today.',
            timestamp=datetime.datetime.now()  # '2024-11-08 10:00:00'
        )

        mood_entry3 = MoodEntry(
            patient_id=2,
            moodscore=2,
            comment='Get better.',
            timestamp=datetime.datetime(year=2024, month=9, day=28, hour=12, minute=0, second=0)
        )

        mood_entry4 = MoodEntry(
            patient_id=2,
            moodscore=3,
            comment='Much better now.',
            timestamp=datetime.datetime(year=2024, month=10, day=2, hour=15, minute=0, second=0)
        )

        mood_entry5 = MoodEntry(
            patient_id=2,
            moodscore=3,
            comment='About the same.',
            timestamp=datetime.datetime(year=2024, month=10, day=4, hour=8, minute=0, second=0)
        )

        mood_entry6 = MoodEntry(
            patient_id=2,
            moodscore=2,
            comment='Get worse a little.',
            timestamp=datetime.datetime(year=2024, month=10, day=10, hour=20, minute=0, second=0)
        )

        mood_entry7 = MoodEntry(
            patient_id=2,
            moodscore=4,
            comment='Feel pretty good today.',
            timestamp=datetime.datetime(year=2024, month=10, day=15, hour=18, minute=0, second=0)
        )

        mood_entry8 = MoodEntry(
            patient_id=2,
            moodscore=4,
            comment='Still feel good.',
            timestamp=datetime.datetime(year=2024, month=10, day=20, hour=18, minute=0, second=0)
        )

        mood_entry9 = MoodEntry(
            patient_id=2,
            moodscore=5,
            comment='I am very happy.',
            timestamp=datetime.datetime(year=2024, month=10, day=25, hour=10, minute=0, second=0)
        )

        mood_entry10 = MoodEntry(
            patient_id=2,
            moodscore=6,
            comment='Just amazing!',
            timestamp=datetime.datetime(year=2024, month=10, day=30, hour=14, minute=0, second=0)
        )

        mood_entry11 = MoodEntry(
            patient_id=2,
            moodscore=4,
            comment='OK, get back to normal.',
            timestamp=datetime.datetime(year=2024, month=11, day=5, hour=12, minute=0, second=0)
        )

        # Insert into database
        db.insert_mood_entry(mood_entry1)
        db.insert_mood_entry(mood_entry2)
        db.insert_mood_entry(mood_entry3)
        db.insert_mood_entry(mood_entry4)
        db.insert_mood_entry(mood_entry5)
        db.insert_mood_entry(mood_entry6)
        db.insert_mood_entry(mood_entry7)
        db.insert_mood_entry(mood_entry8)
        db.insert_mood_entry(mood_entry9)
        db.insert_mood_entry(mood_entry10)
        db.insert_mood_entry(mood_entry11)

        # Create PatientRecord object and insert
        patient_record1 = PatientRecord(
            record_id=1,
            patient_id=2,
            mhwp_id=11,
            notes='Initial assessment notes.',
            conditions=['Anxiety']
        )
        patient_record2 = PatientRecord(
            record_id=2,
            patient_id=4,
            mhwp_id=12,
            notes='Follow-up assessment notes.',
            conditions=['Depression']
        )
        patient_record3 = PatientRecord(
            record_id=2,
            patient_id=3,
            mhwp_id=11,
            notes='Second round of follow-up assessment notes.',
            conditions=['Depression']
        )

        db.insert_patient_record(patient_record1)
        db.insert_patient_record(patient_record2)
        db.insert_patient_record(patient_record3)

        # Create Appointment objects and insert them into the database
        appointment1 = Appointment(
            appointment_id=1,
            room_name="A",
            patient_id=4,
            mhwp_id=12,
            date=datetime.datetime.now(),
            status='active'
        )
        appointment2 = Appointment(
            appointment_id=2,
            room_name="B",
            patient_id=2,
            mhwp_id=11,
            date=datetime.datetime.now(),
            status='active'
        )
        # Insert appointments into the database
        db.insert_appointment(appointment1)
        db.insert_appointment(appointment2)

        reviewentry1 = MHWPReview(
            patient_id=2,
            mhwp_id=5,
            reviewscore=5,
            reviewcomment="Very nice",
            timestamp=datetime.datetime.now()
        )
        reviewentry2 = MHWPReview(
            patient_id=3,
            mhwp_id=5,
            reviewscore=4,
            reviewcomment="Good",
            timestamp=datetime.datetime.now()
        )
        db.insert_review_entry(reviewentry1)
        db.insert_review_entry(reviewentry2)

        forumentry1 = Forum(
            parent_id=0,
            topic="hello everyone, it's nice to be here",
            content="I'm new to here. What are we going to do here?",
            user_id=2,
            timestamp=datetime.datetime.now()
        )
        forumentry2 = Forum(
            parent_id=0,
            topic="Welcome to the garden!",
            content="The garden is a place for everyone to share their feelings,thoughts,anything. But please be gentel and polite",
            user_id=5,
            timestamp=datetime.datetime.now()
        )
        forumentry3 = Forum(
            parent_id=1,
            topic="Nice to know you",
            content="I'm new here too, but feel excited",
            user_id=3,
            timestamp=datetime.datetime.now()
        )
        forumentry4 = Forum(
            parent_id=1,
            topic="Welcome!",
            content="Hope you can enjoy this place",
            user_id=5,
            timestamp=datetime.datetime.now()
        )
        forumentry5 = Forum(
            parent_id=2,
            topic="Roger that, boss",
            content="",
            user_id=6,
            timestamp=datetime.datetime.now()
        )
        forumentry6 = Forum(
            parent_id=2,
            topic="Thank you, I'm happy to join.",
            content="",
            user_id=4,
            timestamp=datetime.datetime.now()
        )
        forumentry7 = Forum(
            parent_id=0,
            topic="Tips Sharing: Ten ways to relieve pressures",
            content="1.Deep Breathing: Practice mindful breathing exercises 2.Exercise: Engage in physical activity like jogging or yoga. 3.Meditation: Spend a few minutes daily meditating. 4.Time Management: Prioritize and plan tasks. 5.Nature Breaks: Spend time outdoors. 6.Social Support: Talk with friends or family. 7.Journaling: Write down your thoughts and feelings. 8.Music: Listen to calming or uplifting music. 9.Hobbies: Engage in activities you enjoy. 10.Sleep: Ensure you get adequate rest.",
            user_id=6,
            timestamp=datetime.datetime.now()
        )
        forumentry8 = Forum(
            parent_id=7,
            topic="Thank you for sharing!",
            content="",
            user_id=5,
            timestamp=datetime.datetime.now()
        )
        db.insert_forum(forumentry1)
        db.insert_forum(forumentry2)
        db.insert_forum(forumentry3)
        db.insert_forum(forumentry4)
        db.insert_forum(forumentry5)
        db.insert_forum(forumentry6)
        db.insert_forum(forumentry7)
        db.insert_forum(forumentry8)

        notify1 = Notification(
            user_id=2,
            notifycontent="SA",
            source_id=0,
            new=True,
            timestamp=datetime.datetime.now(),
        )
        notify2 = Notification(
            user_id=2,
            notifycontent="NM",
            source_id=5,
            new=True,
            timestamp=datetime.datetime.now(),
        )
        db.insert_notification(notify1)
        db.insert_notification(notify2)


if __name__ == "__main__":
    db = Database(overwrite=True)
    initDummyDatabase(db)
    db.close()
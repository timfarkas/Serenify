import os 
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if project_root not in sys.path:
    sys.path.append(project_root)

from .database import Database
from .entities import Admin, Patient, MHWP, PatientRecord, Allocation, JournalEntry, Appointment, MoodEntry, MHWPReview, ChatContent, Forum, Notification, ExerRecord
import datetime

def initDummyDatabase(db, printOut = False):
    ### USERS
    # Create User objects
    admin_user0 = Admin(username='System', password='')
    admin_user1 = Admin(username='admin1', password='')
    admin_user2 = Admin(username='admin2', password='')
    
    patient_user1 = Patient(
        username='patient3',
        password='',
        fName='John',
        lName='Doe',
        email='johndoe@example.com',
        emergency_contact_name='Mary Doe',
        emergency_contact_email='marydoe@example.com',
        is_disabled=False,
    )
    patient_user2 = Patient(
        username='patient4',
        password='',
        fName='Jane',
        lName='Smith',
        email='janesmith@example.com',
        emergency_contact_name='Robert Smith',
        emergency_contact_email='robertsmith@example.com',
        is_disabled=False,
    )
    patient_user3 = Patient(
        username='patient1',
        password='',
        fName='Tony',
        lName='Wills',
        email='tonywills@example.com',
        emergency_contact_name=None,
        emergency_contact_email=None,
        is_disabled=False,
    )
    patient_user4 = Patient(
        username='patient2',
        password='',
        fName='Alice',
        lName='Johnson',
        email='alicejohnson@example.com',
        emergency_contact_name='Emily Johnson',
        emergency_contact_email='emilyjohnson@example.com',
        is_disabled=False,
    )
    patient_user5 = Patient(
        username='patient5',
        password='',
        fName='Bob',
        lName='Brown',
        email='bobbrown@example.com',
        emergency_contact_name=None,
        emergency_contact_email=None,
        is_disabled=False,
    )
    patient_disabled = Patient(
        username='disabled',
        password='',
        fName='Rob',
        lName='Smith',
        email='rob@example.com',
        emergency_contact_name='Laura Smith',
        emergency_contact_email='laurasmith@example.com',
        is_disabled=True,
    )

    mhwp_user1 = MHWP(
        username='mhwp1',
        password='',
        fName='Dr',
        lName='Smith',
        email='drsmith@example.com',
        specialization='Psychology'
    )
    mhwp_user2 = MHWP(
        username='mhwp2',
        password='',
        fName='Dr',
        lName='Brown',
        email='drbrown@example.com',
        specialization='Counseling'
    )
    mhwp_user3 = MHWP(
        username='mhwp3',
        password='',
        fName='Dr',
        lName='White',
        email='drwhite@example.com',
        specialization='Cognitive Behavioral Therapy'
    )

    # Insert Admin, Patient & User
    db.insert_admin(admin_user0) ## ID 1
    db.insert_admin(admin_user1) ## ID 2
    db.insert_admin(admin_user2) ## ID 3
    db.insert_patient(patient_user1) ## ID 4
    db.insert_patient(patient_user2) ## ID 5 
    db.insert_patient(patient_user3) ## ID 6
    db.insert_patient(patient_user4) ## ID 7
    db.insert_patient(patient_user5) ## ID 8
    db.insert_mhwp(mhwp_user1) ## ID 9
    db.insert_mhwp(mhwp_user2) ## ID 10
    db.insert_mhwp(mhwp_user3) ## ID 11
    db.insert_patient(patient_disabled) ## ID 12

    ### ALLOCATIONS
    # Allocate mhwp to patient and insert allocation into database
    allocation1 = Allocation(
        admin_id=1,
        patient_id=6,
        mhwp_id=9,
        start_date=datetime.datetime.now(),
        end_date=datetime.datetime.now()
    )
    allocation2 = Allocation(
        admin_id=1,
        patient_id=7,
        mhwp_id=9,
        start_date=datetime.datetime.now(),
        end_date=datetime.datetime.now()
    )
    allocation3 = Allocation(
        admin_id=1,
        patient_id=8,
        mhwp_id=10,
        start_date=datetime.datetime.now(),
        end_date=datetime.datetime.now()
    )
    allocation4 = Allocation(
        admin_id=2,
        patient_id=4,
        mhwp_id=11,
        start_date=datetime.datetime.now(),
        end_date=datetime.datetime.now()
    )
    allocation5 = Allocation(
        admin_id=2,
        patient_id=5,
        mhwp_id=11,
        start_date=datetime.datetime.now(),
        end_date=datetime.datetime.now()
    )
    db.insert_allocation(allocation1) ## 1
    db.insert_allocation(allocation2) ## 2
    db.insert_allocation(allocation3) ## 3
    db.insert_allocation(allocation4) ## 4 
    db.insert_allocation(allocation5) ## 5

    ### CHAT CONTENT
    # Chat content for allocation 1
    chat1 = ChatContent(
        allocation_id=1,
        user_id=6,
        text="Hello, I'm a patient",
        timestamp=datetime.datetime.now(),
    )
    chat2 = ChatContent(
        allocation_id=1,
        user_id=9,
        text="Hello, I'm a doctor. How do you feel?",
        timestamp=datetime.datetime.now(),
    )
    chat3 = ChatContent(
        allocation_id=1,
        user_id=6,
        text="I feel alright. Thanks.",
        timestamp=datetime.datetime.now(),
    )
    chat4 = ChatContent(
        allocation_id=1,
        user_id=9,
        text="I'm happy to hear that",
        timestamp=datetime.datetime.now(),
    )
    db.insert_chatcontent(chat1)
    db.insert_chatcontent(chat2)
    db.insert_chatcontent(chat3)
    db.insert_chatcontent(chat4)

    # Chat content for allocation 2
    chat11 = ChatContent(
        allocation_id=2,
        user_id=7,
        text="Hi, I have been feeling a bit stressed lately.",
        timestamp=datetime.datetime.now(),
    )
    chat12 = ChatContent(
        allocation_id=2,
        user_id=9,
        text="I'm sorry to hear that. Let's discuss some strategies to help you manage stress.",
        timestamp=datetime.datetime.now(),
    )
    chat13 = ChatContent(
        allocation_id=2,
        user_id=7,
        text="That would be great, thank you.",
        timestamp=datetime.datetime.now(),
    )
    db.insert_chatcontent(chat11)
    db.insert_chatcontent(chat12)
    db.insert_chatcontent(chat13)

    # Chat content for allocation 3
    chat4 = ChatContent(
        allocation_id=3,
        user_id=8,
        text="Hi, I have some questions about my treatment.",
        timestamp=datetime.datetime.now(),
    )
    chat5 = ChatContent(
        allocation_id=3,
        user_id=10,
        text="Sure, I'm here to help. What would you like to know?",
        timestamp=datetime.datetime.now(),
    )
    chat6 = ChatContent(
        allocation_id=3,
        user_id=8,
        text="Can we adjust the schedule for my sessions?",
        timestamp=datetime.datetime.now(),
    )
    db.insert_chatcontent(chat4)
    db.insert_chatcontent(chat5)
    db.insert_chatcontent(chat6)

    # Chat content for allocation 4
    chat7 = ChatContent(
        allocation_id=4,
        user_id=4,
        text="Good morning, doctor.",
        timestamp=datetime.datetime.now(),
    )
    chat8 = ChatContent(
        allocation_id=4,
        user_id=11,
        text="Good morning! How are you feeling today?",
        timestamp=datetime.datetime.now(),
    )
    chat9 = ChatContent(
        allocation_id=4,
        user_id=4,
        text="I'm feeling a bit anxious.",
        timestamp=datetime.datetime.now(),
    )
    db.insert_chatcontent(chat7)
    db.insert_chatcontent(chat8)
    db.insert_chatcontent(chat9)

    # Chat content for allocation 5
    chat10 = ChatContent(
        allocation_id=5,
        user_id=5,
        text="Hello, I need to discuss my progress.",
        timestamp=datetime.datetime.now(),
    )
    chat11 = ChatContent(
        allocation_id=5,
        user_id=11,
        text="Of course, let's go over your recent sessions.",
        timestamp=datetime.datetime.now(),
    )
    chat12 = ChatContent(
        allocation_id=5,
        user_id=5,
        text="I think I'm improving, but I have some concerns.",
        timestamp=datetime.datetime.now(),
    )
    db.insert_chatcontent(chat10)
    db.insert_chatcontent(chat11)
    db.insert_chatcontent(chat12)

    ### MOOD ENTRIES
    # Create MoodEntry objects and insert
    mood_entry1 = MoodEntry(
        patient_id=6,
        moodscore=1,
        comment='Feeling bad now.',
        timestamp=datetime.datetime(year=2024, month=9, day=23, hour=15, minute=30, second=0)
    )
    mood_entry2 = MoodEntry(
        patient_id=6,
        moodscore=5,
        comment='Had a productive session today.',
        timestamp=datetime.datetime(year=2024, month=9, day=25, hour=15, minute=30, second=0)
    )
    mood_entry3 = MoodEntry(
        patient_id=6,
        moodscore=2,
        comment='Get better.',
        timestamp=datetime.datetime(year=2024, month=9, day=28, hour=12, minute=0, second=0)
    )
    mood_entry4 = MoodEntry(
        patient_id=6,
        moodscore=3,
        comment='Much better now.',
        timestamp=datetime.datetime(year=2024, month=10, day=2, hour=15, minute=0, second=0)
    )
    mood_entry5 = MoodEntry(
        patient_id=5,
        moodscore=3,
        comment='About the same.',
        timestamp=datetime.datetime(year=2024, month=10, day=4, hour=8, minute=0, second=0)
    )
    mood_entry6 = MoodEntry(
        patient_id=6,
        moodscore=2,
        comment='Get worse a little.',
        timestamp=datetime.datetime(year=2024, month=10, day=10, hour=20, minute=0, second=0)
    )
    mood_entry7 = MoodEntry(
        patient_id=6,
        moodscore=4,
        comment='Feel pretty good today.',
        timestamp=datetime.datetime(year=2024, month=10, day=15, hour=18, minute=0, second=0)
    )
    mood_entry8 = MoodEntry(
        patient_id=6,
        moodscore=4,
        comment='Still feel good.',
        timestamp=datetime.datetime(year=2024, month=10, day=20, hour=18, minute=0, second=0)
    )
    mood_entry9 = MoodEntry(
        patient_id=6,
        moodscore=5,
        comment='I am very happy.',
        timestamp=datetime.datetime(year=2024, month=10, day=25, hour=10, minute=0, second=0)
    )
    mood_entry10 = MoodEntry(
        patient_id=6,
        moodscore=6,
        comment='Just amazing!',
        timestamp=datetime.datetime(year=2024, month=10, day=30, hour=14, minute=0, second=0)
    )
    mood_entry11 = MoodEntry(
        patient_id=6,
        moodscore=4,
        comment='OK, get back to normal.',
        timestamp=datetime.datetime(year=2024, month=11, day=5, hour=12, minute=0, second=0)
    )
    mood_entry14 = MoodEntry(
        patient_id=6,
        moodscore=3,
        comment='Feeling okay.',
        timestamp=datetime.datetime(year=2024, month=12, day=1, hour=9, minute=0, second=0)
    )
    mood_entry15 = MoodEntry(
        patient_id=6,
        moodscore=4,
        comment='Better than yesterday.',
        timestamp=datetime.datetime(year=2024, month=12, day=3, hour=11, minute=0, second=0)
    )
    mood_entry16 = MoodEntry(
        patient_id=6,
        moodscore=5,
        comment='Feeling good!',
        timestamp=datetime.datetime(year=2024, month=12, day=4, hour=16, minute=0, second=0)
    )
    mood_entry12 = MoodEntry(
        patient_id=7,
        moodscore=1,
        comment='Feel Bad',
        timestamp=datetime.datetime(year=2024, month=11, day=28, hour=12, minute=0, second=0)
    )
    mood_entry13 = MoodEntry(
        patient_id=7,
        moodscore=3,
        comment='Alright.',
        timestamp=datetime.datetime(year=2024, month=11, day=29, hour=12, minute=0, second=0)
    )
    mood_entry18 = MoodEntry(
        patient_id=7,
        moodscore=2,
        comment='Not getting better',
        timestamp=datetime.datetime(year=2024, month=12, day=4, hour=16, minute=0, second=0)
    )
    mood_entry19 = MoodEntry(
        patient_id=7,
        moodscore=2,
        comment='Feeling bad!',
        timestamp=datetime.datetime(year=2024, month=12, day=5, hour=16, minute=0, second=0)
    )
    mood_entry20 = MoodEntry(
        patient_id=7,
        moodscore=1,
        comment='Feel Terrible',
        timestamp=datetime.datetime(year=2024, month=12, day=6, hour=16, minute=0, second=0)
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
    db.insert_mood_entry(mood_entry12)
    db.insert_mood_entry(mood_entry12)
    db.insert_mood_entry(mood_entry13)
    db.insert_mood_entry(mood_entry14)
    db.insert_mood_entry(mood_entry15)
    db.insert_mood_entry(mood_entry16)
    db.insert_mood_entry(mood_entry18)
    db.insert_mood_entry(mood_entry19)
    db.insert_mood_entry(mood_entry20)

    ### JOURNAL ENTRIES
    journal_entry1 = JournalEntry(
        patient_id=6,
        text="Dear Diary, today I felt a mix of emotions.",
        timestamp=datetime.datetime(year=2024, month=11, day=29, hour=12, minute=0, second=0)
    )
    journal_entry2 = JournalEntry(
        patient_id=6,
        text="Feeling grateful for the support I received today.",
        timestamp=datetime.datetime(year=2024, month=12, day=2, hour=18, minute=45, second=0)
    )
    journal_entry3 = JournalEntry(
        patient_id=7,
        text="Today was a challenging day, but I managed to stay positive.",
        timestamp=datetime.datetime(year=2024, month=11, day=30, hour=15, minute=30, second=0)
    )
    journal_entry4 = JournalEntry(
        patient_id=7,
        text="Reflecting on the week, I see progress.",
        timestamp=datetime.datetime(year=2024, month=12, day=3, hour=10, minute=15, second=0)
    )
    journal_entry5 = JournalEntry(
        patient_id=8,
        text="I had a productive day and accomplished a lot.",
        timestamp=datetime.datetime(year=2024, month=12, day=1, hour=9, minute=0, second=0)
    )
    journal_entry6 = JournalEntry(
        patient_id=8,
        text="Enjoyed a peaceful evening with family.",
        timestamp=datetime.datetime(year=2024, month=12, day=4, hour=20, minute=0, second=0)
    )
    journal_entry7 = JournalEntry(
        patient_id=4,
        text="Started a new book today, feeling inspired.",
        timestamp=datetime.datetime(year=2024, month=12, day=5, hour=14, minute=30, second=0)
    )
    journal_entry8 = JournalEntry(
        patient_id=4,
        text="Had a great conversation with a friend.",
        timestamp=datetime.datetime(year=2024, month=12, day=6, hour=16, minute=45, second=0)
    )
    # Insert into database
    db.insert_journal_entry(journal_entry1)
    db.insert_journal_entry(journal_entry2)
    db.insert_journal_entry(journal_entry3)
    db.insert_journal_entry(journal_entry4)
    db.insert_journal_entry(journal_entry5)
    db.insert_journal_entry(journal_entry6)
    db.insert_journal_entry(journal_entry7)
    db.insert_journal_entry(journal_entry8)

    ### PATIENT RECORDS
    # Create PatientRecord object and insert
    patient_record1 = PatientRecord(
        record_id=1,
        patient_id=6,
        mhwp_id=9,
        notes='Patient exhibits symptoms of anxiety; initial assessment conducted.',
        conditions=['Anxiety']
    )
    patient_record2 = PatientRecord(
        record_id=2,
        patient_id=7,
        mhwp_id=9,
        notes='Patient shows signs of improvement; follow-up assessment completed.',
        conditions=['Depression']
    )
    patient_record3 = PatientRecord(
        record_id=3,
        patient_id=8,
        mhwp_id=10,
        notes='Continued monitoring of depressive symptoms; second follow-up conducted.',
        conditions=['Depression']
    )
    patient_record4 = PatientRecord(
        record_id=4,
        patient_id=4,
        mhwp_id=11,
        notes='Initial assessment reveals symptoms consistent with bipolar disorder.',
        conditions=['Bipolar Disorder']
    )
    patient_record5 = PatientRecord(
        record_id=5,
        patient_id=5,
        mhwp_id=11,
        notes='Patient reports anxiety symptoms; initial evaluation performed.',
        conditions=['Anxiety']
    )

    db.insert_patient_record(patient_record1)
    db.insert_patient_record(patient_record2)
    db.insert_patient_record(patient_record3)
    db.insert_patient_record(patient_record4)
    db.insert_patient_record(patient_record5)
    

    ### APPOINTMENTS
    appointmentRelation = db.getRelation('Appointment')
    # Create Appointment objects and insert them into the database
    appointment1 = Appointment(
        appointment_id=1,
        room_name="Room A",
        patient_id=6,
        mhwp_id=9,
        date=(datetime.datetime.now() + datetime.timedelta(days=5)).replace(hour=10, minute=0, second=0, microsecond=0),
        status='Confirmed',
        appointmentRelation=appointmentRelation
    )
    appointment2 = Appointment(
        appointment_id=2,
        room_name="Room B",
        patient_id=8,
        mhwp_id=10,
        status='Confirmed',
        date=(datetime.datetime.now() + datetime.timedelta(days=25)).replace(hour=10, minute=0, second=0, microsecond=0),
        appointmentRelation=appointmentRelation
    )
    appointment3 = Appointment(
        appointment_id=3,
        room_name="Room C",
        patient_id=6,
        mhwp_id=9,
        status='Pending',
        date=(datetime.datetime.now() + datetime.timedelta(days=15)).replace(hour=11, minute=0, second=0, microsecond=0),
        appointmentRelation=appointmentRelation
    )
    appointment4 = Appointment(
        appointment_id=4,
        room_name="Room D",
        patient_id=7,
        mhwp_id=9,
        status='Confirmed',
        date=(datetime.datetime.now() + datetime.timedelta(days=20)).replace(hour=9, minute=0, second=0, microsecond=0),
        appointmentRelation=appointmentRelation
    )
    # Insert appointments into the database
    db.insert_appointment(appointment1)
    db.insert_appointment(appointment2)
    db.insert_appointment(appointment3)
    db.insert_appointment(appointment4)

    ### REVIEWS
    reviewentry1 = MHWPReview(
        patient_id=6,
        mhwp_id=9,
        reviewscore=5,
        reviewcomment="Very nice",
        timestamp=datetime.datetime(year=2024, month=10, day=25, hour=10, minute=0, second=0)
    )
    reviewentry2 = MHWPReview(
        patient_id=7,
        mhwp_id=9,
        reviewscore=4,
        reviewcomment="Good",
        timestamp=datetime.datetime(year=2024, month=11, day=21, hour=10, minute=0, second=0)
    )
    reviewentry3 = MHWPReview(
        patient_id=8,
        mhwp_id=10,
        reviewscore=3,
        reviewcomment="Average experience",
        timestamp=datetime.datetime(year=2024, month=12, day=5, hour=14, minute=0, second=0)
    )
    reviewentry4 = MHWPReview(
        patient_id=4,
        mhwp_id=11,
        reviewscore=2,
        reviewcomment="Not satisfied",
        timestamp=datetime.datetime(year=2024, month=12, day=10, hour=9, minute=0, second=0)
    )
    reviewentry5 = MHWPReview(
        patient_id=5,
        mhwp_id=11,
        reviewscore=5,
        reviewcomment="Excellent service",
        timestamp=datetime.datetime(year=2024, month=12, day=15, hour=11, minute=0, second=0)
    )
    db.insert_review_entry(reviewentry1)
    db.insert_review_entry(reviewentry2)
    db.insert_review_entry(reviewentry3)
    db.insert_review_entry(reviewentry4)
    db.insert_review_entry(reviewentry5)

    ### FORUM ENTRIES
    forumentry1 = Forum(
        parent_id=0,
        topic="hello everyone, it's nice to be here",
        content="I'm new to here. What are we going to do here?",
        user_id=6,
        timestamp=datetime.datetime(year=2024, month=11, day=26, hour=10, minute=0, second=0)
    )
    forumentry2 = Forum(
        parent_id=0,
        topic="Welcome to the garden!",
        content="The garden is a place for everyone to share their feelings,thoughts,anything. But please be gentel and polite",
        user_id=9,
        timestamp=datetime.datetime(year=2024, month=11, day=25, hour=10, minute=0, second=0)
    )
    forumentry3 = Forum(
        parent_id=1,
        topic="Nice to know you",
        content="I'm new here too, but feel excited",
        user_id=7,
        timestamp=datetime.datetime(year=2024, month=11, day=26, hour=12, minute=0, second=0)
    )
    forumentry4 = Forum(
        parent_id=1,
        topic="Welcome!",
        content="Hope you can enjoy this place",
        user_id=4,
        timestamp=datetime.datetime(year=2024, month=11, day=27, hour=12, minute=0, second=0)
    )
    forumentry5 = Forum(
        parent_id=2,
        topic="Roger that, boss",
        content="",
        user_id=10,
        timestamp=datetime.datetime(year=2024, month=11, day=28, hour=12, minute=0, second=0)
    )
    forumentry6 = Forum(
        parent_id=2,
        topic="Thank you, I'm happy to join.",
        content="",
        user_id=8,
        timestamp=datetime.datetime(year=2024, month=11, day=29, hour=12, minute=0, second=0)
    )
    forumentry7 = Forum(
        parent_id=0,
        topic="Tips Sharing: Ten ways to relieve pressures",
        content="1.Deep Breathing: Practice mindful breathing exercises 2.Exercise: Engage in physical activity like jogging or yoga. 3.Meditation: Spend a few minutes daily meditating. 4.Time Management: Prioritize and plan tasks. 5.Nature Breaks: Spend time outdoors. 6.Social Support: Talk with friends or family. 7.Journaling: Write down your thoughts and feelings. 8.Music: Listen to calming or uplifting music. 9.Hobbies: Engage in activities you enjoy. 10.Sleep: Ensure you get adequate rest.",
        user_id=11,
        timestamp=datetime.datetime(year=2024, month=12, day=1, hour=12, minute=0, second=0)
    )
    forumentry8 = Forum(
        parent_id=7,
        topic="Thank you for sharing!",
        content="",
        user_id=4,
        timestamp=datetime.datetime(year=2024, month=12, day=2, hour=12, minute=0, second=0)
    )
    db.insert_forum(forumentry1)
    db.insert_forum(forumentry2)
    db.insert_forum(forumentry3)
    db.insert_forum(forumentry4)
    db.insert_forum(forumentry5)
    db.insert_forum(forumentry6)
    db.insert_forum(forumentry7)
    db.insert_forum(forumentry8)

    ### NOTIFICATIONS
    notify1 = Notification(
        user_id=9,
        notifycontent="Newappointment",
        source_id=0,
        new=True,
        timestamp=datetime.datetime.now(),
    )
    notify2 = Notification(
        user_id=6,
        notifycontent="Newchat",
        source_id=9,
        new=True,
        timestamp=datetime.datetime.now(),
    )
    notify3 = Notification(
        user_id=9,
        notifycontent="Newreview",
        source_id=0,
        new=True,
        timestamp=datetime.datetime.now(),
    )
    notify4 = Notification(
        user_id=9,
        notifycontent="Newchat",
        source_id=7,
        new=True,
        timestamp=datetime.datetime.now(),
    )
    notify5 = Notification(
        user_id=6,
        notifycontent="AppointmentConfirmed",
        source_id=0,
        new=True,
        timestamp=datetime.datetime(year=2024, month=12, day=7, hour=10, minute=0, second=0),
    )
    notify6 = Notification(
        user_id=9,
        notifycontent="MoodAlert",
        source_id=7,
        new=True,
        timestamp=datetime.datetime(year=2024, month=12, day=6, hour=16, minute=0, second=0),
    )


    db.insert_notification(notify1)
    db.insert_notification(notify2)
    db.insert_notification(notify3)
    db.insert_notification(notify4)
    db.insert_notification(notify5)
    db.insert_notification(notify6)

    ### EXERCISE RECORDS
    exer1 = ExerRecord(
        user_id=6,
        exercise="Mindfulness",
        timestamp=datetime.datetime(year=2024, month=11, day=21, hour=10, minute=0, second=0),
    )
    exer2 = ExerRecord(
        user_id=6,
        exercise="Mindfulness",
        timestamp=datetime.datetime(year=2024, month=11, day=22, hour=10, minute=0, second=0),
    )
    exer3 = ExerRecord(
        user_id=6,
        exercise="Mindfulness",
        timestamp=datetime.datetime(year=2024, month=11, day=23, hour=10, minute=0, second=0),
    )
    exer4 = ExerRecord(
        user_id=6,
        exercise="Body Scan",
        timestamp=datetime.datetime(year=2024, month=11, day=24, hour=10, minute=0, second=0),
    )
    exer5 = ExerRecord(
        user_id=6,
        exercise="Body Scan",
        timestamp=datetime.datetime(year=2024, month=11, day=25, hour=10, minute=0, second=0),
    )
    exer6 = ExerRecord(
        user_id=6,
        exercise="Self Guided Mindfulness",
        timestamp=datetime.datetime(year=2024, month=11, day=25, hour=10, minute=0, second=0),
    )
    exer7 = ExerRecord(
        user_id=6,
        exercise="Self Guided Mindfulness",
        timestamp=datetime.datetime(year=2024, month=11, day=25, hour=10, minute=0, second=0),
    )
    exer8 = ExerRecord(
        user_id=6,
        exercise="Body Scan",
        timestamp=datetime.datetime(year=2024, month=11, day=26, hour=10, minute=0, second=0),
    )
    exer9 = ExerRecord(
        user_id=6,
        exercise="Mindfulness",
        timestamp=datetime.datetime(year=2024, month=11, day=26, hour=10, minute=0, second=0),
    )
    exer10 = ExerRecord(
        user_id=6,
        exercise="Mindfulness",
        timestamp=datetime.datetime(year=2024, month=11, day=27, hour=10, minute=0, second=0),
    )
    exer11 = ExerRecord(
        user_id=6,
        exercise="Body Scan",
        timestamp=datetime.datetime(year=2024, month=11, day=28, hour=10, minute=0, second=0),
    )
    exer12 = ExerRecord(
        user_id=6,
        exercise="Mindfulness",
        timestamp=datetime.datetime(year=2024, month=11, day=29, hour=10, minute=0, second=0),
    )
    exer13 = ExerRecord(
        user_id=6,
        exercise="Body Scan",
        timestamp=datetime.datetime(year=2024, month=11, day=30, hour=10, minute=0, second=0),
    )


    db.insert_exerrecord(exer1)
    db.insert_exerrecord(exer2)
    db.insert_exerrecord(exer3)
    db.insert_exerrecord(exer4)
    db.insert_exerrecord(exer5)
    db.insert_exerrecord(exer6)
    db.insert_exerrecord(exer7)
    db.insert_exerrecord(exer8)
    db.insert_exerrecord(exer9)
    db.insert_exerrecord(exer10)
    db.insert_exerrecord(exer11)
    db.insert_exerrecord(exer12)
    db.insert_exerrecord(exer13)
    if printOut:
        db.printAll()


if __name__ == "__main__":
    db = Database(overwrite = True)
    initDummyDatabase(db, printOut = True)
    db.close()
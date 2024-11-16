from datetime import datetime

# Custom exception classes
class UserError(Exception):
    """Base class for exceptions related to user operations."""
    pass

class UserAlreadyExistsError(UserError):
    """Exception raised when attempting to create a user that already exists."""
    pass

class UserNotFoundError(UserError):
    """Exception raised when a user cannot be found."""
    pass

class InvalidUserTypeError(UserError):
    """Exception raised for invalid user types."""
    pass

class RecordError(Exception):
    """Base class for exceptions related to record operations."""
    pass

class RecordAlreadyExistsError(RecordError):
    """Exception raised when attempting to create a record that already exists."""
    pass

class RecordNotFoundError(RecordError):
    """Exception raised when a record cannot be found."""
    pass

# Entities
## Base User class
class User:
    """A class to represent a user in the system."""
    def __init__(self, user_id: int = None, username: str = '', password: str = '', user_type: str = '', is_disabled: bool = False):
        """
        Initialize a User object.

        Parameters:
        user_id (int, optional): The unique identifier for the user. Can be None.
        username (str): The username of the user.
        password (str): The password for the user.
        user_type (str): The type of user (e.g., 'Admin', 'Patient', 'MHWP').
        is_disabled (bool): Flag indicating if the user is disabled.
        """
        self.user_id = user_id
        self.username = username
        self.password = password
        self.type = user_type
        self.is_disabled = is_disabled

## Admin class inheriting from User
class Admin(User):
    """A class to represent an admin user."""
    def __init__(self, user_id: int = None, username: str = '', password: str = '', is_disabled: bool = False):
        """
        Initialize an Admin object.

        Parameters:
        user_id (int, optional): The unique identifier for the admin. Can be None.
        username (str): The username of the admin.
        password (str): The password for the admin.
        is_disabled (bool): Flag indicating if the admin is disabled.
        """
        super().__init__(user_id, username, password, 'Admin', is_disabled)

## Patient class inheriting from User
class Patient(User):
    """A class to represent a patient user."""
    def __init__(self, user_id: int = None, username: str = '', password: str = '', fName: str = '', lName: str = '', email: str = '',
                 emergency_contact_email: str = None, is_disabled: bool = False):
        """
        Initialize a Patient object.

        Parameters:
        user_id (int, optional): The unique identifier for the patient. Can be None.
        username (str): The username of the patient.
        password (str): The password for the patient.
        fName (str): The first name of the patient.
        lName (str): The last name of the patient.
        email (str): The email address of the patient.
        emergency_contact_email (str, optional): The emergency contact email for the patient.
        is_disabled (bool): Flag indicating if the patient is disabled.
        """
        super().__init__(user_id, username, password, 'Patient', is_disabled)
        self.fName = fName
        self.lName = lName
        self.email = email
        self.emergency_contact_email = emergency_contact_email
        
## MHWP class inheriting from User
class MHWP(User):
    """A class to represent a mental health worker professional (MHWP) user."""
    def __init__(self, user_id: int = None, username: str = '', password: str = '', fName: str = '', lName: str = '', email: str = '', specialization: str = '', is_disabled: bool = False):
        """
        Initialize an MHWP object.

        Parameters:
        user_id (int, optional): The unique identifier for the MHWP. Can be None.
        username (str): The username of the MHWP.
        password (str): The password for the MHWP.
        fName (str): The first name of the MHWP.
        lName (str): The last name of the MHWP.
        email (str): The email address of the MHWP.
        specialization (str): The specialization of the MHWP.
        is_disabled (bool): Flag indicating if the MHWP is disabled.
        """
        super().__init__(user_id, username, password, 'MHWP', is_disabled)
        self.fName = fName
        self.lName = lName
        self.email = email
        self.specialization = specialization

## JournalEntry class
class JournalEntry:
    """A class to represent a journal entry."""
    def __init__(self, entry_id: int = None, patient_id: int = None, text: str = '', timestamp: datetime = None):
        """
        Initialize a JournalEntry object.

        Parameters:
        entry_id (int, optional): The unique identifier for the journal entry. Can be None.
        patient_id (int, optional): The ID of the patient associated with the entry. Can be None.
        text (str): The text content of the journal entry.
        timestamp (datetime, optional): The timestamp of when the entry was created. Can be None.
        """
        self.entry_id = entry_id
        self.patient_id = patient_id  # foreign key to Patient
        self.text = text
        self.timestamp = timestamp

## Appointment class
class Appointment:
    """A class to represent an appointment."""
    def __init__(self, appointment_id: int = None, patient_id: int = None, mhwp_id: int = None, date: datetime = None, room_name: str = None, status: str = ''):
        """
        Initialize an Appointment object.

        Parameters:
        appointment_id (int, optional): The unique identifier for the appointment. Can be None.
        patient_id (int, optional): The ID of the patient associated with the appointment. Can be None.
        mhwp_id (int, optional): The ID of the MHWP associated with the appointment. Can be None.
        date (datetime, optional): The date of the appointment. Can be None.
        status (str): The status of the appointment.
        """
        self.appointment_id = appointment_id
        self.patient_id = patient_id  # foreign key to Patient
        self.mhwp_id = mhwp_id        # foreign key to MHWP
        self.date = date
        self.room_name = room_name
        self.status = status

## PatientRecord class
class PatientRecord:
    """A class to represent a patient record entry."""
    def __init__(self, record_id: int = None, patient_id: int = None, mhwp_id: int = None, notes: str = '', conditions: list = None):
        """
        Initialize a PatientRecord entry.

        Parameters:
        record_id (int, optional): The unique identifier for the patient record entry. Can be None.
        patient_id (int, optional): The ID of the patient associated with the record entry. Can be None.
        mhwp_id (int, optional): The ID of the MHWP associated with the record entry. Can be None.
        notes (str): The notes associated with the patient record entry.
        conditions (list, optional): The conditions associated with the patient record entry.
        """
        self.record_id = record_id
        self.patient_id = patient_id  # foreign key to Patient
        self.mhwp_id = mhwp_id        # foreign key to MHWP
        self.notes = notes
        self.conditions = conditions

## Allocation class
class Allocation:
    """A class to represent an allocation."""
    def __init__(self, allocation_id: int = None, admin_id: int = None, patient_id: int = None, mhwp_id: int = None, start_date: datetime = None, end_date: datetime = None):
        """
        Initialize an Allocation object.

        Parameters:
        allocation_id (int, optional): The unique identifier for the allocation. Can be None.
        admin_id (int, optional): The ID of the admin associated with the allocation. Can be None.
        patient_id (int, optional): The ID of the patient associated with the allocation. Can be None.
        mhwp_id (int, optional): The ID of the MHWP associated with the allocation. Can be None.
        start_date (datetime, optional): The start date of the allocation. Can be None.
        end_date (datetime, optional): The end date of the allocation. Can be None.
        """
        self.allocation_id = allocation_id
        self.admin_id = admin_id      # foreign key to Admin
        self.patient_id = patient_id  # foreign key to Patient
        self.mhwp_id = mhwp_id        # foreign key to MHWP
        self.start_date = start_date
        self.end_date = end_date

"""New entities created for new features."""
class MoodEntry:

    def __init__(self,moodentry_id: int = None, patient_id: int = None, moodscore:int=None,comment: str = '', timestamp: datetime = None):
        self.moodentry_id= moodentry_id
        self.moodscore = moodscore
        self.patient_id = patient_id  # foreign key to Patient
        self.comment = comment
        self.timestamp = timestamp

class MHWPReview:
    def __init__(self,MHWP_review_id: int = None, patient_id: int = None,mhwp_id: int = None, reviewscore:int=None,reviewcomment: str = '', timestamp: datetime = None):

        self.MHWP_review_id=MHWP_review_id
        self.patient_id = patient_id
        self.mhwp_id= mhwp_id  # foreign key to Patient
        self.reviewscore = reviewscore
        self.reviewcomment = reviewcomment
        self.timestamp = timestamp

# class ChatRoom:
#     def __init__(self,room_id: int = None, patient_id: int = None, mhwp_id: int = None):
#
#         self.room_id=room_id
#         self.patient_id = patient_id
#         self.mhwp_id= mhwp_id


class ChatContent:
    def __init__(self,chatcontent_id:int=None, allocation_id: int = None, user_id: int = None, text: str = '', timestamp: datetime = None):
        self.chatcontent_id = chatcontent_id
        self.allocation_id = allocation_id
        self.user_id = user_id
        self.text = text
        self.timestamp = timestamp


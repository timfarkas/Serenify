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
class User():
    """A class to represent a user in the system."""
    def __init__(self, user_id=None, username='', password='', user_type='', is_disabled=False):
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
    def __init__(self, user_id=None, username='', password='', is_disabled=False):
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
    def __init__(self, user_id=None, username='', password='', fName='', lName='', email='',
                 emergency_contact_email=None, moods=None, mood_comments=None, is_disabled=False):
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
        moods (list, optional): A list of mood entries for the patient.
        mood_comments (list, optional): A list of mood comments for the patient.
        is_disabled (bool): Flag indicating if the patient is disabled.
        """
        super().__init__(user_id, username, password, 'Patient', is_disabled)
        self.fName = fName
        self.lName = lName
        self.email = email
        self.emergency_contact_email = emergency_contact_email
        self.moods = moods
        self.mood_comments = mood_comments

## MHWP class inheriting from User
class MHWP(User):
    """A class to represent a mental health worker professional (MHWP) user."""
    def __init__(self, user_id=None, username='', password='', fName='', lName='', email='', specialization='', is_disabled=False):
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
class JournalEntry():
    """A class to represent a journal entry."""
    def __init__(self, entry_id=None, patient_id=None, text='', timestamp=None):
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
    def __init__(self, appointment_id=None, patient_id=None, mhwp_id=None, date=None, status=''):
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
        self.status = status

## PatientRecord class
class PatientRecord:
    """A class to represent a patient record."""
    def __init__(self, record_id=None, patient_id=None, mhwp_id=None, notes='', conditions=None):
        """
        Initialize a PatientRecord object.

        Parameters:
        record_id (int, optional): The unique identifier for the patient record. Can be None.
        patient_id (int, optional): The ID of the patient associated with the record. Can be None.
        mhwp_id (int, optional): The ID of the MHWP associated with the record. Can be None.
        notes (str): The notes associated with the patient record.
        conditions (list, optional): The conditions associated with the patient record.
        """
        self.record_id = record_id
        self.patient_id = patient_id  # foreign key to Patient
        self.mhwp_id = mhwp_id        # foreign key to MHWP
        self.notes = notes
        self.conditions = conditions

## Allocation class
class Allocation:
    """A class to represent an allocation."""
    def __init__(self, allocation_id=None, admin_id=None, patient_id=None, mhwp_id=None, start_date=None, end_date=None):
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

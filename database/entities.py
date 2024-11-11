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
    def __init__(self, user_id, username, password, user_type, is_disabled=False):
        """
        Initialize a User object.

        Parameters:
        user_id (int): The unique identifier for the user.
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
    def __init__(self, user_id, username, password, is_disabled=False):
        """
        Initialize an Admin object.

        Parameters:
        user_id (int): The unique identifier for the admin.
        username (str): The username of the admin.
        password (str): The password for the admin.
        is_disabled (bool): Flag indicating if the admin is disabled.
        """
        super().__init__(user_id, username, password, 'Admin', is_disabled)

## Patient class inheriting from User
class Patient(User):
    """A class to represent a patient user."""
    def __init__(self, user_id, username, password, fName, lName, email,
                 emergency_contact_email=None, moods=None, mood_comments=None, is_disabled=False):
        """
        Initialize a Patient object.

        Parameters:
        user_id (int): The unique identifier for the patient.
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
    def __init__(self, user_id, username, password, fName, lName, email, specialization, is_disabled=False):
        """
        Initialize an MHWP object.

        Parameters:
        user_id (int): The unique identifier for the MHWP.
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
    def __init__(self, entry_id, patient_id, text, timestamp):
        """
        Initialize a JournalEntry object.

        Parameters:
        entry_id (int): The unique identifier for the journal entry.
        patient_id (int): The ID of the patient associated with the entry.
        text (str): The text content of the journal entry.
        timestamp (datetime): The timestamp of when the entry was created.
        """
        self.entry_id = entry_id
        self.patient_id = patient_id  # foreign key to Patient
        self.text = text
        self.timestamp = timestamp

## Appointment class
class Appointment:
    """A class to represent an appointment."""
    def __init__(self, appointment_id, patient_id, mhwp_id, date, status):
        """
        Initialize an Appointment object.

        Parameters:
        appointment_id (int): The unique identifier for the appointment.
        patient_id (int): The ID of the patient associated with the appointment.
        mhwp_id (int): The ID of the MHWP associated with the appointment.
        date (datetime): The date of the appointment.
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
    def __init__(self, record_id, patient_id, mhwp_id, notes, conditions):
        """
        Initialize a PatientRecord object.

        Parameters:
        record_id (int): The unique identifier for the patient record.
        patient_id (int): The ID of the patient associated with the record.
        mhwp_id (int): The ID of the MHWP associated with the record.
        notes (str): The notes associated with the patient record.
        conditions (list): The conditions associated with the patient record.
        """
        self.record_id = record_id
        self.patient_id = patient_id  # foreign key to Patient
        self.mhwp_id = mhwp_id        # foreign key to MHWP
        self.notes = notes
        self.conditions = conditions

## Allocation class
class Allocation:
    """A class to represent an allocation."""
    def __init__(self, allocation_id, admin_id, patient_id, mhwp_id, start_date, end_date):
        """
        Initialize an Allocation object.

        Parameters:
        allocation_id (int): The unique identifier for the allocation.
        admin_id (int): The ID of the admin associated with the allocation.
        patient_id (int): The ID of the patient associated with the allocation.
        mhwp_id (int): The ID of the MHWP associated with the allocation.
        start_date (datetime): The start date of the allocation.
        end_date (datetime): The end date of the allocation.
        """
        self.allocation_id = allocation_id
        self.admin_id = admin_id      # foreign key to Admin
        self.patient_id = patient_id  # foreign key to Patient
        self.mhwp_id = mhwp_id        # foreign key to MHWP
        self.start_date = start_date
        self.end_date = end_date

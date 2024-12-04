from datetime import datetime
import re
import os 
from .dataStructs import Relation
import logging

__all__ = [
    'InvalidDataError',
    'User',
    'Admin',
    'Patient',
    'MHWP',
    'PatientRecord',
    'Allocation',
    'JournalEntry',
    'Appointment',
    'MoodEntry',
    'MHWPReview',
    'ChatContent',
    'Forum',
    'Notification',
    'ExerRecord'
]


class InvalidDataError(ValueError):
    """Exception raised for errors in the input data."""

    def __init__(self, message: str):
        super().__init__(message)


class User:
    """A class to represent a user in the system."""

    def __init__(self, user_id: int = None, username: str = '', password: str = '', user_type: str = '',
                 is_disabled: bool = False):
        """
        Initialize a User object.

        Parameters:
        user_id (int, optional): The unique identifier for the user. Can be None.
        username (str): The username of the user.
        password (str): The password for the user.
        user_type (str): The type of user (e.g., 'Admin', 'Patient', 'MHWP').
        is_disabled (bool): Flag indicating if the user is disabled.
        """

        raise RuntimeError("User should not be directly initialized, please use Patient, MHWP, or Admin class.")

    @staticmethod
    def checkValidDataStatic(user_id, username, password, type, is_disabled):
        if user_id is not None and not isinstance(user_id, int):
            raise InvalidDataError(f"User ID must be an integer if provided. (given {user_id})")

        if not username:
            raise InvalidDataError("Username cannot be null.")

        if len(username) > 50:
            raise InvalidDataError("Username must be 3-50 characters long.")

        if not re.match(r'^[a-zA-Z0-9_.-]{3,50}$', username):
            raise InvalidDataError("Username may only contain letters, numbers, and a few special characters (- . _).")

        if re.search(r'[!@#$%^&*(),?":{}|<>]', username):
            raise InvalidDataError("Username contains invalid special characters.")

        if not password:
            raise InvalidDataError("Password cannot be empty.")

        if len(password) < 8:
            raise InvalidDataError("Password must be at least 8 characters long.")

        if type not in ['Admin', 'MHWP', 'Patient']:
            raise InvalidDataError("Type must be one of the following: 'Admin', 'MHWP', 'Patient'.")

        if is_disabled is None:
            raise InvalidDataError("Is_disabled cannot be None.")

        return True


class Admin(User):
    """A class to represent an admin user."""

    def __init__(self,
                 user_id: int = None,
                 username: str = '',
                 password: str = '',
                 is_disabled: bool = False):
        """
        Initialize an Admin object.

        Parameters:
        user_id (int, optional): The unique identifier for the admin. Can be None.
        username (str): The username of the admin.
        password (str): The password for the admin.
        is_disabled (bool): Flag indicating if the admin is disabled.
        """
        self.user_id = user_id
        self.username = username
        self.password = password
        self.type = 'Admin'
        self.is_disabled = is_disabled

        ## Check user data correctness
        User.checkValidDataStatic(self.user_id, self.username, self.password, self.type, self.is_disabled)


class Patient(User):
    """A class to represent a patient user."""

    def __init__(self,
                 user_id: int = None,
                 username: str = '',
                 email: str = '',
                 password: str = '',
                 fName: str = '',
                 lName: str = '',
                 emergency_contact_email: str = None,
                 emergency_contact_name: str = None,
                 is_disabled: bool = False):
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

        self.user_id = user_id
        self.username = username
        self.password = password
        self.type = 'Patient'
        self.is_disabled = is_disabled

        self.fName = fName
        self.lName = lName
        self.email = email
        self.emergency_contact_email = emergency_contact_email
        self.emergency_contact_name = emergency_contact_name

        success = self.checkValidData()

        if not success:
            raise InvalidDataError("Data validity check failed.")

    @staticmethod
    def checkValidDataStatic(user_id, username, email, password, fName, lName, type, emergency_contact_email,
                             emergency_contact_name, is_disabled):
        # Check user-specific data
        User.checkValidDataStatic(user_id, username, password, type, is_disabled)

        # Check fName
        if not fName or not re.match(r'^[a-zA-Z]{1,50}$', fName):
            raise InvalidDataError(
                f"First name ({fName}) must be non-empty and contain only alphabetic characters, with a maximum length of 50.")

        # Check lName
        if not lName or not re.match(r'^[a-zA-Z]{1,50}$', lName):
            raise InvalidDataError(
                f"Last name ({lName}) must be non-empty and contain only alphabetic characters, with a maximum length of 50.")

        # Check email
        if not email or not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            raise InvalidDataError(f"Email ({email}) must be non-empty and follow a valid email format.")

        # Check emergency_contact_email
        if emergency_contact_email and not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
                                                    emergency_contact_email):
            raise InvalidDataError("Emergency contact email must follow a valid email format if provided.")

        # Check emergency_contact_name
        if emergency_contact_name and not re.match(r'^[a-zA-Z ]{1,50}$', emergency_contact_name):
            raise InvalidDataError(
                "Emergency contact name must contain only alphabetic characters and spaces, with a maximum length of 50, if provided.")

        return True

    def checkValidData(self):
        return Patient.checkValidDataStatic(self.user_id, self.username, self.email, self.password, self.fName,
                                            self.lName, self.type, self.emergency_contact_email,
                                            self.emergency_contact_name, self.is_disabled)


class MHWP(User):
    """A class to represent a mental health worker professional (MHWP) user."""

    def __init__(self,
                 user_id: int = None,
                 username: str = '',
                 email: str = '',
                 password: str = '',
                 fName: str = '',
                 lName: str = '',
                 specialization: str = '',
                 is_disabled: bool = False,
                 specializations_file = 'specializations.txt'):
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
        self.user_id = user_id
        self.username = username
        self.password = password
        self.type = 'MHWP'
        self.is_disabled = is_disabled

        self.fName = fName
        self.lName = lName
        self.email = email
        self.specialization = specialization

        app_directory = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        specializations_file = os.path.join(app_directory, specializations_file)

        try:
            with open(specializations_file, 'r') as file:
                self.valid_specializations_list = [re.sub(r'\(.*?\)', '', line).strip() for line in file.readlines()]
        except FileNotFoundError:
            raise InvalidDataError(f"Conditions file '{specializations_file}' not found.")
        except Exception as e:
            raise InvalidDataError(f"An error occurred while loading conditions file: {str(e)}")

        success = self.checkValidData()

        if not success:
            raise InvalidDataError("Data validity check failed.")

    @staticmethod
    def checkValidDataStatic(user_id, username, email, password, fName, lName, type, specialization, is_disabled):
        # Check user-specific data
        User.checkValidDataStatic(user_id, username, password, type, is_disabled)

        # Check fName
        if not fName or not re.match(r'^[a-zA-Z]{1,50}$', fName):
            raise InvalidDataError(
                f"First name ({fName}) must be non-empty and contain only alphabetic characters, with a maximum length of 50.")

        # Check lName
        if not lName or not re.match(r'^[a-zA-Z]{1,50}$', lName):
            raise InvalidDataError(
                f"Last name {lName} must be non-empty and contain only alphabetic characters, with a maximum length of 50.")

        # Check email
        if not email or not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            raise InvalidDataError("Email must be non-empty and follow a valid email format.")

        # Check specialization
        if specialization and not re.match(r'^[a-zA-Z\s]+$', specialization):
            raise InvalidDataError("Specialization must contain only alphabetic characters and spaces if provided.")

        return True

    def checkValidSpecialization(self, specialization : str):
        if specialization not in self.valid_specializations_list:
            raise InvalidDataError(f"Specialization {specialization} is not a valid specialization.")
        else:
            return True
        
    def checkValidData(self):
        success = MHWP.checkValidDataStatic(self.user_id, self.username, self.email, self.password, self.fName, self.lName,
                                         self.type, self.specialization, self.is_disabled) 
        success = success and self.checkValidSpecialization(self.specialization) ## check if specialization is valid
        return success 
    
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

        success = self.checkValidData()

        if not success:
            raise InvalidDataError("Data validity check failed.")

    @staticmethod
    def checkValidDataStatic(entry_id, patient_id, text, timestamp):
        if entry_id is not None and not isinstance(entry_id, int):
            raise InvalidDataError("Entry ID must be an integer if provided.")

        if patient_id is None:
            raise InvalidDataError("Patient ID must not be None.")
        elif patient_id is not None and not isinstance(patient_id, int):
            raise InvalidDataError("Patient ID must be an integer.")

        if not text:
            raise InvalidDataError("Text cannot be empty.")

        if timestamp is None:
            raise InvalidDataError("Timestamp cannot be None.")
        if not isinstance(timestamp, datetime):
            raise InvalidDataError("Timestamp must be a datetime object.")

        return True

    def checkValidData(self):
        return JournalEntry.checkValidDataStatic(self.entry_id, self.patient_id, self.text, self.timestamp)


class Appointment:
    """A class to represent an appointment."""

    def __init__(self, appointment_id: int = None, 
                 patient_id: int = None, 
                 mhwp_id: int = None, 
                 date: datetime = None,
                 room_name: str = None, 
                 status: str = '',
                 collisionChecking: bool = True,
                 appointmentRelation : Relation = None):
        """
        Initialize an Appointment object.

        Parameters:
        appointment_id (int, optional): The unique identifier for the appointment. Can be None.
        patient_id (int, optional): The ID of the patient associated with the appointment. Can be None.
        mhwp_id (int, optional): The ID of the MHWP associated with the appointment. Can be None.
        date (datetime, optional): The date of the appointment. Can be None.
        status (str): The status of the appointment. Can be an empty string.
        relationReferenceChecking (bool, optional): Whether to check for collisions using appointmentsRelation. Defaults to True.
        appointmentRelation (Relation, optional): The relation associated with the appointment. Can be None.
        """

        self.appointment_id = appointment_id
        self.patient_id = patient_id  # foreign key to Patient
        self.mhwp_id = mhwp_id  # foreign key to MHWP
        if date and isinstance(date, datetime):
            self.date = date.replace(second=0, microsecond=0) ### clean date of seconds and microseconds
        else:
            self.date = date
        self.room_name = room_name
        self.status = status
        self.appointmentRelation = appointmentRelation

        success = self.checkValidData()

        if not success:
            raise InvalidDataError("Data validity check failed.")

    @staticmethod
    def checkValidDataStatic(appointment_id, patient_id, mhwp_id, date, room_name, status):
        if appointment_id is not None and not isinstance(appointment_id, int):
            raise InvalidDataError("Appointment ID must be an integer if provided.")

        if patient_id is None:
            raise InvalidDataError("Patient ID must not be None.")
        if not isinstance(patient_id, int):
            raise InvalidDataError("Patient ID must be an integer.")

        if mhwp_id is None:
            raise InvalidDataError("MHWP ID must not be None.")
        if not isinstance(mhwp_id, int):
            raise InvalidDataError("MHWP ID must be an integer.")

        if date is None:
            raise InvalidDataError("Timestamp cannot be None.")
        if not isinstance(date, datetime):
            raise InvalidDataError("Timestamp must be a datetime object.")

        if room_name is None:
            raise InvalidDataError("Room name must not be None.")
        if room_name == '':
            raise InvalidDataError("Room name must not be an empty string.")
        if len(room_name) > 50:
            raise InvalidDataError("Room name must be 50 characters or less.")

        if not status:
            raise InvalidDataError("Status cannot be empty.")

        return True

    @staticmethod 
    def checkTimeAndRoomCollisions(dateAndTime: datetime, room_name : str, appointmentRelation : Relation):
        simultaneousAppointments = appointmentRelation.getWhereEqual("date", dateAndTime)
        if simultaneousAppointments is None or len(simultaneousAppointments) <= 0: ### no simultaneous appointments --> no collisions
            return True
        else:
            equilocalAppointments = simultaneousAppointments.getWhereEqual('room_name', room_name)
            if equilocalAppointments is None or len(equilocalAppointments) <= 0: ### simultaneous appointments all happen in different rooms --> no collisions
                return True
            else:
                raise InvalidDataError("Appointment Collision: There is already an appointment for this time in this room.")
        return False


    def checkValidData(self):
        valid = Appointment.checkValidDataStatic(self.appointment_id, self.patient_id, self.mhwp_id, self.date, self.room_name, self.status)
        if self.appointmentRelation is not None:
            if type(self.appointmentRelation) == Relation and self.appointmentRelation.name == "Appointment":
                valid = valid and self.checkTimeAndRoomCollisions(self.date, self.room_name, self.appointmentRelation)
            else:
                raise ValueError("Appointment was initialized with invalid appointment relation reference. Please remove the reference or use db.getRelation('Appointment') to pass the appointment relation.")
        else:
            logging.warning(f"You are creating or validitychecking an appointment entity (id {self.appointment_id}) without the entity having access to appointmentRelation. This means that this Appointment entity can not check whether the date and room provided collide with other appointments. Please pass an appointmentRelation reference (using db.getRelation('Appointment') to enable date/room collision checking.)")
        return valid 

class PatientRecord:
    """A class to represent a patient record entry."""

    def __init__(self, record_id: int = None, patient_id: int = None, mhwp_id: int = None, notes: str = '',
                 conditions: list = None, conditions_file : str = 'conditions.txt'):
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
        self.mhwp_id = mhwp_id  # foreign key to MHWP
        self.notes = notes
        self.conditions = conditions

        app_directory = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        conditions_file = os.path.join(app_directory, conditions_file)

        try:
            with open(conditions_file, 'r') as file:
                self.valid_conditions_list = [re.sub(r'\(.*?\)', '', line).strip() for line in file.readlines()]
        except FileNotFoundError:
            raise InvalidDataError(f"Conditions file '{conditions_file}' not found.")
        except Exception as e:
            raise InvalidDataError(f"An error occurred while loading conditions file: {str(e)}")

        success = self.checkValidData()

        if not success:
            raise InvalidDataError("Data validity check failed.")

    @staticmethod
    def checkValidDataStatic(record_id, patient_id, mhwp_id, notes, conditions, validConditions : list = None):
        if record_id is not None and not isinstance(record_id, int):
            raise InvalidDataError("Record ID must be an integer if provided.")

        if patient_id is None:
            raise InvalidDataError("Patient ID must not be None.")
        if not isinstance(patient_id, int):
            raise InvalidDataError("Patient ID must be an integer if provided.")

        if mhwp_id is None:
            raise InvalidDataError("MHWP ID must not be None.")
        if not isinstance(mhwp_id, int):
            raise InvalidDataError("MHWP ID must be an integer if provided.")

        if notes is None:
            raise InvalidDataError("Notes must not be None.")
        if len(notes.split()) > 500:
            raise InvalidDataError("Notes must not exceed 500 words.")

        if conditions is None:
            raise InvalidDataError("Conditions must be a list, not None. Pass an empty list if there are no conditions.")
        elif not isinstance(conditions, list):
            raise InvalidDataError("Conditions must be a list.")
        else: ## conditions is a list
            for condition in conditions:
                if validConditions is not None and condition not in validConditions:
                    raise InvalidDataError(f"Condition '{condition}' was not recognized as valid condition.")

        return True

    def checkValidData(self):
        return PatientRecord.checkValidDataStatic(self.record_id, self.patient_id, self.mhwp_id, self.notes, self.conditions, self.valid_conditions_list)


class Allocation:
    """A class to represent an allocation."""

    def __init__(self, allocation_id: int = None, admin_id: int = None, patient_id: int = None, mhwp_id: int = None,
                 start_date: datetime = None, end_date: datetime = None):
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
        self.admin_id = admin_id  # foreign key to Admin
        self.patient_id = patient_id  # foreign key to Patient
        self.mhwp_id = mhwp_id  # foreign key to MHWP
        self.start_date = start_date
        self.end_date = end_date

        success = self.checkValidData()

        if not success:
            raise InvalidDataError("Data validity check failed.")

    @staticmethod
    def checkValidDataStatic(allocation_id, admin_id, patient_id, mhwp_id, start_date, end_date):
        if allocation_id is not None and not isinstance(allocation_id, int):
            raise InvalidDataError("Allocation ID must be an integer if provided.")

        if admin_id is None or not isinstance(admin_id, int):
            raise InvalidDataError("Admin ID must be an integer and not None.")

        if patient_id is None or not isinstance(patient_id, int):
            raise InvalidDataError("Patient ID must be an integer and not None.")

        if mhwp_id is None or not isinstance(mhwp_id, int):
            raise InvalidDataError("MHWP ID must be an integer and not None.")

        if start_date is None:
            raise InvalidDataError("Start date must not be None.")
        if not isinstance(start_date, datetime):
            raise InvalidDataError("Start date must be a datetime object.")

        if end_date is None:
            raise InvalidDataError("End date must not be None.")
        if not isinstance(end_date, datetime):
            raise InvalidDataError("End date must be a datetime object.")

        return True

    def checkValidData(self):
        return Allocation.checkValidDataStatic(self.allocation_id, self.admin_id, self.patient_id, self.mhwp_id,
                                         self.start_date, self.end_date)


class MoodEntry:
    """
    A class to represent a mood entry for a patient.

    Attributes:
    moodentry_id (int, optional): The unique identifier for the mood entry. Can be None.
    patient_id (int, optional): The ID of the patient associated with the mood entry. Can be None.
    moodscore (int, optional): The mood score of the patient. Can be None.
    comment (str): A comment associated with the mood entry.
    timestamp (datetime, optional): The timestamp of when the mood entry was recorded. Can be None.
    """

    def __init__(self, moodentry_id: int = None, patient_id: int = None, moodscore: int = None, comment: str = '',
                 timestamp: datetime = None):

        self.moodentry_id = moodentry_id
        self.patient_id = patient_id  # foreign key to Patient
        self.moodscore = moodscore
        self.comment = comment
        self.timestamp = timestamp

        success = self.checkValidData()

        if not success:
            raise InvalidDataError("Data validity check failed.")

    @staticmethod
    def checkValidDataStatic(moodentry_id, patient_id, moodscore, comment, timestamp):
        if moodentry_id is not None and not isinstance(moodentry_id, int):
            raise InvalidDataError("Mood entry ID must be an integer if provided.")

        if patient_id is None:
            raise InvalidDataError("Patient ID must not be None.")
        if not isinstance(patient_id, int):
            raise InvalidDataError("Patient ID must be an integer.")

        if moodscore is None:
            raise InvalidDataError("Mood score must not be None.")
        if not isinstance(moodscore, int):
            raise InvalidDataError("Mood score must be an integer.")
        if moodscore < 1 or moodscore > 6:
            raise InvalidDataError("Mood score must be an integer between 1 and 6.")

        if comment is None:
            raise InvalidDataError("Comment must not be None.")
        if not isinstance(comment, str):
            raise InvalidDataError("Comment must be a string.")
        if len(comment) >= 255:
            raise InvalidDataError("Comment must be below 255 characters.")

        if timestamp is None:
            raise InvalidDataError("Timestamp must not be None.")
        if not isinstance(timestamp, datetime):
            raise InvalidDataError("Timestamp must be a datetime object.")

        return True

    def checkValidData(self):
        return MoodEntry.checkValidDataStatic(self.moodentry_id, self.patient_id, self.moodscore, self.comment,
                                         self.timestamp)


class MHWPReview:
    """
    A class to represent a review for a Mental Health Worker Professional (MHWP).
     """

    def __init__(self, MHWP_review_id: int = None, patient_id: int = None, mhwp_id: int = None, reviewscore: int = None,
                 reviewcomment: str = '', timestamp: datetime = None):
        """
        Initialize an MHWPReview object.

        Parameters:
        MHWP_review_id (int, optional): The unique identifier for the review. Can be None.
        patient_id (int, optional): The unique identifier for the patient. Must not be None.
        mhwp_id (int, optional): The unique identifier for the MHWP. Must not be None.
        reviewscore (int, optional): The score given in the review. Must be an integer between 0 and 5.
        reviewcomment (str): The comment provided in the review. Must be less than 255 characters.
        timestamp (datetime, optional): The time when the review was created. Must not be None.
        """

        self.MHWP_review_id = MHWP_review_id
        self.patient_id = patient_id
        self.mhwp_id = mhwp_id  # foreign key to Patient
        self.reviewscore = reviewscore
        self.reviewcomment = reviewcomment
        self.timestamp = timestamp

        success = self.checkValidData()

        if not success:
            raise InvalidDataError("Data validity check failed.")

    @staticmethod
    def checkValidDataStatic(MHWP_review_id, patient_id, mhwp_id, reviewscore, reviewcomment, timestamp):
        if MHWP_review_id is not None and not isinstance(MHWP_review_id, int):
            raise InvalidDataError("MHWP review ID must be an integer if provided.")

        if patient_id is None:
            raise InvalidDataError("Patient ID must not be None.")
        if not isinstance(patient_id, int):
            raise InvalidDataError("Patient ID must be an integer.")

        if mhwp_id is None:
            raise InvalidDataError("MHWP ID must not be None.")
        if not isinstance(mhwp_id, int):
            raise InvalidDataError("MHWP ID must be an integer.")

        if reviewscore is None:
            raise InvalidDataError("Review score must not be None.")
        if not isinstance(reviewscore, int):
            raise InvalidDataError("Review score must be an integer.")
        if reviewscore < 0 or reviewscore > 5:
            raise InvalidDataError("Review score must be an integer ranging from 0 to 5.")

        if not isinstance(reviewcomment, str):
            raise InvalidDataError("Review comment must be a string.")
        if len(reviewcomment) >= 255:
            raise InvalidDataError("Review comment must be less than 255 characters.")

        if timestamp is None:
            raise InvalidDataError("Timestamp must not be None.")
        if not isinstance(timestamp, datetime):
            raise InvalidDataError("Timestamp must be a datetime object.")

        return True

    def checkValidData(self):
        return MHWPReview.checkValidDataStatic(self.MHWP_review_id, self.patient_id, self.mhwp_id, self.reviewscore,
                                         self.reviewcomment, self.timestamp)


class ChatContent:
    def __init__(self, chatcontent_id: int = None, allocation_id: int = None, user_id: int = None, text: str = '',
                 timestamp: datetime = None):

        self.chatcontent_id = chatcontent_id
        self.allocation_id = allocation_id
        self.user_id = user_id
        self.text = text
        self.timestamp = timestamp

        success = self.checkValidData()

        if not success:
            raise InvalidDataError("Data validity check failed.")

    @staticmethod
    def checkValidDataStatic(chatcontent_id, allocation_id, user_id, text, timestamp):
        if chatcontent_id is not None and not isinstance(chatcontent_id, int):
            raise InvalidDataError("Chat content ID must be an integer if provided.")

        if allocation_id is None:
            raise InvalidDataError("Allocation ID must not be None.")
        if not isinstance(allocation_id, int):
            raise InvalidDataError("Allocation ID must be an integer.")

        if user_id is None:
            raise InvalidDataError("User ID must not be None.")
        if not isinstance(user_id, int):
            raise InvalidDataError("User ID must be an integer.")

        if text is None:
            raise InvalidDataError("Text must not be None.")
        if not isinstance(text, str):
            raise InvalidDataError("Text must be a string.")
        if text == '':
            raise InvalidDataError("Text must not be an empty string.")
        if len(text) >= 255:
            raise InvalidDataError("Text must be below 255 characters.")

        if timestamp is None:
            raise InvalidDataError("Timestamp must not be None.")
        if not isinstance(timestamp, datetime):
            raise InvalidDataError("Timestamp must be a datetime object.")

        return True

    def checkValidData(self):
        return ChatContent.checkValidDataStatic(self.chatcontent_id, self.allocation_id, self.user_id, self.text,
                                         self.timestamp)


class Forum:
    def __init__(self, thread_id: int = None, parent_id: int = None, topic: str = '', content: str = '',
                 user_id: int = None, timestamp: datetime = None):
        self.thread_id = thread_id
        self.parent_id = parent_id
        self.topic = topic
        self.content = content
        self.user_id = user_id
        self.timestamp = timestamp


class Notification:
    def __init__(self, notification_id: int = None, user_id: int = None, notifycontent: str = '', source_id: int = None,
                 new: bool = None, timestamp: datetime = None):
        self.notification_id = notification_id
        self.user_id = user_id
        self.notifycontent = notifycontent
        self.source_id = source_id
        self.new = new
        self.timestamp = timestamp

class ExerRecord:
    def __init__(self, record_id: int = None, user_id: int = None, exercise: str = '',timestamp: datetime = None):
        self.record_id = record_id
        self.user_id = user_id
        self.exercise = exercise
        self.timestamp = timestamp

class UserError(Exception):
    """Custom exception for user-related errors."""
    pass






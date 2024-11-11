# Custom exception classes
class UserError(Exception):
    pass
class UserAlreadyExistsError(UserError):
    pass
class UserNotFoundError(UserError):
    pass
class InvalidUserTypeError(UserError):
    pass
class RecordError(Exception):
    pass
class RecordAlreadyExistsError(RecordError):
    pass
class RecordNotFoundError(RecordError):
    pass

# Entities
## Base User class
class User():
    def __init__(self, user_id, username, password, user_type, is_disabled=False):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.type = user_type
        self.is_disabled = is_disabled

## Admin class inheriting from User
class Admin(User):
    def __init__(self, user_id, username, password, is_disabled=False):
        super().__init__(user_id, username, password, 'Admin', is_disabled)

## Patient class inheriting from User
class Patient(User):
    def __init__(self, user_id, username, password, fName, lName, email,
                 emergency_contact_email=None, moods=None, mood_comments=None, is_disabled=False):
        super().__init__(user_id, username, password, 'Patient', is_disabled)
        self.fName = fName
        self.lName = lName
        self.email = email
        self.emergency_contact_email = emergency_contact_email
        self.moods = moods
        self.mood_comments = mood_comments

## MHWP class inheriting from User
class MHWP(User):
    def __init__(self, user_id, username, password, fName, lName, email, specialization, is_disabled=False):
        super().__init__(user_id, username, password, 'MHWP', is_disabled)
        self.fName = fName
        self.lName = lName
        self.email = email
        self.specialization = specialization

## JournalEntry class
class JournalEntry():
    def __init__(self, entry_id, patient_id, text, timestamp):
        self.entry_id = entry_id
        self.patient_id = patient_id  # foreign key to Patient
        self.text = text
        self.timestamp = timestamp

## Appointment class
class Appointment:
    def __init__(self, appointment_id, patient_id, mhwp_id, date, status):
        self.appointment_id = appointment_id
        self.patient_id = patient_id  # foreign key to Patient
        self.mhwp_id = mhwp_id        # foreign key to MHWP
        self.date = date
        self.status = status

## PatientRecord class
class PatientRecord:
    def __init__(self, record_id, patient_id, mhwp_id, notes, conditions):
        self.record_id = record_id
        self.patient_id = patient_id  # foreign key to Patient
        self.mhwp_id = mhwp_id        # foreign key to MHWP
        self.notes = notes
        self.conditions = conditions

## Allocation class
class Allocation:
    def __init__(self, allocation_id, admin_id, patient_id, mhwp_id, start_date, end_date):
        self.allocation_id = allocation_id
        self.admin_id = admin_id      # foreign key to Admin
        self.patient_id = patient_id  # foreign key to Patient
        self.mhwp_id = mhwp_id        # foreign key to MHWP
        self.start_date = start_date
        self.end_date = end_date

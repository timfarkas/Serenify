import pandas as pd
import pickle
import os
import logging


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
class User:
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
    def __init__(self, user_id, username, password, name, email,
                 emergency_contact_email=None, mood=None, mood_comment=None, is_disabled=False):
        super().__init__(user_id, username, password, 'Patient', is_disabled)
        self.name = name
        self.email = email
        self.emergency_contact_email = emergency_contact_email
        self.mood = mood
        self.mood_comment = mood_comment

## MHWP class inheriting from User
class MHWP(User):
    def __init__(self, user_id, username, password, name, email, specialization, is_disabled=False):
        super().__init__(user_id, username, password, 'MHWP', is_disabled)
        self.name = name
        self.email = email
        self.specialization = specialization

## JournalEntry class
class JournalEntry:
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

## Database class
class Database:
    """
    A class to represent a database for managing users, admins, patients, MHWPs, journal entries,
    appointments, patient records, and allocations.

    Attributes
    ----------
    data_file : str
        The file path for storing the database.
    logger : logging.Logger
    verbose : bool
        A flag to enable debug logging.

    Methods
    -------
    close():
        Saves the database state and closes database. 
    """

    def __init__(self, data_file:str='database.pkl', logger: logging.Logger = None, verbose: bool = False):
        """
        Constructs all the necessary attributes for the Database object.

        Parameters
        ----------
        data_file : str, optional
            The file path for storing the database (default is 'database.pkl').
        logger : logging.Logger, optional
            The logger for logging database operations (default is None, which creates a new logger).
        verbose : bool, optional
            A flag to enable debug logging (default is False).
        """
        if logger is None:
            logger = logging.getLogger(__name__)
            logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            logger.addHandler(handler)
            self.logger = logger
        else:
            self.logger = logger

        if verbose:
            self.logger.setLevel(logging.DEBUG)
        
        self.logger.info("Initializing database...")

        self.data_file = data_file
        if os.path.exists(self.data_file):
            self.logger.info(f"Found database file {data_file}, loading from file...")
            self.__load_database()
            self.logger.info("Success loading database")
        else:
            # Initialize tables as DataFrames
            self.logger.info(f"Found no database file {data_file}, initializing new database...")
            self.users = pd.DataFrame(columns=['user_id', 'username', 'password', 'type', 'is_disabled'])
            self.admins = pd.DataFrame(columns=['user_id'])
            self.patients = pd.DataFrame(columns=[
                'user_id', 'name', 'email', 'emergency_contact_email', 'mood', 'mood_comment'
            ])
            self.mhwps = pd.DataFrame(columns=['user_id', 'name', 'email', 'specialization'])
            self.journal_entries = pd.DataFrame(columns=['entry_id', 'patient_id', 'text', 'timestamp'])
            self.appointments = pd.DataFrame(columns=[
                'appointment_id', 'patient_id', 'mhwp_id', 'date', 'status'
            ])
            self.patient_records = pd.DataFrame(columns=[
                'record_id', 'patient_id', 'mhwp_id', 'notes', 'conditions'
            ])
            self.allocations = pd.DataFrame(columns=[
                'allocation_id', 'admin_id', 'patient_id', 'mhwp_id', 'start_date', 'end_date'
            ])
        self.logger.info("Successfully initialized database.")

    def close(self):
        self.__save_database()
        self.logger.info("Successfully saved database, exiting")
        del self

    def __load_database(self):
        with open(self.data_file, 'rb') as f:
            data = pickle.load(f)
            self.users = data['users']
            self.admins = data['admins']
            self.patients = data['patients']
            self.mhwps = data['mhwps']
            self.journal_entries = data['journal_entries']
            self.appointments = data['appointments']
            self.patient_records = data['patient_records']
            self.allocations = data['allocations']

    def __save_database(self):
        with open(self.data_file, 'wb') as f:
            pickle.dump({
                'users': self.users,
                'admins': self.admins,
                'patients': self.patients,
                'mhwps': self.mhwps,
                'journal_entries': self.journal_entries,
                'appointments': self.appointments,
                'patient_records': self.patient_records,
                'allocations': self.allocations
            }, f)

    def printAll(self):
        print("Users:")
        print(self.users)
        print("\nAdmins:")
        print(self.admins)
        print("\nPatients:")
        print(self.patients)
        print("\nMHWPs:")
        print(self.mhwps)
        print("\nJournal Entries:")
        print(self.journal_entries)
        print("\nAppointments:")
        print(self.appointments)
        print("\nPatient Records:")
        print(self.patient_records)
        print("\nAllocations:")
        print(self.allocations)

    # User methods
    def insert_user(self, user: User):
        if user.user_id in self.users['user_id'].values:
            raise UserAlreadyExistsError(f"User with user_id {user.user_id} already exists.")
        new_user = {
            'user_id': user.user_id,
            'username': user.username,
            'password': user.password,
            'type': user.type,
            'is_disabled': user.is_disabled
        }
        self.users = pd.concat([self.users, pd.DataFrame([new_user])], ignore_index=True)
        idx = self.users.index[self.users['user_id'] == user.user_id]
        if len(idx) == 0:
            raise UserNotFoundError(f"No user with user_id {user.user_id} exists.")
        self.users.loc[idx, 'username'] = user.username
        self.users.loc[idx, 'password'] = user.password
        self.users.loc[idx, 'type'] = user.type
        self.users.loc[idx, 'is_disabled'] = user.is_disabled

    def get_user(self, user_id):
        user_row = self.users[self.users['user_id'] == user_id]
        if user_row.empty:
            raise UserNotFoundError(f"No user with user_id {user_id} exists.")
        user_data = user_row.iloc[0]
        user_type = user_data['type']
        if user_type == 'Admin':
            return self.get_admin(user_id)
        elif user_type == 'Patient':
            return self.get_patient(user_id)
        elif user_type == 'MHWP':
            return self.get_mhwp(user_id)
        else:
            return User(
                user_id=user_data['user_id'],
                username=user_data['username'],
                password=user_data['password'],
                user_type=user_data['type'],
                is_disabled=user_data['is_disabled']
            )

    # Admin methods
    def insert_admin(self, admin: Admin):
        self.insert_user(admin)
        if admin.user_id in self.admins['user_id'].values:
            raise UserAlreadyExistsError(f"Admin with user_id {admin.user_id} already exists.")
        new_admin = {'user_id': admin.user_id}
        self.admins = pd.concat([self.admins, pd.DataFrame([new_admin])], ignore_index=True)

    def get_admin(self, user_id):
        admin_row = self.admins[self.admins['user_id'] == user_id]
        if admin_row.empty:
            raise UserNotFoundError(f"No Admin with user_id {user_id} exists.")
        user_row = self.users[self.users['user_id'] == user_id].iloc[0]
        return Admin(
            user_id=user_row['user_id'],
            username=user_row['username'],
            password=user_row['password'],
            is_disabled=user_row['is_disabled']
        )

    # Patient methods
    def insert_patient(self, patient: Patient):
        self.insert_user(patient)
        if patient.user_id in self.patients['user_id'].values:
            raise UserAlreadyExistsError(f"Patient with user_id {patient.user_id} already exists.")
        new_patient = {
            'user_id': patient.user_id,
            'name': patient.name,
            'email': patient.email,
            'emergency_contact_email': patient.emergency_contact_email,
            'mood': patient.mood,
            'mood_comment': patient.mood_comment
        }
        self.patients = pd.concat([self.patients, pd.DataFrame([new_patient])], ignore_index=True)

    def get_patient(self, user_id):
        patient_row = self.patients[self.patients['user_id'] == user_id]
        if patient_row.empty:
            raise UserNotFoundError(f"No Patient with user_id {user_id} exists.")
        user_row = self.users[self.users['user_id'] == user_id].iloc[0]
        patient_data = patient_row.iloc[0]
        return Patient(
            user_id=user_row['user_id'],
            username=user_row['username'],
            password=user_row['password'],
            name=patient_data['name'],
            email=patient_data['email'],
            emergency_contact_email=patient_data['emergency_contact_email'],
            mood=patient_data['mood'],
            mood_comment=patient_data['mood_comment'],
            is_disabled=user_row['is_disabled']
        )

    # MHWP methods
    def insert_mhwp(self, mhwp: MHWP):
        self.insert_user(mhwp)
        if mhwp.user_id in self.mhwps['user_id'].values:
            raise UserAlreadyExistsError(f"MHWP with user_id {mhwp.user_id} already exists.")
        new_mhwp = {
            'user_id': mhwp.user_id,
            'name': mhwp.name,
            'email': mhwp.email,
            'specialization': mhwp.specialization
        }
        self.mhwps = pd.concat([self.mhwps, pd.DataFrame([new_mhwp])], ignore_index=True)

    def get_mhwp(self, user_id):
        mhwp_row = self.mhwps[self.mhwps['user_id'] == user_id]
        if mhwp_row.empty:
            raise UserNotFoundError(f"No MHWP with user_id {user_id} exists.")
        user_row = self.users[self.users['user_id'] == user_id].iloc[0]
        mhwp_data = mhwp_row.iloc[0]
        return MHWP(
            user_id=user_row['user_id'],
            username=user_row['username'],
            password=user_row['password'],
            name=mhwp_data['name'],
            email=mhwp_data['email'],
            specialization=mhwp_data['specialization'],
            is_disabled=user_row['is_disabled']
        )

    # JournalEntry methods
    def insert_journal_entry(self, journal_entry: JournalEntry):
        if journal_entry.entry_id in self.journal_entries['entry_id'].values:
            raise RecordAlreadyExistsError(f"JournalEntry with entry_id {journal_entry.entry_id} already exists.")
        if journal_entry.patient_id not in self.patients['user_id'].values:
            raise UserNotFoundError(f"No patient with user_id {journal_entry.patient_id} exists.")
        new_entry = {
            'entry_id': journal_entry.entry_id,
            'patient_id': journal_entry.patient_id,
            'text': journal_entry.text,
            'timestamp': journal_entry.timestamp
        }
        self.journal_entries = pd.concat([self.journal_entries, pd.DataFrame([new_entry])], ignore_index=True)

    def get_journal_entry(self, entry_id):
        entry_row = self.journal_entries[self.journal_entries['entry_id'] == entry_id]
        if entry_row.empty:
            raise RecordNotFoundError(f"No JournalEntry with entry_id {entry_id} exists.")
        entry_data = entry_row.iloc[0]
        return JournalEntry(
            entry_id=entry_data['entry_id'],
            patient_id=entry_data['patient_id'],
            text=entry_data['text'],
            timestamp=entry_data['timestamp']
        )

    # Appointment methods
    def insert_appointment(self, appointment: Appointment):
        if appointment.appointment_id in self.appointments['appointment_id'].values:
            raise RecordAlreadyExistsError(f"Appointment with appointment_id {appointment.appointment_id} already exists.")
        if appointment.patient_id not in self.patients['user_id'].values:
            raise UserNotFoundError(f"No patient with user_id {appointment.patient_id} exists.")
        if appointment.mhwp_id not in self.mhwps['user_id'].values:
            raise UserNotFoundError(f"No MHWP with user_id {appointment.mhwp_id} exists.")
        new_appointment = {
            'appointment_id': appointment.appointment_id,
            'patient_id': appointment.patient_id,
            'mhwp_id': appointment.mhwp_id,
            'date': appointment.date,
            'status': appointment.status
        }
        self.appointments = pd.concat([self.appointments, pd.DataFrame([new_appointment])], ignore_index=True)

    def get_appointment(self, appointment_id):
        appointment_row = self.appointments[self.appointments['appointment_id'] == appointment_id]
        if appointment_row.empty:
            raise RecordNotFoundError(f"No Appointment with appointment_id {appointment_id} exists.")
        appointment_data = appointment_row.iloc[0]
        return Appointment(
            appointment_id=appointment_data['appointment_id'],
            patient_id=appointment_data['patient_id'],
            mhwp_id=appointment_data['mhwp_id'],
            date=appointment_data['date'],
            status=appointment_data['status']
        )

    # PatientRecord methods
    def insert_patient_record(self, patient_record: PatientRecord):
        if patient_record.record_id in self.patient_records['record_id'].values:
            raise RecordAlreadyExistsError(f"PatientRecord with record_id {patient_record.record_id} already exists.")
        if patient_record.patient_id not in self.patients['user_id'].values:
            raise UserNotFoundError(f"No patient with user_id {patient_record.patient_id} exists.")
        if patient_record.mhwp_id not in self.mhwps['user_id'].values:
            raise UserNotFoundError(f"No MHWP with user_id {patient_record.mhwp_id} exists.")
        if patient_record.patient_id in self.patient_records['patient_id'].values:
            raise RecordAlreadyExistsError(f"Patient with user_id {patient_record.patient_id} already has a record.")
        new_record = {
            'record_id': patient_record.record_id,
            'patient_id': patient_record.patient_id,
            'mhwp_id': patient_record.mhwp_id,
            'notes': patient_record.notes,
            'conditions': patient_record.conditions
        }
        self.patient_records = pd.concat([self.patient_records, pd.DataFrame([new_record])], ignore_index=True)

    def get_patient_record(self, record_id):
        record_row = self.patient_records[self.patient_records['record_id'] == record_id]
        if record_row.empty:
            raise RecordNotFoundError(f"No PatientRecord with record_id {record_id} exists.")
        record_data = record_row.iloc[0]
        return PatientRecord(
            record_id=record_data['record_id'],
            patient_id=record_data['patient_id'],
            mhwp_id=record_data['mhwp_id'],
            notes=record_data['notes'],
            conditions=record_data['conditions']
        )

    # Allocation methods
    def insert_allocation(self, allocation: Allocation):
        if allocation.allocation_id in self.allocations['allocation_id'].values:
            raise RecordAlreadyExistsError(f"Allocation with allocation_id {allocation.allocation_id} already exists.")
        if allocation.admin_id not in self.admins['user_id'].values:
            raise UserNotFoundError(f"No Admin with user_id {allocation.admin_id} exists.")
        if allocation.patient_id not in self.patients['user_id'].values:
            raise UserNotFoundError(f"No Patient with user_id {allocation.patient_id} exists.")
        if allocation.mhwp_id not in self.mhwps['user_id'].values:
            raise UserNotFoundError(f"No MHWP with user_id {allocation.mhwp_id} exists.")
        new_allocation = {
            'allocation_id': allocation.allocation_id,
            'admin_id': allocation.admin_id,
            'patient_id': allocation.patient_id,
            'mhwp_id': allocation.mhwp_id,
            'start_date': allocation.start_date,
            'end_date': allocation.end_date
        }
        self.allocations = pd.concat([self.allocations, pd.DataFrame([new_allocation])], ignore_index=True)

    def get_allocation(self, allocation_id):
        allocation_row = self.allocations[self.allocations['allocation_id'] == allocation_id]
        if allocation_row.empty:
            raise RecordNotFoundError(f"No Allocation with allocation_id {allocation_id} exists.")
        allocation_data = allocation_row.iloc[0]
        return Allocation(
            allocation_id=allocation_data['allocation_id'],
            admin_id=allocation_data['admin_id'],
            patient_id=allocation_data['patient_id'],
            mhwp_id=allocation_data['mhwp_id'],
            start_date=allocation_data['start_date'],
            end_date=allocation_data['end_date']
        )


# def testExceptions():
#     # Attempt to get a non-existent Patient Record (will raise an exception)
#     try:
#         record = db.get_patient_record(record_id=300)
#         print(vars(record))
#     except RecordNotFoundError as e:
#         print(e)  # Output: No PatientRecord with record_id 300 exists.

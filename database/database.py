import pandas as pd
import pickle
import os
import logging
import sys
from datetime import datetime as date

from .entities import Admin, Patient, MHWP, JournalEntry, Appointment, PatientRecord, Allocation, MoodEntry, MHWPReview, ChatContent, Forum, Notification, ExerRecord
from .entities import __all__ as entity_classes
from .dataStructs import Row, Relation, RowList
import warnings


## Database class
class Database:
    """
    A class to represent a database for managing user, admin, patient, MHWP, journal entry,
    appointment, patient record, and allocation.

    Attributes
    ----------
    data_file : str
        The file path for storing the database.
    logger : logging.Logger
        The logger for logging database operations.
    verbose : bool
        A flag to enable debug logging.

    Methods
    -------
    close():
        Saves the database state and closes the database.
    initRelations():
        Initializes the relations (tables) in the database.
    initDict():
        Initializes the dictionary mapping entity names to their respective relations.
    __load_database():
        Loads the database from a file.
    __save_database():
        Saves the current state of the database to a file.
    __str__():
        Returns a string representation of the database.
    printAll():
        Prints all the data in the database.
    insert(entity, row, rowList):
        Inserts a row or a list of rows into the specified entity's relation.
    getId(entity, id):
        Retrieves rows from the specified entity's relation where the primary key matches the given id.
    getRelation(entity):
        Returns the relation object for the specified entity.
    insert_admin(admin):
        Inserts an admin user into the User relation.
    insert_patient(patient):
        Inserts a patient user into the User relation.
    insert_mhwp(mhwp):
        Inserts an MHWP user into the User relation.
    insert_allocation(allocation):
        Inserts an allocation into the Allocation relation.
    insert_journal_entry(journal_entry):
        Inserts a journal entry into the JournalEntry relation.
    insert_patient_record(patient_record):
        Inserts a patient record into the PatientRecord relation.
    insert_appointment(appointment):
        Inserts an appointment into the Appointment relation.
    """

    def __init__(self, data_file: str = 'database.pkl', logger: logging.Logger = None, verbose: bool = False,
                 overwrite: bool = False):
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
        overwrite : bool, optional
            A flag to determine whether to overwrite the existing database file (default is False).
        """
        self._is_closed = False
        self.logger = logger if logger is not None else logging.getLogger(__name__)
        if not self.logger.hasHandlers():
            self.logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(handler)

        if verbose:
            self.logger.setLevel(logging.DEBUG)

        self.logger.info("Initializing database...")

        self.app_directory = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

        self.data_file = os.path.join(self.app_directory, data_file)
        if os.path.exists(self.data_file) and not overwrite:
            self.logger.info(f"Found database file {self.data_file}, loading from file...")
            self.__load_database()
            self.logger.info("Success loading database")
        elif os.path.exists(self.data_file) and overwrite:
            self.logger.info(f"Overwriting existing database file {self.data_file}...")
            self.initRelations()
            self.logger.info("Successfully initialized new database with overwriting.")
        else:
            self.logger.info(f"Found no database file {self.data_file}, initializing new database...")
            self.initRelations()
        self.logger.info("Successfully initialized database.")

    def ensure_open(func):
        def wrapper(self, *args, **kwargs):
            if self._is_closed:
                raise RuntimeError("You are performing an action on an instance of database that has already been closed. Try opening a new Database instance or removing the close statement.")
            return func(self, *args, **kwargs)

        return wrapper

    @ensure_open
    def close(self):
        """
        Saves the current state of the database to a file and deletes the database object.
        """
        self.__save_database()
        self.logger.info("Successfully saved database, exiting")

        self.__dict__.clear()
        self._is_closed = True

    @ensure_open
    def initRelations(self):
        """
        Initializes the relations (tables) in the database with predefined schemas.
        """
        self.user = Relation('User',
                             attributeLabels=['user_id',  # 0
                                              'username',  # 1
                                              'email',  # 2
                                              'password',  # 3
                                              'fName',  # 4
                                              'lName',  # 5
                                              'type',  # 6
                                              'emergency_contact_email',  # 7
                                              'emergency_contact_name',  # 8
                                              'specialization',  # 9
                                              'is_disabled'],  # 10
                             relationAttributeTypes=[int, str, str, str, str, str, str, str, str, str, bool],
                             allowDeletedEntry=True, ## support this for MHWP only, for Patients, use db.delete_patient() instead which handles destructive deletion propagation
                             deletedEntryValues=['DeletedMHWP','DeletedEmail', None, 'DeletedMHWP', 'DeletedMHWP', 'MHWP', None, None, 'DeletedMHWP', True])

        self.journal_entry = Relation('JournalEntry',
                                      attributeLabels=['entry_id', 'patient_id', 'text', 'timestamp'],
                                      relationAttributeTypes=[int, int, str, date])

        self.appointment = Relation('Appointment',
                                    attributeLabels=['appointment_id', 'patient_id', 'mhwp_id', 'date', 'room_name',
                                                     'status'],
                                    relationAttributeTypes=[int, int, int, date, str, str])

        self.patient_record = Relation('PatientRecord',
                                       attributeLabels=['record_id', 'patient_id', 'mhwp_id', 'notes', 'conditions'],
                                       relationAttributeTypes=[int, int, int, str, list])

        self.allocation = Relation('Allocation',
                                   attributeLabels=['allocation_id', 'admin_id', 'patient_id', 'mhwp_id', 'start_date',
                                                    'end_date'],
                                   relationAttributeTypes=[int, int, int, int, date, date])

        """New entities created for new features."""
        self.mood_entry = Relation('MoodEntry',
                                   attributeLabels=['moodentry_id', 'patient_id', 'moodscore', 'comment', 'timestamp'],
                                   relationAttributeTypes=[int, int, int, str, date])

        self.review_entry = Relation('MHWPReview',
                                     attributeLabels=['MHWP_review_id', 'patient_id', 'mhwp_id', 'reviewscore',
                                                      'reviewcomment', 'timestamp'],
                                     relationAttributeTypes=[int, int, int, int, str, date])
        #
        self.forum = Relation('Forum',
                              attributeLabels=['thread_id', 'parent_id', 'topic', 'content', 'user_id',
                                               'timestamp'],
                              relationAttributeTypes=[int, int, str, str, int, date])

        self.chatcontent = Relation('ChatContent',
                                    attributeLabels=['chatcontent_id', 'allocation_id', 'user_id', 'text',
                                                     'timestamp'],
                                    relationAttributeTypes=[int, int, int, str, date])

        self.notification = Relation('Notification',
                                     attributeLabels=['notification_id', 'user_id', 'notifytcontent', 'source_id',
                                                      'new', 'timestamp'],
                                     relationAttributeTypes=[int, int, str, int, bool, date])


        self.exerrecord= Relation('ExerRecord',
                                     attributeLabels=['record_id', 'user_id', 'exercise', 'timestamp'],
                                     relationAttributeTypes=[int, int, str, date])

        self.initDict()

    @ensure_open
    def initDict(self):
        """
        Initializes the dictionary mapping entity names to their respective relations.
        """
        self.dataDict = {
            'User':self.user,
            'JournalEntry':self.journal_entry,
            'Appointment':self.appointment,
            'PatientRecord':self.patient_record,
            'Allocation':self.allocation,
            'MoodEntry':self.mood_entry,
            'MHWPReview':self.review_entry,
            'ChatContent':self.chatcontent,
            'Forum': self.forum,
            'Notification': self.notification,
            'ExerRecord': self.exerrecord,
        } 


    @ensure_open
    def __load_database(self):
        """
        Loads the database from a file, restoring the state of all relations.
        """
        self.logger.info(f"Loading DB from {self.data_file}")
        try:
            with open(self.data_file, 'rb') as f:
                data = pickle.load(f) ## if this causes issues, you might want to try removing (and reinitializing) your database.pkl file
                self.user = data['user']
                self.journal_entry = data['journal_entry']
                self.appointment = data['appointment']
                self.patient_record = data['patient_record']
                self.allocation = data['allocation']
                self.mood_entry = data['mood_entry']
                self.review_entry = data['review_entry']
                self.chatcontent = data['chatcontent']
                self.forum = data['forum']
                self.notification = data['notification']
                self.exerrecord = data['exerrecord']
            self.initDict()
        except KeyError as k: ## catch errors being caused by old data
            self.logger.warn(f"Could not find a relation in {self.data_file}. Try deleting (and reinitializing) database.pkl.",k)
        except ModuleNotFoundError as m: ## pickle having different module structure
            self.logger.warn(f"Error when opening {self.data_file}. This might be caused by imports having been wrongly structured when last saving the database. Try deleting (and reinitializing) database.pkl.",k)
        except Exception as e:
            raise e

    @ensure_open
    def __save_database(self):
        """
        Saves the current state of the database to a file.
        """
        with open(self.data_file, 'wb') as f:
            pickle.dump({
                'user': self.user,
                'journal_entry': self.journal_entry,
                'appointment': self.appointment,
                'patient_record': self.patient_record,
                'allocation': self.allocation,
                'mood_entry': self.mood_entry,
                'review_entry': self.review_entry,
                'forum': self.forum,
                'chatcontent': self.chatcontent,
                'notification': self.notification,
                'exerrecord':self.exerrecord,
            }, f)

    @ensure_open
    def __str__(self):
        """
        Returns a string representation of the database, showing all relations and their data.
        """
        return "User:\n" + str(self.user) + "\nJournal Entry:\n" + str(self.journal_entry) + "\nAppointment:\n" + str(
            self.appointment) + "\nPatient Record:\n" + str(self.patient_record) + "\nAllocation:\n" + str(
            self.allocation) + "\nMood Entry\n" + str(self.mood_entry) + "\nChat Content\n" + str(self.chatcontent)

    @ensure_open
    def printAll(self):
        """
        Prints all the data in the database, relation by relation.
        """
        print("User:")
        print(self.user)
        print("\nJournal Entry:")
        print(self.journal_entry)
        print("\nAppointment:")
        print(self.appointment)
        print("\nPatient Record:")
        print(self.patient_record)
        print("\nAllocation:")
        print(self.allocation)
        print("\nMood Entry:")
        print(self.mood_entry)
        print("\nReview Entry:")
        print(self.review_entry)
        print("\nForum:")
        print(self.forum)
        print("\nChat Content:")
        print(self.chatcontent)
        print("\nNotification:")
        print(self.notification)
        print("\nExerRecord:")
        print(self.exerrecord)

    @ensure_open
    def insert(self, entity: str, row: Row = None, rowList: RowList = None):
        """
        Inserts a row or a list of rows into the specified entity's relation.

        Parameters
        ----------
        entity : str
            The name of the entity (relation) to insert data into.
        row : Row, optional
            A single row to insert (default is None).
        rowList : RowList, optional
            A list of rows to insert (default is None).

        Raises
        ------
        KeyError
            If the specified entity is not found in the data dictionary.
        ValueError
            If both row and rowList are provided.
        """
        if row != None and rowList == None:
            entityData = self.dataDict.get(entity)
            if entityData is not None:
                entityData.insertRow(row=row)
            else:
                raise KeyError(
                    f"{entity} not found in data dict, available values {pd.DataFrame.apply(pd.DataFrame(self.dataDict.values()), str)}")
        elif row == None and rowList is not None:
            self.dataDict.get(entity).insertRows(rowList)
        else:
            if row != None and rowList is not None:
                raise ValueError("Received too many inputs, expecting row OR row list")

    @ensure_open
    def getId(self, entity: str, id):
        """
        Retrieves rows from the specified entity's relation where the primary key matches the given id.

        Parameters
        ----------
        entity : str
            The name of the entity (relation) to query.
        id : int
            The primary key value to match.

        Returns
        -------
        RowList
            A list of rows matching the specified primary key.

        Raises
        ------
        KeyError
            If the specified entity is not found in the data dictionary.
        """
        entityData = self.dataDict.get(entity)
        if entityData != None:
            return entityData.getRowsWhereEqual(entityData.primaryKeyName, id)
        else:
            raise KeyError(f"{entity} not found in data dict, available values {self.dataDict.values()}")

    @ensure_open
    def getRelation(self, entity: str) -> Relation:
        """
        Returns the relation object for the specified entity.

        Parameters
        ----------
        entity : str
            The name of the entity (relation) to retrieve.

        Returns
        -------
        Relation
            The relation object corresponding to the specified entity.

        Raises
        ------
        KeyError
            If the specified entity is not found in the data dictionary.
        """
        entityData = self.dataDict.get(entity)
        if entityData != None:
            return entityData
        else:
            raise KeyError(f"{entity} not found in data dict, available values {self.dataDict.values()}")

    @ensure_open
    def insert_admin(self, admin: Admin):
        """
        Inserts an admin user into the User relation.

        Parameters
        ----------
        admin : Admin
            The admin object to insert.
        """
        self.insert("User", Row([admin.username, None, admin.password, None, None, admin.type, None, None, None,
                                 admin.is_disabled]))

    @ensure_open
    def insert_patient(self, patient: Patient):
        """
        Inserts a patient user into the User relation.

        Parameters
        ----------
        patient : Patient
            The patient object to insert.
        """
        self.insert("User",
                    Row([patient.username, patient.email, patient.password, patient.fName, patient.lName, patient.type,
                         patient.emergency_contact_email, patient.emergency_contact_name, None, patient.is_disabled]))

    @ensure_open
    def delete_patient(self, patientId: int):
        """
        Deletes a patient and all associated records from the database.

        Parameters
        ----------
        patientId : int
            The unique identifier of the patient to be deleted.

        Raises
        ------
        TypeError
            If the patientId is not of type int.
        KeyError
            If the patientId does not exist in the User relation or if any of the keys in the deletion process are incorrect.
        """
        if type(patientId) != int:
            raise TypeError("Patient id must be of type int.")

        self.logger.info(f"Deleting patient with id {patientId} and all associated records.")
        
        user_relation = self.getRelation("User")
        if "user_id" not in user_relation.data.columns or patientId not in user_relation.data["user_id"].values:
            raise KeyError(f"Patient id {patientId} does not exist in User relation.")

        if user_relation.getRowsWhereEqual("user_id",patientId)[0][user_relation._typeIndex] != "Patient":
            raise NotImplementedError(f"User with id {patientId} is not a patient, deleting not supported.")

        """
        HERE USED TO BE REFERENCED RELATIONS FOR DELETION PROPAGATION; 
        THESE HAVE MOVED TO RELATION CLASS (getReferencedRelations) FOR EXTENSIBILITY OF DELETIONS AND REDUCED REDUNDANCY.
        """

        referencedRelations = user_relation.getReferencedRelations(type = "Patient")

        for relationName, patientIdColumn in referencedRelations:            
            relation = self.getRelation(relationName)
            if patientIdColumn in relation.data.columns:
                relation.data.drop(relation.data[relation.data[patientIdColumn] == patientId].index, inplace=True)
                relation.data.reset_index(drop=True, inplace=True)
            else:
                raise KeyError(f"One of the keys in delete_patient ({relationName}, key {patientIdColumn}) is wrong, please fix.")
        self.logger.info(f"Success deleting patient with id {patientId}.")
        
    @ensure_open
    def delete_patients(self, patientIds: list):
        """
        Deletes multiple patients and all associated records from the database.

        Parameters
        ----------
        patientIds : list
            A list of unique identifiers of the patients to be deleted.

        Raises
        ------
        TypeError
            If any of the patientIds is not of type int.
        KeyError
            If any patientId does not exist in the User relation or if any of the keys in the deletion process are incorrect.
        """
        for id in patientIds:
            self.delete_patient(id)

    @ensure_open
    def insert_mhwp(self, mhwp: MHWP):
        """
        Inserts an MHWP user into the User relation.

        Parameters
        ----------
        mhwp : MHWP
            The MHWP object to insert.
        """
        self.insert("User",
                    Row([mhwp.username, mhwp.email, mhwp.password, mhwp.fName, mhwp.lName, mhwp.type, None, None,
                         mhwp.specialization, mhwp.is_disabled]))

    @ensure_open
    def insert_allocation(self, allocation: Allocation):
        """
        Inserts an allocation into the Allocation relation.

        Parameters
        ----------
        allocation : Allocation
            The allocation object to insert.
        """
        self.insert("Allocation",
                    Row([allocation.admin_id, allocation.patient_id, allocation.mhwp_id, allocation.start_date,
                         allocation.end_date]))

    @ensure_open
    def insert_journal_entry(self, journal_entry: JournalEntry):
        """
        Inserts a journal entry into the JournalEntry relation.

        Parameters
        ----------
        journal_entry : JournalEntry
            The journal entry object to insert.
        """
        self.insert("JournalEntry", Row([journal_entry.patient_id, journal_entry.text, journal_entry.timestamp]))

    @ensure_open
    def insert_patient_record(self, patient_record: PatientRecord):
        """
        Inserts a patient record into the PatientRecord relation.

        Parameters
        ----------
        patient_record : PatientRecord
            The patient record object to insert.
        """
        self.insert("PatientRecord", Row([patient_record.patient_id, patient_record.mhwp_id, patient_record.notes,
                                          patient_record.conditions]))

    @ensure_open
    def insert_appointment(self, appointment: Appointment):
        """
        Inserts an appointment into the Appointment relation.

        Parameters
        ----------
        appointment : Appointment
            The appointment object to insert.
        """

        self.insert("Appointment",
                    Row([appointment.patient_id, appointment.mhwp_id, appointment.date, appointment.room_name,
                         appointment.status]))

    @ensure_open
    def insert_mood_entry(self, mood_entry: MoodEntry):
        """
        Inserts a journal entry into the JournalEntry relation.

        Parameters
        ----------
        journal_entry : JournalEntry
            The journal entry object to insert.
        """
        self.insert("MoodEntry",
                    Row([mood_entry.patient_id, mood_entry.moodscore, mood_entry.comment, mood_entry.timestamp]))

    @ensure_open
    def insert_review_entry(self, review_entry: MHWPReview):
        self.insert("MHWPReview", Row([review_entry.patient_id, review_entry.mhwp_id, review_entry.reviewscore,
                                       review_entry.reviewcomment, review_entry.timestamp]))

    # def insert_chatroom(self, chatroom : ChatRoom):
    #         self.insert("ChatContent",Row([chatroom.patient_id,chatroom.mhwp_id]))
    @ensure_open
    def insert_chatcontent(self, chatcontent : ChatContent):
            self.insert("ChatContent",Row([chatcontent.allocation_id,chatcontent.user_id,chatcontent.text,chatcontent.timestamp]))

    @ensure_open
    def insert_forum(self, forum : Forum):
            self.insert("Forum",Row([forum.parent_id,forum.topic,forum.content,forum.user_id,forum.timestamp]))

    @ensure_open
    def insert_notification(self, notification : Notification):
            self.insert("Notification",Row([notification.user_id, notification.notifycontent, notification.source_id,notification.new, notification.timestamp]))

    @ensure_open
    def insert_exerrecord(self, exerrecord : ExerRecord):
            self.insert("ExerRecord",Row([exerrecord.user_id, exerrecord.exercise, exerrecord.timestamp]))



class RecordError(Exception):
    def __init__(self, *args, **kwargs):
        warnings.warn("RecordError is deprecated and will be removed soon, please use InvalidDataError instead", DeprecationWarning, stacklevel=2)

class UserError(Exception):
    def __init__(self, *args, **kwargs):
        warnings.warn("UserError is deprecated and will be removed soon, please use InvalidDataError instead", DeprecationWarning, stacklevel=2)

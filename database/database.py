import pandas as pd
import pickle
import os
import logging
import sys
from datetime import datetime as date

# Get the absolute path of the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the project root to sys.path if it's not already there
if project_root not in sys.path:
    sys.path.append(project_root)

from entities import Admin, Patient, MHWP, JournalEntry, Appointment, PatientRecord, Allocation
from dataStructs import Row, Relation, RowList

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
        Inserts an admin user into the Users relation.
    insert_patient(patient):
        Inserts a patient user into the Users relation.
    insert_mhwp(mhwp):
        Inserts an MHWP user into the Users relation.
    insert_allocation(allocation):
        Inserts an allocation into the Allocations relation.
    insert_journal_entry(journal_entry):
        Inserts a journal entry into the JournalEntries relation.
    insert_patient_record(patient_record):
        Inserts a patient record into the PatientRecords relation.
    insert_appointment(appointment):
        Inserts an appointment into the Appointments relation.
    """

    def __init__(self, data_file:str='database.pkl', logger: logging.Logger = None, verbose: bool = False, overwrite : bool = False):
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
        if os.path.exists(self.data_file) and not overwrite:
            self.logger.info(f"Found database file {data_file}, loading from file...")
            self.__load_database()
            self.logger.info("Success loading database")
        elif os.path.exists(self.data_file) and overwrite:
            self.logger.info(f"Overwriting existing database file {data_file}...")
            self.initRelations()
            self.logger.info("Successfully initialized new database with overwriting.")
        else:
            # Initialize tables as DataFrames
            self.logger.info(f"Found no database file {data_file}, initializing new database...")
            self.initRelations()
        self.logger.info("Successfully initialized database.")

    def close(self):
        """
        Saves the current state of the database to a file and deletes the database object.
        """
        self.__save_database()
        self.logger.info("Successfully saved database, exiting")
        del self

    def initRelations(self):
        """
        Initializes the relations (tables) in the database with predefined schemas.
        """
        self.users = Relation('Users',
                                  attributeLabels=['user_id', 'username', 'email', 'password', 'fName', 'lName', 'type','emergency_contact_email', 'mood', 'mood_comment', 'specialization','is_disabled'],
                                  relationAttributeTypes=[int, str, str, str, str, str, str, str, str, str, str, bool])
            
        self.journal_entries = Relation('JournalEntries',
                                        attributeLabels=['entry_id', 'patient_id', 'text', 'score', 'timestamp'],
                                        relationAttributeTypes= [int, int, str, int, date])
        
        self.appointments = Relation('Appointments',
                                        attributeLabels=['appointment_id', 'patient_id', 'mhwp_id', 'date', 'status'],
                                        relationAttributeTypes=[int,int,int,date,str])
        
        self.patient_records = Relation('PatientRecords',
                                        attributeLabels=['record_id', 'patient_id', 'mhwp_id', 'notes', 'conditions'],
                                        relationAttributeTypes=[int,int,int,str,list])
        
        self.allocations = Relation('Allocations',
                                    attributeLabels=['allocation_id', 'admin_id', 'patient_id', 'mhwp_id', 'start_date', 'end_date'],
                                    relationAttributeTypes=[int,int, int, int, date, date])
        self.initDict()

    def initDict(self):
        """
        Initializes the dictionary mapping entity names to their respective relations.
        """
        self.dataDict = {
            'Users':self.users,
            'JournalEntries':self.journal_entries,
            'Appointments':self.appointments,
            'PatientRecords':self.patient_records,
            'Allocations':self.allocations
        } 

    def __load_database(self):
        """
        Loads the database from a file, restoring the state of all relations.
        """
        with open(self.data_file, 'rb') as f:
            data = pickle.load(f)
            self.users = data['users']
            self.journal_entries = data['journal_entries']
            self.appointments = data['appointments']
            self.patient_records = data['patient_records']
            self.allocations = data['allocations']
        self.initDict()

    def __save_database(self):
        """
        Saves the current state of the database to a file.
        """
        with open(self.data_file, 'wb') as f:
            pickle.dump({
                'users': self.users,
                'journal_entries': self.journal_entries,
                'appointments': self.appointments,
                'patient_records': self.patient_records,
                'allocations': self.allocations
            }, f)

    def __str__(self):
        """
        Returns a string representation of the database, showing all relations and their data.
        """
        return "Users:\n"+str(self.users)+"\nJournal Entries:\n"+str(self.journal_entries)+"\nAppointments:\n"+str(self.appointments)+"\nPatient Records:\n"+str(self.patient_records)+"\nAllocations:\n"+str(self.allocations)

    def printAll(self):
        """
        Prints all the data in the database, relation by relation.
        """
        print("Users:")
        print(self.users)
        print("\nJournal Entries:")
        print(self.journal_entries)
        print("\nAppointments:")
        print(self.appointments)
        print("\nPatient Records:")
        print(self.patient_records)
        print("\nAllocations:")
        print(self.allocations)

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
            if entityData != None:
                entityData.insertRow(row=row)
            else:
                raise KeyError(f"{entity} not found in data dict, available values {pd.DataFrame.apply(pd.DataFrame(self.dataDict.values()),str)}")
        elif row == None and rowList != None:
            self.dataDict.get(entity).insertRows(rowList)
        else:
            if row != None and rowList != None:
                raise ValueError("Received too many inputs, expecting row OR row list")

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
            return entityData.getRowsWhereEqual(entityData.primaryKeyName,id)
        else:
            raise KeyError(f"{entity} not found in data dict, available values {self.dataDict.values()}")
    
    def getRelation(self, entity : str) -> Relation:
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

    
    def insert_admin(self, admin:Admin):
        """
        Inserts an admin user into the Users relation.

        Parameters
        ----------
        admin : Admin
            The admin object to insert.
        """
        self.insert("Users",Row([admin.username,None,admin.password,None,None,admin.type,None,None,None,None,admin.is_disabled]))
    
    def insert_patient(self,patient : Patient):
        """
        Inserts a patient user into the Users relation.

        Parameters
        ----------
        patient : Patient
            The patient object to insert.
        """
        self.insert("Users",Row([patient.username,patient.email,patient.password,patient.fName,patient.lName,patient.type,patient.emergency_contact_email,patient.moods,patient.mood_comments,None,patient.is_disabled]))
    
    def insert_mhwp(self, mhwp : MHWP):
        """
        Inserts an MHWP user into the Users relation.

        Parameters
        ----------
        mhwp : MHWP
            The MHWP object to insert.
        """
        self.insert("Users",Row([mhwp.username,mhwp.email,mhwp.password,mhwp.fName,mhwp.lName,mhwp.type,None,None,None,mhwp.specialization,mhwp.is_disabled]))
    
    def insert_allocation(self, allocation : Allocation):
        """
        Inserts an allocation into the Allocations relation.

        Parameters
        ----------
        allocation : Allocation
            The allocation object to insert.
        """
        self.insert("Allocations",Row([allocation.admin_id,allocation.patient_id,allocation.mhwp_id,allocation.start_date,allocation.end_date]))
    
    def insert_journal_entry(self, journal_entry : JournalEntry):
        """
        Inserts a journal entry into the JournalEntries relation.

        Parameters
        ----------
        journal_entry : JournalEntry
            The journal entry object to insert.
        """
        self.insert("JournalEntries",Row([journal_entry.patient_id,journal_entry.text,journal_entry.score,journal_entry.timestamp]))

    def insert_patient_record(self, patient_record : PatientRecord):
        """
        Inserts a patient record into the PatientRecords relation.

        Parameters
        ----------
        patient_record : PatientRecord
            The patient record object to insert.
        """
        self.insert("PatientRecords", Row([patient_record.patient_id, patient_record.mhwp_id, patient_record.notes, patient_record.conditions]))

    def insert_appointment(self, appointment: Appointment):
        """
        Inserts an appointment into the Appointments relation.

        Parameters
        ----------
        appointment : Appointment
            The appointment object to insert.
        """
        self.insert("Appointments", Row([appointment.patient_id, appointment.mhwp_id, appointment.date, appointment.status]))

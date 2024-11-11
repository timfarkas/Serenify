import pandas as pd
import pickle
import os
import logging
from datetime import date
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
            self.users = Relation('Users',
                                  attributeLabels=['user_id', 'username', 'email', 'password', 'fName', 'lName', 'type','emergency_contact_email', 'mood', 'mood_comment', 'specialization','is_disabled'],
                                  relationAttributeTypes=[int, str, str, str, str, str, str, str, str, str, str, bool])
            
            self.journal_entries = Relation('JournalEntries',
                                            attributeLabels=['entry_id', 'patient_id', 'text', 'timestamp'],
                                            relationAttributeTypes= [int, int, str, date])
            
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
        self.logger.info("Successfully initialized database.")

    def close(self):
        self.__save_database()
        self.logger.info("Successfully saved database, exiting")
        del self

    def initDict(self):
        self.dataDict = {
            'Users':self.users,
            'JournalEntries':self.journal_entries,
            'Appointments':self.appointments,
            'PatientRecords':self.patient_records,
            'Allocations':self.allocations
        } 

    def __load_database(self):
        with open(self.data_file, 'rb') as f:
            data = pickle.load(f)
            self.users = data['users']
            self.journal_entries = data['journal_entries']
            self.appointments = data['appointments']
            self.patient_records = data['patient_records']
            self.allocations = data['allocations']
        self.initDict()

    def __save_database(self):
        with open(self.data_file, 'wb') as f:
            pickle.dump({
                'users': self.users,
                'journal_entries': self.journal_entries,
                'appointments': self.appointments,
                'patient_records': self.patient_records,
                'allocations': self.allocations
            }, f)

    def __str__(self):
        return "Users:\n"+str(self.users)+"\nJournal Entries:\n"+str(self.journal_entries)+"\nAppointments:\n"+str(self.appointments)+"\nPatient Records:\n"+str(self.patient_records)+"\nAllocations:\n"+str(self.allocations)

    def printAll(self):
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

    def insert(self, entity: str, row: Row = None,rowList: RowList = None):
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
        entityData = self.dataDict.get(entity)
        if entityData != None:
            return entityData.getRowsWhereEqual(entityData.primaryKeyName,id)
        else:
            raise KeyError(f"{entity} not found in data dict, available values {self.dataDict.values()}")
    
    def getEntity(self, entity : str) -> Relation:
        entityData = self.dataDict.get(entity)
        if entityData != None:
            return entityData
        else:
            raise KeyError(f"{entity} not found in data dict, available values {self.dataDict.values()}")

    
    def insert_admin(self, admin:Admin):
        self.insert("Users",Row([admin.username,None,admin.password,None,None,admin.type,None,None,None,None,admin.is_disabled]))
    
    def insert_patient(self,patient : Patient):
        self.insert("Users",Row([patient.username,patient.email,patient.password,patient.fName,patient.lName,patient.type,patient.emergency_contact_email,patient.moods,patient.mood_comments,None,patient.is_disabled]))
    
    def insert_mhwp(self, mhwp : MHWP):
        self.insert("Users",Row([mhwp.username,mhwp.email,mhwp.password,mhwp.fName,mhwp.lName,mhwp.type,None,None,None,mhwp.specialization,mhwp.is_disabled]))
    
    def insert_allocation(self, allocation : Allocation):
        self.insert("Allocations",Row([allocation.admin_id,allocation.patient_id,allocation.mhwp_id,allocation.start_date,allocation.end_date]))
    
    def insert_journal_entry(self, journal_entry : JournalEntry):
        self.insert("JournalEntries",Row([journal_entry.patient_id,journal_entry.text,journal_entry.timestamp]))
    
    def insert_patient_record(self, patient_record : PatientRecord):
        self.insert("PatientRecords",Row([patient_record.patient_id,patient_record.mhwp_id,patient_record.notes,patient_record.conditions]))



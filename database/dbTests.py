import unittest
import logging
import os
import shutil
from datetime import datetime
from .dataStructs import Row, RowList, Relation 
from .entities import Admin, Patient, MHWP, JournalEntry, PatientRecord, Appointment, Allocation
from .database import Database  

'''
Disclaimer:
    This script was written almost entirely by ChatGPT (GPT-o1-Preview).
    The database, entities, and dataStructs code is almost entirely home-made (with LLM-generated docstrings and boiler plate code snippets in between).
    Contact Tim Farkas for questions.
'''

class TestRow(unittest.TestCase):
    def test_row_initialization(self):
        # Test initialization without labels
        values = [1, 2, 3]
        row = Row(values)
        self.assertEqual(row.values, values)
        self.assertEqual(row.labels, None)
        self.assertFalse(row.labelled)
        
        # Test initialization with labels
        labels = ['a', 'b', 'c']
        row = Row(values, labels)
        self.assertEqual(row.values, values)
        self.assertEqual(row.labels, labels)
        self.assertTrue(row.labelled)
        
        # Test mismatched lengths
        with self.assertRaises(IndexError):
            row = Row([1,2], ['a','b','c'])
            
    def test_row_str(self):
        values = [1, 2, 3]
        labels = ['a', 'b', 'c']
        row = Row(values, labels)
        expected_str = "Row:\n Labels: ['a', 'b', 'c']\n Values:[1, 2, 3]"
        self.assertEqual(row.__str__(), expected_str)
        
        # Test without labels
        row = Row(values)
        expected_str = "Row:\n Labels: None\n Values:[1, 2, 3]"
        self.assertEqual(row.__str__(), expected_str)

class TestRowList(unittest.TestCase):
    def test_rowlist_initialization(self):
        # Test initialization with labels
        labels = ['a', 'b', 'c']
        row1 = Row([1, 2, 3], labels)
        row2 = Row([4, 5, 6], labels)
        rowlist = RowList([row1, row2], labels)
        self.assertEqual(rowlist.labels, labels)
        self.assertEqual(len(rowlist), 2)
        self.assertEqual(rowlist[0], row1)
        self.assertEqual(rowlist[1], row2)
        
        # Test initialization without labels
        row1 = Row([1, 2, 3])
        row2 = Row([4, 5, 6])
        rowlist = RowList([row1, row2])
        self.assertEqual(rowlist.labels, None)
        self.assertEqual(len(rowlist), 2)
        
        # Test initialization with non-Row object
        with self.assertRaises(TypeError):
            rowlist = RowList([row1, [7,8,9]])
        
class TestRelation(unittest.TestCase):
    def test_relation_initialization(self):
        # Initialize relation with attribute labels and types
        relationName = "TestRelation"
        attributeLabels = ['id', 'name', 'age']
        attributeTypes = [int, str, int]
        relation = Relation(relationName, attributeLabels, attributeTypes)
        self.assertEqual(relation.name, relationName)
        self.assertEqual(relation.attributeLabels, attributeLabels)
        self.assertEqual(relation.types, attributeTypes)
        self.assertEqual(relation.primaryKeyName, 'id')
        self.assertEqual(relation.primaryKeyType, int)
        self.assertTrue(relation.autoIncrementPrimaryKey)
        self.assertEqual(len(relation.data), 0)
        
        # Test type checking when attributeTypes is None
        relation = Relation(relationName, attributeLabels)
        self.assertFalse(relation.typeChecking)
        
        # Test error when lengths of labels and types do not match
        with self.assertRaises(ValueError):
            relation = Relation(relationName, attributeLabels, [int, str])
        
        # Test error when autoIncrementPrimaryKey is True but primaryKeyType is not int
        with self.assertRaises(ValueError):
            relation = Relation(relationName, attributeLabels, [str, str, int])
    
    def test_insert_row(self):
        relationName = "TestRelation"
        attributeLabels = ['id', 'name', 'age']
        attributeTypes = [int, str, int]
        relation = Relation(relationName, attributeLabels, attributeTypes)
        
        # Insert a row without specifying id (autoIncrementPrimaryKey=True)
        relation.insertRow(attributeList=['Alice', 30])
        self.assertEqual(len(relation.data), 1)
        self.assertEqual(relation.data.iloc[0]['id'], 1)
        self.assertEqual(relation.data.iloc[0]['name'], 'Alice')
        self.assertEqual(relation.data.iloc[0]['age'], 30)
        
        # Insert another row
        relation.insertRow(attributeList=['Bob', 25])
        self.assertEqual(len(relation.data), 2)
        self.assertEqual(relation.data.iloc[1]['id'], 2)
        self.assertEqual(relation.data.iloc[1]['name'], 'Bob')
        self.assertEqual(relation.data.iloc[1]['age'], 25)
        
        # Insert row with mismatched attribute list length
        with self.assertRaises(ValueError):
            relation.insertRow(attributeList=['Charlie'])
        
        # Insert row with incorrect type
        with self.assertRaises(TypeError):
            relation.insertRow(attributeList=['Charlie', 'Thirty'])
        
        # Insert row with duplicate primary key when autoIncrementPrimaryKey=False
        relation_no_auto = Relation(relationName, attributeLabels, attributeTypes, autoIncrementPrimaryKey=False)
        relation_no_auto.insertRow(attributeList=[1, 'Alice', 30])
        with self.assertRaises(KeyError):
            relation_no_auto.insertRow(attributeList=[1, 'Bob', 25])
    
    def test_get_attribute_max_row(self):
        relationName = "TestRelation"
        attributeLabels = ['id', 'name', 'age']
        attributeTypes = [int, str, int]
        relation = Relation(relationName, attributeLabels, attributeTypes)
        relation.insertRow(attributeList=['Alice', 30])
        relation.insertRow(attributeList=['Bob', 25])
        relation.insertRow(attributeList=['Charlie', 35])
        
        max_row = relation.getAttributeMaxRow('age')
        self.assertEqual(max_row.values, [3, 'Charlie', 35])
        
        # Test with empty data
        empty_relation = Relation(relationName, attributeLabels, attributeTypes)
        self.assertIsNone(empty_relation.getAttributeMaxRow('age'))
        
        # Test with non-existing attribute
        with self.assertRaises(KeyError):
            relation.getAttributeMaxRow('salary')
    
    def test_get_attribute_min_row(self):
        # Similar to test_get_attribute_max_row
        relationName = "TestRelation"
        attributeLabels = ['id', 'name', 'age']
        attributeTypes = [int, str, int]
        relation = Relation(relationName, attributeLabels, attributeTypes)
        relation.insertRow(attributeList=['Alice', 30])
        relation.insertRow(attributeList=['Bob', 25])
        relation.insertRow(attributeList=['Charlie', 35])
        
        min_row = relation.getAttributeMinRow('age')
        self.assertEqual(min_row.values, [2, 'Bob', 25])
        
        # Test with empty data
        empty_relation = Relation(relationName, attributeLabels, attributeTypes)
        self.assertIsNone(empty_relation.getAttributeMinRow('age'))
        
        # Test with non-existing attribute
        with self.assertRaises(KeyError):
            relation.getAttributeMinRow('salary')
    
    def test_get_all_rows(self):
        relationName = "TestRelation"
        attributeLabels = ['id', 'name', 'age']
        attributeTypes = [int, str, int]
        relation = Relation(relationName, attributeLabels, attributeTypes)
        relation.insertRow(attributeList=['Alice', 30])
        relation.insertRow(attributeList=['Bob', 25])
        
        all_rows = relation.getAllRows()
        self.assertEqual(len(all_rows), 2)
        self.assertEqual(all_rows[0].values, [1, 'Alice', 30])
        self.assertEqual(all_rows[1].values, [2, 'Bob', 25])
    
    def test_get_all_row_ids(self):
        relationName = "TestRelation"
        attributeLabels = ['id', 'name', 'age']
        attributeTypes = [int, str, int]
        relation = Relation(relationName, attributeLabels, attributeTypes)
        relation.insertRow(attributeList=['Alice', 30])
        relation.insertRow(attributeList=['Bob', 25])
        
        ids = relation.getAllRowIDs()
        self.assertEqual(ids, [1, 2])
    
    def test_get_rows_where_equal(self):
        relationName = "TestRelation"
        attributeLabels = ['id', 'name', 'age']
        attributeTypes = [int, str, int]
        relation = Relation(relationName, attributeLabels, attributeTypes)
        relation.insertRow(attributeList=['Alice', 30])
        relation.insertRow(attributeList=['Bob', 25])
        relation.insertRow(attributeList=['Alice', 35])
        
        rows = relation.getRowsWhereEqual('name', 'Alice')
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0].values, [1, 'Alice', 30])
        self.assertEqual(rows[1].values, [3, 'Alice', 35])
        
        # Test with non-existing attribute
        with self.assertRaises(KeyError):
            relation.getRowsWhereEqual('salary', 1000)
        
        # Test with empty result
        rows = relation.getRowsWhereEqual('name', 'Eve')
        self.assertEqual(len(rows), 0)
    
    def test_get_ids_where_equal(self):
        # Similar to test_get_rows_where_equal
        relationName = "TestRelation"
        attributeLabels = ['id', 'name', 'age']
        attributeTypes = [int, str, int]
        relation = Relation(relationName, attributeLabels, attributeTypes)
        relation.insertRow(attributeList=['Alice', 30])
        relation.insertRow(attributeList=['Bob', 25])
        relation.insertRow(attributeList=['Alice', 35])
        
        ids = relation.getIDsWhereEqual('name', 'Alice')
        self.assertEqual(ids, [1, 3])
        
        # Test with non-existing attribute
        with self.assertRaises(KeyError):
            relation.getIDsWhereEqual('salary', 1000)
        
        # Test with empty result
        ids = relation.getIDsWhereEqual('name', 'Eve')
        self.assertEqual(ids, [])
    
    def test_get_where_equal(self):
        # Similar to test_get_rows_where_equal, but returns a Relation
        relationName = "TestRelation"
        attributeLabels = ['id', 'name', 'age']
        attributeTypes = [int, str, int]
        relation = Relation(relationName, attributeLabels, attributeTypes)
        relation.insertRow(attributeList=['Alice', 30])
        relation.insertRow(attributeList=['Bob', 25])
        relation.insertRow(attributeList=['Alice', 35])
        
        new_relation = relation.getWhereEqual('name', 'Alice')
        self.assertEqual(len(new_relation), 2)
        self.assertEqual(new_relation.data.iloc[0]['name'], 'Alice')
        self.assertEqual(new_relation.data.iloc[1]['name'], 'Alice')
        
        # Test with empty result
        new_relation = relation.getWhereEqual('name', 'Eve')
        self.assertEqual(len(new_relation), 0)
        
    def test_get_rows_where_larger(self):
        # Test rows where age > 30
        relationName = "TestRelation"
        attributeLabels = ['id', 'name', 'age']
        attributeTypes = [int, str, int]
        relation = Relation(relationName, attributeLabels, attributeTypes)
        relation.insertRow(attributeList=['Alice', 30])
        relation.insertRow(attributeList=['Bob', 25])
        relation.insertRow(attributeList=['Charlie', 35])
        
        rows = relation.getRowsWhereLarger('age', 30)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].values, [3, 'Charlie', 35])
        
        # Test with empty result
        rows = relation.getRowsWhereLarger('age', 40)
        self.assertEqual(len(rows), 0)
    
    def test_get_ids_where_larger(self):
        # Similar to test_get_rows_where_larger
        relationName = "TestRelation"
        attributeLabels = ['id', 'name', 'age']
        attributeTypes = [int, str, int]
        relation = Relation(relationName, attributeLabels, attributeTypes)
        relation.insertRow(attributeList=['Alice', 30])
        relation.insertRow(attributeList=['Bob', 25])
        relation.insertRow(attributeList=['Charlie', 35])
        
        ids = relation.getIDsWhereLarger('age', 30)
        self.assertEqual(ids, [3])
        
        # Test with empty result
        ids = relation.getIDsWhereLarger('age', 40)
        self.assertEqual(ids, [])
    
    def test_get_where_larger(self):
        # Similar to above, but returns a Relation
        relationName = "TestRelation"
        attributeLabels = ['id', 'name', 'age']
        attributeTypes = [int, str, int]
        relation = Relation(relationName, attributeLabels, attributeTypes)
        relation.insertRow(attributeList=['Alice', 30])
        relation.insertRow(attributeList=['Bob', 25])
        relation.insertRow(attributeList=['Charlie', 35])
        
        new_relation = relation.getWhereLarger('age', 30)
        self.assertEqual(len(new_relation), 1)
        self.assertEqual(new_relation.data.iloc[0]['name'], 'Charlie')
        
        # Test with empty result
        new_relation = relation.getWhereLarger('age', 40)
        self.assertEqual(len(new_relation), 0)
    
    def test_get_rows_where_smaller(self):
        # Test rows where age < 30
        relationName = "TestRelation"
        attributeLabels = ['id', 'name', 'age']
        attributeTypes = [int, str, int]
        relation = Relation(relationName, attributeLabels, attributeTypes)
        relation.insertRow(attributeList=['Alice', 30])
        relation.insertRow(attributeList=['Bob', 25])
        relation.insertRow(attributeList=['Charlie', 35])
        
        rows = relation.getRowsWhereSmaller('age', 30)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].values, [2, 'Bob', 25])
        
        # Test with empty result
        rows = relation.getRowsWhereSmaller('age', 20)
        self.assertEqual(len(rows), 0)
    
    def test_get_ids_where_smaller(self):
        # Similar to test_get_rows_where_smaller
        relationName = "TestRelation"
        attributeLabels = ['id', 'name', 'age']
        attributeTypes = [int, str, int]
        relation = Relation(relationName, attributeLabels, attributeTypes)
        relation.insertRow(attributeList=['Alice', 30])
        relation.insertRow(attributeList=['Bob', 25])
        relation.insertRow(attributeList=['Charlie', 35])
        
        ids = relation.getIDsWhereSmaller('age', 30)
        self.assertEqual(ids, [2])
        
        # Test with empty result
        ids = relation.getIDsWhereSmaller('age', 20)
        self.assertEqual(ids, [])
    def test_edit_row(self):
        relationName = "TestRelation"
        attributeLabels = ['id', 'name', 'age']
        attributeTypes = [int, str, int]
        relation = Relation(relationName, attributeLabels, attributeTypes)
        relation.insertRow(attributeList=['Alice', 30])
        
        # Edit row with new values using primary key index
        relation.editRow(1, newValues=['Alice', 31])
        self.assertEqual(relation.data.iloc[0]['age'], 31)
        
        # Edit row with Row object using primary key index
        new_row = Row(['Alice', 32])
        relation.editRow(1, row=new_row)
        self.assertEqual(relation.data.iloc[0]['age'], 32)
        
        # Test IndexError for out of bounds primary key index
        with self.assertRaises(IndexError):
            relation.editRow(2, newValues=[2, 'Bob', 25])
        
        # Test ValueError for both newValues and row provided
        with self.assertRaises(ValueError):
            relation.editRow(1, newValues=['Alice', 33], row=new_row)
        
        # Test ValueError for neither newValues nor row provided
        with self.assertRaises(ValueError):
            relation.editRow(1)
        
        # Test ValueError for mismatched lengths
        with self.assertRaises(ValueError):
            relation.editRow(1, newValues=['Alice'])
        
        # Test TypeError for incorrect type
        with self.assertRaises(TypeError):
            relation.editRow(1, newValues=['Alice', 'thirty'])

    def test_edit_field_in_row(self):
        relationName = "TestRelation"
        attributeLabels = ['id', 'name', 'age']
        attributeTypes = [int, str, int]
        relation = Relation(relationName, attributeLabels, attributeTypes)
        relation.insertRow(attributeList=['Alice', 30])
        
        # Edit field in row using primary key index
        relation.editFieldInRow(1, 'age', 31)
        self.assertEqual(relation.data.iloc[0]['age'], 31)
        
        # Test IndexError for out of bounds primary key index
        with self.assertRaises(IndexError):
            relation.editFieldInRow(2, 'age', 25)
        
        # Test ValueError for invalid attribute
        with self.assertRaises(ValueError):
            relation.editFieldInRow(1, 'height', 170)
        
        # Test TypeError for incorrect type
        with self.assertRaises(TypeError):
            relation.editFieldInRow(1, 'age', 'thirty')
        
    def test_get_where_smaller(self):
        # Similar to above, but returns a Relation
        relationName = "TestRelation"
        attributeLabels = ['id', 'name', 'age']
        attributeTypes = [int, str, int]
        relation = Relation(relationName, attributeLabels, attributeTypes)
        relation.insertRow(attributeList=['Alice', 30])
        relation.insertRow(attributeList=['Bob', 25])
        relation.insertRow(attributeList=['Charlie', 35])
        
        new_relation = relation.getWhereSmaller('age', 30)
        self.assertEqual(len(new_relation), 1)
        self.assertEqual(new_relation.data.iloc[0]['name'], 'Bob')
        
        # Test with empty result
        new_relation = relation.getWhereSmaller('age', 20)
        self.assertEqual(len(new_relation), 0)
    
    def test_drop_rows(self):
        relationName = "TestRelation"
        attributeLabels = ['id', 'name', 'age']
        attributeTypes = [int, str, int]
        relation = Relation(relationName, attributeLabels, attributeTypes)
        relation.insertRow(attributeList=['Alice', 30]) # id=1
        relation.insertRow(attributeList=['Bob', 25])   # id=2
        relation.insertRow(attributeList=['Charlie', 35]) # id=3
        
        # Drop by id
        relation.dropRows(id=2)
        self.assertEqual(len(relation), 2)
        ids = relation.getAllRowIDs()
        self.assertEqual(ids, [1,3])
        
        # Drop by ids
        relation.dropRows(ids=[1,3])
        self.assertEqual(len(relation), 0)
        
        # Test error when both id and ids are specified
        with self.assertRaises(ValueError):
            relation.dropRows(id=1, ids=[2,3])
        
        # Test error when id is not integer
        with self.assertRaises(TypeError):
            relation.dropRows(id='1')
        
        # Test error when ids is not a list
        with self.assertRaises(TypeError):
            relation.dropRows(ids='1')
    
    def test_length(self):
        relationName = "TestRelation"
        attributeLabels = ['id', 'name', 'age']
        relation = Relation(relationName, attributeLabels)
        self.assertEqual(len(relation), 0)
        relation.insertRow(attributeList=['Alice', 30])
        self.assertEqual(len(relation), 1)

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Set up a temporary database file for testing
        self.test_db_file = 'test_database.pkl'
        # Ensure the test database is clean before each test
        if os.path.exists(self.test_db_file):
            os.remove(self.test_db_file)
        self.logger = logging.getLogger('TestDatabase')
        self.logger.setLevel(logging.CRITICAL)  # Suppress logging output during tests
        self.db = Database(data_file=self.test_db_file, logger=self.logger, verbose=False, overwrite=True)

    def tearDown(self):
        # Clean up the database file after each test
        if os.path.exists(self.test_db_file):
            os.remove(self.test_db_file)
        del self.db

    def test_insert_admin(self):
        admin = Admin(username='admin1', password='password123')
        self.db.insert_admin(admin)
        user = self.db.getRelation('User').data
        self.assertEqual(len(user), 1)
        self.assertEqual(user.iloc[0]['username'], 'admin1')
        self.assertEqual(user.iloc[0]['type'], 'Admin')

    def test_insert_patient(self):
        patient = Patient(
            username='patient1',
            email='patient1@example.com',
            password='password123',
            fName='John',
            lName='Doe',
            emergency_contact_email='contact@example.com',
            is_disabled=False
        )
        self.db.insert_patient(patient)
        user = self.db.getRelation('User').data
        self.assertEqual(len(user), 1)
        self.assertEqual(user.iloc[0]['username'], 'patient1')
        self.assertEqual(user.iloc[0]['type'], 'Patient')
        self.assertEqual(user.iloc[0]['email'], 'patient1@example.com')

    def test_insert_mhwp(self):
        mhwp = MHWP(
            username='mhwp1',
            email='mhwp1@example.com',
            password='password123',
            fName='Jane',
            lName='Smith',
            specialization='Counseling',
            is_disabled=False
        )
        self.db.insert_mhwp(mhwp)
        user = self.db.getRelation('User').data
        self.assertEqual(len(user), 1)
        self.assertEqual(user.iloc[0]['username'], 'mhwp1')
        self.assertEqual(user.iloc[0]['type'], 'MHWP')
        self.assertEqual(user.iloc[0]['specialization'], 'Counseling')

    def test_insert_journal_entry(self):
        journal_entry = JournalEntry(patient_id=1, text='Today was a good day.')
        self.db.insert_journal_entry(journal_entry)
        entry = self.db.getRelation('JournalEntry').data
        self.assertEqual(len(entry), 1)
        self.assertEqual(entry.iloc[0]['patient_id'], 1)
        self.assertEqual(entry.iloc[0]['text'], 'Today was a good day.')

    def test_insert_appointment(self):
        appointment = Appointment(
            patient_id=1,
            mhwp_id=2,
            date=datetime(2023, 1, 1, 10, 0),
            status='Scheduled',
            room_name='Room 101'
        )
        self.db.insert_appointment(appointment)
        appointment_data = self.db.getRelation('Appointment').data
        self.assertEqual(len(appointment_data), 1)
        self.assertEqual(appointment_data.iloc[0]['patient_id'], 1)
        self.assertEqual(appointment_data.iloc[0]['mhwp_id'], 2)
        self.assertEqual(appointment_data.iloc[0]['status'], 'Scheduled')
        self.assertEqual(appointment_data.iloc[0]['room_name'], 'Room 101')

    def test_insert_patient_record(self):
        patient_record = PatientRecord(
            patient_id=1,
            mhwp_id=2,
            notes='Patient is recovering well.',
            conditions=['Anxiety', 'Depression']
        )
        self.db.insert_patient_record(patient_record)
        record = self.db.getRelation('PatientRecord').data
        self.assertEqual(len(record), 1)
        self.assertEqual(record.iloc[0]['patient_id'], 1)
        self.assertEqual(record.iloc[0]['notes'], 'Patient is recovering well.')
        self.assertEqual(record.iloc[0]['conditions'], ['Anxiety', 'Depression'])

    def test_insert_allocation(self):
        allocation = Allocation(
            admin_id=1,
            patient_id=2,
            mhwp_id=3,
            start_date=datetime(2023, 1, 1),
            end_date=datetime(2023, 12, 31)
        )
        self.db.insert_allocation(allocation)
        allocation_data = self.db.getRelation('Allocation').data
        self.assertEqual(len(allocation_data), 1)
        self.assertEqual(allocation_data.iloc[0]['admin_id'], 1)
        self.assertEqual(allocation_data.iloc[0]['patient_id'], 2)
        self.assertEqual(allocation_data.iloc[0]['mhwp_id'], 3)

    def test_close_and_load_database(self):
        # Insert some data
        admin = Admin(username='admin1', password='password123')
        self.db.insert_admin(admin)
        # Close the database
        self.db.close()
        # Reopen the database
        self.db = Database(data_file=self.test_db_file, logger=self.logger, verbose=False)
        user = self.db.getRelation('User').data
        self.assertEqual(len(user), 1)
        self.assertEqual(user.iloc[0]['username'], 'admin1')

    def test_print_all(self):
        # Insert some data
        admin = Admin(username='admin1', password='password123')
        self.db.insert_admin(admin)
        # Capture the print output
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.db.printAll()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn('User:', output)
        self.assertIn('admin1', output)

    def test_get_id(self):
        admin = Admin(username='admin1', password='password123')
        self.db.insert_admin(admin)
        result = self.db.getId('User', 1)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].values[1], 'admin1')  # username is at index 1

    def test_get_relation(self):
        user_relation = self.db.getRelation('User')
        self.assertIsInstance(user_relation, Relation)
        self.assertEqual(user_relation.name, 'User')

    def test_insert_with_invalid_entity(self):
        with self.assertRaises(KeyError):
            self.db.insert('InvalidEntity', Row([1, 2, 3]))

    def test_get_id_with_invalid_entity(self):
        with self.assertRaises(KeyError):
            self.db.getId('InvalidEntity', 1)

    def test_get_relation_with_invalid_entity(self):
        with self.assertRaises(KeyError):
            self.db.getRelation('InvalidEntity')

    def test_insert_row_and_rowlist(self):
        row = Row([1, 'testuser', 'test@example.com', 'password', 'Test', 'User', 'patient', None, None, None, None, False])
        rowList = RowList([row])
        with self.assertRaises(ValueError):
            self.db.insert('User', row=row, rowList=rowList)

    def test_overwrite_database(self):
        # Insert some data
        admin = Admin(username='admin1', password='password123')
        self.db.insert_admin(admin)
        self.db.close()
        # Reopen the database with overwrite=True
        self.db = Database(data_file=self.test_db_file, logger=self.logger, verbose=False, overwrite=True)
        user = self.db.getRelation('User').data
        self.assertEqual(len(user), 0)

    def test_auto_increment_primary_key(self):
        # Insert multiple admins
        admin1 = Admin(username='admin1', password='password123')
        admin2 = Admin(username='admin2', password='password123')
        self.db.insert_admin(admin1)
        self.db.insert_admin(admin2)
        user = self.db.getRelation('User').data
        self.assertEqual(len(user), 2)
        self.assertEqual(user.iloc[0]['user_id'], 1)
        self.assertEqual(user.iloc[1]['user_id'], 2)

    def test_insert_row_list(self):
        # Insert a list of rows without the primary key
        row1 = Row(['user1', 'user1@example.com', 'password', 'First1', 'Last1', 'patient', None, None, False])
        row2 = Row(['user2', 'user2@example.com', 'password', 'First2', 'Last2', 'patient', None, None, False])
        rowList = RowList([row1, row2])
        self.db.insert('User', rowList=rowList)
        user = self.db.getRelation('User').data
        self.assertEqual(len(user), 2)
        self.assertEqual(user.iloc[0]['username'], 'user1')
        self.assertEqual(user.iloc[1]['username'], 'user2')

    def test_insert_invalid_row(self):
        # Insert a row with missing fields
        row = Row([1, 'user1'])  # Missing required fields
        with self.assertRaises(ValueError):
            self.db.insert('User', row=row)

    def test_insert_invalid_row_type(self):
        # Insert an invalid row type
        with self.assertRaises(TypeError):
            self.db.insert('User', row=[1, 'user1'])  # Should be a Row object

    def test_data_persistence(self):
        # Insert data and close the database
        patient = Patient(
            username='patient1',
            email='patient1@example.com',
            password='password123',
            fName='John',
            lName='Doe',
            emergency_contact_email='contact@example.com',
            is_disabled=False
        )
        self.db.insert_patient(patient)
        self.db.close()
        # Reopen the database
        self.db = Database(data_file=self.test_db_file, logger=self.logger, verbose=False)
        user = self.db.getRelation('User').data
        self.assertEqual(len(user), 1)
        self.assertEqual(user.iloc[0]['username'], 'patient1')

if __name__ == '__main__':
    unittest.main()
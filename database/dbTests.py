import unittest
import logging
import os
import shutil
from datetime import datetime
from .dataStructs import Row, RowList, Relation
from .entities import InvalidDataError, User, Admin, Patient, MHWP, JournalEntry, PatientRecord, Appointment, Allocation, MoodEntry
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
    
    def test_slicing_and_index_assignment(self):
        # Test slicing with labels
        values = [1, 2, 3, 4, 5]
        labels = ['a', 'b', 'c', 'd', 'e']
        row = Row(values, labels)
        
        # Slice the first three elements
        sliced_row = row[:3]
        self.assertEqual(sliced_row, [1, 2, 3])
        
        # Slice with negative index
        sliced_row = row[-2:]
        self.assertEqual(sliced_row, [4, 5])
        
        # Slice with step
        sliced_row = row[::2]
        self.assertEqual(sliced_row, [1, 3, 5])
        
        # Test slicing without labels
        row_no_labels = Row(values)
        
        # Slice the first three elements
        sliced_row = row_no_labels[:3]
        self.assertEqual(sliced_row, [1, 2, 3])
        
        # Slice with negative index
        sliced_row = row_no_labels[-2:]
        self.assertEqual(sliced_row, [4, 5])
        
        # Slice with step
        sliced_row = row_no_labels[::2]
        self.assertEqual(sliced_row, [1, 3, 5])
        
        # Test index assignment
        row[3] = 6
        self.assertEqual(row[3], 6)
        
        # Test index assignment without labels
        row_no_labels[3] = 7
        self.assertEqual(row_no_labels[3], 7)
    
    def test_get_field(self):
        # Test label-based field lookup
        values = [10, 20, 30]
        labels = ['x', 'y', 'z']
        row = Row(values, labels)
        
        self.assertEqual(row.getField('x'), 10)
        self.assertEqual(row.getField('y'), 20)
        self.assertEqual(row.getField('z'), 30)
        
        # Test field lookup with non-existent label
        with self.assertRaises(ValueError):
            row.getField('a')
        
        # Test field lookup when labels are None
        row_no_labels = Row(values)
        with self.assertRaises(ValueError):
            row_no_labels.getField('x')

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
        
        # Test if single rows also have labels
        self.assertEqual(row1.labels, labels)
        self.assertEqual(row2.labels, labels)
        
        # Test initialization without labels
        row1 = Row([1, 2, 3])
        row2 = Row([4, 5, 6])
        rowlist = RowList([row1, row2])
        self.assertEqual(rowlist.labels, None)
        self.assertEqual(len(rowlist), 2)
        
        # Test initialization with non-Row object
        with self.assertRaises(TypeError):
            rowlist = RowList([row1, [7,8,9]])
        
        # Test initialization with mismatched row labels
        with self.assertRaises(ValueError):
            row1 = Row([1, 2, 3], ['a', 'b', 'c'])
            row2 = Row([4, 5, 6], ['x', 'y', 'z'])
            rowlist = RowList([row1, row2], labels)
        
class TestRelation(unittest.TestCase):
    def test_relation_initialization(self):
        # Initialize relation with attribute labels and types
        relationName = "TestRelation"
        attributeLabels = ['id', 'name', 'age']
        attributeTypes = [int, str, int]
        relation = Relation(relationName, attributeLabels, attributeTypes,validityChecking=False)
        self.assertEqual(relation.name, relationName)
        self.assertEqual(relation.attributeLabels, attributeLabels)
        self.assertEqual(relation.types, attributeTypes)
        self.assertEqual(relation.primaryKeyName, 'id')
        self.assertEqual(relation.primaryKeyType, int)
        self.assertTrue(relation.autoIncrementPrimaryKey)
        self.assertEqual(len(relation.data), 0)
        
        # Test type checking when attributeTypes is None
        relation = Relation(relationName, attributeLabels,validityChecking=False)
        self.assertFalse(relation.typeChecking)
        
        # Test error when lengths of labels and types do not match
        with self.assertRaises(ValueError):
            relation = Relation(relationName, attributeLabels, [int, str],validityChecking=False)
        
        # Test error when autoIncrementPrimaryKey is True but primaryKeyType is not int
        with self.assertRaises(ValueError):
            relation = Relation(relationName, attributeLabels, [str, str, int],validityChecking=False)
    
    def test_insert_row(self):
        relationName = "TestRelation"
        attributeLabels = ['id', 'name', 'age']
        attributeTypes = [int, str, int]
        relation = Relation(relationName, attributeLabels, attributeTypes,validityChecking=False)
        
        # Insert a row without specifying id (autoIncrementPrimaryKey=True)
        relation.insertRow(attributeList=['Alice', 30])
        self.assertEqual(len(relation.data), 1)
        self.assertEqual(relation.data.iloc[0]['id'], 1)
        self.assertEqual(relation.data.iloc[0]['name'], 'Alice')
        self.assertEqual(relation.data.iloc[0]['age'], 30)
        
        # Test if row attribute labels match relation attribute labels
        row_labels = relation.data.columns.tolist()
        self.assertEqual(row_labels, attributeLabels)
        
        # Insert another row
        relation.insertRow(attributeList=['Bob', 25])
        self.assertEqual(len(relation.data), 2)
        self.assertEqual(relation.data.iloc[1]['id'], 2)
        self.assertEqual(relation.data.iloc[1]['name'], 'Bob')
        self.assertEqual(relation.data.iloc[1]['age'], 25)
        
        # Test if row attribute labels match relation attribute labels
        row_labels = relation.data.columns.tolist()
        self.assertEqual(row_labels, attributeLabels)
        
        # Insert row with mismatched attribute list length
        with self.assertRaises(ValueError):
            relation.insertRow(attributeList=['Charlie'])
        
        # Insert row with incorrect type
        with self.assertRaises(TypeError):
            relation.insertRow(attributeList=['Charlie', 'Thirty'])
        
        # Insert row with duplicate primary key when autoIncrementPrimaryKey=False
        relation_no_auto = Relation(relationName, attributeLabels, attributeTypes, autoIncrementPrimaryKey=False, validityChecking=False)
        relation_no_auto.insertRow(attributeList=[1, 'Alice', 30])
        with self.assertRaises(KeyError):
            relation_no_auto.insertRow(attributeList=[1, 'Bob', 25])
    
    def test_insert_row_invalid_user(self):
        relationName = "User"
        attributeLabels = ['user_id', 'username', 'email', 'password', 'fName', 'lName', 'type', 'emergency_contact_email', 'emergency_contact_name', 'specialization', 'is_disabled']
        attributeTypes = [int, str, str, str, str, str, str, str, str, str, bool]
        relation = Relation(relationName, attributeLabels, attributeTypes, autoIncrementPrimaryKey=False, validityChecking=True)

        # Test inserting a row with an invalid email
        with self.assertRaises(InvalidDataError):
            relation.insertRow(attributeList=[1, 'user1', 'invalid-email', 'password', 'John', 'Doe', 'Patient', None, None, None, False])

        # Test inserting a row with an invalid first name
        with self.assertRaises(InvalidDataError):
            relation.insertRow(attributeList=[1, 'user1', 'user1@example.com', 'password', '123', 'Doe', 'Patient', None, None, None, False])

        # Test inserting a row with an invalid last name
        with self.assertRaises(InvalidDataError):
            relation.insertRow(attributeList=[1, 'user1', 'user1@example.com', 'password', 'John', '123', 'Patient', None, None, None, False])

        # Test inserting a row with an invalid type
        with self.assertRaises(TypeError):
            relation.insertRow(attributeList=[1, 'user1', 'user1@example.com', 'password', 'John', 'Doe', 'InvalidType', None, None, None, False])

        # # Test inserting a row with an invalid specialization
        # with self.assertRaises(InvalidDataError):
        #     relation.insertRow(attributeList=[1, 'user1', 'user1@example.com', 'password', 'John', 'Doe', 'MHWP', None, None, '123', False])

    def test_insert_row_invalid_appointment(self):
        relationName = "Appointment"
        attributeLabels = ['appointment_id', 'patient_id', 'mhwp_id', 'date', 'room_name', 'status']
        attributeTypes = [int, int, int, datetime, str, str]
        relation = Relation(relationName, attributeLabels, attributeTypes, autoIncrementPrimaryKey=False, validityChecking=True)

        # Test inserting a row with an invalid date
        with self.assertRaises(TypeError):
            relation.insertRow(attributeList=[1, 1, 1, 'invalid-date', 'Room1', 'Scheduled'])

        # Test inserting a row with an invalid room name
        with self.assertRaises(InvalidDataError):
            relation.insertRow(attributeList=[1, 1, 1, datetime.today(), None, 'Scheduled'])

        # Test inserting a row with an invalid status
        with self.assertRaises(InvalidDataError):
            relation.insertRow(attributeList=[1, 1, 1, datetime.today(), 'Room1', None])

    def test_insert_row_invalid_journal_entry(self):
        relationName = "JournalEntry"
        attributeLabels = ['entry_id', 'patient_id', 'text', 'timestamp']
        attributeTypes = [int, int, str, datetime]
        relation = Relation(relationName, attributeLabels, attributeTypes, autoIncrementPrimaryKey=False, validityChecking=True)

        # Test inserting a row with an invalid text type
        with self.assertRaises(TypeError):
            relation.insertRow(attributeList=[1, 1, 123, datetime.today()])

        # Test inserting a row with an invalid text type
        with self.assertRaises(InvalidDataError):
            relation.insertRow(attributeList=[1, 1, None, datetime.today()])

        # Test inserting a row with an invalid timestamp
        with self.assertRaises(InvalidDataError):
            relation.insertRow(attributeList=[1, 1, 'Valid text', None])

    def test_get_attribute_max_row(self):
        relationName = "TestRelation"
        attributeLabels = ['id', 'name', 'age']
        attributeTypes = [int, str, int]
        relation = Relation(relationName, attributeLabels, attributeTypes,validityChecking=False)
        relation.insertRow(attributeList=['Alice', 30])
        relation.insertRow(attributeList=['Bob', 25])
        relation.insertRow(attributeList=['Charlie', 35])
        
        max_row = relation.getAttributeMaxRow('age')
        self.assertEqual(max_row.values, [3, 'Charlie', 35])
        
        # Test if row attribute labels match relation attribute labels
        self.assertEqual(max_row.labels, attributeLabels)
        
        # Test with empty data
        empty_relation = Relation(relationName, attributeLabels, attributeTypes,validityChecking=False)
        self.assertIsNone(empty_relation.getAttributeMaxRow('age'))
        
        # Test with non-existing attribute
        with self.assertRaises(KeyError):
            relation.getAttributeMaxRow('salary')
    
    def test_get_attribute_min_row(self):
        # Similar to test_get_attribute_max_row
        relationName = "TestRelation"
        attributeLabels = ['id', 'name', 'age']
        attributeTypes = [int, str, int]
        relation = Relation(relationName, attributeLabels, attributeTypes,validityChecking=False)
        relation.insertRow(attributeList=['Alice', 30])
        relation.insertRow(attributeList=['Bob', 25])
        relation.insertRow(attributeList=['Charlie', 35])
        
        min_row = relation.getAttributeMinRow('age')
        self.assertEqual(min_row.values, [2, 'Bob', 25])
        
        # Test if row attribute labels match relation attribute labels
        self.assertEqual(min_row.labels, attributeLabels)
        
        # Test with empty data
        empty_relation = Relation(relationName, attributeLabels, attributeTypes,validityChecking=False)
        self.assertIsNone(empty_relation.getAttributeMinRow('age'))
        
        # Test with non-existing attribute
        with self.assertRaises(KeyError):
            relation.getAttributeMinRow('salary')
    
    def test_get_all_rows(self):
        relationName = "TestRelation"
        attributeLabels = ['id', 'name', 'age']
        attributeTypes = [int, str, int]
        relation = Relation(relationName, attributeLabels, attributeTypes,validityChecking=False)
        relation.insertRow(attributeList=['Alice', 30])
        relation.insertRow(attributeList=['Bob', 25])
        
        all_rows = relation.getAllRows()
        self.assertEqual(len(all_rows), 2)
        self.assertEqual(all_rows[0].values, [1, 'Alice', 30])
        self.assertEqual(all_rows[1].values, [2, 'Bob', 25])
        
        # Test if row attribute labels match relation attribute labels
        for row in all_rows:
            self.assertEqual(row.labels, attributeLabels)
    
    def test_get_all_row_ids(self):
        relationName = "TestRelation"
        attributeLabels = ['id', 'name', 'age']
        attributeTypes = [int, str, int]
        relation = Relation(relationName, attributeLabels, attributeTypes,validityChecking=False)
        relation.insertRow(attributeList=['Alice', 30])
        relation.insertRow(attributeList=['Bob', 25])
        
        ids = relation.getAllRowIDs()
        self.assertEqual(ids, [1, 2])
    
    def test_get_rows_where_equal(self):
        relationName = "TestRelation"
        attributeLabels = ['id', 'name', 'age']
        attributeTypes = [int, str, int]
        relation = Relation(relationName, attributeLabels, attributeTypes,validityChecking=False)
        relation.insertRow(attributeList=['Alice', 30])
        relation.insertRow(attributeList=['Bob', 25])
        relation.insertRow(attributeList=['Alice', 35])
        
        rows = relation.getRowsWhereEqual('name', 'Alice')
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0].values, [1, 'Alice', 30])
        self.assertEqual(rows[1].values, [3, 'Alice', 35])
        
        # Test if row attribute labels match relation attribute labels
        for row in rows:
            self.assertEqual(row.labels, attributeLabels)
        
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
        relation = Relation(relationName, attributeLabels, attributeTypes,validityChecking=False)
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
        relation = Relation(relationName, attributeLabels, attributeTypes,validityChecking=False)
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
        relation = Relation(relationName, attributeLabels, attributeTypes,validityChecking=False)
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
        relation = Relation(relationName, attributeLabels, attributeTypes,validityChecking=False)
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
        relation = Relation(relationName, attributeLabels, attributeTypes,validityChecking=False)
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
        relation = Relation(relationName, attributeLabels, attributeTypes,validityChecking=False)
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
        relation = Relation(relationName, attributeLabels, attributeTypes,validityChecking=False)
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
        relation = Relation(relationName, attributeLabels, attributeTypes,validityChecking=False)
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

    def test_edit_row_validityChecking(self):
        relationName = "User"
        attributeLabels = ['user_id', 'username', 'email', 'password', 'fName', 'lName', 'type', 'emergency_contact_email', 'emergency_contact_name', 'specialization', 'is_disabled']
        attributeTypes = [int, str, str, str, str, str, str, str, str, str, bool]
        relation = Relation(relationName, attributeLabels, attributeTypes, autoIncrementPrimaryKey=True, validityChecking=True)
        relation.insertRow(attributeList=['user1', 'user1@example.com', 'password', 'John', 'Doe', 'Patient', None, None, None, False])
        
        # Edit row with new values using primary key index
        relation.editRow(1, newValues=['user1', 'user1@example.com', 'password', 'John', 'Doe', 'Patient', None, None, None, True])
        self.assertEqual(relation.data.iloc[0]['is_disabled'], True)
        
        # Edit row with Row object using primary key index
        new_row = Row(['user1', 'user1@example.com', 'password', 'John', 'Doe', 'Patient', None, None, None, False])
        relation.editRow(1, row=new_row)
        self.assertEqual(relation.data.iloc[0]['is_disabled'], False)
        
        # Test IndexError for out of bounds primary key index
        with self.assertRaises(IndexError):
            relation.editRow(2, newValues=['user2', 'user2@example.com', 'password', 'Jane', 'Doe', 'Patient', None, None, None, False])
        
        # Test ValueError for both newValues and row provided
        with self.assertRaises(ValueError):
            relation.editRow(1, newValues=['user1', 'user1@example.com', 'password', 'John', 'Doe', 'Patient', None, None, None, True], row=new_row)
        
        # Test ValueError for neither newValues nor row provided
        with self.assertRaises(ValueError):
            relation.editRow(1)
        
        # Test InvalidDataError for invalid email format
        with self.assertRaises(InvalidDataError):
            relation.editRow(1, newValues=['user1', 'invalid-email', 'password', 'John', 'Doe', 'Patient', None, None, None, False])
        
        # Test InvalidDataError for invalid first name
        with self.assertRaises(InvalidDataError):
            relation.editRow(1, newValues=['user1', 'user1@example.com', 'password', '123', 'Doe', 'Patient', None, None, None, False])
        
        # Test InvalidDataError for invalid last name
        with self.assertRaises(InvalidDataError):
            relation.editRow(1, newValues=['user1', 'user1@example.com', 'password', 'John', '123', 'Patient', None, None, None, False])
        
        # Test TypeError for invalid type
        with self.assertRaises(TypeError):
            relation.editRow(1, newValues=['user1', 'user1@example.com', 'password', 'John', 'Doe', 'InvalidType', None, None, None, False])
        
        # TODO
        # # Test InvalidDataError for invalid specialization
        # with self.assertRaises(InvalidDataError):
        #     relation.editRow(1, newValues=[1, 'user1', 'user1@example.com', 'password', 'John', 'Doe', 'Patient', None, None, 'InvalidSpecialization', False])
        
        # Test TypeError for incorrect type
        with self.assertRaises(TypeError):
            relation.editRow(1, newValues=['user1', 'user1@example.com', 'password', 'John', 'Doe', 'Patient', None, None, None, 'not_a_bool'])

    def test_edit_field_in_row(self):
        relationName = "TestRelation"
        attributeLabels = ['id', 'name', 'age']
        attributeTypes = [int, str, int]
        relation = Relation(relationName, attributeLabels, attributeTypes,validityChecking=False)
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

    def test_edit_field_in_row_validityChecking(self):
        relationName = "User"
        attributeLabels = ['user_id', 'username', 'email', 'password', 'fName', 'lName', 'type', 'emergency_contact_email', 'emergency_contact_name', 'specialization', 'is_disabled']
        attributeTypes = [int, str, str, str, str, str, str, str, str, str, bool]
        relation = Relation(relationName, attributeLabels, attributeTypes, autoIncrementPrimaryKey=False, validityChecking=True)
        relation.insertRow(attributeList=[1, 'user1', 'user1@example.com', 'password', 'John', 'Doe', 'Patient', None, None, None, False])
        
        # Edit field with valid data
        relation.editFieldInRow(1, 'is_disabled', True)
        self.assertEqual(relation.data.iloc[0]['is_disabled'], True)
        
        # Test IndexError for out of bounds primary key index
        with self.assertRaises(IndexError):
            relation.editFieldInRow(2, 'username', 'user2')
        
        # Test ValueError for invalid attribute
        with self.assertRaises(ValueError):
            relation.editFieldInRow(1, 'non_existent_attribute', 'value')
        
        # Test TypeError for incorrect type
        with self.assertRaises(TypeError):
            relation.editFieldInRow(1, 'is_disabled', 'not_a_bool')
        
        # TODO
        # # Test InvalidDataError for invalid email format
        # with self.assertRaises(InvalidDataError):
        #     relation.editFieldInRow(1, 'emergency_contact_email', 'invalid-email')
        #     print(relation.getRowsWhereEqual('user_id',1))

        # # Test InvalidDataError for invalid email format
        # with self.assertRaises(InvalidDataError):
        #     relation.editFieldInRow(1, 'email', 'invalid-email')
        #     print(relation.getRowsWhereEqual('user_id',1))
        
        
        # Test InvalidDataError for invalid first name
        with self.assertRaises(InvalidDataError):
            relation.editFieldInRow(1, 'fName', '123')
        
        # Test InvalidDataError for invalid last name
        with self.assertRaises(InvalidDataError):
            relation.editFieldInRow(1, 'lName', '123')
        
        # Test TypeError for invalid type
        with self.assertRaises(TypeError):
            relation.editFieldInRow(1, 'type', 'InvalidType')
        
        # TODO
        # # Test InvalidDataError for invalid specialization
        # with self.assertRaises(InvalidDataError):
        #     relation.editFieldInRow(1, 'specialization', 'InvalidSpecialization')
       
    def test_edit_field_in_row_user_relation(self):
        # Create a user relation with autoIncrementPrimaryKey set to True
        relationName = "User"
        attributeLabels = ['user_id', 'username', 'email', 'password', 'fName', 'lName', 'type', 'emergency_contact_email', 'emergency_contact_name', 'specialization', 'is_disabled']
        attributeTypes = [int, str, str, str, str, str, str, str, str, str, bool]
        user_relation = Relation(relationName, attributeLabels, attributeTypes, autoIncrementPrimaryKey=True, validityChecking=True)
        
        # Populate the relation with users
        user_relation.insertRow(attributeList=['user1', 'user1@example.com', 'password', 'John', 'Doe', 'Patient', None, None, None, False])
        user_relation.insertRow(attributeList=['user2', 'user2@example.com', 'password', 'Jane', 'Smith', 'MHWP', None, None, None, False])
        user_relation.insertRow(attributeList=['user3', 'user3@example.com', 'password', 'Alice', 'Johnson', 'Admin', None, None, None, False])
        
        # Edit field with valid data
        user_relation.editFieldInRow(2, 'email', 'test123@newdomain.com')
        self.assertEqual(user_relation.data.iloc[1]['email'], 'test123@newdomain.com')
        
        # Test IndexError for out of bounds primary key index
        with self.assertRaises(IndexError):
            user_relation.editFieldInRow(4, 'username', 'user4')
        
        # Test ValueError for invalid attribute
        with self.assertRaises(ValueError):
            user_relation.editFieldInRow(1, 'non_existent_attribute', 'value')
        
        # Test TypeError for incorrect type
        with self.assertRaises(TypeError):
            user_relation.editFieldInRow(1, 'is_disabled', 'not_a_bool')
        
        # Test InvalidDataError for invalid email format
        with self.assertRaises(InvalidDataError):
            user_relation.editFieldInRow(1, 'email', 'invalid-email')
        
        # Test InvalidDataError for invalid first name
        with self.assertRaises(InvalidDataError):
            user_relation.editFieldInRow(1, 'fName', '123')
        
        # Test InvalidDataError for invalid last name
        with self.assertRaises(InvalidDataError):
            user_relation.editFieldInRow(1, 'lName', '123')
        
        # Test TypeError for invalid type
        with self.assertRaises(TypeError):
            user_relation.editFieldInRow(1, 'type', 'InvalidType')
        
        # Test InvalidDataError for invalid specialization
        # with self.assertRaises(InvalidDataError):
        #     user_relation.editFieldInRow(1, 'specialization', 'InvalidSpecialization')
        ## TODO

    def  test_edit_field_in_row_user_relation_noautoincrement(self):
        relationName = "User"
        attributeLabels = ['user_id', 'username', 'email', 'password', 'fName', 'lName', 'type', 'emergency_contact_email', 'emergency_contact_name', 'specialization', 'is_disabled']
        attributeTypes = [int, str, str, str, str, str, str, str, str, str, bool]
        user_relation = Relation(relationName, attributeLabels, attributeTypes, autoIncrementPrimaryKey=False, validityChecking=True)
        
        # Populate the relation with users
        user_relation.insertRow(attributeList=[1, 'user1', 'user1@example.com', 'password', 'John', 'Doe', 'Patient', None, None, None, False])
        user_relation.insertRow(attributeList=[2, 'user2', 'user2@example.com', 'password', 'Jane', 'Smith', 'MHWP', None, None, None, False])
        user_relation.insertRow(attributeList=[3, 'user3', 'user3@example.com', 'password', 'Alice', 'Johnson', 'Admin', None, None, None, False])
        
        # Edit field with valid data
        user_relation.editFieldInRow(2, 'email', 'test123@newdomain.com')
        self.assertEqual(user_relation.data.iloc[1]['email'], 'test123@newdomain.com')
        
        # Test IndexError for out of bounds primary key index
        with self.assertRaises(IndexError):
            user_relation.editFieldInRow(4, 'username', 'user4')
        
        # Test ValueError for invalid attribute
        with self.assertRaises(ValueError):
            user_relation.editFieldInRow(1, 'non_existent_attribute', 'value')
        
        # Test TypeError for incorrect type
        with self.assertRaises(TypeError):
            user_relation.editFieldInRow(1, 'is_disabled', 'not_a_bool')
        
        # Test InvalidDataError for invalid email format
        with self.assertRaises(InvalidDataError):
            user_relation.editFieldInRow(1, 'email', 'invalid-email')
        
        # Test InvalidDataError for invalid first name
        with self.assertRaises(InvalidDataError):
            user_relation.editFieldInRow(1, 'fName', '123')
        
        # Test InvalidDataError for invalid last name
        with self.assertRaises(InvalidDataError):
            user_relation.editFieldInRow(1, 'lName', '123')
        
        # Test TypeError for invalid type
        with self.assertRaises(TypeError):
            user_relation.editFieldInRow(1, 'type', 'InvalidType')
        
        # Test InvalidDataError for invalid specialization
        # with self.assertRaises(InvalidDataError):
        #     user_relation.editFieldInRow(1, 'specialization', 'InvalidSpecialization')

    def test_get_where_smaller(self):
        # Similar to above, but returns a Relation
        relationName = "TestRelation"
        attributeLabels = ['id', 'name', 'age']
        attributeTypes = [int, str, int]
        relation = Relation(relationName, attributeLabels, attributeTypes,validityChecking=False)
        relation.insertRow(attributeList=['Alice', 30])
        relation.insertRow(attributeList=['Bob', 25])
        relation.insertRow(attributeList=['Charlie', 35])
        
        new_relation = relation.getWhereSmaller('age', 30)
        self.assertEqual(len(new_relation), 1)
        self.assertEqual(new_relation.data.iloc[0]['name'], 'Bob')
        
        # Test with empty result
        new_relation = relation.getWhereSmaller('age', 20)
        self.assertEqual(len(new_relation), 0)

    def test_length(self):
        relationName = "TestRelation"
        attributeLabels = ['id', 'name', 'age']
        relation = Relation(relationName, attributeLabels,validityChecking=False)
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

    def test_ensure_open_decorator(self):
        # Test that the @ensure_open decorator ensures the database is open before operations
        self.db.close()  # Manually close the database
        with self.assertRaises(Exception):  # Expect an error if the database is closed
            self.db.insert_admin(Admin(username='admin2', password='password456'))
        
        # Reopen the database and perform an operation to ensure it works when open
        self.db = Database(data_file=self.test_db_file, logger=self.logger, verbose=False, overwrite=False)
        admin = Admin(username='admin2', password='password456')
        self.db.insert_admin(admin)
        user = self.db.getRelation('User').data
        self.assertEqual(len(user), 1)
        self.assertEqual(user.iloc[0]['username'], 'admin2')
        self.assertEqual(user.iloc[0]['type'], 'Admin')

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
            emergency_contact_name='Jane Doe',
            is_disabled=False
        )
        self.db.insert_patient(patient)
        user = self.db.getRelation('User').data
        self.assertEqual(len(user), 1)
        self.assertEqual(user.iloc[0]['username'], 'patient1')
        self.assertEqual(user.iloc[0]['type'], 'Patient')
        self.assertEqual(user.iloc[0]['email'], 'patient1@example.com')

    def test_delete_patient_and_propagation(self):
        # Insert some patients
        patient1 = Patient(username='patient1', email='patient1@example.com', password='password123', fName='John', lName='Doe', emergency_contact_email='contact@example.com', is_disabled=False)
        patient2 = Patient(username='patient2', email='patient2@example.com', password='password123', fName='Jane', lName='Doe', emergency_contact_email='contact@example.com', is_disabled=False)
        patient3 = Patient(username='patient3', email='patient3@example.com', password='password123', fName='Jim', lName='Beam', emergency_contact_email='contact@example.com', is_disabled=False)
        
        self.db.insert_patient(patient1)
        self.db.insert_patient(patient2)
        self.db.insert_patient(patient3)

        # Insert appointments for patients
        appointment1 = Appointment(patient_id=2, mhwp_id=2, date=datetime(2023, 1, 1, 10, 0), status='Scheduled', room_name='Room 101')
        appointment2 = Appointment(patient_id=1, mhwp_id=3, date=datetime(2023, 1, 2, 11, 0), status='Scheduled', room_name='Room 102')

        self.db.insert_appointment(appointment1)
        self.db.insert_appointment(appointment2)

        # Delete by patient_id
        self.db.delete_patient(patientId=2)
        user = self.db.getRelation('User').data
        self.assertEqual(len(user), 2)
        remaining_ids = user['user_id'].tolist()
        self.assertEqual(remaining_ids, [1, 3])

        

        # Check if associated records in Appointment relation are deleted
        appointment_data = self.db.getRelation('Appointment').data
        self.assertEqual(len(appointment_data), 1)
        self.assertEqual(appointment_data.iloc[0]['patient_id'], 1)
        
        # Delete by multiple patient_ids
        self.db.delete_patient(patientId=1)
        self.db.delete_patient(patientId=3)
        user = self.db.getRelation('User').data
        self.assertEqual(len(user), 0)
        
        # Test error when patientId is not an integer
        with self.assertRaises(TypeError):
            self.db.delete_patient(patientId='1')
        
        # Test error when patientId does not exist
        with self.assertRaises(KeyError):
            self.db.delete_patient(patientId=99)

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
        journal_entry = JournalEntry(patient_id=1, text='Today was a good day.', timestamp=datetime.now())
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
        row = Row([None, 
                   'testuser', 
                   'test@example.com', 
                   'password', 
                   'Test', 
                   'User', 
                   'Patient', 
                   None, None, None, None, False])
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
        row1 = Row(['user1', 'user1@example.com', 'password', 'FirstOne', 'LastOne', 'Patient', None, None, None, False])
        row2 = Row(['user2', 'user2@example.com', 'password', 'FirstTwo', 'LastTwo', 'Patient', None, None, None, False])
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

class TestEntities(unittest.TestCase):
   
    def test_mhwp_invalid_data(self):
        # Test invalid first name
        with self.assertRaises(InvalidDataError):
            MHWP(username='mhwpUser', password='validPass123', fName='123', lName='Valid', email='valid@example.com', specialization='Psychology')
        
        # Test invalid last name
        with self.assertRaises(InvalidDataError):
            MHWP(username='mhwpUser', password='validPass123', fName='Valid', lName='123', email='valid@example.com', specialization='Psychology')
        
        # Test invalid email
        with self.assertRaises(InvalidDataError):
            MHWP(username='mhwpUser', password='validPass123', fName='Valid', lName='Valid', email='invalid-email', specialization='Psychology')
        
        # Test invalid specialization
        with self.assertRaises(InvalidDataError):
            MHWP(username='mhwpUser', password='validPass123', fName='Valid', lName='Valid', email='valid@example.com', specialization='123')

    def test_journal_entry_invalid_data(self):
        # Test invalid entry_id
        with self.assertRaises(InvalidDataError):
            JournalEntry(entry_id='not_an_int', patient_id=1, text='Valid text', timestamp=datetime.now())
        
        # Test invalid patient_id
        with self.assertRaises(InvalidDataError):
            JournalEntry(entry_id=1, patient_id='not_an_int', text='Valid text', timestamp=datetime.now())
        
        # Test empty text
        with self.assertRaises(InvalidDataError):
            JournalEntry(entry_id=1, patient_id=1, text='', timestamp=datetime.now())
        
        # Test invalid timestamp
        with self.assertRaises(InvalidDataError):
            JournalEntry(entry_id=1, patient_id=1, text='Valid text', timestamp='not_a_datetime')

    def test_appointment_invalid_data(self):
        # Test invalid appointment_id
        with self.assertRaises(InvalidDataError):
            Appointment(appointment_id='not_an_int', patient_id=1, mhwp_id=1, date=datetime.now(), room_name='Room A', status='Scheduled')
        
        # Test invalid patient_id
        with self.assertRaises(InvalidDataError):
            Appointment(appointment_id=1, patient_id='not_an_int', mhwp_id=1, date=datetime.now(), room_name='Room A', status='Scheduled')
        
        # Test invalid mhwp_id
        with self.assertRaises(InvalidDataError):
            Appointment(appointment_id=1, patient_id=1, mhwp_id='not_an_int', date=datetime.now(), room_name='Room A', status='Scheduled')
        
        # Test invalid date
        with self.assertRaises(InvalidDataError):
            Appointment(appointment_id=1, patient_id=1, mhwp_id=1, date='not_a_datetime', room_name='Room A', status='Scheduled')
        
    def test_patient_invalid_data(self):
        # Test invalid username
        with self.assertRaises(InvalidDataError):
            Patient(username='!nv@l!d', email='valid@example.com', password='validPass123', fName='John', lName='Doe', emergency_contact_email='contact@example.com', emergency_contact_name='Jane Doe', is_disabled=False)
        
        # Test invalid email
        with self.assertRaises(InvalidDataError):
            Patient(username='validUser', email='invalid-email', password='validPass123', fName='John', lName='Doe', emergency_contact_email='contact@example.com', emergency_contact_name='Jane Doe', is_disabled=False)
        
        # Test invalid first name
        with self.assertRaises(InvalidDataError):
            Patient(username='validUser', email='valid@example.com', password='validPass123', fName='123', lName='Doe', emergency_contact_email='contact@example.com', emergency_contact_name='Jane Doe', is_disabled=False)
        
        # Test invalid last name
        with self.assertRaises(InvalidDataError):
            Patient(username='validUser', email='valid@example.com', password='validPass123', fName='John', lName='123', emergency_contact_email='contact@example.com', emergency_contact_name='Jane Doe', is_disabled=False)

    def test_admin_invalid_data(self):
        # Test invalid username
        with self.assertRaises(InvalidDataError):
            Admin(username='!nv@l!d', password='validPass123')
        
        # Test invalid password
        with self.assertRaises(InvalidDataError):
            Admin(username='validUser', password='short')

    def test_allocation_invalid_data(self):
        # Test invalid allocation_id
        with self.assertRaises(InvalidDataError):
            Allocation(allocation_id='not_an_int', patient_id=1, mhwp_id=1, start_date=datetime.now(), end_date=datetime.now())
        
        # Test invalid patient_id
        with self.assertRaises(InvalidDataError):
            Allocation(allocation_id=1, patient_id='not_an_int', mhwp_id=1, start_date=datetime.now(), end_date=datetime.now())
        
        # Test invalid mhwp_id
        with self.assertRaises(InvalidDataError):
            Allocation(allocation_id=1, patient_id=1, mhwp_id='not_an_int', start_date=datetime.now(), end_date=datetime.now())
        
        # Test invalid start_date
        with self.assertRaises(InvalidDataError):
            Allocation(allocation_id=1, patient_id=1, mhwp_id=1, start_date='not_a_datetime', end_date=datetime.now())
        
        # Test invalid end_date
        with self.assertRaises(InvalidDataError):
            Allocation(allocation_id=1, patient_id=1, mhwp_id=1, start_date=datetime.now(), end_date='not_a_datetime')

    def test_moodentry_invalid_data(self):
        # Test invalid moodentry_id
        with self.assertRaises(InvalidDataError):
            MoodEntry(moodentry_id='not_an_int', patient_id=1, moodscore=3, comment='Feeling good', timestamp=datetime.now())
        
        # Test invalid patient_id
        with self.assertRaises(InvalidDataError):
            MoodEntry(moodentry_id=1, patient_id='not_an_int', moodscore=3, comment='Feeling good', timestamp=datetime.now())
        
        # Test invalid moodscore
        with self.assertRaises(InvalidDataError):
            MoodEntry(moodentry_id=1, patient_id=1, moodscore='not_an_int', comment='Feeling good', timestamp=datetime.now())
        
        # Test moodscore out of range
        with self.assertRaises(InvalidDataError):
            MoodEntry(moodentry_id=1, patient_id=1, moodscore=7, comment='Feeling good', timestamp=datetime.now())
        
        # Test invalid timestamp
        with self.assertRaises(InvalidDataError):
            MoodEntry(moodentry_id=1, patient_id=1, moodscore=3, comment='Feeling good', timestamp='not_a_datetime')



if __name__ == '__main__':
    unittest.main()
import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database'))
sys.path.append(project_root)
from database.database import Database
from database.initDBwithDummyData_FeatureTest import initDummyDatabase

db = Database(overwrite = True)
initDummyDatabase(db)
db.close()
db = Database()

room1 = db.getRelation('User')
print(room1)
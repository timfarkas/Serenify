import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if project_root not in sys.path:
    sys.path.append(project_root)

from .database import Database
import database.initDummyData
import logging

# Test functions
def initDummyDatabase(db: Database):
    logging.warning("Warning, this way of calling initDummyDatabase is deprecated, please use initDummyData.initDummyDatabase (instead of initDBwithDummyData.initDummyDatabase, changed for brevity).")
    database.initDummyData.initDummyDatabase(db, printOut=True)
    logging.warning("Warning, this way of calling initDummyDatabase is deprecated, please use initDummyData.initDummyDatabase (instead of initDBwithDummyData.initDummyDatabase, changed for brevity).")

if __name__ == "__main__":
    db = Database(overwrite=True)
    initDummyDatabase(db)
    db.close()
    
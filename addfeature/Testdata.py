import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database'))
sys.path.append(project_root)

from .globalvariables import db


room1 = db.getRelation('Notification')
print(room1)
# for i in room1:
#     print(i)

# doc= room1.getRowsWhereEqual('mhwp_id',5)
# print(len(doc))
# room1.editFieldInRow(1, 'lName',str("AAA"))
# room2 = db.getRelation('User')

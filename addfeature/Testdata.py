import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.database import Database
from sessions import Session


# sess = Session()
# sess.open()
# sess.close()
# sess.set("Test",1)
# a=sess.get("Test")
# a+=100
# sess.set("Test",a)
# print(sess.get("Test"))
db=Database()
room1 = db.getRelation('Notification')
print(room1)
# # for i in room1:
#     print(i)

# doc= room1.getRowsWhereEqual('mhwp_id',5)
# print(len(doc))
# room1.editFieldInRow(1, 'lName',str("AAA"))
# room2 = db.getRelation('User')

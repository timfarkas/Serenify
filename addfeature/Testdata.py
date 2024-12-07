import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.database import Database
from addfeature.notificationbox import opennotification
from sessions import Session
from datetime import datetime



# sess = Session()
# sess.open()
# sess.close()
# sess.set("Test",1)
# a=sess.get("Test")
# a+=100
# sess.set("Test",a)
# print(sess.get("Test"))

db=Database()
# db.close()
print(db._is_closed)
# opennotification()

# usermoodlog=db.getRelation('MoodEntry').getRowsWhereEqual('patient_id',3)
# lastrecorddate=usermoodlog[-1][4].strftime("%Y-%m-%d")
# # datelist=[]
# # for i in room1:
# #     datelist.append(i[4])
# # print(datelist)
# time=datetime.now().strftime("%Y-%m-%d")
# print(lastrecord==time)
# # for i in room1:
#     print(i)

# doc= room1.getRowsWhereEqual('mhwp_id',5)
# print(len(doc))
# room1.editFieldInRow(1, 'lName',str("AAA"))
# room2 = db.getRelation('User')

room1=db.getRelation('MoodEntry').getRowsWhereEqual("patient_id",6)
# print(room1[0][3]>datetime.now())
print(room1)
    # exercisedata.append(i[2])

# for i in range(-1,-4,-1):
#     print(i)
# print(userdata[-1])
# print(room1.data.columns)
# lastindex=userdata[-1][0]
# print(lastindex)
# room1.data.drop(room1.data[room1.data['moodentry_id'] == lastindex].index, inplace=True)
# room1.data.reset_index(drop=True, inplace=True)
#
# print(room1)
# db.close()



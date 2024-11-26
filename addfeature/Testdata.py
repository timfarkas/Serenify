import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database'))
sys.path.append(project_root)

from .globalvariables import db
# import admin.


# exec(open("adminFunctions.py").read())
#
#
userdata = db.getRelation('Allocation')
# patientdata=userdata.getRowsWhereEqual('username','patient1')

print(userdata)


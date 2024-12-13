import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sessions import Session

# 1: Create a session instance
session = Session(debug=True)

# 2: Initialize the session file
session._initialize()

# 3: Open the session
try:
    session.open()
except RuntimeError as e:
    print(e)

# 4: Set some session data
session.setId("user123")
session.setRole("Admin")
session.set("isDisabled", False)


print("User ID:", session.getId())
print("Role:", session.getRole())
print("isDisabled:", session.get("isDisabled"))

session.close()
import os
import pickle
import tempfile


#Session manager 
class Session:
    def __init__(self, debug = False):
        self.session_data = {}
        self.debugMode = debug
        self.file_path = os.path.join(tempfile.gettempdir(), 'serenify_session.tmp')
    
    def _initialize(self):
        with open(self.file_path, 'wb') as f:
            if self.debugMode:
                print(f"Initialized session in {self.file_path}")
            pass  # this creates the session file (overwriting it if it already exists)

    def open(self):
        if not os.path.exists(self.file_path):
            raise RuntimeError(f"Session file not found at {self.file_path}. Please initialize the session.")
        try:
            try:
                with open(self.file_path, 'rb+') as f:
                    self.session_data = pickle.load(f)
            except EOFError:
                self.session_data = {}
        except Exception as e:
            print("An error occured during opening the session. Try deleting the session tmp file or reinitializing the session.")
            raise e  

    def close(self):
        with open(self.file_path, 'wb') as f:
            pickle.dump(self.session_data, f)
        
    def setId(self, user_id):
        """Store the user ID in the session data."""
        self.session_data['user_id'] = user_id

    def getId(self):
        """Retrieve the user ID from the session data."""
        return self.session_data.get('user_id')

    def setRole(self, role):
        """Store the user role in the session data."""
        if role not in ['Admin', 'MHWP', 'Patient']:
            raise ValueError("Role must be 'Admin', 'MHWP', or 'Patient'.")
        self.session_data['role'] = role

    def getRole(self):
        """Retrieve the user role from the session data."""
        return self.session_data.get('role')

    def set(self, key, value):
        """Store a key-value pair in the session data."""
        self.session_data[key] = value

    def get(self, key=None, default=None):
        """Retrieve a value from the session data by key."""
        if key:
            return self.session_data.get(key, default)
        else: ## return all session data if no key was set
            return self.session_data

    def clear(self):
        """Clear all session data."""
        self.session_data.clear()
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
        

    def __repr__(self):
        return f"Session(session_id={self.session_id}, user_id={self.user_id}, data={self.session_data})"

session = Session()


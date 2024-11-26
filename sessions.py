
#Session manager 
class Session:
    def __init__(self, session_id=None, user_id=None):
        # Store session data
        self.session_data = {}
        self.session_id = session_id or "default_session_id"  # Generate a default
        self.user_id = user_id  # Set user_id as provided or None if not logged in

    def set(self, key, value):
        """Store a key-value pair in the session data."""
        self.session_data[key] = value

    def get(self, key=None):
        """Retrieve a value from the session data. If key is None, return all session data."""
        if key:
            return self.session_data.get(key)
        return self.session_data

    def clear(self):
        """Clear all session data."""
        self.session_data.clear()

    def __repr__(self):
        return f"Session(session_id={self.session_id}, user_id={self.user_id}, data={self.session_data})"

session = Session()


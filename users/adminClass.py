from UserClass import user

class admin(user):
    def __init__(self, admin_id, user_id, username, password, type, is_disabled):
        super().__init__(user_id, username, password, type, is_disabled)
        self.admin_id = admin_id



from flask_login import login_user

import database_manager
from login.user import User


def attempt_login(username, password):
    result = database_manager.get_user(username)
    if result[0]:
        if result[1]['password'] == password:
            logged_in_user = User(username, password)
            login_user(logged_in_user)
            return True
        else:
            return False
    return False

from flask import session


VALID_USERS = {
    "admin": ("tlevel", "admin"),
    "user": ("tlevel", "user"),
}


def is_admin():
    return session.get("role") == "admin"


def is_logged_in():
    return session.get("role") in ("user", "admin")


def authenticate_user(username, password):
    user_details = VALID_USERS.get(username)
    if user_details and user_details[0] == password:
        return user_details[1]
    return None
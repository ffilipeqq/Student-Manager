from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

from pytools.sqlTools import sql_commit, sql_fetch


def is_admin():
    return session.get("role") == "admin"


def is_logged_in():
    return session.get("role") in ("user", "admin")


def authenticate_user(username, password):
    user = sql_fetch(
        "SELECT username, password, role FROM users WHERE username = %s",
        (username,),
        fetch_type="one",
    )
    if not user:
        return None

    stored_password = user["password"]
    if check_password_hash(stored_password, password):
        return user["role"]

    # Upgrade the existing plaintext admin password after its first successful login.
    if stored_password == password:
        hashed_password = generate_password_hash(password)
        if sql_commit(
            "UPDATE users SET password = %s WHERE username = %s",
            (hashed_password, username),
        ):
            return user["role"]

    return None
import re


def clean_text(value):
    return " ".join(value.strip().split())


def validate_login(username, password):
    errors = []

    if not username:
        errors.append("Username cannot be empty.")

    if not password:
        errors.append("Password cannot be empty.")

    return errors


def validate_user(username, password, confirm_password, role):
    errors = validate_login(username, password)

    if not confirm_password:
        errors.append("Please confirm the password.")
    elif password != confirm_password:
        errors.append("Passwords do not match.")

    if role not in ("user", "admin"):
        errors.append("Choose a valid role.")

    return errors


def validate_student(name, email, course):
    errors = []

    if not name:
        errors.append("Name is required.")

    if not email:
        errors.append("Email is required.")
    elif not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        errors.append("Enter a valid email address.")

    if not course:
        errors.append("Course is required.")

    return errors

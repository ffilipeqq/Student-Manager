## Student Management System.

Used to manage students in a **SQL** database, and **display data** about courses onto a **dynamic** website.

This was built using **Python**, **Flask**, **Git**, AND **MySQL**, as a small solo project in class.

Includes a **login/logout system** using **sessions** and accounts - Features a **dashboard** page, **students list** page, **student editing**, and **student adding**.

User accounts are read from the MySQL `users` table with the columns `id`,
`username`, `password`, and `role`. New passwords are stored as Werkzeug
hashes, never as plain text. The existing admin account keeps its current
password and is upgraded to a hash the first time it logs in.

## Requirements
- Python 3.14
- A running MySQL server
- The required Database and tables
- Python packages in requirements.txt

## Setup
1. Clone the repository and open its folder.
2. Create and activate a Python virtual environment.
3. Install the dependencies with `pip install -r requirements.txt`.
4. Create the MySQL database and required tables.
5. Set the environment variables referring to **Powershell Commands**, then run the app with `python app.py`.

## Powershell Commands
```powershell
py -m venv .venv
```

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

```powershell
$env:db_host = "localhost"
$env:DB_PORT = "3306"
$env:DB_NAME = "college_db"
$env:DB_USER = "root"
$env:DB_PASSWORD = ""
```

```powershell
$packagingKey = .\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_hex(32))"
```

```powershell
$env:FLASK_SECRET_KEY = $packagingKey
```
```powershell
.\.venv\Scripts\python.exe -m flask --app app run
```

## Login
- Username: `admin`
- Password: `tlevel`

After logging in as an admin, use **Add User** in the navigation to create
additional accounts. The `id` column is generated automatically by MySQL.



## Important
- The MySQL database, tables, and local data are not included in this repository.
- This project was created for practising Flask and front-end design skills; it is not production-ready and should not be considered secure.

## Screenshots

### Dashboard
![Student Management System dashboard](projectimg/dashboard_overview.png)

### Students table
![Student Management System students table](projectimg/students_table.png)

### Add user
![Student Management System add user page](projectimg/add_user.png)
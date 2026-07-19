# TaskPilot

TaskPilot is a simple Flask-based task management web application that lets users register, log in, create tasks, and manage them through a clean web interface.

## Features

- User registration and login
- Secure password hashing
- Task creation and management
- Responsive templates with Flask and SQLAlchemy

## Project Structure

- `app.py` - Main Flask application
- `models.py` - Database models
- `forms.py` - WTForms for authentication and task handling
- `templates/` - HTML templates for the UI
- `instance/` - Local instance files

## Requirements

Make sure you have Python 3.8+ installed.

Install the required dependencies:

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not present, install the core packages manually:

```bash
pip install flask flask_sqlalchemy flask_login flask_wtf flask_migrate python-dotenv psycopg2-binary
```

## Environment Variables

Create a `.env` file in the project root with values such as:

```env
FLASK_APP=app.py
FLASK_DEBUG=1
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///todo.db
```

## Run the Application

From the project root, run:

```bash
flask run
```

Then open your browser at:

```text
http://127.0.0.1:5000
```

## Notes

- The default database is SQLite, but you can switch to PostgreSQL by changing `DATABASE_URL`.
- If you use migrations, initialize them once with:

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

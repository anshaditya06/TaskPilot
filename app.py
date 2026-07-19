from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from forms import RegisterForm, LoginForm, TaskForm
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db_url = os.environ.get('DATABASE_URL')
if db_url and db_url.startswith('postgres://'):
    db_url = db_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = 'login'  # type: ignore[assignment]
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('tasks'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        password = form.password.data or ''
        hashed_pw = generate_password_hash(password)
        new_user = User()
        new_user.username = form.username.data or ''
        new_user.email = form.email.data or ''
        new_user.password_hash = hashed_pw
        db.session.add(new_user)
        db.session.commit()
        flash('Account created — please log in.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data or ''
        password = form.password.data or ''
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('tasks'))
        flash('Invalid email or password.')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

from models import db, User, Task
from forms import RegisterForm, LoginForm, TaskForm

@app.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    form = TaskForm()
    if form.validate_on_submit():
        new_task = Task()
        new_task.title = form.title.data
        new_task.due_date = form.due_date.data
        new_task.user_id = current_user.id
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('tasks'))
    user_tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.id.desc()).all()
    return render_template('tasks.html', form=form, tasks=user_tasks)

@app.route('/tasks/<int:task_id>/toggle')
@login_required
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        abort(403)
    task.done = not task.done
    db.session.commit()
    return redirect(url_for('tasks'))

@app.route('/tasks/<int:task_id>/delete')
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        abort(403)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('tasks'))

@app.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        abort(403)

    form = TaskForm(obj=task)  # pre-fills the form with task's current data
    form.submit.label.text = 'Save Changes'
    if form.validate_on_submit():
        task.title = form.title.data
        db.session.commit()
        return redirect(url_for('tasks'))

    return render_template('edit_task.html', form=form, task=task)

if __name__ == '__main__':
    app.run(debug=True)


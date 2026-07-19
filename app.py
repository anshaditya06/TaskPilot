from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-this-later'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db.init_app(app)

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

@app.route('/tasks')
@login_required
def tasks():
    return f'Logged in as {current_user.username} — tasks page coming next.'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
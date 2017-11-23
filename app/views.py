from flask import Flask, render_template, request, flash, url_for
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.utils import redirect

from app.forms import RegisterForm, CreateEventForm
from app.models.event import Event
from app.models.user import User
from app.models.user_acounts import UserAccounts

app = Flask(__name__)
app.secret_key = '\xcd]\x1f\x8a\xa7\xd0J\xd6\x99\x8c/\x1e\x91~hU4tgd\xe5\xa2\xab3'

# Create login manager class
login_manager = LoginManager()

# Configure login
login_manager.init_app(app)

# View to be directed to for unauthorized attempt to access a protected page
login_manager.login_view = "/"

# Message flashed for unauthorized attempt to access a protected page
login_manager.login_message = u"Please Login First to access this page"
login_manager.login_message_category = "info"

# User accounts object
user_accounts = UserAccounts()


# Callback method to reload the user object
@login_manager.user_loader
def load_user(username):
    return user_accounts.get_specific_user(username)


# Index route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_f = request.form['password']
        if user_accounts.get_specific_user(username):
            if password_f == user_accounts.get_specific_user(username).password:
                app.logger.info('Password Matched')
                login_user(user_accounts.get_specific_user(username))
                flash("You have logged in successfully", 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid Password'
                return render_template("index.html", error=error)

        else:
            error = 'Invalid Username, The Username does not exist'
            return render_template("index.html", error=error)
    return render_template("index.html")


# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        if user_accounts.get_specific_user(form.username.data):
            flash("User already exists, choose another username", 'warning')
        else:
            user = User(form.username.data, form.email.data, form.password.data, form.confirm_password.data)
            user_accounts.create_user(user)
            flash("You have been registered successfully and can proceed to login", 'success')
            return redirect(url_for('login'))
    return render_template("register.html", form=form)


# User dashboard route
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html")


# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are logged out', 'success')
    return redirect(url_for('login'))


# User crud operations
# Create an event
@app.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = CreateEventForm(request.form)
    if request.method == 'POST' and form.validate():
        event = Event(form.name.data, form.category.data, form.location.data, form.owner.data, form.description.data)
        try:
            current_user.create_event(event)
            return redirect(url_for('dashboard'))
        except KeyError:
            flash('The event already exists', 'warning')
            return render_template("create_event.html", form=form)
    return render_template("create_event.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)

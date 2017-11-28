from flask import Flask, render_template, request, flash, url_for
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.utils import redirect

from app.forms import RegisterForm, CreateEventForm, UpdateEventForm
from app.models.event import Event
from app.models.user import User
from app.models.user_acounts import UserAccounts

app = Flask(__name__)

# Import the apps configuration settings from config file in instance folder
app.config.from_object('app.instance.config.DevelopmentConfig')

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


# Home route
@app.route('/', methods=['GET', 'POST'])
def login():
    # To check if current user is logged in
    # If logged in and they enter home route they should not be redirected to the home page
    if current_user.is_authenticated:
        return render_template("dashboard.html")
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
@app.route('/api/v1/register', methods=['GET', 'POST'])
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
@app.route('/api/v1/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html")


# Logout route
@app.route('/api/v1/logout')
@login_required
def logout():
    logout_user()
    flash('You are logged out', 'success')
    return redirect(url_for('login'))


# User crud operations
# Create an event
@app.route('/api/v1/create_events', methods=['GET', 'POST'])
@login_required
def create_events():
    form = CreateEventForm(request.form)
    if request.method == 'POST' and form.validate():
        event = Event(form.name.data, form.category.data, form.location.data, form.owner.data, form.description.data)
        try:
            current_user.create_event(event)
            user_accounts.add_all_individual_events(current_user)
            return redirect(url_for('dashboard'))
        except KeyError:
            flash('The event already exists', 'warning')
            return render_template("create_event.html", form=form)
    return render_template("create_event.html", form=form)


# Delete an event
@app.route('/api/v1/delete_events/<string:eventName>')
@login_required
def delete_events(eventName):
    try:
        current_user.delete_event(eventName)
        return redirect(url_for('dashboard'))
    except KeyError:
        flash('The event does not exist', 'warning')


# Update an Event
# Name field should not be editable
@app.route('/api/v1/update_events/<string:eventName>', methods=['GET', 'PATCH', 'POST'])
@login_required
def update_events(eventName):
    form = UpdateEventForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            current_user.update_event(eventName, form.category.data, form.location.data, form.owner.data,
                                      form.description.data)
            flash('The event has been updated successfully', 'success')
            return redirect(url_for('dashboard'))
        except KeyError:
            flash('The event does not exist', 'warning')

    return render_template("update_event.html", form=form)


# Route for viewing all public events
@app.route('/api/v1/public_events', methods=['GET'])
@login_required
def public_events():
    return render_template("public_events.html", user_accounts=user_accounts)


# Route for viewing a single event
# Extracts single event by name
@app.route('/api/v1/single_events/<string:eventName>', methods=['GET'])
@login_required
def single_events(eventName):
    event_dict = user_accounts.events
    event = event_dict.get(eventName)
    return render_template("single_event.html", event=event)


# Route for a user to RSVP
# Requires login and extracts a persons details
@app.route('/api/v1/rsvp_event<string:eventName>/rsvp')
@login_required
def rsvp_event(eventName):
    event_dict = user_accounts.events
    event = event_dict.get(eventName)
    event.add_attendants(current_user)
    return render_template("single_event.html", event=event)


if __name__ == '__main__':
    app.run()

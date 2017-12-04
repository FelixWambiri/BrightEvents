from flask import Flask, render_template, request, flash, url_for
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.utils import redirect

from app.forms import RegisterForm, CreateEventForm, UpdateEventForm, ResetPasswordForm
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

# Initialize a registered user for faster testing
user = User("felix", "felixwambiri21@gmail.com", "bootcamprtofellow")

user_accounts.create_user(user)


# Callback method to reload the user object
@login_manager.user_loader
def load_user(email):
    return user_accounts.get_specific_user(email)


# Home route
@app.route('/', methods=['GET', 'POST'])
def login():
    # To check if current user is logged in
    # If logged in and they enter home route they should not be redirected to the home page
    if request.method == 'POST':
        email = request.form['email']
        password_f = request.form['password']
        user = user_accounts.get_specific_user(email)
        if user:
            if user.compare_hashed_password(password_f):
                login_user(user)
                flash("You have logged in successfully", 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid credentials'
                return render_template("index.html", error=error)
        else:
            error = 'Invalid credentials'
            return render_template("index.html", error=error)
    return render_template("index.html")


# Registration route
@app.route('/api/v1/auth/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        if user_accounts.get_specific_user(form.email.data):
            flash("User already exists, choose another email", 'warning')
        else:
            user = User(form.username.data, form.email.data, form.password.data)
            user_accounts.create_user(user)
            flash("You have been registered successfully and can proceed to login", 'success')
            return redirect(url_for('login'))
    return render_template("register.html", form=form)


# User dashboard route
@app.route('/api/v1/auth/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html")


# Logout route
@app.route('/api/v1/auth/logout')
@login_required
def logout():
    logout_user()
    flash('You are logged out', 'success')
    return redirect(url_for('login'))


# User crud operations
# Create an event
@app.route('/api/v1/events', methods=['GET', 'POST'])
@login_required
def create_events():
    form = CreateEventForm(request.form)
    if request.method == 'POST' and form.validate():
        event = Event(form.name.data, form.category.data, form.location.data, form.owner.data, form.description.data)
        try:
            current_user.create_event(event)
            user_accounts.add_all_individual_events(None, current_user)
            return redirect(url_for('dashboard'))
        except KeyError:
            flash('The event already exists', 'warning')
            return render_template("create_event.html", form=form)
    return render_template("create_event.html", form=form)


# Delete an event
# Delete it from the users dashboard and also from the public events list
@app.route('/api/v1/delete/events/<string:event_name>')
@login_required
def delete_events(event_name):
    try:
        current_user.delete_event(event_name)
        user_accounts.delete_an_individuals_events(event_name)
        flash('The event has been deleted successfully', 'warning')
        return redirect(url_for('dashboard'))
    except KeyError:
        flash('The event does not exist', 'warning')
        return render_template("dashboard.html")


# Update an Event
# should populate for with previous data stored
@app.route('/api/v1/events/update/<string:eventName>', methods=['GET', 'POST'])
@login_required
def update_events(eventName):
    event = current_user.get_specific_event(eventName)
    form = UpdateEventForm(request.form, obj=event)
    if request.method == 'POST' and form.validate():
        try:
            up_event = current_user.update_event(eventName, form.name.data, form.category.data, form.location.data,
                                                 form.owner.data,
                                                 form.description.data)
            # Update also in the pubic events
            user_accounts.add_all_individual_events(eventName, current_user)
            form.process(obj=up_event)
            flash('The event has been updated successfully', 'success')
            return redirect(url_for('dashboard'))
        except KeyError:
            flash('The event does not exist', 'warning')
    return render_template("update_event.html", form=form)


# Route for viewing all public events
@app.route('/api/v1/all_events', methods=['GET'])
@login_required
def public_events():
    return render_template("public_events.html", user_accounts=user_accounts)


# Route for viewing a single event
# Extracts single event by name
@app.route('/api/v1/one_event/<string:eventName>', methods=['GET'])
@login_required
def single_events(eventName):
    event_dict = user_accounts.events
    event = event_dict.get(eventName)
    return render_template("single_event.html", event=event)


# Route for a user to RSVP
# Requires login and extracts a persons details
@app.route('/api/v1/event<string:eventName>/rsvp')
@login_required
def rsvp_event(eventName):
    event_dict = user_accounts.events
    event = event_dict.get(eventName)
    event.add_attendants(current_user.id, current_user.username)
    flash('You have successfully RSVP to this event, thank you for the initiative ', 'success')
    return render_template("single_event.html", event=event)


# Route to reset password
@app.route('/api/auth/reset_password', methods=['GET', 'POST'])
@login_required
def reset_password():
    form = ResetPasswordForm(request.form)
    if request.method == 'POST':
        if current_user.compare_hashed_password(form.previous_password.data):
            current_user.user_reset_password(form.new_password.data)
            flash('You have successfully updated your password', 'success')
            return redirect(url_for('dashboard'))
        else:
            error: 'Please try to remember you previous password'
            return render_template("reset_pw.html", error=error)

    return render_template("reset_pw.html", form=form)


if __name__ == '__main__':
    app.run()

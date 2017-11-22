from flask import Flask, render_template, request, flash, url_for
from werkzeug.utils import redirect

from app.forms import RegisterForm
from app.models.user import User
from app.models.user_acounts import UserAccounts

app = Flask(__name__)
app.secret_key = '\xcd]\x1f\x8a\xa7\xd0J\xd6\x99\x8c/\x1e\x91~hU4tgd\xe5\xa2\xab3'
user_accounts = UserAccounts()


# Index route
@app.route('/')
def login():
    return render_template("index.html")


# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        if user_accounts.get_specific_user(form.username.data):
            flash("User already exists, choose another username")
        else:
            user = User(form.username.data, form.email.data, form.password.data, form.confirm_password.data)
            user_accounts.create_user(user)
            flash("You have been registered successfully and can proceed to login", 'success')
            return redirect(url_for('login'))
    return render_template("register.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)

    

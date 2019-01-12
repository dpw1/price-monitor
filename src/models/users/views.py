from flask import Blueprint, session, request, url_for, render_template
from werkzeug.utils import redirect
from src.models.users.user import User
from src.models.monitors.monitor import Monitor
import src.models.users.errors as UserErrors
import src.models.users.decorators as user_decorators

user_blueprint = Blueprint('users', __name__ )

@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            if User.is_login_valid(email, password):
                session['email'] = email
                return redirect(url_for('.user_monitors'))
        except UserErrors.UserError as e:
            return e.message

    return render_template("users/login.html")


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            if User.register_user(email, password):
                session['email'] = email
                return redirect(url_for('.user_monitors'))
        except UserErrors.UserError as e:
            return e.message

    return render_template("users/register.html")

@user_blueprint.route('/monitors')
@user_decorators.requires_login
def user_monitors():
    monitors = User.get_monitors_by_user_id( User.get_by_email(session['email'])._id)
    return render_template('users/monitors.html', monitors=monitors)

@user_blueprint.route('/logout')
def logout_user():
    session['email'] = None
    return redirect(url_for('home'))

@user_blueprint.route('/check_monitors/<string:user_id>')
def check_user_monitors(user_id):
    pass
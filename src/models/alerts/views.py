from flask import Blueprint, request, render_template, session, redirect, url_for

from src.models.alerts.alert import Alert

alert_blueprint = Blueprint('alerts', __name__)

@alert_blueprint.route('/')
def index():
    return 'index alert page'

@alert_blueprint.route('/new', methods=['GET', 'POST'])
def create_alert():
    if request.method == 'POST':
        pass

    return render_template('alerts/new_alert.html')


@alert_blueprint.route('/edit/<string:alert_id>', methods=['GET', 'POST'])
def edit_alert(alert_id):
    pass


@alert_blueprint.route('/deactivate/<string:alert_id>')
def deactivate_alert(alert_id):
    Alert.get_by_id(alert_id).deactivate()
    return redirect(url_for('users.user_monitors'))


@alert_blueprint.route('/activate/<string:alert_id>')
def activate_alert(alert_id):
    Alert.get_by_id(alert_id).activate()
    return redirect(url_for('users.user_monitors'))

@alert_blueprint.route('/delete/<string:alert_id>')
def delete_alert(alert_id):
    pass


@alert_blueprint.route('/<string:alert_id>')
def get_alert_page(alert_id):
    return 'alert page'


@alert_blueprint.route('/check_price/<string:alert_id>')
def check_alert_price(alert_id):
    pass
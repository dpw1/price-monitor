from flask import Blueprint, render_template, request, redirect, url_for

from src.models.items.item import Item
from src.models.monitors.monitor import Monitor
import src.models.users.decorators as user_decorators

monitor_blueprint = Blueprint('monitors', __name__, )

@monitor_blueprint.route('/')
def index():
    return 'Monitor index;'

@monitor_blueprint.route('/new', methods=['POST', 'GET'])
@user_decorators.requires_login
def create_monitor():
    """
    Three steps form, goes from Monitor > First Item of this monitor > Monitor Page
    :return:
    """
    if "step" not in request.form:
        return render_template('monitors/create_monitor.html', step="monitor_step")
    elif request.form["step"] == "item_step":
        return render_template('monitors/create_monitor.html', step=request.form["step"], monitor_name=request.form['monitor'])
    elif request.form["step"] == "final_step":
        monitor_name = request.form['monitor']
        item_name = request.form['name']
        item_url = request.form['url']
        item_css = request.form['css']

        monitor = Monitor("4b566d3c33a64d8a9ac83658b6eddc9c", monitor_name)
        monitor.save_to_mongo()

        item = Item(monitor._id, item_url, item_name, item_css)
        item.save_to_mongo()

        return redirect(url_for('users/monitors.html', alert='success'))

@monitor_blueprint.route('/delete/<string:monitor_id>', methods=['POST'])
@user_decorators.requires_login
def delete_monitor(monitor_id):
    pass

@monitor_blueprint.route('/monitor/<string:monitor_id>')
@user_decorators.requires_login
def get_monitor_page(monitor_id):
    return 'specific monitor page'

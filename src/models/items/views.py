from flask import Blueprint, render_template, request, url_for
from werkzeug.utils import redirect

from src.models.items.item import Item
from src.models.alerts.alert import Alert
import src.models.users.decorators as user_decorators

item_blueprint = Blueprint('items', __name__, )

@item_blueprint.route('/<string:name>')
@user_decorators.requires_login
def item_page(name):
    pass

@item_blueprint.route('/create', methods=['POST', 'GET'])
@user_decorators.requires_login
def create_item():
    if request.method == 'POST':
        print('hey')

    return render_template('items/create_item.html')

@item_blueprint.route('/load')
@user_decorators.requires_login
def load_item():
    """
    Loads an item's data using their store and return a JSON representation of it
    :return:
    """
    pass

@item_blueprint.route('/delete/<string:item_id>', methods=['GET'])
def delete_item(item_id):
    if request.method == 'GET':
        Item.delete_by_item_id(item_id)
    return redirect(url_for('users.user_monitors'))

@item_blueprint.route('/update/<string:item_id>', methods=['POST', 'GET'])
def update_item_price(item_id):
    """
    Checks if price has changed. Connected to the monitors.html template.
    :return:
    """
    item = Item.get_by_id(item_id)

    current_price = item.load_price()
    old_price = item.price
    if old_price == current_price:
        return redirect(url_for('users.user_monitors', alert='No changes!'))
    else:
        # save new price
        pass
    pass
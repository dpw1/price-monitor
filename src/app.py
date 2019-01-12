from flask import Flask, render_template
from src.common.database import Database
from src.common.utils import Utils
import uuid
from src.alert_updater import test

app = Flask(__name__)

app.config.from_object('src.config')
app.secret_key = uuid.uuid4().hex


@app.before_first_request
def init_db():
    Database.initialize()

from src.models.users.views import user_blueprint
from src.models.monitors.views import monitor_blueprint
from src.models.alerts.views import alert_blueprint
from src.models.items.views import item_blueprint

app.register_blueprint(user_blueprint, url_prefix='/users')
app.register_blueprint(monitor_blueprint, url_prefix='/monitors')
app.register_blueprint(alert_blueprint, url_prefix='/alerts')
app.register_blueprint(item_blueprint, url_prefix='/items')

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(port=1337)
from src.common.database import Database
from src.models.alerts.alert import Alert
from src.models.monitors.monitor import Monitor

Database.initialize()

def test():
    puppy = 'hi'
    alerts_needing_update = Alert.find_needing_update()

    for alert in alerts_needing_update:
        alert.check_if_price_is_different(True)
import requests
import uuid
import src.models.alerts.constants as AlertConstants
import datetime
from src.common.database import Database
from src.models.items.item import Item
from src.models.users.user import User

class Alert(object):
    def __init__(self, user_email, item_id, active=True, last_checked=None, _id=None):
        self.user_email = user_email
        self.item = Item.get_by_id(item_id)
        self.active = active
        self.last_checked = datetime.datetime.utcnow() if last_checked is None else last_checked
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return '<Alert for {}, last checked at {}>'\
            .format(self.item.item_name, self.last_checked)

    def send(self):
        # return requests.post(
        #     AlertConstants.URL,
        #     auth=("api", AlertConstants.API_KEY),
        #     data={"from": AlertConstants.FROM,
        #           "to": self.user.email,
        #           "subject": "New Price! {} is now {}".format(self.item.item_name, self.item.price),
        #           "text": "The website has updated the price!"})
        return requests.post(
            AlertConstants.URL,
            auth=("api", AlertConstants.API_KEY),
            data={"from": AlertConstants.FROM,
                  "to": ["diego.boarutto.fortes@gmail.com"],
                  "subject": "Hello",
                  "text": "Testing some Mailgun awesomeness!"})

    @classmethod
    def find_needing_update(cls, minutes_since_update=AlertConstants.ALERT_TIMEOUT):
        last_updated_limit = datetime.datetime.utcnow() - datetime.timedelta(minutes=minutes_since_update)
        if minutes_since_update < int(last_updated_limit.minute):
            print('time to update! {}'.format(int(last_updated_limit.minute)))
        else:
            print('Last updated: {}'.format(last_updated_limit))
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION, {"last_checked": {'$lte':last_updated_limit}})]

    def save_to_mongo(self):
        Database.update(AlertConstants.COLLECTION, {'_id':self._id}, self.json())

    def json(self):
        return {
            '_id':self._id,
            'user_email':self.user_email,
            'last_checked':self.last_checked,
            'item_id': self.item._id,
            'active':self.active
        }

    def deactivate(self):
        self.active = False
        self.save_to_mongo()

    def activate(self):
        self.active = True
        self.save_to_mongo()

    def check_if_price_is_different(self, send_email=False):
        current_price = self.item.load_price()
        last_price = self.item.price
        self.last_checked = datetime.datetime.utcnow()
        self.save_to_mongo()
        if (current_price != last_price):
            if send_email:
                self.send()
            return current_price
        return False

    @classmethod
    def get_by_id(cls, id):
        return cls(**Database.find_one(AlertConstants.COLLECTION, {"_id": id}))

    @classmethod
    def get_by_item_id(cls, id):
        return cls(**Database.find_one(AlertConstants.COLLECTION, {"item_id": id}))
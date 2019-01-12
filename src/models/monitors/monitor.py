import uuid
from src.common.database import Database
import src.models.monitors.constants as MonitorConstants
from src.models.items.item import Item

class Monitor(object):
    def __init__(self, user_id, name, frequency_check=None, _id=None):
        self.user_id = user_id
        self.name = name
        self.frequency_check = frequency_check
        self._id = uuid.uuid4().hex if _id is None else _id
        self.items = self.get_items_by_id(self._id)

    def __repr__(self):
        return '<Monitor named {}\'s monitors every {} minutes.'\
            .format(self.name, self.frequency_check)

    def json(self):
        return{
            "_id": self._id,
            "user_id": self.user_id,
            "name":self.name,
            "frequency_check":self.frequency_check
        }

    @classmethod
    def get_by_id(cls, id):
        return cls(**Database.find_one(MonitorConstants.COLLECTION, {'_id':id}))

    @classmethod
    def get_by_user_id(cls, user_id):
        monitors = Database.find(MonitorConstants.COLLECTION, {'user_id':user_id})
        return [cls(**monitor) for monitor in monitors]

    def save_to_mongo(self):
        Database.insert(MonitorConstants.COLLECTION, self.json())

    @classmethod
    def get_by_name(cls, monitor_name):
        return cls(**Database.find_one(MonitorConstants.COLLECTION, {'name':monitor_name}))

    @classmethod
    def get_items_by_id(cls, _id):
        return Item.get_by_monitor_id(_id)

    @classmethod
    def delete_from_mongo(cls, query):
        Database.delete_one(MonitorConstants.COLLECTION, query)
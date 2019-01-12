import uuid
import requests
from fake_useragent import UserAgent
import re
import datetime
from bs4 import BeautifulSoup
import src.models.items.constants as ItemConstants
from src.common.database import Database
import src.models.items.errors as ItemErrors

#TODO: 1. Make ip rotation for load_item()
# https://codelike.pro/create-a-crawler-with-rotating-ip-proxy-in-python/
# https://www.scrapehero.com/tutorial-how-to-scrape-amazon-product-details-using-python/

class Item(object):
    def __init__(self, monitor_id, item_url, item_name, css, date=None, price=None, _id=None):
        self.monitor_id = monitor_id
        self.item_url = item_url
        self.item_name = item_name
        self.css = css
        self.date = datetime.datetime.utcnow() if date is None else date
        self.price = self.load_price() if price is None else price
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return '<Item from monitor ID: {}.\nName: {}\nURL: {}\nPrice: {}\nDate: {}.'\
            .format(self.monitor_id, self.item_name, self.item_url, self.price, self.date)

    def load_price(self):
        """
        request URL and return value from specific CSS selector.
        :return:
        """
        try:
            headers = requests.utils.default_headers()
            headers.update({
                'User-Agent': UserAgent().random,
            })
            request = requests.get(self.item_url, headers=headers)
            content = request.content
            soup = BeautifulSoup(content, "html.parser")
            element = soup.select(self.css)[0].text
            return element
        except ItemErrors.BeautifulSoupRequestError as e:
            return e.message

    def save_to_mongo(self):
        Database.insert(ItemConstants.COLLECTION,  self.json())

    def json(self):
        return {
            "_id": self._id,
            "monitor_id": self.monitor_id,
            "item_url": self.item_url,
            "item_name": self.item_name,
            "date": self.date,
            "css": self.css,
            "price": self.price
        }

    @classmethod
    def get_by_id(cls, item_id):
        return cls(**Database.find_one(ItemConstants.COLLECTION, {"_id": item_id}))

    @classmethod
    def get_by_monitor_id(cls, monitor_id):
        items = Database.find(ItemConstants.COLLECTION, {"monitor_id": monitor_id})
        return [cls(**item) for item in items]

    @classmethod
    def get_by_name_regex(cls, item_name):
        return cls(**Database.find(ItemConstants.COLLECTION, {"item_name": {"$regex": '{}'.format(item_name)}}))

    @classmethod
    def delete_by_item_id(cls, id):
        Database.delete_one(ItemConstants.COLLECTION, {"_id": id})

    @classmethod
    def update_by_item_id(cls, id, query):
        Database.update(ItemConstants.COLLECTION, {"_id": id}, query)
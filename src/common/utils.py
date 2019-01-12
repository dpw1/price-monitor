import json
import requests
from passlib.hash import pbkdf2_sha512

class Utils(object):

    @staticmethod
    def email_is_valid(email):
        email_address_matcher = re.compile("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        return True if email_address_matcher.match(email) else False

    @staticmethod
    def hash_password(password):
        """
        hashes a password using pbkdf2_sha512
        :param password: the sha512 from login/register form
        :return: pbkdf2_sha512 encrypted pass
        """
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        Checks that the password the user sent matches the DB password.
        DB password is encrypted more than the user's password at this stage.
        :param password: sha512-hashed password
        :param hashed_password: pbkdf2_sha512 encrypted password
        :return: True if password matches, False otherwise
        """

        return pbkdf2_sha512.verify(password, hashed_password)

    @staticmethod
    def get_shopify_json(url):
        """
        j = json object
        # get last added product ID j['products'][len(j['products']) - 1]['id']
        :param url:
        :return:
        """
        request = requests.get(url)
        return json.loads(request.content)



from src.common.database import Database
import uuid
import src.models.users.errors as UserErrors
from src.common.utils import Utils
import src.models.users.constants as UserConstants
from src.models.monitors.monitor import Monitor

class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id


    def __repr__(self):
        return '<User {}.'.format(self.email)

    @staticmethod
    def is_login_valid(email, password):
        """
        This method verifies that an e-mail/password combo (sent by the website form) is valid or not
        Checks that the email exists & password is correct
        :param email: User's email
        :param password: a sha512 hashed password
        :return: true if valid, false otherwise
        """
        user_data = Database.find_one(UserConstants.COLLECTION, {"email":email})
        if user_data is None:
            raise UserErrors.UserNotExistsError("Your user does not exist.")
        if not Utils.check_hashed_password(password, user_data['password']):
            raise UserErrors.IncorrectPasswordError("Your password was wrong.")

        return True

    @staticmethod
    def register_user(email, password):
        """
        This method registers a user using e-mail and password.
        The password already comes hashed as sha-512.
        :param email: user's e-mail (might be invalid)
        :param password: sha512-hashed password
        :return: True if registered successfully, or False otherwise (exceptions can also be raised)
        """
        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})

        if user_data is not None:
            raise UserErrors.UserAlreadyRegisteredError("The e-mail you used to register already exists.")
        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError("The e-mail does not have the right format.")

        User(email, Utils.hash_password(password)).save_to_db()

        return True

    def save_to_db(self):
        Database.insert("users", self.json())

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password
        }

    @classmethod
    def get_by_id(cls, id):
        return cls(**Database.find_one(UserConstants.COLLECTION, {"_id": id}))

    @classmethod
    def get_by_email(cls, email):
        return cls(**Database.find_one(UserConstants.COLLECTION, {"email": email}))

    @classmethod
    def get_monitors_by_user_id(cls, id):
        return Monitor.get_by_user_id(id)
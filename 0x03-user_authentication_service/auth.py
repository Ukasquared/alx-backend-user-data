#!/usr/bin/env python3
""" auth modulr """
import bcrypt
from db import DB
from user import User
import uuid


def _hash_password(password):
    """ return salted
    password
    """
    password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password, salt)
    return hash


def _generate_uuid():
    """ string representation
    of uuid
    """
    u_string = uuid.uuid4()
    return u_string
 

class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email, password) -> User:
        """ register users """
        user = self._db._session.query(User).filter(User.email == email).first()
        if user:
            raise ValueError(f"User {email} already exists")
        new_user = self._db.add_user(email, _hash_password(password))
        return new_user

    def valid_login(self, email, password):
        """ check if existing user can login"""
        user = self._db._session.query(User).filter(User.email == email).first()
        if user:
            u_password = password.encode('utf-8')
            result = bcrypt.checkpw(u_password, user.password)
            return result

    def create_session(self, email):
        """ create session """
        user = self._db.find_user_by(email=email)
        if user:
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id

    def get_user_from_session_id(self, id_session):
        """get user from session
        """
        if id_session is None:
            return None
        try:
            user = self._db.find_user_by(session_id=id_session)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id):
        """ destroy existing session
        """
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email):
        """get user reset token """
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(user.id, reset_token=token)
        except NoResultFound:
            raise ValueError
        return token

    def update_password(self, reset_token, password):
        """ update user password """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            new_passwd = _hash_password(password)
            self._db.update_user(user.id, 
                                 password=password,
                                 reset_token=None)
        except NoResultFound:
            raise ValueError

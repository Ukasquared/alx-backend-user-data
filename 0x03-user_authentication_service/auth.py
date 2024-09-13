#!/usr/bin/env python3
""" auth modulr """
import bcrypt
from db import DB
from user import User
import uuid
from typing import TypeVar


def _hash_password(password: str) -> str:
    """ return salted
    password
    """
    password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password, salt)
    return hash


def _generate_uuid() -> str:
    """ string representation
    of uuid
    """
    u_string = uuid.uuid4()
    return str(u_string)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str,
                      password: str) -> TypeVar(User):
        """ register users """
        user = self._db._session.query(User).filter(
               User.email == email).first()
        if user:
            raise ValueError(f"User {email} already exists")
        new_user = self._db.add_user(email, _hash_password(password))
        return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """ check if existing user can login"""
        user = self._db._session.query(User).filter(
                 User.email == email).first()
        if user:
            u_password = password.encode('utf-8')
            result = bcrypt.checkpw(u_password,
                                    user.hashed_password)
            if result:
                return True
        return False

    def create_session(self, u_email: str) -> str:
        """ create session """
        try:
            user = self._db.find_user_by(email=u_email)
            if user:
                id_session = _generate_uuid()
                self._db.update_user(user.id, session_id=id_session)
                return id_session
        except Exception:
            return None

    def get_user_from_session_id(self, id_session):
        """get user from session
        """
        if id_session is None:
            return None
        try:
            user = self._db.find_user_by(session_id=id_session)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ destroy existing session
        """
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """get user reset token """
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(user.id, reset_token=token)
        except NoResultFound:
            raise ValueError
        return token

    def update_password(self, reset_token: str, password: str) -> None:
        """ update user password """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            new_passwd = _hash_password(password)
            self._db.update_user(user.id,
                                 password=password,
                                 reset_token=None)
        except NoResultFound:
            raise ValueError

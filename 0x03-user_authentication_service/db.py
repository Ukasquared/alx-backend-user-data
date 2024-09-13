#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User



class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
         add user to database
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
          finds a user and
          returns first found
          user
        """
        for k, v in kwargs.items():
            if not hasattr(User, k):
                raise InvalidRequestError
        curr_user = self._session.query(User).\
            filter_by(**kwargs).first()
        if curr_user is None:
            raise NoResultFound
        return curr_user

    def update_user(self, user_id, **kwargs) -> None:
        """
        update users
        informaton
        """
        update_val = {}
        for k, v in kwargs.items():
            if hasattr(User, k):
                update_val[getattr(User, k)] = v
            else:
                raise ValueError

        user = self.find_user_by(id=user_id)
        if not user:
            return
        self._session.query(User).filter(User.id == user.id).update(update_val)
        self._session.commit()

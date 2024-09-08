#!/usr/bin/env python3
"""
Session
Authentication
Module
"""
from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """ create sessions for
    the user
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
         creates a session id for user
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(
            self, session_id: str = None) -> str:
        """
         returns a User ID
         based on a Session ID
        """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        user_id = self.user_id_by_session_id
        return user_id.get(session_id)

    def current_user(self, request=None) -> User:
        """
          returns a User instance
          based on a cookie value:
        """
        cokie_value = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cokie_value)
        user = User.get(user_id)
        return user

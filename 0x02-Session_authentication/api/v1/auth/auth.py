#!/usr/bin/env python3
""" authentication class
"""
from flask import request
from typing import List, TypeVar
import os


class Auth():
    """ a class for
    authenticating
    users
    """
    def require_auth(self, path: str,
                     excluded_paths: List[str]
                     ) -> bool:
        """ require authentication """
        if path is None:
            return True
        if excluded_paths is None or len(
                excluded_paths) == 0:
            return True
        if path in excluded_paths:
            return False
        if path[-1] != '/':
            if rf"{path}/" in excluded_paths:
                return False
        return True

    def authorization_header(self, request=None
                             ) -> str:
        """ auth header """
        if request is None:
            return None
        header = request.headers.get('Authorization')
        return header

    def current_user(self, request=None
                     ) -> TypeVar('User'):
        """ current user """
        return None

    def session_cookie(self, request=None):
        """a cookie value
        from a request
        """
        if request is None:
            return None
        session_cookie = os.getenv("SESSION_NAME")
        return request.cookies.get(session_cookie)

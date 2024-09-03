#!/usr/bin/env python3
""" authentication class
"""
from flask import request
from typing import List, TypeVar


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
        return None

    def current_user(self, request=None
                     ) -> TypeVar('User'):
        """ current user """
        return None

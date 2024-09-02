#!/usr/bin/env python3
""" authentication class
"""
from flask import request
from typing import List


class Auth():
    """ a class for
    authenticating
    users
    """
    def require_auth(self, path: str,
                     excluded_paths: List[str]
                     ) -> bool:
        """ require authentication """
        return False

    def authorization_header(self, request=None
                             ) -> str:
        """ auth header """
        return None

    def current_user(self, request=None
                     ) -> TypeVar('User'):
        """ current user """
        return None
